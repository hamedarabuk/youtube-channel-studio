#!/usr/bin/env python3
"""PreToolUse hook: block access to .env files in this repo.

Exits 2 on violation so Claude sees the block reason.
Allows .env.example, .env.sample, .env.template.
Covers Read, Grep, and Bash tools.

Registered from .claude/settings.json via $CLAUDE_PROJECT_DIR so this
safeguard travels with the repo, whoever clones it.
"""
import json
import re
import sys

_SAFE = {".env.example", ".env.sample", ".env.template"}
_ENV_IN_CMD = re.compile(r"\.env(?:\.[a-zA-Z0-9_-]+)?")


def path_is_env(path: str) -> bool:
    if not path:
        return False
    base = path.replace("\\", "/").rsplit("/", 1)[-1].lower()
    if base in _SAFE:
        return False
    return base == ".env" or base.startswith(".env.")


def command_touches_env(cmd: str) -> bool:
    if not cmd:
        return False
    for m in _ENV_IN_CMD.finditer(cmd):
        if m.group(0).lower() not in _SAFE:
            return True
    return False


def block(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool = payload.get("tool_name", "")
    inp = payload.get("tool_input") or {}

    if tool == "Read" and path_is_env(inp.get("file_path", "")):
        block(".env is off-limits. Read .env.example or route through config.py.")

    if tool == "Grep" and path_is_env(inp.get("path", "")):
        block("Grepping .env is off-limits. Use config.py to inspect resolved values.")

    if tool == "Bash" and command_touches_env(inp.get("command", "")):
        block("Command references .env. Use config.py or .env.example instead.")

    sys.exit(0)


if __name__ == "__main__":
    main()
