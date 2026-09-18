# Example day — how the daily record looks when committed

This directory contains one day of the **live record** (2026-09-18), copied exactly as
the bot commits it: the human-readable briefing. The machine artifacts that accompany it
in the private record (per-ticker signal state, portfolio state) are summarized here
rather than published field-by-field, because their full schema encodes internal
decision layers.

What the daily commit actually contains in the private record (for reference):

| Artifact | Purpose |
|---|---|
| `daily_briefing_YYYYMMDD.txt` | This human summary: portfolio, active signals, regimes. |
| `daily_signals.jsonl` | Machine signal state per instrument (published here only in summary). |
| `portfolio_state.json` | Paper-portfolio state (no real money). |
| `pevent_YYYYMMDD.json` | The day's P(event) forecasts per region (internal format, not published). |
| `registry_health.json` | Health of the record itself; alerts if anything failed. |
| `verification_state.json` | Rolling verification ledger — the public copy lives in `/record`. |

The commit timestamp is the proof: the briefing below was committed on 2026-09-18, and the
day's OpenTimestamps anchor (see `/seals`) seals its hash into Bitcoin.

---

```
CAUSALQUANT ORACLE — DAILY BRIEFING
Date: 2026-09-18  |  Portfolio: $100,000  |  Allocation: 30%
(vg. the file briefing_2026-09-18.txt in this directory: 0 active signals that day,
 3 instruments inactive — cocoa, orange juice, wheat — exposure $0)
```
