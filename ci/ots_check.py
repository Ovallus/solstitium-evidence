#!/usr/bin/env python3
"""OpenTimestamps chain checks for this repository.

For every seals/daily/anchor_*.json.ots:
  - a sibling anchor_*.json exists with a valid ots-anchor.v1 shape;
  - the sha256 embedded in the .ots proof equals the sha256 of the .json bytes;
  - at least one Bitcoin block attestation is present once the anchor is older
    than GRACE_DAYS (younger anchors may legitimately still be pending).

Also checks that the published record/verification_state.json is the artifact
pinned by the latest manifest that lists it (the diligence coherence check).

Exit code 0 = all good, 1 = at least one hard failure. Recent-but-pending is a
warning, not a failure. Needs the pinned client:
  pip install opentimestamps-client==0.7.2   (or set OTS_BIN=/path/to/ots)
"""

import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

ANCHOR_DIR = "seals/daily"
GRACE_DAYS = 3
LEDGER_KEY = "logs/daily/verification_state.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def ots_binary():
    path = os.environ.get("OTS_BIN") or shutil.which("ots")
    if not path or not os.path.exists(path):
        sys.exit("ots client not found; install opentimestamps-client==0.7.2 "
                 "or set OTS_BIN")
    return path


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def proof_facts(ots, ots_path, timeout=120):
    r = subprocess.run([ots, "info", ots_path], capture_output=True, text=True,
                       timeout=timeout)
    out = r.stdout + r.stderr
    m = re.search(r"File sha256 hash: ([0-9a-f]{64})", out)
    digest = m.group(1) if m else None
    heights = sorted({int(h) for h in
                      re.findall(r"BitcoinBlockHeaderAttestation\((\d+)\)", out)})
    pending = "PendingAttestation" in out
    return digest, heights, pending


def anchor_day(name):
    return name.split("_")[1][:8]


def scan_chain(anchor_dir=ANCHOR_DIR):
    """Returns (entries, errors, warnings).

    entries: sorted list of per-anchor dicts (day, path, ledger_hash, sig_hash,
             proof_digest, heights, pending).
    """
    ots = ots_binary()
    entries, errors, warnings = [], [], []
    names = sorted(n for n in os.listdir(anchor_dir) if n.endswith(".json.ots"))
    for name in names:
        day = anchor_day(name)
        jpath = os.path.join(anchor_dir, name[:-4])
        opath = os.path.join(anchor_dir, name)
        e: dict = {"day": day, "ots": name}
        if not os.path.exists(jpath):
            errors.append(f"{name}: missing {name[:-4]}")
            entries.append(e)
            continue
        try:
            d = json.load(open(jpath))
        except Exception as exc:
            errors.append(f"{name[:-4]}: not valid JSON ({exc})")
            entries.append(e)
            continue
        if d.get("schema") != "ots-anchor.v1":
            errors.append(f"{name[:-4]}: unexpected schema {d.get('schema')!r}")
        files = d.get("files") or {}
        if not files:
            errors.append(f"{name[:-4]}: empty files map")
        for k, v in files.items():
            if not (isinstance(v, dict) and HEX64.match(str(v.get("sha256", "")))
                    and isinstance(v.get("bytes"), int) and v["bytes"] > 0):
                errors.append(f"{name[:-4]}: bad manifest entry for {k}")
        jhash = sha256_file(jpath)
        digest, heights, pending = proof_facts(ots, opath)
        e.update(jhash=jhash, digest=digest, heights=heights,
                 ledger_hash=(files.get(LEDGER_KEY) or {}).get("sha256"),
                 sig_hash=(files.get("logs/daily/daily_signals.jsonl")
                           or {}).get("sha256"))
        if digest != jhash:
            errors.append(f"{name}: proof commits to {digest}, "
                          f"json hashes to {jhash}")
        age = (datetime.datetime.now(datetime.timezone.utc).date()
               - datetime.date.fromisoformat(f"{day[:4]}-{day[4:6]}-{day[6:]}")).days
        e["age_days"] = age
        if not heights:
            if age > GRACE_DAYS:
                errors.append(f"{name}: no Bitcoin attestation after {age} days")
            else:
                warnings.append(f"{name}: still pending (age {age} days)")
        entries.append(e)
    return entries, errors, warnings


def seal_summary(anchor_dir=ANCHOR_DIR):
    entries, errors, warnings = scan_chain(anchor_dir)
    with_btc = sum(1 for e in entries if e.get("heights"))
    return {
        "total": len(entries),
        "with_bitcoin": with_btc,
        "pending": len(entries) - with_btc,
        "errors": errors,
        "warnings": warnings,
        "entries": entries,
    }


def chain_hashes(anchor_dir=ANCHOR_DIR):
    """Ordered (day, ledger_hash, sig_hash) tuples from the chain."""
    out = []
    for name in sorted(os.listdir(anchor_dir)):
        if not name.endswith(".json"):
            continue
        d = json.load(open(os.path.join(anchor_dir, name)))
        files = d.get("files") or {}
        out.append((anchor_day(name),
                    (files.get(LEDGER_KEY) or {}).get("sha256"),
                    (files.get("logs/daily/daily_signals.jsonl")
                     or {}).get("sha256")))
    return out


def missing_days(chain):
    days = [c[0] for c in chain]
    out = []
    for a, b in zip(days, days[1:]):
        da = datetime.date.fromisoformat(f"{a[:4]}-{a[4:6]}-{a[6:]}")
        db = datetime.date.fromisoformat(f"{b[:4]}-{b[4:6]}-{b[6:]}")
        step = datetime.timedelta(days=1)
        cur = da + step
        while cur < db:
            out.append(cur.isoformat())
            cur += step
    return out


def coherence_check(ledger_path="record/verification_state.json",
                    anchor_dir=ANCHOR_DIR):
    """The published ledger must be the artifact pinned by the latest manifest."""
    pubs = sha256_file(ledger_path)
    pins = [(day, h) for day, h, _ in chain_hashes(anchor_dir) if h]
    if not pins:
        return [f"{ledger_path}: no manifest pins {LEDGER_KEY}"]
    latest_day, latest_hash = pins[-1]
    if latest_hash != pubs:
        return [f"{ledger_path}: sha256 {pubs[:16]}... does not match the latest "
                f"pinned value {latest_hash[:16]}... ({latest_day}); refresh the "
                f"published copy"]
    return []


def main():
    summary = seal_summary()
    for e in summary["entries"]:
        hs = ",".join(str(h) for h in e.get("heights", [])) or "-"
        state = "bitcoin" if e.get("heights") else "pending"
        print(f"{e['day']} {state:8s} heights=[{hs}] digest_match="
              f"{'yes' if e.get('digest') and e.get('digest') == e.get('jhash') else 'NO'}")
    print(f"\nproofs: {summary['total']}, with Bitcoin attestation: "
          f"{summary['with_bitcoin']}, pending: {summary['pending']}")
    chain = chain_hashes()
    gaps = missing_days(chain)
    if gaps:
        print(f"missing anchor days: {len(gaps)} -> {gaps[:10]}")
    errs = list(summary["errors"]) + coherence_check()
    for w in summary["warnings"]:
        print(f"warning: {w}")
    if errs:
        print("\nFAILURES:")
        for e in errs:
            print(f"  - {e}")
        return 1
    print("chain OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
