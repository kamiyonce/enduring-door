#!/usr/bin/env python3
"""Place a gold check one space before each printed first letter.

Prefers door.good.html when present. Otherwise patches the unzipped
enduring-pages/door.html with plain string replaces (no regex).
Does not change ASK_AT / TROPES_AT / BLANK_AT / Next-gate / reprint flow
beyond ensuring those already-agreed values exist.
"""
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
    "TROPES_AT = 11.05",
    "BLANK_AT = 13.13",
    "ASK_AT = 6.4",
    'class="trope-hit"',
]


def assert_good(text, label):
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
    content: "\\2713";
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
    left: 9%;
    right: 9%;
    top: 12%;
    bottom: 10%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 0.38em;
    z-index: 6;
    pointer-events: none;
    text-align: center;
    opacity: 0;
    visibility: hidden;
  }
  .stage.reprint .chosen-stack,
  .hero.reprint .chosen-stack { opacity: 1; visibility: visible; }
  .chosen-stack i {
    display: block;
    color: #e8c98a;
    font-family: Cinzel, Palatino, Georgia, serif;
    font-style: normal;
    font-weight: 600;
    font-size: clamp(13px, 3.05vw, 19px);
    letter-spacing: .045em;
    line-height: 1.18;
  }
  .stage.reprint .trope-hits,
  .stage.reprint .trope-next,
  .hero.reprint .trope-hits,
  .hero.reprint .trope-next { opacity: 0 !important; pointer-events: none !important; }
"""

BTNS = """          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_demon\" aria-label=\"Morally Dark MMC\"><span class=\"trope-label\">Morally Dark MMC</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_prox\" aria-label=\"Forced Proximity- One Bed\"><span class=\"trope-label\">Forced Proximity- One Bed</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_medical\" aria-label=\"Medical K!nk\"><span class=\"trope-label\">Medical K!nk</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_wings\" aria-label=\"Learn Me Agony- Don't do that again\"><span class=\"trope-label\">Learn Me Agony- Don't do that again</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_enemies\" aria-label=\"Enemies to Lovers to Enemies\"><span class=\"trope-label\">Enemies to Lovers to *Enemies*</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_hefalls\" aria-label=\"He. Falls. First\"><span class=\"trope-label\">He. Falls. First</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_touch\" aria-label=\"Tøuch Her and D!E\"><span class=\"trope-label\">Tøuch Her and D!E</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_fated\" aria-label=\"Fated Mates\"><span class=\"trope-label\">Fated Mates</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_academia\" aria-label=\"Academia / Battle Setting\"><span class=\"trope-label\">Academia / Battle Setting</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_slowburn\" aria-label=\"Slow BURN\"><span class=\"trope-label\">Slow BURN</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_captor\" aria-label=\"Cǃptor/ Capt!ve\"><span class=\"trope-label\">Cǃptor/ Capt!ve</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_mortal\" aria-label=\"Mortal / Immortal\"><span class=\"trope-label\">Mortal / Immortal</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_harem\" aria-label=\"Reverse Harem- Beg Me\"><span class=\"trope-label\">Reverse Harem- Beg Me</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_forbidden\" aria-label=\"Forbidden Feelings\"><span class=\"trope-label\">Forbidden Feelings</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_possessive\" aria-label=\"Possessive/ Protective MMC\"><span class=\"trope-label\">Possessive/ Protective MMC</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_dom\" aria-label=\"Dom/Sub-Brat Heat\"><span class=\"trope-label\">Dom/Sub-Brat Heat</span></button>
          <button type=\"button\" class=\"trope-hit\" data-q1=\"ML_meta\" aria-label=\"Fourth Wall Seduction (I'm talking to you)\"><span class=\"trope-label\">Fourth Wall Seduction (I'm talking to you)</span></button>
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

OLD_CLICK = """document.querySelectorAll('.trope-hit, #s1 .ink').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('on');
    syncQ1(btn.dataset.q1);
  });
});"""

NEW_CLICK = """function syncTropeNext() {
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


def patch_zip_html(h: str) -> str:
    h = h.replace("const TROPES_AT = 13.15;", "const TROPES_AT = 11.05;")
    h = h.replace("const TROPES_AT = 10.17;", "const TROPES_AT = 11.05;")
    if "const BLANK_AT" not in h:
        h = h.replace(
            "const TROPES_AT = 11.05;",
            "const TROPES_AT = 11.05;\nconst BLANK_AT = 13.13;\nconst BLANK_MAX = 13.40;",
            1,
        )
    h = h.replace('          <source src=\"https://enduring-timeline.netlify.app/assets/book-open.mp4\" type=\"video/mp4\">\n', "")
    h = h.replace("color: #070707;", "color: transparent;")
    h = h.replace("color:#070707;", "color: transparent;")
    h = h.replace("text-shadow: 0 0 1px #000;", "text-shadow: none;")
    h = h.replace("object-fit: cover;", "object-fit: contain;")

    start = h.find("  .trope-hits {")
    nxt = h.find("  .trope-next {")
    if start < 0 or nxt < 0 or nxt < start:
        raise SystemExit("could not find .trope-hits / .trope-next CSS block")
    h = h[:start] + OVERLAY + h[nxt:]

    wash = """  .trope-hit:active,
  .trope-hit.on {
    background: rgba(226,195,122,.14);
  }
"""
    h = h.replace(wash, "")
    h = h.replace("background: rgba(226,195,122,.14);", "background: transparent;")

    bstart = h.find('<div class=\"trope-hits\" id=\"tropeHits\"')
    if bstart < 0:
        raise SystemExit("tropeHits missing")
    bend = h.find("</div>", bstart)
    if bend < 0:
        raise SystemExit("tropeHits close missing")
    h = h[:bstart] + '<div class=\"trope-hits\" id=\"tropeHits\" aria-label=\"Choose tropes\">\n' + BTNS + "        " + h[bend:]

    if 'id=\"doorStage\"' not in h:
        h = h.replace(
            '<div class=\"hero\">\n        <video id=\"doorZoom\"',
            '<div class=\"hero\">\n        <div class=\"stage\" id=\"doorStage\">\n        <video id=\"doorZoom\"',
            1,
        )
        if '<button type=\"button\" id=\"start\" class=\"yes-btn\">Yes</button>' in h and h.count('id=\"doorStage\"') == 1:
            h = h.replace(
                '<button type=\"button\" id=\"start\" class=\"yes-btn\">Yes</button>\n        </div>',
                '<button type=\"button\" id=\"start\" class=\"yes-btn\">Yes</button>\n        </div>\n        </div>',
                1,
            )

    if 'id=\"chosenStack\"' not in h:
        h = h.replace(
            '<button type=\"button\" class=\"trope-next\"',
            '<div class=\"chosen-stack\" id=\"chosenStack\" aria-live=\"polite\"></div>\n        <button type=\"button\" class=\"trope-next\"',
            1,
        )

    if OLD_NEXT in h:
        h = h.replace(OLD_NEXT, OPEN_NEXT, 1)
    if "function syncTropeNext()" not in h and OLD_CLICK in h:
        h = h.replace(OLD_CLICK, NEW_CLICK, 1)
    return h


if GOOD.exists():
    text = GOOD.read_text()
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
