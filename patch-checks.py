from pathlib import Path

p = Path("enduring-pages/door.html")
h = p.read_text()

h = h.replace("height: 3.6%;", "height: 4.4%;", 1)

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

if "eyes closed in the shower" not in h:
    raise SystemExit("failed to insert runaway closer")

p.write_text(h)
print("patched checks + next gate + runaway copy")
