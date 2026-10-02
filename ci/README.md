# ci/ scripts

The checks the GitHub workflows run. All of them are plain python3 (plus curl for the
link check) and run from the repository root:

| Script | What it enforces |
|---|---|
| `render_readme.py` | README.md and freshness.json are generated from the ledger and the seal chain; `--check` fails on any hand-edited number |
| `claims_lint.py` | prohibited claim terms outside explicit negations |
| `check_links.py` | every URL in the published documents resolves (GitHub repo/file links via the GitHub API; curl elsewhere) |
| `ots_check.py` | every seal proof parses, matches its manifest byte-for-byte, and carries a Bitcoin attestation; the published ledger matches the pinned hash |
| `qa_grep.py` | the internal-content terms removed in the cleanup stay out of the tree |

Local run: `python3 ci/<script>.py`. `render_readme.py` and `ots_check.py` need the
pinned client: `pip install opentimestamps-client==0.7.2` (or set `OTS_BIN`).

Workflows: `.github/workflows/ci.yml` runs all checks on push and pull requests;
`.github/workflows/freshness.yml` regenerates freshness.json daily and commits it if
changed. The README badge reads freshness.json from `main`. The check tolerates the
freshness day count being one day behind (UTC rollover); anything more fails as stale.
