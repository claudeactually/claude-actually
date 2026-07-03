#!/usr/bin/env python3
"""Voice check: fail if any em dash reaches the site.

The Claude, Actually voice rules (persona/voice.md, brand/BRAND-GUIDE.md) ban
em dashes in anything published. This scans every HTML and Markdown file in
the repo for a literal em dash or its entities and exits nonzero if found.
Gated field-test payloads are base64, so this only sees rendered page copy.

Runs standalone or as the pre-commit hook:
  python3 scripts/voice_check.py
"""

import pathlib
import re
import sys

BANNED = re.compile("—|&mdash;|&#8212;|&#x2014;")
ROOT = pathlib.Path(__file__).resolve().parent.parent

bad = []
for pattern in ("*.html", "*.md", "field-tests/*.html", "scripts/*.html"):
    for f in ROOT.glob(pattern):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if BANNED.search(line):
                bad.append(f"{f.relative_to(ROOT)}:{i}")

if bad:
    print("EM DASH FOUND (voice.md: instant fail). Replace with a comma, colon, or period:")
    print("\n".join(f"  {b}" for b in bad))
    sys.exit(1)
print("voice check: clean, no em dashes")
