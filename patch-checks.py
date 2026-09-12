#!/usr/bin/env python3
"""17 first-letter checks + Kami ornate Next arrow between Fated Mates and the buckle."""
from pathlib import Path
import base64

DST = Path("enduring-pages/door.html")
if not DST.exists():
    raise SystemExit("enduring-pages/door.html missing after unzip")
h = DST.read_text()

h = h.replace("const TROPES_AT = 13.15;", "const TROPES_AT = 11.05;")
h = h.replace("const TROPES_AT = 10.17;", "const TROPES_AT = 11.05;")
if "const BLANK_AT" not in h:
    h = h.replace(
        "const TROPES_AT = 11.05;",
        "const TROPES_AT = 11.05;\nconst BLANK_AT = 13.13;\nconst BLANK_MAX = 13.40;",
        1,
    )
h = h.replace("color: #070707;", "color: transparent;")
h = h.replace("color:#070707;", "color: transparent;")
h = h.replace("object-fit: cover;", "object-fit: contain;")
h = h.replace("background: rgba(226,195,122,.14);", "background: transparent;")

LINES = [
    (13.91, 24.31, 47.89),
    (19.02, 20.28, 57.12),
    (24.02, 31.67, 33.53),
    (28.83, 14.58, 68.82),
    (33.40, 15.56, 67.04),
    (37.77, 30.69, 34.71),
    (42.38, 25.00, 46.40),
    (46.99, 33.61, 29.99),
    (51.76, 21.94, 53.06),
    (56.37, 32.22, 31.78),
    (61.17, 28.06, 39.64),
    (65.27, 27.92, 40.48),
    (69.77, 22.36, 52.24),
    (74.34, 27.78, 39.62),
    (79.06, 20.00, 56.00),
    (83.40, 25.69, 44.91),
    (87.77, 24.44, 49.16),
]
nth = "\n".join(
    "  .trope-hit:nth-child(%d) { top: %.2f%%; left: %.2f%%; width: %.2f%%;%s }"
    % (i, t, l, w, " height: 6.35%;" if i == 17 else "")
    for i, (t, l, w) in enumerate(LINES, 1)
)

OVERLAY = """  .stage {
    position: absolute; top: 50%%; left: 50%%;
    width: min(100vw, calc(100dvh * 9 / 16));
    height: min(100dvh, calc(100vw * 16 / 9));
    transform: translate(-50%%, -50%%); z-index: 3; overflow: visible;
  }
  .stage video, .hero video {
    display: block; position: absolute; inset: 0; width: 100%%; height: 100%%;
    object-fit: contain; object-position: center; background: #000;
  }
  .trope-hits {
    position: absolute; inset: 0; opacity: 0; pointer-events: none;
    z-index: 4; overflow: visible;
  }
  .trope-hits.on { opacity: 1; pointer-events: auto; }
  .trope-hit {
    appearance: none; position: absolute; height: 5.05%%; margin: 0; padding: 0;
    border: 0; background: transparent; cursor: pointer; display: block;
    transform: translateY(-50%%); overflow: visible;
    -webkit-tap-highlight-color: transparent; z-index: 4;
  }
%s
  .trope-label {
    position: absolute; width: 1px; height: 1px; overflow: hidden;
    clip: rect(0 0 0 0); clip-path: inset(50%%); white-space: nowrap;
    pointer-events: none;
  }
  .trope-hit.on::before {
    content: "\\2713"; position: absolute; right: 100%%; margin-right: 0.62em;
    top: 50%%; transform: translateY(-50%%); color: #e2c37a;
    font-size: clamp(15px, 3.6vw, 20px); font-weight: 700; line-height: 1;
    text-shadow: 0 1px 4px rgba(0,0,0,.95); pointer-events: none;
  }
  .chosen-stack {
    position: absolute; left: 9%%; right: 9%%; top: 12%%; bottom: 10%%;
    display: flex; flex-direction: column; justify-content: center;
    align-items: center; gap: 0.38em; z-index: 6; pointer-events: none;
    text-align: center; opacity: 0; visibility: hidden;
  }
  .stage.reprint .chosen-stack, .hero.reprint .chosen-stack { opacity: 1; visibility: visible; }
  .chosen-stack i {
    display: block; color: #e8c98a; font-family: Cinzel, Palatino, Georgia, serif;
    font-style: normal; font-weight: 600; font-size: clamp(13px, 3.05vw, 19px);
    letter-spacing: .045em; line-height: 1.18;
  }
  .stage.reprint .trope-hits, .stage.reprint .trope-next,
  .hero.reprint .trope-hits, .hero.reprint .trope-next {
    opacity: 0 !important; pointer-events: none !important;
  }
""" % nth

start = h.find("  .trope-hits {")
nxt = h.find("  .trope-next {")
if start < 0 or nxt <= start:
    raise SystemExit("overlay anchors missing")
h = h[:start] + OVERLAY + h[nxt:]

b64p = Path("next-arrow.b64")
if not b64p.exists():
    raise SystemExit("next-arrow.b64 missing at repo root")
asset = Path("enduring-pages/assets")
asset.mkdir(parents=True, exist_ok=True)
(asset / "next-arrow.png").write_bytes(base64.b64decode("".join(b64p.read_text().split())))

NEXT_CSS = """  .trope-next {
    position: absolute; left: 72%; top: 46.99%; bottom: auto;
    transform: translate(-50%, -50%);
    opacity: 0; pointer-events: none;
    z-index: 5;
    appearance: none;
    box-sizing: content-box;
    width: 13.4%;
    min-width: 72px;
    max-width: 110px;
    height: 44px;
    margin: 0;
    padding: 0;
    border: 0;
    background: transparent;
    color: transparent;
    font-size: 0;
    line-height: 0;
    letter-spacing: 0;
    text-transform: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    -webkit-tap-highlight-color: transparent;
  }
  .trope-next img {
    display: block;
    width: 100%;
    height: auto;
    max-height: 36px;
    object-fit: contain;
    pointer-events: none;
    user-select: none;
    -webkit-user-drag: none;
    filter: drop-shadow(0 1px 3px rgba(0,0,0,.9));
  }
  .trope-next:focus-visible {
    outline: 1px solid #e2c37a;
    outline-offset: 3px;
  }
"""
a = h.find("  .trope-next {")
b = h.find("  .trope-next.on {", a)
if a < 0 or b <= a:
    raise SystemExit("next css missing")
h = h[:a] + NEXT_CSS + h[b:]

end_btn = "</button>"
img = '<img src="assets/next-arrow.png" alt="" width="200" height="62" draggable="false">'
old_next_btns = [
    'id="tropeNext">Next' + end_btn,
    'id="tropeNext" aria-label="Next">Next' + end_btn,
    'id="tropeNext" aria-label="Next">\u279c' + end_btn,
    'id="tropeNext" aria-label="Next">➜' + end_btn,
    'id="tropeNext" aria-label="Next">' + end_btn,
]
new_next_btn = 'id="tropeNext" aria-label="Next">' + img + end_btn
found_btn = False
for old in old_next_btns:
    if old in h:
        h = h.replace(old, new_next_btn, 1)
        found_btn = True
        break
if not found_btn and ">Next" + end_btn in h and "tropeNext" in h:
    h = h.replace(">Next" + end_btn, ' aria-label="Next">' + img + end_btn, 1)
    found_btn = True
if not found_btn:
    raise SystemExit("tropeNext button label not found")

TROPES = [
    ("ML_demon", "Morally Dark MMC"),
    ("ML_prox", "Forced Proximity- One Bed"),
    ("ML_medical", "Medical K!nk"),
    ("ML_wings", "Learn Me Agony- Don't do that again"),
    ("ML_enemies", "Enemies to Lovers to Enemies"),
    ("ML_hefalls", "He. Falls. First"),
    ("ML_touch", "Touch Her and D!E"),
    ("ML_fated", "Fated Mates"),
    ("ML_academia", "Academia / Battle Setting"),
    ("ML_slowburn", "Slow BURN"),
    ("ML_captor", "Captor/ Captive"),
    ("ML_mortal", "Mortal / Immortal"),
    ("ML_harem", "Reverse Harem- Beg Me"),
    ("ML_forbidden", "Forbidden Feelings"),
    ("ML_possessive", "Possessive/ Protective MMC"),
    ("ML_dom", "Dom/Sub-Brat Heat"),
    ("ML_meta", "Fourth Wall Seduction (I'm talking to you)"),
]
endtag = "</button>"
btns = "\n".join(
    '          <button type="button" class="trope-hit" data-q1="%s" aria-label="%s"><span class="trope-label">%s</span>%s'
    % (k, lab.replace("*", ""), lab, endtag)
    for k, lab in TROPES
)
bs = h.find('<div class="trope-hits" id="tropeHits"')
be = h.find("</div>", bs) if bs >= 0 else -1
if bs < 0 or be < 0:
    raise SystemExit("tropeHits missing")
h = h[:bs] + '<div class="trope-hits" id="tropeHits" aria-label="Choose tropes">\n' + btns + "\n        " + h[be:]

if 'id="doorStage"' not in h:
    h = h.replace(
        '<div class="hero">\n        <video id="doorZoom"',
        '<div class="hero">\n        <div class="stage" id="doorStage">\n        <video id="doorZoom"',
        1,
    )
if 'id="chosenStack"' not in h:
    h = h.replace(
        '<button type="button" class="trope-next"',
        '<div class="chosen-stack" id="chosenStack" aria-live="polite"></div>\n        <button type="button" class="trope-next"',
        1,
    )

OLD_NEXT = (
    "document.getElementById('tropeNext').onclick = () => {\n"
    "  document.body.classList.remove('landing-on');\n"
    "  show('s2');\n"
    "};"
)
OPEN_NEXT = """document.getElementById('tropeNext').onclick = function () {
  const v = document.getElementById('doorZoom');
  const next = document.getElementById('tropeNext');
  const hits = document.getElementById('tropeHits');
  if (!v || !next || !hits) return;
  if (hits.querySelectorAll('.trope-hit.on').length < 3) return;
  hits.classList.remove('on');
  next.classList.remove('on');
  let turning = true;
  function showChosenOnBlank() {
    const stack = document.getElementById('chosenStack');
    const host = document.getElementById('doorStage') || document.querySelector('.hero');
    const selected = [...document.querySelectorAll('.trope-hit.on')];
    if (stack) {
      stack.textContent = '';
      selected.forEach(function(btn) {
        const raw = ((btn.querySelector('.trope-label') || btn).textContent || '').trim();
        const row = document.createElement('i');
        row.textContent = raw.split(' (')[0];
        stack.appendChild(row);
      });
    }
    if (host) host.classList.add('reprint');
  }
  v.addEventListener('timeupdate', function() {
    if (turning && v.currentTime >= 13.13) {
      try { v.pause(); v.currentTime = 13.13; } catch (e) {}
      turning = false;
      showChosenOnBlank();
    }
  });
  v.play().catch(function(){});
};"""
if OLD_NEXT in h:
    h = h.replace(OLD_NEXT, OPEN_NEXT, 1)

if "function syncTropeNext()" not in h:
    old = """document.querySelectorAll('.trope-hit, #s1 .ink').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('on');
    syncQ1(btn.dataset.q1);
  });
});"""
    new = """function syncTropeNext() {
  const n = document.querySelectorAll('.trope-hit.on').length;
  const b = document.getElementById('tropeNext');
  if (b) b.classList.toggle('on', n >= 3);
}
document.querySelectorAll('.trope-hit, #s1 .ink').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('on');
    syncQ1(btn.dataset.q1);
    syncTropeNext();
  });
});"""
    if old in h:
        h = h.replace(old, new, 1)

need = [
    "top: 13.91%",
    "left: 24.31%",
    "left: 14.58%",
    "top: 87.77%",
    "right: 100%",
    "margin-right: 0.62em",
    "left: 72%",
    "top: 46.99%; bottom: auto",
    "assets/next-arrow.png",
    "TROPES_AT = 11.05",
]
missing = [n for n in need if n not in h]
if missing:
    raise SystemExit("missing " + str(missing))
if h.count('class="trope-hit"') != 17:
    raise SystemExit("expected 17 buttons")
if "rgba(226,195,122,.14)" in h or "#070707" in h or "object-fit: cover" in h:
    raise SystemExit("wash/black/cover leaked")
if 'id="tropeNext">Next<' in h or 'aria-label="Next">Next<' in h:
    raise SystemExit("Next label still visible")
if ">/button>" in h:
    raise SystemExit("broken closing button tag")
if not (Path("enduring-pages/assets/next-arrow.png")).exists():
    raise SystemExit("next-arrow.png was not written")
DST.write_text(h)
print("patched", DST, "bytes", DST.stat().st_size)
