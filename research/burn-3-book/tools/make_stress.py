"""Make a throwaway stress copy of the book prototype: N dummy pages + M dummy ~200 KB images.

Usage: python -I tools/make_stress.py <site-proto dir> <stress dir> [pages=300] [images=50]
The stress dir is deleted and recreated. Delete it after the test.
Images are random-noise PNGs (incompressible), so each really is ~200 KB on disk.
"""
import random
import shutil
import struct
import sys
import zlib
from pathlib import Path

WORDS = ("light curve transit depth star planet binary eclipse sector flux noise period orbit radius "
         "candidate vetting magnitude cadence baseline centroid shift odd even secondary dip signal").split()


def png(path, w=260, h=260, seed=0):
    rnd = random.Random(seed)
    rows = b"".join(b"\x00" + rnd.randbytes(w * 3) for _ in range(h))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    n_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    n_images = int(sys.argv[4]) if len(sys.argv) > 4 else 50
    shutil.rmtree(dst, ignore_errors=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("site", ".cache"))
    pages = dst / "docs" / "stress"
    (pages / "img").mkdir(parents=True)
    rnd = random.Random(42)
    for i in range(1, n_pages + 1):
        paras = "\n\n".join(" ".join(rnd.choice(WORDS) for _ in range(120)).capitalize() + "." for _ in range(8))
        (pages / f"p{i:03d}.md").write_text(f"# Stress page {i}\n\n## Section A\n\n{paras}\n\n## Section B\n\n{paras}\n", encoding="utf-8")
    for i in range(1, n_images + 1):
        png(pages / "img" / f"i{i:02d}.png", seed=i)
    gallery = "\n\n".join(f"![Dummy image {i}](img/i{i:02d}.png)" for i in range(1, n_images + 1))
    (pages / "gallery.md").write_text(f"# Stress gallery\n\n{gallery}\n", encoding="utf-8")
    sizes = [p.stat().st_size for p in (pages / "img").iterdir()]
    print(f"made {n_pages} pages + gallery, {n_images} images, {min(sizes)}-{max(sizes)} bytes each, {sum(sizes) / 2**20:.1f} MB total")


if __name__ == "__main__":
    main()
