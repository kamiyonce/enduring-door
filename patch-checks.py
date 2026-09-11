#!/usr/bin/env python3
"""Align 17 trope hit-boxes to printed ink on book-open.mp4 @ 11.05s.

Check sits one space before the first letter. Click target is the printed line.
Video and overlay share the same 9:16 .stage box.
Next isolates selected tropes and darkens the rest on the 11.05 freeze.
"""
from pathlib import Path
import re

TROPES = [
    ("ML_demon", "Morally Dark MMC", "morally dark MMC"),
    ("ML_prox", "Forced Proximity- One Bed", "forced proximity / one bed"),
    ("ML_medical", "Medical K!nk", "medical kink"),
    ("ML_wings", "Learn Me Agony- Don't do that again", "learn me agony"),
    ("ML_enemies", "Enemies to Lovers to *Enemies*", "enemies to lovers to enemies"),
    ("ML_hefalls", "He. Falls. First", "he falls first"),
    ("ML_touch", "Tøuch Her and D!E", "touch her and die"),
    ("ML_fated", "Fated Mates", "fated mates"),
    ("ML_academia", "Academia / Battle Setting", "academia / battle setting"),
    ("ML_slowburn", "Slow BURN", "slow burn"),
    ("ML_captor", "Cǃptor/ Capt!ve", "captor / captive"),
    ("ML_mortal", "Mortal / Immortal", "mortal / immortal"),
    ("ML_harem", "Reverse Harem- Beg Me", "reverse harem"),
    ("ML_forbidden", "Forbidden Feelings", "forbidden feelings"),
    ("ML_possessive", "Possessive/ Protective MMC", "possessive / protective MMC"),
    ("ML_dom", "Dom/Sub-Brat Heat", "Dom / brat heat"),
    ("ML_meta", "Fourth Wall Seduction (I'm talking to you)", "fourth wall seduction"),
]
# top = vertical center of ink, first = left edge of first letter,
# last = right edge of last letter. Percent of 720x1280 frame at 11.05s.
LINES = [
    (13.91, 24.31, 70.80),
    (19.02, 20.28, 76.00),
    (24.02, 31.67, 63.80),
    (28.83, 14.58, 82.00),
    (33.40, 15.56, 81.20),
    (37.77, 30.69, 64.00),
    (42.38, 25.00, 70.00),
    (46.99, 33.61, 62.20),
    (51.76, 21.94, 73.60),
    (56.37, 32.22, 62.60),
    (61.17, 28.06, 66.30),
    (65.27, 27.92, 67.00),
    (69.77, 22.36, 73.20),
    (74.34, 27.78, 66.00),
    (79.06, 20.00, 74.60),
    (83.40, 25.69, 69.20),
    (87.77, 24.44, 72.20),
]
CORES = ["ML_demon", "ML_enemies", "ML_hefalls"]
FLAVOR = [k for k, _, __ in TROPES if k not in CORES]

p = Path("enduring-pages/door.html")
h = p.read_text()

h = h.replace("const TROPES_AT = 13.15;", "const TROPES_AT = 11.05;")
h = h.replace("const TROPES_AT = 10.17;", "const TROPES_AT = 11.05;")
h = h.replace(
    '          <source src="https://enduring-timeline.netlify.app/assets/book-open.mp4" type="video/mp4">\n',
    "",
)

NEW_OVERLAY_CSS = """  .hero {
    position: absolute;
    inset: 0;
    background: #000;
  }
  .stage {
    position: absolute;
    top: 50%;
    left: 50%;
    width: min(100vw, calc(100dvh * 9 / 16));
    height: min(100dvh, calc(100vw * 16 / 9));
    transform: translate(-50%, -50%);
    z-index: 3;
    overflow: visible;
  }
  .stage video,
  .hero video {
    display: block;
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    object-position: center;
    background: #000;
  }
  .hero video.laugh { display: none; z-index: 2; }
  .hero video.laugh.on { display: block; }
  .isolate-veil {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 3;
    pointer-events: none;
    opacity: 0;
    transition: opacity .55s ease;
  }
  .stage.isolated .isolate-veil { opacity: 1; }
  .stage.isolated .trope-hits { pointer-events: none; }
  .stage.isolated .trope-hit:not(.on) { opacity: 0; }
  .stage.isolated .trope-hit.on {
    z-index: 6;
    background: rgba(226,195,122,.10);
  }
  .stage.isolated .trope-next { opacity: 0 !important; pointer-events: none !important; }
  .trope-hits {
    position: absolute;
    inset: 0;
    opacity: 0;
    pointer-events: none;
    z-index: 4;
    overflow: visible;
  }
  .trope-hits.on { opacity: 1; pointer-events: auto; }
  .trope-hit {
    appearance: none;
    position: absolute;
    height: 5.05%;
    margin: 0;
    padding: 0;
    border: 0;
    background: transparent;
    cursor: pointer;
    display: block;
    transform: translateY(-50%);
    overflow: visible;
    -webkit-tap-highlight-color: transparent;
    z-index: 4;
  }
  .trope-hit:nth-child(17) { height: 6.35%; }
  .trope-hit:active,
  .trope-hit.on {
    background: rgba(226,195,122,.14);
  }
"""
for i, (top, first, last) in enumerate(LINES, start=1):
    width = max(18.0, (last - first) + 1.4)
    NEW_OVERLAY_CSS += (
        f"  .trope-hit:nth-child({i}) {{ "
        f"top: {top:.2f}%; left: {first:.2f}%; width: {width:.2f}%; }}\n"
    )

NEW_OVERLAY_CSS += """  .trope-label {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    clip-path: inset(50%);
    white-space: nowrap;
    pointer-events: none;
  }
  .trope-hit.on::before {
    content: \"\u2713\";
    position: absolute;
    right: 100%;
    margin-right: 0.62em;
    top: 50%;
    transform: translateY(-50%);
    color: #e2c37a;
    font-size: clamp(15px, 3.6vw, 20px);
    font-weight: 700;
    line-height: 1;
    text-shadow: 0 1px 4px rgba(0,0,0,.95);
  }
  .trope-next {
    position: absolute; left: 50%; bottom: 2.2%;
    transform: translateX(-50%);
    opacity: 0; pointer-events: none;
    z-index: 5;
    background: transparent; color: #c9a36a;
    border: 1px solid #c9a36a;
    padding: 8px 26px;
    letter-spacing: .28em;
    text-transform: uppercase;
    font-size: 11px;
    font-family: \"Iowan Old Style\", Palatino, Georgia, serif;
  }
  .trope-next.on { opacity: 1; pointer-events: auto; }
"""

m = re.search(
    r"  \\.hero \\{.*?\\n  \\.trope-next\\.on \\{ opacity: 1; pointer-events: auto; \\}\\n",
    h,
    re.S,
)
if not m:
    raise SystemExit("hero/trope css block not found")
h = h[: m.start()] + NEW_OVERLAY_CSS + h[m.end() :]

h = re.sub(
    r"  @media \\(min-aspect-ratio: 3/4\\) \\{.*?\\.hero video \\{ object-fit: contain; \\}\\n  \\}\\n",
    "",
    h,
    count=1,
    flags=re.S,
)
h = h.replace("object-fit: cover;", "object-fit: contain;")

h = re.sub(
    r"\\n  \\.isolate-veil \\{.*?\\n  \\.stage\\.isolated \\.trope-next \\{[^}]+\\}\\n",
    "\\n",
    h,
    count=1,
    flags=re.S,
)

btns = "\\n".join(
    f'          <button type="button" class="trope-hit" data-q1="{k}" aria-label="{lab.replace("*", "")}"><span class="trope-label">{lab}</span></button>'
    for k, lab, _ in TROPES
)
NEW_HERO = f'''      <div class="hero">
        <div class="stage" id="doorStage">
        <video id="doorZoom" muted playsinline preload="auto" poster="assets/book-open-freeze.jpg" aria-label="Enduring — can you endure me?">
          <source src="assets/book-open.mp4" type="video/mp4">
        </video>
        <svg class="isolate-veil" id="isolateVeil" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path id="isolatePath" fill="rgba(0,0,0,.78)" fill-rule="evenodd"></path></svg>
        <div class="trope-hits" id="tropeHits" aria-label="Choose tropes">
{btns}
        </div>
        <button type="button" class="trope-next" id="tropeNext">Next</button>
        <button type="button" id="start" class="yes-btn">Yes</button>
        </div>
      </div>'''

m = re.search(r'      <div class="hero">.*?</div>\\n      </div>', h, re.S)
if not m:
    m = re.search(r'      <div class="hero">.*?<button type="button" id="start" class="yes-btn">Yes</button>\\s*</div>\\s*</div>', h, re.S)
if not m:
    raise SystemExit("hero html block not found")
h = h[: m.start()] + NEW_HERO + h[m.end() :]

lab = re.search(r"const Q1_LABEL = \\{.*?\\};", h, re.S)
if lab:
    body = ",\\n".join(f"  {k}: {v!r}" for k, _, v in TROPES)
    h = h[: lab.start()] + "const Q1_LABEL = {\\n" + body + "\\n};" + h[lab.end() :]

sr = re.search(r'<div class="sr-q1" aria-hidden="true">.*?</div>', h, re.S)
if sr:
    boxes = "\\n".join(f'      <input type="checkbox" data-q1="{k}">' for k, _, __ in TROPES)
    h = (
        h[: sr.start()]
        + f'<div class="sr-q1" aria-hidden="true">\\n{boxes}\\n    </div>'
        + h[sr.end() :]
    )

h = re.sub(
    r"const flavor = \\[ [^\\]]+\\]\\.filter\\(k => state\\.q1\\[k\\]\\)\\.map\\(k => Q1_LABEL\\[k\\]\\);",
    "const flavor = ["
    + ",".join(repr(k) for k in FLAVOR)
    + "].filter(k => state.q1[k]).map(k => Q1_LABEL[k]);",
    h,
    count=1,
)

old_show = """      document.getElementById('tropeHits').classList.add('on');
      document.getElementById('tropeNext').classList.add('on');"""
new_show = """      document.getElementById('tropeHits').classList.add('on');
      syncTropeNext();"""
if old_show in h:
    h = h.replace(old_show, new_show, 1)

if "function syncTropeNext()" not in h:
    old_click = """document.querySelectorAll('.trope-hit, #s1 .ink').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('on');
    syncQ1(btn.dataset.q1);
  });
});"""
    new_click = """function syncTropeNext() {
  const n = document.querySelectorAll('.trope-hit.on').length;
  document.getElementById('tropeNext').classList.toggle('on', n >= 3);
}
document.querySelectorAll('.trope-hit, #s1 .ink').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('on');
    syncQ1(btn.dataset.q1);
    syncTropeNext();
  });
});"""
    if old_click in h:
        h = h.replace(old_click, new_click, 1)

ISOLATE_JS = """function isolatePicks() {
  const stage = document.getElementById('doorStage');
  const path = document.getElementById('isolatePath');
  const selected = [...document.querySelectorAll('.trope-hit.on')];
  if (!stage || !path || !selected.length) return;
  const sr = stage.getBoundingClientRect();
  if (!sr.width || !sr.height) return;
  const holes = selected.map(el => {
    const r = el.getBoundingClientRect();
    const padL = sr.width * 0.048;
    const padR = sr.width * 0.012;
    const padY = sr.height * 0.005;
    const x = ((r.left - sr.left - padL) / sr.width) * 100;
    const y = ((r.top - sr.top - padY) / sr.height) * 100;
    const w = ((r.width + padL + padR) / sr.width) * 100;
    const hgt = ((r.height + padY * 2) / sr.height) * 100;
    return 'M' + x.toFixed(2) + ' ' + y.toFixed(2) + 'h' + w.toFixed(2) + 'v' + hgt.toFixed(2) + 'h' + (-w).toFixed(2) + 'z';
  });
  path.setAttribute('d', 'M0 0H100V100H0z ' + holes.join(' '));
  stage.classList.add('isolated');
  document.getElementById('tropeNext').classList.remove('on');
}
function refreshIsolate() {
  const stage = document.getElementById('doorStage');
  if (stage && stage.classList.contains('isolated')) isolatePicks();
}
window.addEventListener('resize', refreshIsolate);
document.getElementById('tropeNext').onclick = () => {
  isolatePicks();
};"""

h = re.sub(
    r"function isolatePicks\\(\\) \\{.*?\\ndocument\\.getElementById\\('tropeNext'\\)\\.onclick = \\(\\) => \\{\\n  isolatePicks\\(\\);\\n\\};",
    ISOLATE_JS,
    h,
    count=1,
    flags=re.S,
)
old_next = """document.getElementById('tropeNext').onclick = () => {
  document.body.classList.remove('landing-on');
  show('s2');
};"""
if old_next in h:
    h = h.replace(old_next, ISOLATE_JS, 1)
if "function isolatePicks()" not in h:
    raise SystemExit("failed to insert isolatePicks")

if "syncTropeNext" not in h:
    raise SystemExit("failed to insert Next gate")

old_no = "I felt your heart flutter on the first (' + (first || 'mismatch') + '). Trust me"
new_no = "I felt your heart flutter when you clicked it. But you are nervous so this door is not opening for you. Trust me"
if old_no in h:
    h = h.replace(old_no, new_no, 1)

old_end = "I won’t bait you in.';"
new_end = "I won’t bait you in. unless you bait me with your eyes closed in the shower.';"
if old_end in h and "eyes closed in the shower" not in h:
    h = h.replace(old_end, new_end, 1)
old_end2 = "I won't bait you in.';"
if old_end2 in h and "eyes closed in the shower" not in h:
    h = h.replace(old_end2, new_end, 1)

h = h.replace(" shower. yeah yeah", " shower.")
h = h.replace(" yeah yeah", "")
h = h.replace("-Menace who Kneels", "Menace who Kneels")

old_vid = '<video class="door-open-vid" id="doorOpenVid" src="assets/door-open.mp4" playsinline muted autoplay controls loop preload="auto" aria-label="The door opens"></video>'
new_vid = '<video class="door-open-vid" id="doorOpenVid" src="assets/door-open.mp4" poster="assets/door-open-poster.jpg" playsinline autoplay loop preload="auto" aria-label="The door opens"></video>'
if old_vid in h:
    h = h.replace(old_vid, new_vid, 1)

old_play = "if (v) { try { v.currentTime = 0; v.muted = true; v.play(); } catch (e) {} }"
new_play = "if (v) { try { v.currentTime = 0; v.muted = false; v.play().catch(() => { v.muted = true; v.play(); }); } catch (e) {} }"
if old_play in h:
    h = h.replace(old_play, new_play, 1)

checks = [
    "top: 13.91%",
    "top: 87.77%",
    "left: 24.31%",
    "left: 14.58%",
    "left: 15.56%",
    'id="doorStage"',
    'id="isolateVeil"',
    "function isolatePicks()",
    "right: 100%",
    "margin-right: 0.62em",
    "TROPES_AT = 11.05",
]
for c in checks:
    if c not in h:
        raise SystemExit(f"missing {c}")
if h.count(".trope-hit:nth-child") < 17:
    raise SystemExit("expected 17 line rules")
if "object-fit: cover" in h:
    raise SystemExit("cover leaked")
if h.count('class="trope-hit"') != 17:
    raise SystemExit(f"expected 17 buttons, got {h.count('class=\"trope-hit\"')}")
nxt = h.split("document.getElementById('tropeNext').onclick")[-1][:240]
if "s2" in nxt:
    raise SystemExit("Next still jumps to s2")

p.write_text(h)
print("patched: isolate-on-Next + first-letter checks")
print("line1", "top: 13.91%; left: 24.31%" in h)
print("isolate", "isolatePicks" in h and "isolateVeil" in h)
