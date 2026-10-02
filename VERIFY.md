# VERIFY.md: what a third party can and cannot check

Everything in this repository is meant to be checkable from the outside with public
tools only. This file states precisely what that allows today, and what it does not.

| # | Check | Possible today? | Section |
|---|---|---|---|
| 1 | Recompute the published scores from the published pairs | Yes | 1 |
| 2 | Verify that each daily seal proof is valid and reached Bitcoin | Yes | 2 |
| 3 | Verify that the published ledger is the file the chain pins | Yes | 3 |
| 4 | Read the record cadence (including its current stall) from the chain | Yes | 4 |
| 5 | Check, pair by pair, that each prediction preceded its outcome | Not yet, from this repository alone | 5 |
| 6 | Check that the record will be updated in the future | No, and nothing here promises it | 5 |

## 1. Recompute the scores

```bash
python3 - <<'EOF'
import json
d = json.load(open("record/verification_state.json"))
print("pairs:", d["n_verified_total"])
oe = d["overall"]
print("global BSS:", oe.get("brier_skill_score"), "(n =", oe.get("n"), ")")
for ev, m in sorted(d["by_event"].items()):
    print(f"  {ev}: n={m.get('n')} bss={m.get('brier_skill_score')}")
EOF
```

The ledger is self-contained: every pair carries its forecast probability, its observed
values and its outcome. A `null` Brier Skill Score means the climatological baseline is
zero for that cell in this sample (undefined, not failed). Per-event rows and threshold
slices (`frost`, `frost_lt0`, `heat_gt35`, ...) answer different questions; each carries
its `n`.

## 2. Verify the seals

The chain lives in `seals/daily/`. For every day there is a manifest
(`anchor_YYYYMMDD.json`: the SHA-256 of that day's record artifacts, plus the head commit
of the private record repository at seal time) and its OpenTimestamps proof (`.ots`).

```bash
pip install opentimestamps-client==0.7.2
ots info seals/daily/anchor_20260917.json.ots
```

Real output, abridged:

```
File sha256 hash: eefbe9616f7fc9242aa8b01d6c8d1fe31e7aa38df5b5538c475f10b15116c914
Timestamp:
append 19a8f2737675d66075887c12477927ef
sha256
  [... proof branches omitted ...]
    verify BitcoinBlockHeaderAttestation(967447)
    verify BitcoinBlockHeaderAttestation(967477)
```

What to take from it:

- `File sha256 hash` must equal `shasum -a 256 seals/daily/anchor_20260917.json`. It
  does: the value above is the sha256 of that file. The proof binds those exact bytes.
- Each `BitcoinBlockHeaderAttestation(H)` is an attestation folded from a public calendar
  into Bitcoin block H: after that block confirmed, the manifest bytes provably existed.
- `PendingAttestation(...)` on some branches is normal: calendars publish on their own
  schedules, and a proof can be complete (as this one is) while an individual branch
  still shows pending.

Full cryptographic verification without a local Bitcoin node: drop the manifest and its
`.ots` on the verifier at https://opentimestamps.org. The plain `ots verify` command
requires a local Bitcoin node and reports a connection error without one; that is a
client limitation, not a problem with the proof.

Do not edit any manifest or proof: any byte change breaks the seal.

## 3. The published ledger is the file the chain pins

```bash
shasum -a 256 record/verification_state.json
# then read files["logs/daily/verification_state.json"]["sha256"] in any
# seals/daily/anchor_*.json
```

The value you compute is listed in every manifest from 2026-08-27 through 2026-10-02.
That means: the published ledger is the exact artifact the record held on those days,
and it did not change across them (identical hashes in consecutive attested manifests).

## 4. Read the record cadence from the chain

The same day-by-day comparison shows when each pinned artifact was last rewritten:

```bash
python3 - <<'EOF'
import json, glob
key = "logs/daily/daily_signals.jsonl"
prev = None
for f in sorted(glob.glob("seals/daily/anchor_*.json")):
    day = f.split("_")[-1][:8]
    h = json.load(open(f))["files"][key]["sha256"]
    if h != prev:
        print("changed:", day)
    prev = h
EOF
```

A run of identical hashes means the artifact was not advanced on those days. The current
stall of the record is visible exactly this way, with dates; the repository README shows
the summary table generated from this same comparison.

## 5. What is NOT checkable today, precisely

- **Pair by pair no-look-ahead.** For any single pair, that its forecast probability
  existed before its outcome cannot be shown from this repository alone, because the
  forecast artifacts are not published: the manifests pin their hashes, not their
  contents. That check becomes possible for a given day if and when the underlying
  artifact is disclosed and matches the hash in that day's manifest. The manifest chain
  is the commitment that makes such a future check possible; it is not the check itself.
- **Pairs whose forecast day predates the chain.** The chain starts 2026-07-03. Pairs
  with earlier init times cannot be tied to a public seal of their own; their provenance
  rests on the engine's internal record.
- **The private artifacts themselves.** Only hashes are pinned. What the private files
  contain beyond their published summaries is not checkable here.
- **Future updates.** No file here promises that the record resumes, or when. If it
  does, the new manifests and ledger snapshots will extend this chain visibly; until
  then the honest statement is the one the chain supports: each pinned artifact either
  advances or does not, and its dates are read from the chain (section 4).
- **Claims that were removed.** Earlier versions of the README contained claims that are
  not verifiable ("verified independently, without trusting us"; "repaired the day it
  was found"). They were removed and are no longer made. The surviving text is limited
  to what the published artifacts support.

## 6. The checks this repository runs on itself

CI runs the same discipline on every change (see `ci/`):

- `ci/render_readme.py --check`: every number in README.md is regenerated from the
  ledger and the chain; a hand-edited number fails the build.
- `ci/ots_check.py`: every proof parses, matches its manifest byte-for-byte, and (for
  manifests older than a short grace window) carries at least one Bitcoin attestation;
  it also checks that the published ledger matches the pinned hash.
- `ci/qa_grep.py`, `ci/claims_lint.py`: published text stays clear of internal terms
  and of prohibited claim language.
- `ci/check_links.py`: every URL in the documents resolves.

Run them locally from the repository root after
`pip install opentimestamps-client==0.7.2`.
