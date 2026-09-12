#!/usr/bin/env python3
"""17 first-letter checks + Next between Fated Mates and the buckle."""
from pathlib import Path

DST = Path("enduring-pages/door.html")
GOOD = Path("door.good.html")

NEEDLES = [
    "top: 13.91%",
    "left: 24.31%",
    "left: 14.58%",
    "top: 87.77%",
    "right: 100%",
    "margin-right: 0.62em",
    "left: 70%",
    "top: 46.99%; bottom: auto",
    "TROPES_AT = 11.05",
    "BLANK_AT = 13.13",
    "ASK_AT = 6.4",
    'class="trope-hit"',
]

TROPES = [
    ("ML_demon", "Morally Dark MMC"),
    ("ML_prox", "Forced Proximity- One Bed"),
    ("ML_medical", "Medical K!nk"),
    ("ML_wings", "Learn Me Agony- Don't do that again"),
    ("ML_enemies", "Enemies to Lovers to Enemies"),
    ("ML_hefalls", "He. Falls. First"),
    ("ML_touch", "Tøuch Her and D!E"),
    ("ML_fated", "Fated Mates"),
    ("ML_academia", "Academia / Battle Setting"),
    ("ML_slowburn", "Slow BURN"),
    ("ML_captor", "Cǃptor/ Capt!ve"),
    ("ML_mortal", "Mortal / Immortal"),
    ("ML_harem", "Reverse Harem- Beg Me"),
    ("ML_forbidden", "Forbidden Feelings"),
    ("ML_possessive", "Possessive/ Protective MMC"),
    ("ML_dom", "Dom/Sub-Brat Heat"),
    ("ML_meta", "Fourth Wall Seduction (I'm talking to you)"),
]

END_BTN = "</" + "button>"
END_DIV = "</" + "div>"


def buttons():
    rows = []
    for k, lab in TROPES:
        rows.append(
            '          <button type="button" class="trope-hit" data-q1="%s" aria-label="%s"><span class="trope-label">%s</span>%s'
            % (k, lab.replace('*',''), lab, END_BTN)
        )
    return "\n".join(rows)


def place_next_button(h):
    nxt_css = h.find("  .trope-next {")
    nxt_on = h.find("  .trope-next.on {", nxt_css) if nxt_css >= 0 else -1
    if nxt_css < 0 or nxt_on <= nxt_css:
        return h
    block = h[nxt_css:nxt_on]
    block = block.replace("left: 50%;", "left: 70%;")
    block = block.replace("bottom: 6%;", "top: 46.99%; bottom: auto;")
    block = block.replace("bottom: 2.2%;", "top: 46.99%; bottom: auto;")
    block = block.replace("transform: translateX(-50%);", "transform: translate(-50%, -50%);")
    block = block.replace("padding: 8px 26px;", "padding: 5px 10px;")
    block = block.replace("letter-spacing: .28em;", "letter-spacing: .18em;")
    block = block.replace("font-size: 11px;", "font-size: 10px;")
    block = block.replace("z-index: 4;", "z-index: 5;")
    if "left: 70%" not in block:
        raise SystemExit("failed to move Next")
    return h[:nxt_css] + block + h[nxt_on:]


def assert_good(text, label):
    missing = [n for n in NEEDLES if n not in text]
    if missing:
        raise SystemExit(f"{label} missing {missing}")
    n = text.count('class="trope-hit"')
    if n != 17:
        raise SystemExit(f"{label} expected 17 buttons, got {n}")
    if "rgba(226,195,122,.14)" in text:
        raise SystemExit(f"{label} wash still present")
    if "#070707" in text:
        raise SystemExit(f"{label} black label leaked")


OVERLAY = """  .stage {
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
  .trope-hit:nth-child(1) { top: 13.91%; left: 24.31%; width: 47.89%; }
  .trope-hit:nth-child(2) { top: 19.02%; left: 20.28%; width: 57.12%; }
  .trope-hit:nth-child(3) { top: 24.02%; left: 31.67%; width: 33.53%; }
  .trope-hit:nth-child(4) { top: 28.83%; left: 14.58%; width: 68.82%; }
  .trope-hit:nth-child(5) { top: 33.40%; left: 15.56%; width: 67.04%; }
  .trope-hit:nth-child(6) { top: 37.77%; left: 30.69%; width: 34.71%; }
  .trope-hit:nth-child(7) { top: 42.38%; left: 25.00%; width: 46.40%; }
  .trope-hit:nth-child(8) { top: 46.99%; left: 33.61%; width: 29.99%; }
  .trope-hit:nth-child(9) { top: 51.76%; left: 21.94%; width: 53.06%; }
  .trope-hit:nth-child(10) { top: 56.37%; left: 32.22%; width: 31.78%; }
  .trope-hit:nth-child(11) { top: 61.17%; left: 28.06%; width: 39.64%; }
  .trope-hit:nth-child(12) { top: 65.27%; left: 27.92%; width: 40.48%; }
  .trope-hit:nth-child(13) { top: 69.77%; left: 22.36%; width: 52.24%; }
  .trope-hit:nth-child(14) { top: 74.34%; left: 27.78%; width: 39.62%; }
  .trope-hit:nth-child(15) { top: 79.06%; left: 20.00%; width: 56.00%; }
  .trope-hit:nth-child(16) { top: 83.40%; left: 25.69%; width: 44.91%; }
  .trope-hit:nth-child(17) { top: 87.77%; left: 24.44%; width: 49.16%; height: 6.35%; }
  .trope-label {
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
    content: "\u2713";
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
    pointer-events: none;
  }
  .chosen-stack {
    position: absolute;
    left: 9%; right: 9%; top: 12%; bottom: 10%;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    gap: 0.38em; z-index: 6; pointer-events: none; text-align: center;
    opacity: 0; visibility: hidden;
  }
  .stage.reprint .chosen-stack,
  .hero.reprint .chosen-stack { opacity: 1; visibility: visible; }
  .chosen-stack i {
    display: block; color: #e8c98a;
    font-family: Cinzel, Palatino, Georgia, serif;
    font-style: normal; font-weight: 600;
    font-size: clamp(13px, 3.05vw, 19px); letter-spacing: .045em; line-height: 1.18;
  }
  .stage.reprint .trope-hits,
  .stage.reprint .trope-next,
  .hero.reprint .trope-hits,
  .hero.reprint .trope-next { opacity: 0 !important; pointer-events: none !important; }
"""

OPEN_NEXT = """function showChosenOnBlank() {
  const stack = document.getElementById('chosenStack');
  const host = document.getElementById('doorStage') || document.querySelector('.hero');
  const selected = [...document.querySelectorAll('.trope-hit.on')];
  if (stack) {
    stack.textContent = '';
    stack.setAttribute('data-n', String(selected.length));
    selected.forEach(function(btn) {
      const raw = ((btn.querySelector('.trope-label') || btn).textContent || '').replace(/\\*/g, '').trim();
      const cut = raw.indexOf(' (');
      const row = document.createElement('i');
      if (cut > 0) {
        row.textContent = raw.slice(0, cut);
        const sub = document.createElement('em');
        sub.textContent = raw.slice(cut + 1);
        row.appendChild(sub);
      } else {
        row.textContent = raw;
      }
      stack.appendChild(row);
    });
  }
  if (host) host.classList.add('reprint');
  const hitsEl = document.getElementById('tropeHits');
  if (hitsEl) hitsEl.classList.remove('on');
  const nxt = document.getElementById('tropeNext');
  if (nxt) nxt.classList.remove('on');
}
(function bindTropeNext() {
  const v = document.getElementById('doorZoom');
  const next = document.getElementById('tropeNext');
  const hits = document.getElementById('tropeHits');
  if (!v || !next || !hits) return;
  let turning = false;
  function holdBlank() {
    try { v.pause(); v.currentTime = 13.13; } catch (e) {}
    turning = false;
    showChosenOnBlank();
  }
  function watch() {
    if (!turning) return;
    if (v.currentTime >= 13.13) { holdBlank(); return; }
    if (typeof v.requestVideoFrameCallback === 'function') v.requestVideoFrameCallback(function(){ watch(); });
    else requestAnimationFrame(watch);
  }
  v.addEventListener('timeupdate', function() {
    if (turning && v.currentTime >= 13.13) holdBlank();
  });
  next.onclick = function() {
    if (hits.querySelectorAll('.trope-hit.on').length < 3) return;
    hits.classList.remove('on');
    next.classList.remove('on');
    turning = true;
    v.play().catch(function(){});
    watch();
  };
})();
"""

OLD_NEXT = """document.getElementById('tropeNext').onclick = () => {
  document.body.classList.remove('landing-on');
  show('s2');
};"""


def patch_zip_html(h):
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
    start = h.find("  .trope-hits {")
    nxt = h.find("  .trope-next {")
    if start < 0 or nxt < 0 or nxt < start:
        raise SystemExit("overlay anchors missing")
    h = h[:start] + OVERLAY + h[nxt:]
    h = place_next_button(h)
    h = h.replace("background: rgba(226,195,122,.14);", "background: transparent;")
    bstart = h.find('<div class="trope-hits" id="tropeHits"')
    if bstart < 0:
        raise SystemExit("tropeHits missing")
    bend = h.find(END_DIV, bstart)
    if bend < 0:
        raise SystemExit("tropeHits close missing")
    h = h[:bstart] + '<div class="trope-hits" id="tropeHits" aria-label="Choose tropes">\n' + buttons() + "\n        " + h[bend:]
    if 'id="doorStage"' not in h:
        h = h.replace(
            '<div class="hero">\n        <video id="doorZoom"',
            '<div class="hero">\n        <div class="stage" id="doorStage">\n        <video id="doorZoom"',
            1,
        )
        h = h.replace(
            '<button type="button" id="start" class="yes-btn">Yes</button>\n        </div>',
            '<button type="button" id="start" class="yes-btn">Yes</button>\n        </div>\n        </div>',
            1,
        )
    if 'id="chosenStack"' not in h:
        h = h.replace(
            '<button type="button" class="trope-next"',
            '<div class="chosen-stack" id="chosenStack" aria-live="polite"></div>\n        <button type="button" class="trope-next"',
            1,
        )
    if OLD_NEXT in h:
        h = h.replace(OLD_NEXT, OPEN_NEXT, 1)
    return h


if GOOD.exists():
    text = place_next_button(GOOD.read_text())
    assert_good(text, GOOD.as_posix())
    if not DST.parent.exists():
        raise SystemExit("enduring-pages missing after unzip")
    DST.write_text(text)
    assert_good(DST.read_text(), DST.as_posix())
    print("patched", DST, "from", GOOD, "bytes", DST.stat().st_size)
else:
    if not DST.exists():
        raise SystemExit("enduring-pages/door.html missing after unzip")
    text = patch_zip_html(DST.read_text())
    assert_good(text, "patched zip")
    DST.write_text(text)
    assert_good(DST.read_text(), DST.as_posix())
    print("patched", DST, "from zip", "bytes", DST.stat().st_size)
