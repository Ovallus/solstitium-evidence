# Solstitium — Public Evidence

The reproducible slice of our daily climate-prediction record. Forecast-outcome pairs,
a model bakeoff, index specifications, and time-sealed anchors. **Everything here can be
recomputed or verified independently, without trusting us.**

## Why it is built this way

Our full daily record is a private repository where a bot commits each day's predictions
**before** outcomes are known, and each day is sealed with OpenTimestamps (Bitcoin).
A sealed daily record is the only no-look-ahead proof that cannot be fabricated after the
fact. This repository is the curated public slice for auditors, buyers and investors.

## Contents

| Path | What it is |
|---|---|
| `record/verification_state.json` | **9,414 verified forecast-outcome pairs.** Each pair carries region, event definition, lead time, predicted probability `p`, observed outcome and observation source. Recompute the Brier Skill Score yourself. |
| `record/example-day/` | One day of the live record as committed (human briefing plus an explanation of the scheme). |
| `bakeoff/` | Model bakeoff for the July 2021 Brazil frost hindcast: RMSE, bias, frost detection, compute cost per model. |
| `terms/` | Two index specifications (term sheets): frost coffee (Brazil anchor) and cold spell (EU cities). |
| `seals/` | One daily OpenTimestamps anchor — a SHA-256 manifest of the day's artifacts — and its `.ots` proof. |

## Verify in 5 minutes (no account, no trust)

1. **Recompute the scores from the pairs:**

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

2. **Verify the time seal:**

   ```bash
   pip install opentimestamps-client
   ots info  seals/anchor_20260917.json.ots   # shows the Bitcoin attestation chain
   ots verify seals/anchor_20260917.json.ots  # verifies against the Bitcoin blockchain
   ```

3. **Check that the manifest matches the files:** the anchor in `seals/` contains the
   SHA-256 of that day's artifacts (including `verification_state.json`). Compare:

   ```bash
   shasum -a 256 record/verification_state.json
   # and read the "files" section of seals/anchor_20260917.json
   ```

## What the record shows — honestly

- The **aggregate Brier Skill Score over all 9,414 pairs is negative**. Most days are
  quiet, and beating local climatology on quiet days is hard. We publish the compound,
  negative and all; the per-event breakdown (each number with its `n`) is in the JSON.
  Positive skill concentrates in specific event classes; read them with their sample sizes.
- The record had a **22-day gap** (2026-08-28 to 2026-09-18) caused by an infrastructure
  timeout. It is visible in the commit history, it was repaired the day it was found, and
  the OpenTimestamps anchors kept sealing uninterrupted throughout — which is how the gap
  can be dated exactly. We treat visible failure plus repair as part of the record's value.

## What this is not

- Not a fund. No real money is traded on the trading signals in the record (paper only).
- Not a promise of future performance. Verification windows are short for some event
  classes; every number carries its `n` for that reason.
- Not the full engine. Internal calibration layers, feature pipelines and weights are not
  published.

## Contact

Solstitium — engineered by CausalQuant.
`contacto@solstitium.eu` (activate at domain registration) · github.com/Ovallus

*Published for verification, diligence and research. Redistribution with attribution;
commercial use of the term sheets or record requires a license.*
