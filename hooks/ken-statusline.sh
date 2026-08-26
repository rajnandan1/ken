#!/usr/bin/env bash
# CLAUDE_CONFIG_DIR overrides ~/.claude, matching where the hooks write the flags
dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
flag="$dir/.ken-active"
[ -f "$flag" ] || exit 0

mode=$(head -n1 "$flag" | tr -d '[:space:]')

# Delta complement: when ponytail is also active, say so in the badge.
pt=""
pt_flag="$dir/.ponytail-active"
if [ -f "$pt_flag" ]; then
    pt_mode=$(head -n1 "$pt_flag" | tr -d '[:space:]')
    [ -n "$pt_mode" ] && [ "$pt_mode" != "off" ] && pt="+PT"
fi

# ultra is the high-intensity mode; flag it amber so it stands out from the
# default green at a glance. The level is still in the text, so color is a
# redundant cue, not the only one.
color=108
[ "$mode" = "ultra" ] && color=173

if [ -z "$mode" ] || [ "$mode" = "full" ]; then
    printf '\033[38;5;%sm[KEN%s]\033[0m' "$color" "$pt"
else
    printf '\033[38;5;%sm[KEN:%s%s]\033[0m' "$color" "$(printf '%s' "$mode" | tr '[:lower:]' '[:upper:]')" "$pt"
fi
