# seals

The OpenTimestamps chain of the daily record.

- `daily/`: one manifest (`anchor_YYYYMMDD.json`) and its proof (`anchor_YYYYMMDD.json.ots`)
  per day since the first anchor. The current count and date range are generated in the
  repository README; once published, a manifest is never rewritten.
- Each manifest lists the SHA-256 and byte size of that day's record artifacts, plus the
  head commit of the private record repository at seal time.
- Quick check (info works anywhere, no Bitcoin node needed):
  `pip install opentimestamps-client==0.7.2` then
  `ots info daily/anchor_YYYYMMDD.json.ots`
- Full guide for third parties: see `../VERIFY.md`.
- Never edit a manifest or its `.ots`: the proof binds the exact bytes.
