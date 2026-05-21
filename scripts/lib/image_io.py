"""
scripts/lib/image_io.py — image metadata sanitiser for AI-generated images.

Why this exists: AI image generators (OpenAI gpt-image-2, Google Gemini, etc.)
embed C2PA / Content Authenticity Initiative metadata as PNG iTXt chunks
(`c2pa` chunk plus `xmpRights` etc.). LinkedIn, Instagram, and other social
platforms read these and display a visible "Cr" / "Made with AI" badge on the
post. This module strips ALL ancillary chunks by re-encoding the pixel data
into a fresh image, leaving only the bare image data.

The invisible SynthID watermark embedded in pixel data by Google cannot be
removed by metadata stripping, and no attempt is made to do so.

Stdlib + Pillow only. No other dependencies.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional


def strip_metadata(path: Path | str, out_path: Optional[Path | str] = None) -> Path:
    """
    Strip ALL metadata (EXIF, XMP, iTXt including C2PA, tEXt, etc.) from a PNG/JPEG.
    If `out_path` is None, overwrites the source file in place.

    Returns the path written. Raises ImportError if Pillow isn't installed.
    """
    from PIL import Image

    src = Path(path)
    dst = Path(out_path) if out_path is not None else src

    img = Image.open(src)
    img.load()

    # Build a fresh image with the same mode and size, copy raw pixel data.
    # This drops all PIL-known metadata in info dict AND any platform-specific
    # ancillary chunks (PNG iTXt, JPEG EXIF/XMP segments).
    clean = Image.new(img.mode, img.size)
    clean.putdata(list(img.getdata()))

    # Detect format from src extension; default to PNG for unknown.
    fmt = (img.format or "PNG").upper()
    save_kwargs: dict = {"format": fmt}
    if fmt == "PNG":
        save_kwargs["optimize"] = True
        # pnginfo=None ensures no chunks beyond the required ones are written.
        from PIL import PngImagePlugin
        save_kwargs["pnginfo"] = PngImagePlugin.PngInfo()  # empty info
    elif fmt in ("JPEG", "JPG"):
        save_kwargs["quality"] = 95
        save_kwargs["optimize"] = True
        # exif="" prevents Pillow from carrying any EXIF.
        save_kwargs["exif"] = b""

    clean.save(dst, **save_kwargs)
    return dst


def has_c2pa_chunk(path: Path | str) -> bool:
    """Quick check: does this PNG file contain a C2PA manifest chunk?"""
    p = Path(path)
    data = p.read_bytes()
    # Look for any iTXt or tEXt chunk whose keyword starts with 'c2pa'
    # PNG chunks: 4-byte length, 4-byte type, payload, 4-byte CRC
    # iTXt keyword starts at offset 8 of the chunk's payload
    return b"c2pa" in data[:8000].lower() or b"contentcredentials" in data[:8000].lower()
