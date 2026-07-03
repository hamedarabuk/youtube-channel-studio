"""
scripts/yt_studio.py: shared helpers for the youtube-channel-studio toolkit.

Functions:
  slugify(text)              -- kebab-case slug, max 60 chars.
  today_iso()                -- returns today as YYYY-MM-DD.
  ensure_channel_dir(...)    -- creates channels/<slug>/ and videos/ subdirectory.
  load_foundation(...)       -- reads channels/<slug>/foundation.md.
  write_video_manifest(...)  -- writes outputs/run.json.

Import from anywhere in the repo:
  from scripts.yt_studio import slugify, today_iso, ensure_channel_dir, ...
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path


def slugify(text: str) -> str:
    """
    Convert arbitrary text to a kebab-case slug.

    Rules:
    - Strip leading '@' (handles YouTube handles like @ConcreetoClay).
    - Lowercase.
    - Replace any non-alphanumeric character with a hyphen.
    - Collapse consecutive hyphens to one.
    - Strip leading/trailing hyphens.
    - Truncate to 60 characters (truncation at a hyphen boundary where possible).

    Examples:
        slugify('@ConcreetoClay')  -> 'concreettoclay'
        slugify('How I Made a Gold Ring') -> 'how-i-made-a-gold-ring'
    """
    text = text.lstrip("@").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    if len(text) > 60:
        truncated = text[:60]
        # Prefer a clean cut at the last hyphen within the limit.
        last_hyphen = truncated.rfind("-")
        if last_hyphen > 0:
            truncated = truncated[:last_hyphen]
        text = truncated.strip("-")
    return text


def today_iso() -> str:
    """Return today's date as YYYY-MM-DD (ISO 8601)."""
    return date.today().isoformat()


def ensure_channel_dir(repo_root: Path, handle: str) -> Path:
    """
    Given a channel handle (e.g. '@ConcreetoClay' or 'concreettoclay'),
    compute the slug and create the channel directory structure:

        channels/<slug>/
        channels/<slug>/videos/

    Returns the channel directory path. Idempotent: safe to call repeatedly.
    """
    slug = slugify(handle)
    channel_dir = repo_root / "channels" / slug
    videos_dir = channel_dir / "videos"
    channel_dir.mkdir(parents=True, exist_ok=True)
    videos_dir.mkdir(parents=True, exist_ok=True)
    return channel_dir


def load_foundation(repo_root: Path, handle: str) -> str:
    """
    Read channels/<slug>/foundation.md and return its full content as a string.

    Raises FileNotFoundError with a helpful message if the file does not exist.
    Run the yt-channel-init skill first to create it.
    """
    slug = slugify(handle)
    foundation_path = repo_root / "channels" / slug / "foundation.md"
    if not foundation_path.exists():
        raise FileNotFoundError(
            f"Foundation file not found: {foundation_path}\n"
            f"Run the yt-channel-init skill for '{handle}' to create it."
        )
    return foundation_path.read_text(encoding="utf-8")


def write_video_manifest(video_dir: Path, manifest: dict) -> Path:
    """
    Write the manifest dict to outputs/run.json inside video_dir.

    Creates the outputs/ subdirectory if it does not exist.
    Returns the path of the written file.
    """
    outputs_dir = video_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    run_path = outputs_dir / "run.json"
    run_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )
    return run_path


if __name__ == "__main__":
    print("youtube-channel-studio helpers v0.1")
