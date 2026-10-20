"""Draw the two-suns app icon as PNG with the standard library only (no Pillow)."""
import struct, sys, zlib
from pathlib import Path

def png(size, path):
    bg, amber, blue = (11, 15, 26), (242, 181, 85), (138, 180, 255)
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            u, v = x / size, y / size
            c = bg
            if (u - .42) ** 2 + (v - .5) ** 2 < .2 ** 2: c = amber      # big sun
            if (u - .72) ** 2 + (v - .38) ** 2 < .09 ** 2: c = blue     # second sun
            row += bytes(c)
        rows.append(bytes(row))
    def chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b"")
    Path(path).write_bytes(data)

out = Path(sys.argv[1])
for s in (180, 512):
    png(s, out / f"icon-{s}.png")
