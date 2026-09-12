#!/usr/bin/env python3
"""Place gold checks one space before each printed first letter."""
from pathlib import Path
import re

p = Path("enduring-pages/door.html")
if not p.exists():
    raise SystemExit('enduring-pages/door.html missing after unzip')
h = p.read_text()
h = h.replace('const TROPES_AT = 13.15;', 'const TROPES_AT = 11.05;')
h = h.replace('const TROPES_AT = 10.17;', 'const TROPES_AT = 11.05;')
if 'const BLANK_AT' not in h:
    h = h.replace('const TROPES_AT = 11.05;', 'const TROPES_AT = 11.05;\nconst BLANK_AT = 13.13;\nconst BLANK_MAX = 13.40;', 1)
h = h.replace('          <source src="https://enduring-timeline.netlify.app/assets/book-open.mp4" type="video/mp4">\n', '')
h = h.replace('color: #070707;', 'color: transparent;')
h = h.replace('color:#070707;', 'color: transparent;')
h = h.replace('text-shadow: 0 0 1px #000;', 'text-shadow: none;')
OVERLAY = '\n  .stage {\n    position: absolute;\n    top: 50%;\n    left: 50%;\n    width: min(100vw, calc(100dvh * 9 / 16));\n    height: min(100dvh, calc(100vw * 16 / 9));\n    transform: translate(-50%, -50%);\n    z-index: 3;\n    overflow: visible;\n  }\n  .stage video,\n  .hero video {\n    display: block;\n    position: absolute;\n    inset: 0;\n    width: 100%;\n    height: 100%;\n    object-fit: contain;\n    object-position: center;\n    background: #000;\n  }\n  .trope-hits {\n    position: absolute;\n    inset: 0;\n    opacity: 0;\n    pointer-events: none;\n    z-index: 4;\n    overflow: visible;\n  }\n  .trope-hits.on { opacity: 1; pointer-events: auto; }\n  .trope-hit {\n    appearance: none;\n    position: absolute;\n    height: 5.05%;\n    margin: 0;\n    padding: 0;\n    border: 0;\n    background: transparent;\n    cursor: pointer;\n    display: block;\n    transform: translateY(-50%);\n    overflow: visible;\n    -webkit-tap-highlight-color: transparent;\n    z-index: 4;\n  }\n  .trope-hit:nth-child(1) { top: 13.91%; left: 24.31%; width: 47.89%; }\n  .trope-hit:nth-child(2) { top: 19.02%; left: 20.28%; width: 57.12%; }\n  .trope-hit:nth-child(3) { top: 24.02%; left: 31.67%; width: 33.53%; }\n  .trope-hit:nth-child(4) { top: 28.83%; left: 14.58%; width: 68.82%; }\n  .trope-hit:nth-child(5) { top: 33.40%; left: 15.56%; width: 67.04%; }\n  .trope-hit:nth-child(6) { top: 37.77%; left: 30.69%; width: 34.71%; }\n  .trope-hit:nth-child(7) { top: 42.38%; left: 25.00%; width: 46.40%; }\n  .trope-hit:nth-child(8) { top: 46.99%; left: 33.61%; width: 29.99%; }\n  .trope-hit:nth-child(9) { top: 51.76%; left: 21.94%; width: 53.06%; }\n  .trope-hit:nth-child(10) { top: 56.37%; left: 32.22%; width: 31.78%; }\n  .trope-hit:nth-child(11) { top: 61.17%; left: 28.06%; width: 39.64%; }\n  .trope-hit:nth-child(12) { top: 65.27%; left: 27.92%; width: 40.48%; }\n  .trope-hit:nth-child(13) { top: 69.77%; left: 22.36%; width: 52.24%; }\n  .trope-hit:nth-child(14) { top: 74.34%; left: 27.78%; width: 39.62%; }\n  .trope-hit:nth-child(15) { top: 79.06%; left: 20.00%; width: 56.00%; }\n  .trope-hit:nth-child(16) { top: 83.40%; left: 25.69%; width: 44.91%; }\n  .trope-hit:nth-child(17) { top: 87.77%; left: 24.44%; width: 49.16%; height: 6.35%; }\n  .trope-label {\n    position: absolute;\n    width: 1px;\n    height: 1px;\n    overflow: hidden;\n    clip: rect(0 0 0 0);\n    clip-path: inset(50%);\n    white-space: nowrap;\n    pointer-events: none;\n  }\n  .trope-hit.on::before {\n    content: "\\2713";\n    position: absolute;\n    right: 100%;\n    margin-right: 0.62em;\n    top: 50%;\n    transform: translateY(-50%);\n    color: #e2c37a;\n    font-size: clamp(15px, 3.6vw, 20px);\n    font-weight: 700;\n    line-height: 1;\n    text-shadow: 0 1px 4px rgba(0,0,0,.95);\n    pointer-events: none;\n  }\n'

h = re.sub(r'  \\.trope-hits \\{.*?\\n  \\.trope-next \\{', OVERLAY + '  .trope-next {', h, count=1, flags=re.S)
h = re.sub(r'  \\.trope-hit\\.on \\.trope-label \\{[^}]+\\}\\n', '', h)
h = h.replace('object-fit: cover;', 'object-fit: contain;')
h = re.sub(r'  \\.trope-hit:active,\\n  \\.trope-hit\\.on \\{\\n    background: rgba\\(226,195,122,\\.14\\);\\n  \\}\\n', '', h)
BTNS = '          <button type="button" class="trope-hit" data-q1="ML_demon" aria-label="Morally Dark MMC"><span class="trope-label">Morally Dark MMC</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_prox" aria-label="Forced Proximity- One Bed"><span class="trope-label">Forced Proximity- One Bed</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_medical" aria-label="Medical K!nk"><span class="trope-label">Medical K!nk</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_wings" aria-label="Learn Me Agony- Don\'t do that again"><span class="trope-label">Learn Me Agony- Don\'t do that again</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_enemies" aria-label="Enemies to Lovers to Enemies"><span class="trope-label">Enemies to Lovers to Enemies</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_hefalls" aria-label="He. Falls. First"><span class="trope-label">He. Falls. First</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_touch" aria-label="Tøuch Her and D!E"><span class="trope-label">Tøuch Her and D!E</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_fated" aria-label="Fated Mates"><span class="trope-label">Fated Mates</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_academia" aria-label="Academia / Battle Setting"><span class="trope-label">Academia / Battle Setting</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_slowburn" aria-label="Slow BURN"><span class="trope-label">Slow BURN</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_captor" aria-label="Cǃptor/ Capt!ve"><span class="trope-label">Cǃptor/ Capt!ve</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_mortal" aria-label="Mortal / Immortal"><span class="trope-label">Mortal / Immortal</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_harem" aria-label="Reverse Harem- Beg Me"><span class="trope-label">Reverse Harem- Beg Me</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_forbidden" aria-label="Forbidden Feelings"><span class="trope-label">Forbidden Feelings</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_possessive" aria-label="Possessive/ Protective MMC"><span class="trope-label">Possessive/ Protective MMC</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_dom" aria-label="Dom/Sub-Brat Heat"><span class="trope-label">Dom/Sub-Brat Heat</span></button>\n          <button type="button" class="trope-hit" data-q1="ML_meta" aria-label="Fourth Wall Seduction (I\'m talking to you)"><span class="trope-label">Fourth Wall Seduction (I\'m talking to you)</span></button>'

h = re.sub(
    r'<div class="trope-hits" id="tropeHits" aria-label="Choose tropes">.*?</div>',
    '<div class="trope-hits" id="tropeHits" aria-label="Choose tropes">\n' + BTNS + '\n        </div>',
    h, count=1, flags=re.S)
if 'id="doorStage"' not in h:
    h = h.replace(
        '<div class="hero">\n        <video id="doorZoom"',
        '<div class="hero">\n        <div class="stage" id="doorStage">\n        <video id="doorZoom"',
        1)
    h = h.replace(
        '<button type="button" id="start" class="yes-btn">Yes</button>\n        </div>',
        '<button type="button" id="start" class="yes-btn">Yes</button>\n        </div>\n        </div>',
        1)
if 'id="chosenStack"' not in h:
    h = h.replace(
        '<button type="button" class="trope-next"',
        '<div class="chosen-stack" id="chosenStack" aria-live="polite"></div>\n        <button type="button" class="trope-next"',
        1)
OPEN_NEXT = "function showChosenOnBlank() {\n  const stack = document.getElementById('chosenStack');\n  const host = document.getElementById('doorStage') || document.querySelector('.hero');\n  const selected = [...document.querySelectorAll('.trope-hit.on')];\n  if (stack) {\n    stack.textContent = '';\n    stack.setAttribute('data-n', String(selected.length));\n    selected.forEach(function(btn) {\n      const raw = ((btn.querySelector('.trope-label') || btn).textContent || '').replace(/\\*/g, '').trim();\n      const cut = raw.indexOf(' (');\n      const row = document.createElement('i');\n      if (cut > 0) {\n        row.textContent = raw.slice(0, cut);\n        const sub = document.createElement('em');\n        sub.textContent = raw.slice(cut + 1);\n        row.appendChild(sub);\n      } else {\n        row.textContent = raw;\n      }\n      stack.appendChild(row);\n    });\n  }\n  if (host) host.classList.add('reprint');\n  const hitsEl = document.getElementById('tropeHits');\n  if (hitsEl) hitsEl.classList.remove('on');\n  const nxt = document.getElementById('tropeNext');\n  if (nxt) nxt.classList.remove('on');\n}\n(function bindTropeNext() {\n  const v = document.getElementById('doorZoom');\n  const next = document.getElementById('tropeNext');\n  const hits = document.getElementById('tropeHits');\n  if (!v || !next || !hits) return;\n  let turning = false;\n  function holdBlank() {\n    try { v.pause(); v.currentTime = 13.13; } catch (e) {}\n    turning = false;\n    showChosenOnBlank();\n  }\n  function watch() {\n    if (!turning) return;\n    if (v.currentTime >= 13.13) { holdBlank(); return; }\n    if (typeof v.requestVideoFrameCallback === 'function') v.requestVideoFrameCallback(function(){ watch(); });\n    else requestAnimationFrame(watch);\n  }\n  v.addEventListener('timeupdate', function() {\n    if (turning && v.currentTime >= 13.13) holdBlank();\n  });\n  next.onclick = function() {\n    if (hits.querySelectorAll('.trope-hit.on').length < 3) return;\n    hits.classList.remove('on');\n    next.classList.remove('on');\n    turning = true;\n    v.play().catch(function(){});\n    watch();\n  };\n})();"

OLD_NEXT = """document.getElementById('tropeNext').onclick = () => {
  document.body.classList.remove('landing-on');
  show('s2');
};"""
if OLD_NEXT in h:
    h = h.replace(OLD_NEXT, OPEN_NEXT, 1)

if 'function syncTropeNext()' not in h:
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

if h.count('class="trope-hit"') != 17:
    raise SystemExit('expected 17 trope buttons, got %s' % h.count('class="trope-hit"'))
if 'top: 13.91%' not in h or 'left: 14.58%' not in h or 'top: 87.77%' not in h:
    raise SystemExit('17-line first-letter geometry missing')
if 'right: 100%' not in h or 'margin-right: 0.62em' not in h:
    raise SystemExit('check not one space before first letter')
if 'rgba(226,195,122,.14)' in h:
    raise SystemExit('yellow wash still present')
if '#070707' in h:
    raise SystemExit('black label color leaked')
if 'object-fit: cover' in h:
    raise SystemExit('cover leaked')
p.write_text(h)
print('patched', p, 'bytes', p.stat().st_size)
