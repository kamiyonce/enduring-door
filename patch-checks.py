from pathlib import Path
p = Path('enduring-pages/door.html')
h = p.read_text()
h = h.replace('height: 3.6%;', 'height: 4.4%;', 1)
old = """  .trope-hit.on .trope-label {
    color: #070707;
    font-weight: 600;
    text-shadow: 0 0 1px #000;
  }"""
new = """  .trope-hit.on::before {
    content: \"\\2713\";
    color: #e2c37a;
    font-size: clamp(13px, 3.2vw, 17px);
    font-weight: 700;
    line-height: 1;
    margin-right: 0.32em;
    text-shadow: 0 1px 4px rgba(0,0,0,.9);
    pointer-events: none;
  }"""
# write the check rule with a real check character
new = (
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
if old not in h:
    raise SystemExit('expected black-text CSS missing')
h = h.replace(old, new, 1)
if '-webkit-tap-highlight-color' not in h:
    h = h.replace(
        'transform: translateY(-50%);',
        'transform: translateY(-50%);\n    -webkit-tap-highlight-color: transparent;',
        1,
    )
p.write_text(h)
print('patched checks')
