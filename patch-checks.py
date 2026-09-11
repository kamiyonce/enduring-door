from pathlib import Path
import re

TROPES = [
    ("ML_demon", "Morally Dark MMC", "morally dark MMC"),
    ("ML_prox", "Forced Proximity- One Bed", "forced proximity / one bed"),
    ("ML_medical", "Medical K!nk", "medical kink"),
    ("ML_wings", "Learn Me Agony- Don't do that again", "learn me agony"),
    ("ML_enemies", "Enemies to Lovers to *Enemies*", "enemies to lovers to enemies"),
    ("ML_hefalls", "He. Falls. First", "he falls first"),
    ("ML_touch", "T\u00f8uch Her and D!E", "touch her and die"),
    ("ML_fated", "Fated Mates", "fated mates"),
    ("ML_academia", "Academia / Battle Setting", "academia / battle setting"),
    ("ML_slowburn", "Slow BURN", "slow burn"),
    ("ML_captor", "C\u01c3ptor/ Capt!ve", "captor / captive"),
    ("ML_mortal", "Mortal / Immortal", "mortal / immortal"),
    ("ML_harem", "Reverse Harem- Beg Me", "reverse harem"),
    ("ML_forbidden", "Forbidden Feelings", "forbidden feelings"),
    ("ML_possessive", "Possessive/ Protective MMC", "possessive / protective MMC"),
    ("ML_dom", "Dom/Sub-Brat Heat", "Dom / brat heat"),
    ("ML_meta", "Fourth Wall Seduction (I'm talking to you)", "fourth wall seduction"),
]
CORES = ["ML_demon", "ML_enemies", "ML_hefalls"]
FLAVOR = [k for k, _, __ in TROPES if k not in CORES]

p = Path("enduring-pages/door.html")
h = p.read_text()

h = h.replace("height: 3.6%;", "height: 3.7%;", 1)
h = h.replace("height: 4.4%;", "height: 3.7%;", 1)
h = h.replace("const TROPES_AT = 13.15;", "const TROPES_AT = 10.17;")

old_css = """  .trope-hit.on .trope-label {
    color: #070707;
    font-weight: 600;
    text-shadow: 0 0 1px #000;
  }"""
new_css = (
    "  .trope-hit.on::before {\n"
    "    content: \"" + "\u2713" + "\";\n"
    "    color: #e2c37a;\n"
    "    font-size: clamp(13px, 3.2vw, 17px);\n"
    "    font-weight: 700;\n"
    "    line-height: 1;\n"
    "    margin-right: 0.32em;\n"
    "    text-shadow: 0 1px 4px rgba(0,0,0,.9);\n"
    "    pointer-events: none;\n"
    "  }"
)
if old_css in h:
    h = h.replace(old_css, new_css, 1)

if "-webkit-tap-highlight-color" not in h:
    h = h.replace(
        "transform: translateY(-50%);",
        "transform: translateY(-50%);\n    -webkit-tap-highlight-color: transparent;",
        1,
    )

nth = re.search(
    r"  \.trope-hit:nth-child\(1\) \{ top: [0-9.]+%; \}.*?  \.trope-hit:nth-child\(\d+\) \{ top: [0-9.]+%; \}\n",
    h,
    re.S,
)
if nth:
    n = len(TROPES)
    start, end = 20.6, 84.2
    step = (end - start) / (n - 1)
    block = "".join(
        f"  .trope-hit:nth-child({i+1}) {{ top: {start + i * step:.2f}%; }}\n" for i in range(n)
    )
    h = h[: nth.start()] + block + h[nth.end() :]

hits = re.search(
    r'<div class="trope-hits" id="tropeHits" aria-label="Choose tropes">.*?</div>',
    h,
    re.S,
)
if hits:
    btns = "\n".join(
        f'          <button type="button" class="trope-hit" data-q1="{k}" aria-label="{lab.replace("*", "")}"><span class="trope-label">{lab}</span></button>'
        for k, lab, _ in TROPES
    )
    h = (
        h[: hits.start()]
        + f'<div class="trope-hits" id="tropeHits" aria-label="Choose tropes">\n{btns}\n        </div>'
        + h[hits.end() :]
    )

lab = re.search(r"const Q1_LABEL = \{.*?\};", h, re.S)
if lab:
    body = ",\n".join(f"  {k}: {v!r}" for k, _, v in TROPES)
    h = h[: lab.start()] + "const Q1_LABEL = {\n" + body + "\n};" + h[lab.end() :]

sr = re.search(r'<div class="sr-q1" aria-hidden="true">.*?</div>', h, re.S)
if sr:
    boxes = "\n".join(f'      <input type="checkbox" data-q1="{k}">' for k, _, __ in TROPES)
    h = (
        h[: sr.start()]
        + f'<div class="sr-q1" aria-hidden="true">\n{boxes}\n    </div>'
        + h[sr.end() :]
    )

h = re.sub(
    r"const flavor = \[[^\]]+\]\.filter\(k => state\.q1\[k\]\)\.map\(k => Q1_LABEL\[k\]\);",
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

if "syncTropeNext" not in h:
    raise SystemExit("failed to insert Next gate")

old_no = "I felt your heart flutter on the first (' + (first || 'mismatch') + '). Trust me"
new_no = "I felt your heart flutter when you clicked it. But you are nervous so this door is not opening for you. Trust me"
if old_no in h:
    h = h.replace(old_no, new_no, 1)

old_end = "I won\u2019t bait you in.';"
new_end = "I won\u2019t bait you in. unless you bait me with your eyes closed in the shower.';"
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

if "ML_captor" not in h or "TROPES_AT = 10.17" not in h:
    raise SystemExit("pause timestamp or tropes failed")

p.write_text(h)
print("patched tropes + pause 10.17")
