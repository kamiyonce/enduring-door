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

p.write_text(h)
print("patched checks + next gate")
