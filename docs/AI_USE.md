# AI use log

The sprint allows AI tools. The team is responsible for everything in the report.

| Date | Tool | Use | Human check |
|---|---|---|---|
| 18 Oct 2026 | Claude (research agents) | Literature scan and idea list | Author to open cited papers before use |
| 22 Oct 2026 | Claude Code | Wrote the experiment harness, tests, docs and this repository structure | Author reviews code; test suite (36 tests) passes; code review and debug pass on 22 Oct fixed 5 issues |
| 23 Oct 2026 | Claude Code | Logged runs 6–8; proposed and wrote the final-run changes (request de-duplication, `same_notes` branch, calibrated audit H5c, H9, exploratory agreement and price-dynamics tables, `pool.py --shared`, `inspect_replies.py`, parallel GPU chunks, configs for runs 9–12) and their pre-registration text | Author reviews the code and the pre-registration before the runs start; 67 tests pass |
| 23 Oct 2026 | Claude Code | Wrote the exploratory 3D behavior figures (price paths, PCA of price paths) and their tests | Author checks the figures against `docs/RESULTS.md`; 71 tests pass |
| | | | |

Rules for the report:

- The author writes the report text.
- AI tools may check reasoning, find errors, and propose edits.
- Every number comes from `results/<run>/analysis/`. Every reference is in `docs/RELATED_WORK.md`
  with a "Checked" entry.
