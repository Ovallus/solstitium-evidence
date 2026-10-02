#!/usr/bin/env python3
"""Render README.md and freshness.json from the record and the seal chain.

Usage:
  python3 ci/render_readme.py           # write README.md and freshness.json
  python3 ci/render_readme.py --check   # verify both match (CI; exit 1 on drift)

Every number in README.md is generated from:
  - record/verification_state.json        (the verification ledger)
  - seals/daily/anchor_*.json + .ots      (the OpenTimestamps chain)
  - record/example-day/example_pairs.json (checked to still exist in the ledger)

Never edit README.md by hand: edit README.template.md and re-run this script.
Needs the pinned client (see .github/workflows/ci.yml):
  pip install opentimestamps-client==0.7.2   (or set OTS_BIN=/path/to/ots)
"""

import datetime
import difflib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "ci"))

import ots_check  # noqa: E402

TEMPLATE = "README.template.md"
README = "README.md"
FRESHNESS = "freshness.json"
RECORD = "record/verification_state.json"


def iso(day):
    return f"{day[:4]}-{day[4:6]}-{day[6:]}"


def fresh_values():
    rec = json.load(open(RECORD))
    pairs = rec["verified"]
    chain = ots_check.chain_hashes()
    days = [c[0] for c in chain]
    ledger = [c[1] for c in chain]
    signals = [c[2] for c in chain]

    j = len(chain) - 1
    while j > 0 and ledger[j - 1] == ledger[j]:
        j -= 1
    ledger_first = days[j]
    ledger_stale = len(chain) - j
    ledger_days = (datetime.date.fromisoformat(iso(days[-1]))
                   - datetime.date.fromisoformat(iso(ledger_first))).days

    def runs_of(seq):
        out = []
        start = 0
        for i in range(1, len(seq) + 1):
            if i == len(seq) or seq[i] != seq[start]:
                out.append((start, i - 1))
                start = i
        return out

    sig_runs = runs_of(signals)
    signals_changed = len(sig_runs)
    signals_last = days[sig_runs[-1][0]]
    gap = max(sig_runs[:-1], key=lambda r: r[1] - r[0], default=None)
    if gap and gap[1] > gap[0]:
        signals_gap_start = iso(days[gap[0]])
        signals_gap_end = iso(days[gap[1]])
        signals_gap_days = str(gap[1] - gap[0] + 1)
        signals_resume = iso(days[gap[1] + 1])
    else:
        signals_gap_start = signals_gap_end = signals_resume = "n/a"
        signals_gap_days = "0"

    gaps = ots_check.missing_days(chain)
    ss = ots_check.seal_summary()
    rec_gen = rec["generated_at"]

    rows = ["| Event class | n | Brier Skill Score |", "|---|---|---|"]
    for ev in sorted(rec["by_event"]):
        m = rec["by_event"][ev]
        bss = ("null" if m.get("brier_skill_score") is None
               else json.dumps(m["brier_skill_score"]))
        rows.append(f"| {ev} | {m['n']} | {bss} |")

    today = datetime.datetime.now(datetime.timezone.utc).date()
    days_old = (today - datetime.date.fromisoformat(iso(ledger_first))).days
    color = "green" if days_old <= 2 else ("yellow" if days_old <= 7 else "red")

    tokens = {
        "N_PAIRS": f"{rec['n_verified_total']:,}",
        "AS_OF": iso(rec_gen[:10].replace("-", "")),
        "FIRST_INIT": rec["first_init"][:10],
        "LAST_INIT": rec["last_init"][:10],
        "BSS_OVERALL": json.dumps(rec["overall"]["brier_skill_score"]),
        "N_ANCHORS": str(len(chain)),
        "ANCHOR_FIRST": iso(days[0]),
        "ANCHOR_LAST": iso(days[-1]),
        "ANCHOR_MID": days[len(days) // 2],
        "CHAIN_GAPS": ("no missing days" if not gaps
                       else f"{len(gaps)} missing: {', '.join(gaps)}"),
        "LEDGER_HASH_SHORT": f"{ledger[-1][:16]}...",
        "LEDGER_FIRST_PINNED": iso(ledger_first),
        "LEDGER_STALE_ANCHORS": str(ledger_stale),
        "LEDGER_STALE_DAYS": str(ledger_days),
        "SIGNALS_LAST_CHANGE": iso(signals_last),
        "SIGNALS_CHANGED_DAYS": str(signals_changed),
        "SIGNALS_GAP_START": signals_gap_start,
        "SIGNALS_GAP_END": signals_gap_end,
        "SIGNALS_GAP_DAYS": signals_gap_days,
        "SIGNALS_RESUME": signals_resume,
        "OTS_BTC": str(ss["with_bitcoin"]),
        "OTS_TOTAL": str(ss["total"]),
        "OTS_PENDING": str(ss["pending"]),
        "BY_EVENT_TABLE": "\n".join(rows),
    }
    freshness = {
        "schemaVersion": 1,
        "label": "record freshness",
        "message": f"{days_old} days",
        "color": color,
        "meta": {
            "meaning": ("days since the verification ledger last advanced, "
                        "as of the refresh date"),
            "ledger_last_advanced": iso(ledger_first),
            "latest_anchor": iso(days[-1]),
            "refreshed_at_utc": datetime.datetime.now(
                datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
    }
    return tokens, freshness


def render(tokens):
    text = open(TEMPLATE).read()
    for key, val in tokens.items():
        text = text.replace("{{" + key + "}}", val)
    if "{{" in text or "}}" in text:
        leftover = [l for l in text.splitlines() if "{{" in l or "}}" in l]
        sys.exit("unreplaced tokens in template:\n" + "\n".join(leftover[:10]))
    return text


def check_examples(pairs):
    ex = json.load(open("record/example-day/example_pairs.json"))
    for p in ex["pairs"]:
        if p not in pairs:
            return [f"example pair not found verbatim in {RECORD}: "
                    f"{p['region']} {p['event']} {p['init_time']}"]
    return []


def check():
    rec = json.load(open(RECORD))
    tokens, freshness = fresh_values()
    rendered = render(tokens)
    problems = check_examples(rec["verified"])

    current = open(README).read()
    if current != rendered:
        diff = difflib.unified_diff(current.splitlines(),
                                    rendered.splitlines(),
                                    "README.md (committed)",
                                    "README.md (generated)", lineterm="")
        sys.stderr.write("\n".join(list(diff)[:80]) + "\n")
        problems.append("README.md differs from the generated version "
                        "(edit README.template.md and re-run ci/render_readme.py)")

    try:
        fr = json.load(open(FRESHNESS))
    except Exception as exc:
        problems.append(f"freshness.json unreadable: {exc}")
        fr = None
    if fr is not None:
        days_now = int(freshness["message"].split()[0])
        try:
            days_committed = int(str(fr["message"]).split()[0])
        except Exception:
            days_committed = None
        if fr.get("label") != freshness["label"]:
            problems.append("freshness.json label mismatch")
        if fr.get("meta", {}).get("ledger_last_advanced") != \
                freshness["meta"]["ledger_last_advanced"]:
            problems.append("freshness.json ledger_last_advanced mismatch")
        if fr.get("meta", {}).get("latest_anchor") != \
                freshness["meta"]["latest_anchor"]:
            problems.append("freshness.json latest_anchor mismatch")
        if days_committed not in (days_now, days_now - 1):
            problems.append(
                f"freshness.json is stale: says {fr.get('message')!r}, "
                f"recomputed {freshness['message']!r} "
                f"(re-run ci/render_readme.py or dispatch the refresh workflow)")

    for p in problems:
        print(f"FAIL: {p}")
    if problems:
        return 1
    print(f"README.md OK ({len(rendered)} bytes); freshness.json OK "
          f"({freshness['message']})")
    return 0


def write():
    rec = json.load(open(RECORD))
    tokens, freshness = fresh_values()
    rendered = render(tokens)
    problems = check_examples(rec["verified"])
    if problems:
        sys.exit("\n".join(problems))
    open(README, "w").write(rendered)
    with open(FRESHNESS, "w") as fh:
        json.dump(freshness, fh, indent=2)
        fh.write("\n")
    print(f"wrote {README} ({len(rendered)} bytes) and {FRESHNESS} "
          f"(freshness: {freshness['message']})")
    return 0


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check())
    sys.exit(write())
