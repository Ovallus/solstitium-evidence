#!/usr/bin/env python3
"""Veto prohibited claim language in the published content.

Fails if a listed claim term appears in any content file an outsider reads,
unless the term is explicitly negated on the same line ("no garantiza...",
"not a certification..."). The linter's own directory and .github/ are
excluded: the list below necessarily contains the terms it forbids.

Run from the repository root: python3 ci/claims_lint.py
"""

import os
import re
import sys

TERMS = [
    r"certific",                       # certificacion / certificado / certified
    r"motor verificado", r"verified engine",
    r"incontestable", r"incontrovertible",
    r"\binmune\b", r"\bimmune\b",
    r"prueba matem[aá]tica", r"mathematically proven", r"mathematical proof",
    r"garant[ií]a", r"garantiz", r"guarantee",
    r"sin riesgo", r"riesgo cero", r"risk[- ]free", r"zero risk",
    r"infalible", r"infallible",
    r"no puede fallar", r"cannot fail", r"nunca falla",
]
NEGATION = re.compile(
    r"(?i)\b(no|ni|sin|nunca|jam[aá]s|not|never|nor|without)\b[^.;:\n]{0,48}$")

EXCLUDE_DIRS = {".git", "ci", ".github"}
TEXT_EXT = {".md", ".txt", ".json", ".cff", ".yml", ".yaml", ".csv"}
SPECIAL = {"LICENSE"}


def content_files():
    for base, dirs, names in os.walk("."):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in names:
            ext = os.path.splitext(name)[1].lower()
            if ext in TEXT_EXT or name in SPECIAL:
                yield os.path.join(base, name)


def main():
    pattern = re.compile("|".join(f"(?:{t})" for t in TERMS), re.IGNORECASE)
    violations = []
    negated = 0
    for path in sorted(content_files()):
        try:
            lines = open(path, encoding="utf-8").read().splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(lines, 1):
            for m in pattern.finditer(line):
                if NEGATION.search(line[:m.start()]):
                    negated += 1
                    continue
                violations.append((path, n, m.group(0), line.strip()[:110]))
    for path, n, term, line in violations:
        print(f"{path}:{n}: {term!r} -> {line}")
    if violations:
        print(f"\nFAIL: {len(violations)} prohibited claim term(s)")
        return 1
    print(f"claims lint OK ({negated} explicitly negated use(s) allowed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
