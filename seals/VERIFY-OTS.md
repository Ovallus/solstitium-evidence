# Verifying the time seal (OpenTimestamps)

The file `anchor_20260917.json` is a manifest: it lists the SHA-256 of that day's record
artifacts. Its companion `anchor_20260917.json.ots` is an OpenTimestamps proof that the
manifest existed at that date — anchored in the Bitcoin blockchain through four public
calendar servers.

## Verify it yourself

```bash
pip install opentimestamps-client

# 1. See the attestation chain (which calendars, which Bitcoin block):
ots info anchor_20260917.json.ots

# 2. Verify against the Bitcoin blockchain:
ots verify anchor_20260917.json.ots
```

Notes:

- `ots verify` needs to fetch the Bitcoin block from a public explorer; with no local
  Bitcoin node it still verifies through public endpoints. If your client complains about
  a missing local node, that only affects the optional local-node path — the calendar
  attestation chain is the proof.
- Freshly stamped files show `Pending confirmation in Bitcoin blockchain` for a few hours
  until the next Bitcoin block confirms them. A completed proof reports
  `Success! Timestamp complete`.
- Any byte change to the anchored file breaks the proof. That is the point: this record
  cannot be edited retroactively.

More: https://opentimestamps.org
