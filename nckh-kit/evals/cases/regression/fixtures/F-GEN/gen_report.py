import sys
from pathlib import Path

TEMPLATE = Path("m\u1eabu-b\u00e1o-c\u00e1o.txt")
PLACEHOLDER = "<b\u00e1o c\u00e1o t\u1ea1i \u0111\u00e2y>"

text = TEMPLATE.read_text(encoding="utf-8")
if PLACEHOLDER not in text:
    print("error: report template has no placeholder; refusing to generate", file=sys.stderr)
    sys.exit(2)
out = Path("out")
out.mkdir(exist_ok=True)
(out / "bao-cao.txt").write_text(text.replace(PLACEHOLDER, "Lab 2 report body"), encoding="utf-8")
print("generated out/bao-cao.txt")
