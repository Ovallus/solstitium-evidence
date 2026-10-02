#!/usr/bin/env python3
"""P0 QA: the internal-content terms removed in the cleanup must not return.

Two passes over every text file in the tree:

1. Exact rule (case sensitive): zero matches. This is the acceptance grep.
2. Stricter audit (case insensitive): zero matches outside a small, justified
   allowlist of pre-existing locations:
     - part (2) in terms/*.md: module-path references that predate the cleanup
       (documented, not public claims);
     - part (1) in seals/daily/*.json: the sealed manifests pin an internal
       artifact name; their bytes are frozen by their .ots proofs, so editing
       them would break the seals.

Run from the repository root: python3 ci/qa_grep.py
"""

import os
import re
import sys

# Stored split so this checker does not contain the contiguous terms itself.
PARTS = [("Wyck", "off"), ("Port", "folio"), ("ORAC", "LE"), ("activate", " at")]
JOINED = "|".join(a + b for a, b in PARTS)
EXACT = re.compile(JOINED)
FUZZY = re.compile(JOINED, re.IGNORECASE)

EXCLUDE_DIRS = {".git"}
TEXT_EXT = {".md", ".txt", ".json", ".cff", ".yml", ".yaml", ".py", ".csv"}
SPECIAL = {"LICENSE"}
SELF = "ci/qa_grep.py"


def text_files():
    for base, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in names:
            ext = os.path.splitext(name)[1].lower()
            if ext in TEXT_EXT or name in SPECIAL:
                yield os.path.relpath(os.path.join(base, name), ".")


def part_index(m):
    g = m.group(0).lower()
    for i, (a, b) in enumerate(PARTS):
        if g == (a + b).lower():
            return i
    return -1


def allow_reason(rel, idx):
    if rel == SELF:
        return "the checker itself (patterns are stored split)"
    if idx == 2 and rel.startswith("terms/"):
        return "pre-existing module path reference in term sheets"
    if idx == 1 and rel.startswith("seals/daily/"):
        return "sealed manifest pins an internal artifact name (immutable by proof)"
    return None


def main():
    exact_hits = []
    fuzzy_bad = []
    allowed = 0
    for rel in sorted(text_files()):
        try:
            lines = open(rel, encoding="utf-8").read().splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(lines, 1):
            if EXACT.search(line):
                exact_hits.append((rel, n, line.strip()[:100]))
            for m in FUZZY.finditer(line):
                if allow_reason(rel, part_index(m)):
                    allowed += 1
                else:
                    fuzzy_bad.append((rel, n, part_index(m), line.strip()[:100]))
    for rel, n, line in exact_hits:
        print(f"EXACT {rel}:{n}: {line}")
    seen = set()
    for rel, n, idx, line in fuzzy_bad:
        key = (rel, idx)
        if key in seen:
            continue
        seen.add(key)
        print(f"FUZZY {rel}:{n}: part({idx}) -> {line}")
    print(f"\nexact hits: {len(exact_hits)}; "
          f"case-insensitive outside allowlist: {len(seen)}; "
          f"case-insensitive allowlisted: {allowed}")
    if exact_hits or seen:
        return 1
    print("QA grep OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
