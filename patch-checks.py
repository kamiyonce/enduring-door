#!/usr/bin/env python3
from pathlib import Path
src = Path("door.final.html")
dst = Path("enduring-pages/door.html")
if not src.exists():
    raise SystemExit("door.final.html missing")
dst.write_text(src.read_text())
print("copied door.final.html")
