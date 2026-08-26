#!/usr/bin/env python3
"""Maintenance-over-time benchmark: N tickets in sequence against ONE persistent
workspace; the headline is what survives.

  python run.py --selftest
      Push the scripted good/bad reference agents through the full pipeline —
      no API, no spend. Good must score perfectly; the lazy twin (which passes
      every VISIBLE test) must be caught by every scored rate. Doubles as the
      end-to-end dry run. Run first, always.

  python run.py --run --arms baseline,ken --repeats 3 --model haiku
      Live run (spends API; approve the cost gate first). One run = one
      (arm, repeat): seed once, then 10 fresh headless Claude Code sessions in
      the same workspace, git commit per round.

  python run.py --rescore runs/<stamp>
      Recompute end-state survival/rates/reported from kept workspaces. No API.

ken: invocation flags, plugin-dir resolution, and tree-kill are stolen from
benchmarks/agentic/run.py — one proven way to drive a headless session.
"""
import argparse
import concurrent.futures
import datetime
import json
import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path

from refs import REFS
from scorers import rates, reported, score_round, survival_matrix
from tickets import TICKETS

HERE = Path(__file__).resolve().parent
SEED = HERE / "seed"
RUNS_DIR = HERE / "runs"

MODELS = {"haiku": "claude-haiku-4-5-20251001", "sonnet": "claude-sonnet-4-6", "opus": "claude-opus-4-8"}
PLUGIN_CACHE = Path.home() / ".claude" / "plugins" / "cache"
ROUND_TIMEOUT = 300

NO_RUN = ("Write the implementation (include tests if you normally would for a change like "
          "this). Do not run a dev server, install dependencies, or open a browser -- just "
          "write the code and stop. Only the code you write is measured, not its execution.")


def _plugin_dir(name):
    env = os.environ.get(f"{name.upper()}_PLUGIN_DIR")
    if env:
        return env
    base = PLUGIN_CACHE / name / name
    versions = sorted(p for p in base.glob("*") if p.is_dir()) if base.exists() else []
    if not versions:
        sys.exit(f"{name} plugin dir not found under {base}; install the plugin or set {name.upper()}_PLUGIN_DIR")
    return str(versions[-1])


def _tree_kill(proc):
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass


def _git(ws, *args):
    return subprocess.run([shutil.which("git") or "git", *args], cwd=str(ws),
                          capture_output=True, text=True)


def seed_workspace(ws):
    shutil.copytree(SEED, ws, dirs_exist_ok=True)
    (ws / ".gitignore").write_text("_claude*.json\n__pycache__/\n")
    _git(ws, "init", "-q")
    _git(ws, "add", "-A")
    _git(ws, "-c", "user.email=bench@local", "-c", "user.name=bench",
         "commit", "-q", "-m", "seed", "--no-verify")


def write_visible_test(ws, ticket):
    (ws / "tests").mkdir(exist_ok=True)
    (ws / "tests" / f"test_r{ticket['round']}.py").write_text(ticket["visible"])


def commit_round(ws, label):
    _git(ws, "add", "-A")
    _git(ws, "-c", "user.email=bench@local", "-c", "user.name=bench",
         "commit", "-q", "-m", label, "--no-verify")


def churn(ws):
    out = _git(ws, "diff", "HEAD~1", "HEAD", "--numstat").stdout
    added = deleted = 0
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3 and parts[0] != "-":
            added += int(parts[0])
            deleted += int(parts[1])
    return {"added": added, "deleted": deleted}


def run_claude_round(ws, ticket, arm, model):
    claude = shutil.which("claude")
    if not claude:
        sys.exit("claude CLI not found on PATH")
    prompt = (f"{ticket['prompt']}\n\n{NO_RUN}")
    cmd = [claude, "-p", prompt, "--model", MODELS[model],
           "--permission-mode", "bypassPermissions", "--output-format", "json",
           "--setting-sources", "project,local", "--strict-mcp-config",
           "--disallowedTools", "Bash"]
    if arm == "ken":
        cmd += ["--plugin-dir", _plugin_dir("ken")]
    cmd += ["--append-system-prompt", NO_RUN]
    out_path = ws / "_claude.json"
    with open(out_path, "wb") as so, open(ws / "_claude.stderr.txt", "wb") as se:
        proc = subprocess.Popen(cmd, cwd=str(ws), stdout=so, stderr=se,
                                start_new_session=(os.name != "nt"))
        try:
            proc.wait(timeout=ROUND_TIMEOUT)
        except subprocess.TimeoutExpired:
            _tree_kill(proc)
            try:
                proc.wait(timeout=15)
            except Exception:
                pass
    meta = {}
    try:
        j = json.loads(out_path.read_text(encoding="utf-8"))
        u = j.get("usage") or {}
        meta = {"cost": j.get("total_cost_usd"), "duration_ms": j.get("duration_ms"),
                "turns": j.get("num_turns"), "out_tokens": u.get("output_tokens"),
                "in_tokens": u.get("input_tokens"),
                # cache tokens carry the injected ruleset -- per-round evidence the arm activated
                "cache_tokens": (u.get("cache_read_input_tokens") or 0) + (u.get("cache_creation_input_tokens") or 0)}
    except Exception:
        pass
    return meta


def play_run(ws, apply_round, label):
    """Drive one full run: apply_round(ticket) mutates the workspace per round."""
    records = []
    for t in TICKETS:
        write_visible_test(ws, t)
        commit_round(ws, f"r{t['round']} tests")
        meta = apply_round(t) or {}
        commit_round(ws, f"r{t['round']} {label}")
        rec = score_round(ws, t)
        rec.update(meta)
        rec["churn"] = churn(ws)
        rec["reported"] = reported(ws)
        records.append(rec)
    final = survival_matrix(ws, 10)
    return {"rounds": records, "final_matrix": final, "rates": rates(records, final)}


def selftest():
    failures = []
    results = {}
    for name, apply_fn in REFS.items():
        ws = RUNS_DIR / "_selftest" / name
        if ws.exists():
            shutil.rmtree(ws)
        ws.mkdir(parents=True)
        seed_workspace(ws)
        res = play_run(ws, lambda t, f=apply_fn: f(t["round"], ws), name)
        results[name] = res
        r = res["rates"]
        print(f"{name:5} survival {r['survival']['survived']}/{r['survival']['of']}  "
              f"reuse {r['reuse']['passed']}/{r['reuse']['of']}  "
              f"root-cause {r['root_cause']['passed']}/{r['root_cause']['of']}  "
              f"rewrite {r['rewrite_on_rot']['passed']}/{r['rewrite_on_rot']['of']}")

    g, b = results["good"]["rates"], results["bad"]["rates"]
    def need(cond, msg):
        if not cond:
            failures.append(msg)
            print("XX", msg)
        else:
            print("ok", msg)

    need(g["survival"]["survived"] == 9, "good ref survives 9/9")
    need(g["reuse"]["passed"] == 4, "good ref reuse 4/4")
    need(g["root_cause"]["passed"] == 2, "good ref root-cause 2/2")
    need(g["rewrite_on_rot"]["passed"] == 2, "good ref rewrite 2/2")
    bad_visible = all(rec["visible"] == 1 for rec in results["bad"]["rounds"])
    need(bad_visible, "bad ref passes every VISIBLE test at round time (the traps are invisible)")
    need(b["reuse"]["passed"] == 0, "bad ref caught on reuse (0/4)")
    need(b["root_cause"]["passed"] == 0, "bad ref caught on root-cause (0/2)")
    need(b["rewrite_on_rot"]["passed"] == 0, "bad ref caught on rewrite (0/2)")
    need(b["survival"]["survived"] < g["survival"]["survived"], "bad ref loses survival by end of run")
    print(f"\nselftest: {'all instruments valid' if not failures else str(len(failures)) + ' BROKEN'}")
    return len(failures)


def live(args):
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = RUNS_DIR / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    arms = [a.strip() for a in args.arms.split(",")]
    specs = [(arm, rep) for arm in arms for rep in range(args.repeats)]

    def one(spec):
        arm, rep = spec
        ws = out_dir / f"{arm}__r{rep}"
        ws.mkdir(parents=True, exist_ok=True)
        seed_workspace(ws)
        res = play_run(ws, lambda t: run_claude_round(ws, t, arm, args.model), arm)
        return {"arm": arm, "repeat": rep, **res}

    print(f"running {len(specs)} runs x 10 rounds, {args.workers} at a time", flush=True)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(one, s): s for s in specs}
        for fut in concurrent.futures.as_completed(futs):
            arm, rep = futs[fut]
            try:
                res = fut.result()
            except Exception as e:  # a blown run is data, not a crash
                res = {"arm": arm, "repeat": rep, "error": str(e)[:300]}
            results.append(res)
            r = res.get("rates", {}).get("survival", {})
            print(f"  done {arm} #{rep}  survival {r.get('survived')}/{r.get('of')}", flush=True)
            (out_dir / "results.json").write_text(json.dumps(
                {"date": stamp, "model": MODELS[args.model], "results": results}, indent=2))
    print(f"wrote {out_dir}/results.json")


def rescore(run_dir):
    run_dir = Path(run_dir)
    if not run_dir.exists():
        run_dir = RUNS_DIR / run_dir.name
    for ws in sorted(p for p in run_dir.iterdir() if p.is_dir()):
        final = survival_matrix(ws, 10)
        early = [m for rnd, m in final.items() if rnd <= 9]
        print(f"{ws.name:20} end-state survival {sum(m['survives'] for m in early)}/{len(early)}  "
              f"reported {reported(ws)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--rescore")
    ap.add_argument("--arms", default="baseline,ken")
    ap.add_argument("--model", default="haiku", choices=sorted(MODELS))
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    if args.selftest:
        sys.exit(1 if selftest() else 0)
    if args.rescore:
        return rescore(args.rescore)
    if args.run:
        if selftest():
            sys.exit("instruments broken; refusing to spend on the API")
        return live(args)
    sys.exit("give --selftest, --run, or --rescore <dir>")


if __name__ == "__main__":
    main()
