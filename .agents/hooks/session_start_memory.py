#!/usr/bin/env python3
"""Antigravity SessionStart hook for Abs By AI.

Loads two things automatically at the start of every new Antigravity session:
1. The remainder of AGENTS.md past Antigravity's 24 KB per-file rule cap, read
   live from disk so it never goes stale as Claude/Codex/Antigravity update it.
2. The merged MEMORY.md index from Dan's local Claude memory folder (including
   local-only entries on his Mac) plus any repo-only entries in Docs/memory/.

Stdlib-only, fast (~20 ms), read-only, and fail-safe (outputs {} on error so a
session is never blocked).
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

AGENTS_CAP_BYTES = 23800  # Slightly under Antigravity's 24,000-byte per-file cap
LINK_RE = re.compile(r"\(([^()\s]+\.md)\)")


def resolve_workspace(payload: dict) -> Path:
    ws_paths = payload.get("workspacePaths") or []
    if ws_paths and Path(ws_paths[0]).is_dir():
        return Path(ws_paths[0])
    cwd = payload.get("cwd")
    if cwd and Path(cwd).is_dir():
        return Path(cwd)
    return Path(__file__).resolve().parents[2]


def find_local_memory_dir(workspace: Path) -> Path | None:
    """Locate Claude's local memory directory for this project on Dan's Mac."""
    home = Path.home()
    candidates = []
    for path_variant in (workspace, workspace.resolve()):
        slug = re.sub(r"[^A-Za-z0-9]", "-", str(path_variant))
        candidates.append(home / ".claude" / "projects" / slug / "memory")
    # Also check legacy username symlink if present
    candidates.append(
        home
        / ".claude"
        / "projects"
        / "-Users-danrrose-Projects-Claude-Projects-Abs-By-AI"
        / "memory"
    )
    for cand in candidates:
        if (cand / "MEMORY.md").is_file():
            return cand
    return None


def extract_agents_overflow(agents_path: Path) -> tuple[str, int, int]:
    """Return (overflow_markdown, start_line, total_lines) for AGENTS.md past 24 KB."""
    if not agents_path.is_file():
        return "", 0, 0
    raw_bytes = agents_path.read_bytes()
    total_lines = raw_bytes.count(b"\n") + 1
    if len(raw_bytes) <= AGENTS_CAP_BYTES:
        return "", 0, total_lines

    prefix_text = raw_bytes[:AGENTS_CAP_BYTES].decode("utf-8", errors="ignore")
    full_text = raw_bytes.decode("utf-8", errors="replace")
    lines = full_text.splitlines()
    cutoff_line_idx = max(0, prefix_text.count("\n") - 1)

    # Walk backward to the nearest '## ' heading before the cutoff so we inject
    # clean complete sections without a broken mid-paragraph fragment.
    start_idx = cutoff_line_idx
    for idx in range(cutoff_line_idx, -1, -1):
        if lines[idx].startswith("## "):
            start_idx = idx
            break

    overflow = "\n".join(lines[start_idx:]).strip()
    return overflow, start_idx + 1, total_lines


def build_merged_memory_index(
    local_dir: Path | None, repo_dir: Path
) -> tuple[str, list[str]]:
    """Merge local MEMORY.md (canonical) with any repo-only entries in Docs/memory/MEMORY.md."""
    sources: list[str] = []
    local_lines: list[str] = []
    seen_targets: set[str] = set()

    if local_dir and (local_dir / "MEMORY.md").is_file():
        sources.append(f"local={local_dir}")
        local_lines = (local_dir / "MEMORY.md").read_text(
            encoding="utf-8", errors="replace"
        ).splitlines()
        for line in local_lines:
            for match in LINK_RE.findall(line):
                seen_targets.add(match)

    repo_extra: list[str] = []
    repo_index = repo_dir / "MEMORY.md"
    if repo_index.is_file():
        sources.append(f"repo={repo_dir}")
        repo_lines = repo_index.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines()
        if not local_lines:
            local_lines = repo_lines
        else:
            for line in repo_lines:
                matches = LINK_RE.findall(line)
                if matches and all(m not in seen_targets for m in matches):
                    repo_extra.append(line)
                    seen_targets.update(matches)

    if not local_lines:
        return "", sources

    merged = "\n".join(local_lines).rstrip()
    if repo_extra:
        merged += (
            "\n\n## Additional Repo-Only Memory Entries (`Docs/memory/`)\n"
            + "\n".join(repo_extra)
        )
    return merged, sources


def file_mtime_str(path: Path) -> str:
    if not path.is_file():
        return "missing"
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def main() -> int:
    try:
        raw_stdin = sys.stdin.read().strip()
        payload = json.loads(raw_stdin) if raw_stdin else {}
    except Exception:
        payload = {}

    try:
        workspace = resolve_workspace(payload)
        agents_path = workspace / "AGENTS.md"
        repo_mem_dir = workspace / "Docs" / "memory"
        local_mem_dir = find_local_memory_dir(workspace)

        sections: list[str] = []
        sections.append(
            "# Abs By AI — Shared Persistent Memory & Complete Rules (Auto-Loaded)\n"
            "Loaded live by `.agents/hooks/session_start_memory.py` at session start."
        )

        # 1. Status pointers
        coord_path = workspace / "AI_COORDINATION.md"
        decisions_path = workspace / "Docs" / "DAN_DECISIONS.md"
        primary_mem_path = str(local_mem_dir) if local_mem_dir else str(repo_mem_dir)
        sections.append(
            "## Quick Pointers\n"
            f"- Primary memory directory (read specific `.md` files here on demand): `{primary_mem_path}`\n"
            f"- Repo memory mirror: `{repo_mem_dir}`\n"
            f"- Active coordination board: `{coord_path}` (last updated {file_mtime_str(coord_path)} — read before starting/claiming work)\n"
            f"- Dan's open decisions: `{decisions_path}` (last updated {file_mtime_str(decisions_path)})"
        )

        # 2. Merged MEMORY.md index
        merged_mem, sources = build_merged_memory_index(local_mem_dir, repo_mem_dir)
        if merged_mem:
            sections.append(
                f"## Shared Memory Index (`MEMORY.md` — {', '.join(sources)})\n"
                "Scan this index before acting in any domain and use `read_file` on any matching `.md` file above.\n\n"
                + merged_mem
            )

        # 3. Overflow of AGENTS.md past 24 KB
        overflow, start_line, total_lines = extract_agents_overflow(agents_path)
        if overflow:
            sections.append(
                f"## Remainder of `AGENTS.md` (Lines {start_line}–{total_lines}, Truncated Past 24 KB Cap)\n"
                "These standing rules are active on equal footing with lines 1–112 loaded in `<user_rules>`.\n\n"
                + overflow
            )

        if len(sections) <= 1:
            print("{}")
            return 0

        out = {
            "injectSteps": [
                {
                    "systemMessage": {
                        "systemMessage": "\n\n---\n\n".join(sections)
                    }
                }
            ]
        }
        sys.stdout.write(json.dumps(out))
        return 0
    except Exception:
        # Never block session startup on an unexpected hook error
        sys.stdout.write("{}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
