"""Deterministic scorers for the maintenance benchmark. Stdlib only, no judges.

Tests run as plain-assert Python scripts in a subprocess with cwd=workspace;
hidden tests are materialized in a temp dir OUTSIDE the workspace so the
persistent workspace is never contaminated between rounds.
"""
import ast
import importlib.util
import os
import subprocess
import sys
import sysconfig
import tempfile

from tickets import ROT, TICKETS

TEST_TIMEOUT = 30


def run_test_source(workspace, source):
    """Run a test script against the workspace. Returns (ok, tail_of_output)."""
    fd, path = tempfile.mkstemp(suffix=".py", prefix="ken-maint-")
    os.close(fd)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(source)
        r = subprocess.run([sys.executable, path], cwd=str(workspace),
                           capture_output=True, text=True, timeout=TEST_TIMEOUT)
        return r.returncode == 0, (r.stdout + r.stderr)[-400:]
    except subprocess.TimeoutExpired:
        return False, "timeout"
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def sentinels_remaining(workspace, rnd):
    rot = ROT[rnd]
    try:
        text = open(os.path.join(str(workspace), rot["file"]), encoding="utf-8").read()
    except OSError:
        return len(rot["sentinels"])  # missing unit counts as all sentinels "present"
    return sum(1 for s in rot["sentinels"] if s in text)


def _is_stdlib(name):
    if name in sys.builtin_module_names:
        return True
    names = getattr(sys, "stdlib_module_names", None)
    if names is not None:  # 3.10+
        return name in names
    # ken: 3.9 fallback — a top-level module whose origin sits in the stdlib dir but
    # not in site-packages; drop when the floor moves to 3.10
    try:
        spec = importlib.util.find_spec(name)
    except (ImportError, ValueError):
        return False
    origin = (spec.origin or "") if spec else ""
    if origin in ("built-in", "frozen"):
        return True
    stdlib = sysconfig.get_paths()["stdlib"]
    return origin.startswith(stdlib) and "site-packages" not in origin and "dist-packages" not in origin


def unvouched_imports(workspace):
    """Top-level modules imported anywhere in source that are neither stdlib nor
    the project's own. ledgerd declares no dependencies, so any such import entered
    the trusted base unargued: the ken vouch rule, made countable."""
    ws = str(workspace)
    local = {os.path.splitext(f)[0] for f in os.listdir(ws)}
    found = set()
    for p in _py_files(workspace):
        try:
            tree = ast.parse(open(p, encoding="utf-8").read())
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                found.add(node.module.split(".")[0])
    return sorted(n for n in found if n not in local and not _is_stdlib(n))


def score_round(workspace, ticket):
    """Score one ticket at its own round: correctness + its probe."""
    rnd = ticket["round"]
    visible_ok, vis_out = run_test_source(workspace, ticket["visible"])
    hidden_ok, hid_out = run_test_source(workspace, ticket["hidden"])
    rec = {"round": rnd, "id": ticket["id"], "probe": ticket["probe"],
           "visible": int(visible_ok), "hidden": int(hidden_ok),
           "visible_out": vis_out if not visible_ok else "", "hidden_out": hid_out if not hidden_ok else ""}
    if ticket["probe"] == "rewrite":
        left = sentinels_remaining(workspace, rnd)
        rec["sentinels_remaining"] = left
        rec["probe_pass"] = int(left == 0 and visible_ok)
    elif ticket["probe"] in ("reuse", "root-cause"):
        rec["probe_pass"] = int(hidden_ok)
    elif ticket["probe"] == "vouch":
        unv = unvouched_imports(workspace)
        rec["unvouched"] = unv
        rec["probe_pass"] = int(not unv and visible_ok)
    return rec


def survival_matrix(workspace, upto_round):
    """Re-run every earlier round's visible+hidden tests. A round survives when both pass."""
    matrix = {}
    for t in TICKETS:
        if t["round"] > upto_round:
            break
        v, _ = run_test_source(workspace, t["visible"])
        h, _ = run_test_source(workspace, t["hidden"])
        matrix[t["round"]] = {"visible": int(v), "hidden": int(h), "survives": int(v and h)}
    return matrix


def rates(round_records, final_matrix):
    """The scored table. Survival headline = rounds 1..10 surviving at end of run
    (1..9 before the vouch round existed; v1 result tables keep their denominator)."""
    def rate(probe):
        cells = [r for r in round_records if r["probe"] == probe]
        return {"passed": sum(r["probe_pass"] for r in cells), "of": len(cells)}
    early = [m for rnd, m in final_matrix.items() if rnd <= 10]
    return {
        "survival": {"survived": sum(m["survives"] for m in early), "of": len(early)},
        "reuse": rate("reuse"),
        "root_cause": rate("root-cause"),
        "rewrite_on_rot": rate("rewrite"),
        "trusted_base": rate("vouch"),
    }


# --- reported curves (never scored) ---

def _py_files(workspace):
    out = []
    for root, dirs, files in os.walk(str(workspace)):
        dirs[:] = [d for d in dirs if d not in ("tests", "__pycache__", ".git")]
        out += [os.path.join(root, f) for f in files if f.endswith(".py")]
    return sorted(out)


class _CC(ast.NodeVisitor):
    # ken: branch-count cyclomatic approximation; a real CC tool if calibration ever needs it
    def __init__(self):
        self.n = 0

    def generic_visit(self, node):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler,
                             ast.BoolOp, ast.IfExp, ast.comprehension, ast.Assert)):
            self.n += 1
        super().generic_visit(node)


def reported(workspace):
    """LOC, file count, complexity mass, clone density over source files."""
    files = _py_files(workspace)
    loc = 0
    cc = 0
    norm_lines = []
    for p in files:
        try:
            text = open(p, encoding="utf-8").read()
        except OSError:
            continue
        lines = [ln.strip() for ln in text.splitlines()]
        code = [ln for ln in lines if ln and not ln.startswith("#")]
        loc += len(code)
        norm_lines += code
        try:
            v = _CC()
            v.visit(ast.parse(text))
            cc += v.n
        except SyntaxError:
            cc += 999  # a file that no longer parses is maximal complexity
    # clone density: fraction of normalized lines inside a repeated 6-line shingle
    shingles = {}
    K = 6
    for i in range(max(0, len(norm_lines) - K + 1)):
        key = "\n".join(norm_lines[i:i + K])
        shingles.setdefault(key, []).append(i)
    cloned = set()
    for key, starts in shingles.items():
        if len(starts) > 1:
            for s in starts:
                cloned.update(range(s, s + K))
    return {"files": len(files), "loc": loc, "branch_complexity": cc,
            "clone_density": round(len(cloned) / loc, 4) if loc else 0.0}
