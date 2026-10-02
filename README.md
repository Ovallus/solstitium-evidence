# Solstitium: public evidence

[![record freshness](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Ovallus/solstitium-evidence/main/freshness.json)](freshness.json)

Public slice of Solstitium's daily climate-prediction record: the verification ledger of
forecast-outcome pairs, a model bakeoff, index term sheets, and a complete chain of daily
OpenTimestamps-sealed manifests. You can recompute the published scores from the pairs
themselves and check every seal against Bitcoin. `VERIFY.md` states precisely what is and
is not checkable today.

## Status (generated from the record and the seals; do not edit by hand)

| Field | Value |
|---|---|
| Published pairs | 9,414 (ledger generated 2026-08-27; init times 2021-07-18 to 2026-08-23) |
| Aggregate skill | Brier Skill Score -0.5986 over n = 9,414: negative, and published as it is. The per-class table below is the honest breakdown |
| Daily anchors | 92 published (2026-07-03 to 2026-10-02), no missing days |
| Ledger vs chain | the published ledger (sha256 1d37ad828e0e2c81...) appears unchanged in 37 consecutive daily manifests: 2026-08-27 to 2026-10-02 (36 days) |
| Signals vs chain | rewritten on 70 of 92 days; longest identical-content run 2026-08-27 to 2026-09-17 (22 days); last change 2026-10-02 |
| Seal proofs | 92 of 92 `.ots` proofs carry a Bitcoin block attestation; 0 pending |
| Freshness | the badge above: days since the verification ledger last advanced, recomputed on every refresh; the table reports the same fact anchored to the latest published anchor |

The CI regenerates this table from `record/verification_state.json` and `seals/daily/` on
every change, and fails if any number was edited by hand. The freshness badge is
regenerated daily by a scheduled workflow.

### Skill by event class

| Event class | n | Brier Skill Score |
|---|---|---|
| frost | 96 | 0.72 |
| frost_lt0 | 2712 | null |
| frost_lt2 | 2712 | null |
| frost_lt4 | 2034 | null |
| heat_gt32 | 342 | -0.1159 |
| heat_gt35 | 852 | -3.6565 |
| heat_gt38 | 510 | null |
| heatwave | 156 | -0.012 |

`null` = the climatological baseline is zero for that cell in this sample: the score is
undefined, not failed. Read every row with its `n`.

## Contents

| Path | What it is |
|---|---|
| `record/verification_state.json` | The verification ledger: 9,414 forecast-outcome pairs. Each pair carries region, event definition, lead time, forecast probability `p`, observed outcome and observation source. Recompute the scores from the pairs yourself. |
| `record/example-day/` | Two worked pairs (a frost hit and a quiet day) and how to locate them in the ledger. |
| `bakeoff/` | Model bakeoff for the July 2021 Brazil frost case: RMSE, bias, frost detection, compute cost per model. |
| `terms/` | Two index specifications (term sheets): frost coffee (Brazil anchor) and cold spell (EU cities). |
| `seals/daily/` | The daily OpenTimestamps chain: 92 manifests (2026-07-03 to 2026-10-02), each a SHA-256 manifest of that day's record artifacts, plus its `.ots` proof. |
| `VERIFY.md` | What a third party can and cannot check with what is published today. |
| `ci/` | The checks that keep this repository honest (see `ci/README.md`). |

## Verify in 5 minutes

1. Recompute the scores from the pairs:

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

2. Check one seal (no Bitcoin node needed):

   ```bash
   pip install opentimestamps-client==0.7.2
   ots info seals/daily/anchor_20260818.json.ots
   ```

   You will see the SHA-256 of the manifest that the proof commits to, the calendar
   branches, and the Bitcoin block attestations. For full verification without a local
   node, drop the manifest and its `.ots` on https://opentimestamps.org. `VERIFY.md`
   has the complete guide.

3. Check that the published ledger matches the chain:

   ```bash
   shasum -a 256 record/verification_state.json
   # compare with the sha256 recorded under
   # seals/daily/anchor_YYYYMMDD.json -> files["logs/daily/verification_state.json"]
   ```

## What the record shows, honestly

- The aggregate Brier Skill Score is negative (-0.5986 over 9,414 pairs):
  most days are quiet and beating local climatology on quiet days is hard. The compound
  is published negative and all of it; positive skill concentrates in defined classes
  and every row carries its `n`.
- The verification side of the record is stalled, and the chain shows it: the published
  ledger has not advanced since 2026-08-27 (its hash is unchanged across
  37 consecutive manifests, 36 days through
  2026-10-02). The same chain shows the signals artifact moving again: unchanged
  from 2026-08-27 to 2026-09-17 (22 days), then
  rewritten daily, most recently 2026-10-02.

## What this is not

- Not a fund and not investment advice. No real money is traded on any signal in this
  repository or in the record it comes from.
- Not a promise of future performance. Verification windows are short for some event
  classes; every number carries its `n` for that reason.
- Not the full engine: internal calibration layers, feature pipelines and weights are
  not published.
- Not a commercial validation: the bakeoff covers a single historical case (n=1) and
  one evaluated model is licensed CC-BY-NC-SA-4.0.

## Contact

Questions, corrections and verification requests: open an issue at
https://github.com/Ovallus/solstitium-evidence/issues

Solstitium, engineered by CausalQuant. GitHub: https://github.com/Ovallus

## License

Everything in this repository: `LicenseRef-Solstitium-1.0` (see `LICENSE`): verification,
technical diligence and research use is granted; commercial redistribution, or use in
competing products, requires a license. Zenodo DOI: pending (see `RELEASING.md`).
