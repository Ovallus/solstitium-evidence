# Example pairs from the record

Two worked examples of the unit the public record is built from: a **forecast-outcome
pair** (a prediction for a defined region and day, and the outcome later observed for
it). `example_pairs.json` contains both pairs copied verbatim from
`record/verification_state.json`:

| Pair | Region | Init (issued) | Valid day | Lead | Forecast p | Observed Tmin | Outcome |
|---|---|---|---|---|---|---|---|
| frost hit | parana | 2021-07-18 | 2021-07-19 | 1 day | 0.6383 | 0.21 C | 1 (frost) |
| quiet day | minas_gerais | 2021-07-18 | 2021-07-19 | 1 day | 0.0128 | 10.68 C | 0 (no frost) |

Both pairs come from the first forecast day in the ledger and share one event
definition: `t2m_min` below 2.0 C. One verified positive, one verified negative.

## What a pair carries

- `p`: the model's probability that the event would occur on `valid_time`, issued at
  `init_time`, at the given lead time.
- `outcome`: 0 or 1, computed from the observed values (`obs_t2m_min_c`,
  `obs_t2m_max_c`) against the event `definition`.
- `obs_source`: the observation dataset the pair was graded against.

## Check the examples yourself

Both pairs are in the published ledger. Find them and re-derive the outcome:

```python
import json
d = json.load(open("record/verification_state.json"))
hit = next(x for x in d["verified"] if x["event"] == "frost" and x["outcome"] == 1)
quiet = next(x for x in d["verified"]
             if x["event"] == "frost" and x["outcome"] == 0 and x["p"] <= 0.05)
for x in (hit, quiet):
    t = x["definition"]["threshold_c"]
    observed = x["obs_t2m_min_c"]
    recomputed = int(observed < t) if x["definition"]["direction"] == "below" else int(observed > t)
    print(x["region"], x["p"], observed, "outcome", x["outcome"], "recomputed", recomputed)
```

The last two numbers must match for every pair: that is the arithmetic behind the
ledger's `outcome` column. CI re-checks that the example pairs still exist verbatim
in the ledger, so these copies cannot drift from the record.
