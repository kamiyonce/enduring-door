#!/usr/bin/env python3
"""Install the measured 17-line overlay onto enduring-pages/door.html.

Click target = printed ink. Gold check sits one space before the first letter.
No wash, no black label text. Timing and Next gate stay untouched.
"""
from pathlib import Path

DST = Path("enduring-pages/door.html")
SRC_CANDIDATES = [
    Path("door.good.html"),
    Path("door.final.html"),
    Path("enduring-pages/door.html"),
]

NEEDLES = [
    "top: 13.91%",
    "left: 24.31%",
    "left: 14.58%",
    "top: 87.77%",
    "right: 100%",
    "margin-right: 0.62em",
    "TROPES_AT = 11.05",
    "BLANK_AT = 13.13",
    "ASK_AT = 6.4",
    'id="doorStage"',
    'class="trope-hit"',
]


def pick_source() -> Path:
    for p in SRC_CANDIDATES:
        if not p.exists():
            continue
        text = p.read_text()
        if all(n in text for n in NEEDLES) and text.count('class="trope-hit"') == 17:
            return p
    raise SystemExit("no known-good door.html with 17 first-letter boxes")


def assert_good(text: str, label: str) -> None:
    missing = [n for n in NEEDLES if n not in text]
    if missing:
        raise SystemExit(f"{label} missing {missing}")
    n = text.count('class="trope-hit"')
    if n != 17:
        raise SystemExit(f"{label} expected 17 trope buttons, got {n}")
    if "rgba(226,195,122,.14)" in text:
        raise SystemExit(f"{label} yellow wash still present")
    if "#070707" in text:
        raise SystemExit(f"{label} black label color leaked")
    if "object-fit: cover" in text:
        raise SystemExit(f"{label} cover leaked")


src = pick_source()
text = src.read_text()
assert_good(text, src.as_posix())

if not DST.parent.exists():
    raise SystemExit("enduring-pages missing after unzip")

DST.write_text(text)
assert_good(DST.read_text(), DST.as_posix())
print("patched", DST, "from", src, "bytes", DST.stat().st_size)
