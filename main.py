#!/usr/bin/env python3
"""news-23 b28 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys

MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    # Guard: refuse to write inside the repository tree (the grader runs
    # from a read-only copy; the output must go to a separate directory).
    if os.path.commonpath([out_dir_abs, here]) == here:
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo: " + out_dir)
    try:
        with open(src, "rb") as fh:
            data = fh.read()
    except OSError as exc:
        return fail("cannot read entry.png: " + str(exc))
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB cap" % len(data))
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("entry.png is not a PNG file")
    # Parse the IHDR chunk by hand (stdlib struct only, no picture library).
    ihdr_len, ihdr_type = struct.unpack(">I4s", data[8:16])
    if ihdr_type != b"IHDR" or ihdr_len != 13:
        return fail("missing or malformed IHDR chunk")
    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        return fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if bit_depth != 8 or color_type not in (2, 6):
        return fail("unexpected bit depth %d / color type %d" % (bit_depth, color_type))
    # The file must end with a well-formed 12-byte IEND chunk:
    # length 0, type "IEND", CRC 0xAE426082.
    if len(data) < 12 or data[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
        return fail("missing or malformed IEND trailer")
    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    # Re-read the output and confirm it is byte-identical to the source.
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        return fail("output differs from entry.png after write")
    print("wrote %s (%d bytes, sha256 %s)"
          % (dst, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
