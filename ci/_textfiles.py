#!/usr/bin/env python3
"""Shared walker: every text file in the repository tree.

Binary formats are skipped by extension; everything else is yielded and the
caller decides what to do with files it cannot decode. This keeps the checkers
honest about new file types: a term planted in a file with an unexpected
extension still gets scanned.
"""

import os

EXCLUDE_DIRS = {".git"}
BINARY_EXT = {".ots", ".png", ".jpg", ".jpeg", ".gif", ".zip", ".gz",
              ".pdf", ".bundle", ".ico", ".woff", ".woff2"}


def text_files(exclude_dirs=(), extra_skip=()):
    skip_dirs = EXCLUDE_DIRS | set(exclude_dirs)
    skip_files = set(extra_skip)
    for base, dirs, names in os.walk("."):
        dirs[:] = sorted(d for d in dirs if d not in skip_dirs)
        for name in sorted(names):
            rel = os.path.relpath(os.path.join(base, name), ".")
            if os.path.splitext(name)[1].lower() in BINARY_EXT:
                continue
            if rel in skip_files:
                continue
            yield rel
