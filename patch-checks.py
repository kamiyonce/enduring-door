#!/usr/bin/env python3
"""Upgrade unpacked door.html: Next at 3 checks → freeze 13.13 → chosen lines."""
from pathlib import Path

p = Path("enduring-pages/door.html")
if not p.exists():
    raise SystemExit("enduring-pages/door.html missing after unzip")
h = p.read_text()

h = h.replace("const TROPES_AT = 13.15;", "const TROPES_AT = 11.05;")
h = h.replace("const TROPES_AT = 10.17;", "const TROPES_AT = 11.05;")
if "const BLANK_AT" not in h:
    h = h.replace(
        "const TROPES_AT = 11.05;",
        "const TROPES_AT = 11.05;\nconst BLANK_AT = 13.13;\nconst BLANK_MAX = 13.40;",
        1,
    )

CSS = """
  .chosen-stack {
    position: absolute; left: 9%; right: 9%; top: 12%; bottom: 10%;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    gap: 0.38em; z-index: 6; pointer-events: none; text-align: center;
    opacity: 0; visibility: hidden; transition: opacity .7s ease;
  }
  .hero.reprint .chosen-stack, .stage.reprint .chosen-stack { opacity: 1; visibility: visible; }
  .chosen-stack i {
    display: block; color: #e8c98a; font-family: Cinzel, Palatino, Georgia, serif;
    font-style: normal; font-weight: 600; font-size: clamp(13px, 3.05vw, 19px);
    letter-spacing: .045em; line-height: 1.18;
    text-shadow: 0 0 14px rgba(201,163,106,.28), 0 1px 3px rgba(0,0,0,.92);
  }
  .chosen-stack i em {
    display: block; margin-top: .12em; font-size: .78em; font-weight: 500;
    letter-spacing: .06em; font-style: italic;
    font-family: \"IM Fell English\", Palatino, Georgia, serif; opacity: .88;
  }
  .hero.reprint .trope-hits, .hero.reprint .trope-next,
  .stage.reprint .trope-hits, .stage.reprint .trope-next {
    opacity: 0 !important; pointer-events: none !important;
  }
"""
if ".chosen-stack" not in h:
    h = h.replace("  .yes-btn {", CSS + "  .yes-btn {", 1)

if 'id="chosenStack"' not in h:
    h = h.replace(
        '<button type="button" class="trope-next"',
        '<div class="chosen-stack" id="chosenStack" aria-live="polite"></div>\n        <button type="button" class="trope-next"',
        1,
    )

OLD_PLAY = """function playDoorZoom() {
  const v = document.getElementById('doorZoom');
  const yes = document.getElementById('start');
  if (!v || !yes) return;"""

NEW_PLAY = """function playDoorZoom() {
  const v = document.getElementById('doorZoom');
  const yes = document.getElementById('start');
  const next = document.getElementById('tropeNext');
  const hits = document.getElementById('tropeHits');
  if (!v || !yes || !next || !hits) return;"""

if OLD_PLAY in h:
    h = h.replace(OLD_PLAY, NEW_PLAY, 1)

OLD_NEXT = """document.getElementById('tropeNext').onclick = () => {
  document.body.classList.remove('landing-on');
  show('s2');
};"""
NEW_NEXT = """function showChosenOnBlank() {
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
})();"""

if OLD_NEXT in h:
    h = h.replace(OLD_NEXT, NEW_NEXT, 1)
elif "showChosenOnBlank" not in h:
    raise SystemExit("could not bind Next away from s2")

h = h.replace(
    "document.getElementById('tropeNext').classList.add('on');",
    "if (document.querySelectorAll('.trope-hit.on').length >= 3) document.getElementById('tropeNext').classList.add('on');",
)

if "function syncTropeNext()" not in h:
    h = h.replace(
        """document.querySelectorAll('.trope-hit, #s1 .ink').forEach(btn => {
  btn.addEventListener('click', () => {
    btn.classList.toggle('on');
    syncQ1(btn.dataset.q1);
  });
});""",
        """function syncTropeNext() {
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
});""",
        1,
    )

if "BLANK_AT = 13.13" not in h and "currentTime = 13.13" not in h:
    raise SystemExit("13.13 freeze missing")
if "show('s2')" in h[h.find("tropeNext"):h.find("tropeNext")+400]:
    raise SystemExit("Next still jumps to s2")
p.write_text(h)
print("patched", p, "bytes", p.stat().st_size)
