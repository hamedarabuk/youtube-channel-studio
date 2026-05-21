"""
scripts/gpt_image_client.py — OpenAI gpt-image-2 image generation client.

Dependencies:
    pip install openai

Auth:
    OPENAI_API_KEY must be set in .env (at repo root) or as an environment variable.

Supported sizes:
    Popular: 1024x1024 (default), 1536x1024, 1024x1536, 2048x2048,
             2048x1152, 3840x2160, 2160x3840, auto
    Custom:  any WIDTHxHEIGHT meeting gpt-image-2 constraints
             (multiples of 16, max edge 3840, ratio <= 3:1,
             655,360 to 8,294,400 total pixels). Example: 1792x1024 for YouTube thumbnails.

Use this client for visuals that require readable on-image text (English, or
other languages), infographics, charts, posters, social cards with overlay
typography, diagrams, and YouTube thumbnails with text overlays.

Limitations:
    - Transparent backgrounds are NOT supported by gpt-image-2. Use --background auto
      or --background opaque.
    - input_fidelity is NOT a valid parameter for gpt-image-2; the model processes all
      reference images at high fidelity automatically.

Usage:
    # Text-to-image (YouTube thumbnail):
    python scripts/gpt_image_client.py \\
        --action generate \\
        --prompt "YouTube thumbnail: creator looking surprised, bold text 'FIRST TRY'" \\
        --size 1792x1024 \\
        --quality high \\
        --output channels/my-channel/videos/2026-05-21-my-video/outputs/thumbnail.png

    # Image editing with references:
    python scripts/gpt_image_client.py \\
        --action edit \\
        --prompt "Add dramatic lighting and text overlay 'IT WORKED'" \\
        --reference channels/my-channel/reference.png \\
        --output channels/my-channel/videos/2026-05-21-my-video/outputs/thumbnail-edit.png

Exit codes: 0=success, 1=error.

Note: C2PA metadata is stripped automatically via scripts/lib/image_io.strip_metadata.
Pricing (approximate): low ~$0.006, medium ~$0.053, high ~$0.21 per 1024x1024 image.
"""

from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXIT_OK = 0
EXIT_ERROR = 1

_POPULAR_SIZES = {
    "1024x1024",
    "1536x1024",
    "1024x1536",
    "2048x2048",
    "2048x1152",
    "3840x2160",
    "2160x3840",
    "auto",
}

# gpt-image-2 size constraints (from OpenAI Image API docs):
# - max edge length <= 3840 px
# - both edges multiples of 16 px
# - long edge to short edge ratio <= 3:1
# - total pixels >= 655,360 and <= 8,294,400
_MAX_EDGE = 3840
_MIN_PIXELS = 655_360
_MAX_PIXELS = 8_294_400
_MAX_RATIO = 3.0


def _validate_size(size: str) -> tuple[bool, str]:
    """Return (ok, error_message). Empty error_message when ok=True."""
    if size in _POPULAR_SIZES:
        return True, ""
    if "x" not in size:
        return False, f"--size '{size}' must be WIDTHxHEIGHT (e.g. 1792x1024) or one of: {', '.join(sorted(_POPULAR_SIZES))}"
    try:
        w_str, h_str = size.split("x", 1)
        w, h = int(w_str), int(h_str)
    except ValueError:
        return False, f"--size '{size}' must be integer WIDTHxHEIGHT (e.g. 1792x1024)"
    if w <= 0 or h <= 0:
        return False, f"--size '{size}' edges must be positive"
    if w % 16 != 0 or h % 16 != 0:
        return False, f"--size '{size}' both edges must be multiples of 16 px"
    if max(w, h) > _MAX_EDGE:
        return False, f"--size '{size}' max edge length must be <= {_MAX_EDGE}px"
    ratio = max(w, h) / min(w, h)
    if ratio > _MAX_RATIO:
        return False, f"--size '{size}' long-to-short edge ratio must be <= {_MAX_RATIO}:1 (got {ratio:.2f}:1)"
    pixels = w * h
    if pixels < _MIN_PIXELS:
        return False, f"--size '{size}' total pixels must be >= {_MIN_PIXELS:,} (got {pixels:,})"
    if pixels > _MAX_PIXELS:
        return False, f"--size '{size}' total pixels must be <= {_MAX_PIXELS:,} (got {pixels:,})"
    return True, ""


def _load_api_key() -> str:
    sys.path.insert(0, str(PROJECT_ROOT))
    from config import load_config
    cfg = load_config()
    if not cfg.openai_api_key:
        print(
            "gpt_image: OPENAI_API_KEY is not set. "
            "Add it to .env or set as an environment variable.",
            file=sys.stderr,
        )
        sys.exit(EXIT_ERROR)
    return cfg.openai_api_key


def _write_output(b64_data: str, output_path: Path) -> None:
    """Decode base64 image, write to disk, strip C2PA metadata."""
    image_bytes = base64.b64decode(b64_data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)

    try:
        sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
        from lib.image_io import strip_metadata
        strip_metadata(output_path)
    except Exception as e:
        print(f"gpt_image: warning — metadata strip failed: {e}", file=sys.stderr)

    size_kb = output_path.stat().st_size // 1024
    print(f"gpt_image: saved {size_kb} KB -> {output_path}", file=sys.stderr)


def _action_generate(
    prompt: str,
    size: str,
    quality: str,
    output_format: str,
    compression: int | None,
    background: str,
    moderation: str,
    output_path: Path,
) -> None:
    try:
        from openai import OpenAI
    except ImportError:
        print(
            "gpt_image: openai is not installed. Run: pip install openai",
            file=sys.stderr,
        )
        sys.exit(EXIT_ERROR)

    print(
        f"gpt_image: generating {size} {quality}-quality {output_format} via gpt-image-2...",
        file=sys.stderr,
    )

    api_key = _load_api_key()
    client = OpenAI(api_key=api_key)

    kwargs: dict = dict(
        model="gpt-image-2",
        prompt=prompt,
        size=size,
        quality=quality,
        output_format=output_format,
        n=1,
        background=background,
        moderation=moderation,
    )
    if output_format in ("jpeg", "webp") and compression is not None:
        kwargs["output_compression"] = compression

    result = client.images.generate(**kwargs)
    b64 = result.data[0].b64_json
    if not b64:
        print("gpt_image: no image data returned by the API.", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    _write_output(b64, output_path)


def _action_edit(
    prompt: str,
    reference_paths: list[Path],
    mask_path: Path | None,
    size: str,
    quality: str,
    output_path: Path,
) -> None:
    try:
        from openai import OpenAI, NOT_GIVEN
    except ImportError:
        print(
            "gpt_image: openai is not installed. Run: pip install openai",
            file=sys.stderr,
        )
        sys.exit(EXIT_ERROR)

    print(
        f"gpt_image: editing with {len(reference_paths)} reference(s), "
        f"{size} {quality}-quality via gpt-image-2...",
        file=sys.stderr,
    )

    api_key = _load_api_key()
    client = OpenAI(api_key=api_key)

    ref_handles = [open(p, "rb") for p in reference_paths]
    mask_handle = open(mask_path, "rb") if mask_path else NOT_GIVEN

    try:
        result = client.images.edit(
            model="gpt-image-2",
            image=ref_handles,
            mask=mask_handle,
            prompt=prompt,
            size=size,
            quality=quality,
        )
    finally:
        for fh in ref_handles:
            fh.close()
        if mask_path and mask_handle is not NOT_GIVEN:
            mask_handle.close()

    b64 = result.data[0].b64_json
    if not b64:
        print("gpt_image: no image data returned by the API.", file=sys.stderr)
        sys.exit(EXIT_ERROR)

    _write_output(b64, output_path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or edit images via OpenAI gpt-image-2."
    )
    parser.add_argument(
        "--action",
        choices=["generate", "edit"],
        required=True,
        help="Action to perform.",
    )
    parser.add_argument("--prompt", required=True, help="Text prompt for image generation or editing.")
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output file path. Parent directories are created automatically.",
    )
    parser.add_argument(
        "--size",
        default="1024x1024",
        metavar="SIZE",
        help=(
            f"Output image size. Popular: {', '.join(sorted(_POPULAR_SIZES))}. "
            "Or any WIDTHxHEIGHT meeting gpt-image-2 constraints (multiples of 16, "
            "max edge 3840, ratio <= 3:1, 655,360 to 8,294,400 total pixels). "
            "Default: 1024x1024"
        ),
    )
    parser.add_argument(
        "--quality",
        choices=["low", "medium", "high", "auto"],
        default="medium",
        help="Image quality. Default: medium",
    )
    parser.add_argument(
        "--format",
        choices=["png", "jpeg", "webp"],
        default="png",
        dest="output_format",
        help="Output image format. Default: png",
    )
    parser.add_argument(
        "--compression",
        type=int,
        default=None,
        metavar="0-100",
        help="Compression level 0-100. Only applied when --format is jpeg or webp.",
    )
    parser.add_argument(
        "--background",
        choices=["auto", "opaque"],
        default="auto",
        help=(
            "Background style. gpt-image-2 does not support transparent backgrounds. "
            "Default: auto"
        ),
    )
    parser.add_argument(
        "--moderation",
        choices=["auto", "low"],
        default="auto",
        help="Content moderation level. Default: auto",
    )
    parser.add_argument(
        "--reference",
        action="append",
        default=[],
        dest="reference",
        type=Path,
        metavar="PATH",
        help=(
            "Local image file for the edit action. "
            "Pass multiple times for multiple references. "
            "Only valid with --action edit."
        ),
    )
    parser.add_argument(
        "--mask",
        type=Path,
        default=None,
        metavar="PATH",
        help="Optional mask image for the edit action. Only valid with --action edit.",
    )

    args = parser.parse_args()

    # Validate size against gpt-image-2 constraints (popular preset or custom).
    ok, err = _validate_size(args.size)
    if not ok:
        print(f"gpt_image: {err}", file=sys.stderr)
        return EXIT_ERROR

    # Validate compression range.
    if args.compression is not None and not (0 <= args.compression <= 100):
        print(
            f"gpt_image: --compression must be 0-100, got {args.compression}",
            file=sys.stderr,
        )
        return EXIT_ERROR

    if args.action == "generate":
        if args.reference:
            print(
                "gpt_image: --reference is only valid with --action edit.",
                file=sys.stderr,
            )
            return EXIT_ERROR
        if args.mask:
            print(
                "gpt_image: --mask is only valid with --action edit.",
                file=sys.stderr,
            )
            return EXIT_ERROR

        _action_generate(
            prompt=args.prompt,
            size=args.size,
            quality=args.quality,
            output_format=args.output_format,
            compression=args.compression,
            background=args.background,
            moderation=args.moderation,
            output_path=args.output,
        )

    elif args.action == "edit":
        if not args.reference:
            print(
                "gpt_image: --action edit requires at least one --reference file.",
                file=sys.stderr,
            )
            return EXIT_ERROR

        for ref in args.reference:
            if not ref.exists():
                print(
                    f"gpt_image: --reference path does not exist: {ref}",
                    file=sys.stderr,
                )
                return EXIT_ERROR
            if not ref.is_file():
                print(
                    f"gpt_image: --reference path is not a file: {ref}",
                    file=sys.stderr,
                )
                return EXIT_ERROR

        if args.mask is not None:
            if not args.mask.exists():
                print(
                    f"gpt_image: --mask path does not exist: {args.mask}",
                    file=sys.stderr,
                )
                return EXIT_ERROR
            if not args.mask.is_file():
                print(
                    f"gpt_image: --mask path is not a file: {args.mask}",
                    file=sys.stderr,
                )
                return EXIT_ERROR

        _action_edit(
            prompt=args.prompt,
            reference_paths=args.reference,
            mask_path=args.mask,
            size=args.size,
            quality=args.quality,
            output_path=args.output,
        )

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
