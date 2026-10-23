# AI use log

The sprint allows AI tools. The team is responsible for everything in the report.

| Date | Tool | Use | Human check |
|---|---|---|---|
| 18 Oct 2026 | Claude (research agents) | Literature scan and idea list | Author to open cited papers before use |
| 22 Oct 2026 | Claude Code | Wrote the experiment harness, tests, docs and this repository structure | Author reviews code; test suite (36 tests) passes; code review and debug pass on 22 Oct fixed 5 issues |
| 23 Oct 2026 | Claude Code | Logged runs 6–8; proposed and wrote the final-run changes (request de-duplication, `same_notes` branch, calibrated audit H5c, H9, exploratory agreement and price-dynamics tables, `pool.py --shared`, `inspect_replies.py`, parallel GPU chunks, configs for runs 9–12) and their pre-registration text | Author reviews the code and the pre-registration before the runs start; 67 tests pass |
| 23 Oct 2026 | Claude Code | Wrote the exploratory 3D behavior figures (price paths, PCA of price paths) and their tests | Author checks the figures against `docs/RESULTS.md`; 71 tests pass |
| 23 Oct 2026 | Claude Code | At the author's explicit request, drafted the report (`Apart Research/main3.tex`) from the run logs and analysis files, and wrote `scripts/paper_figures.py` for the report figures. The report states this in Appendix E | Every number in the report traced by script to `results/<run>/analysis/`, `docs/RUN_LOG.md` or `Apart Research/figures/figure_data.json`; the author reviews and is responsible for every statement |
| 23 Oct 2026 | Claude Code | At the author's request, rewrote the report in the official sprint template (`Apart Research/report.md` → `report.docx`, `report.pdf`, `main3.tex` via `scripts/build_report.py`), added the run, controls and run-9 tables, and made the project image (`scripts/project_image.py`), the slides (`Apart Research/slides_src/`) and `Apart Research/README.md` | Every decimal in the report checked by script against stored analysis files, `figure_data.json` and `docs/RUN_LOG.md`; the author reviews and owns every statement |
| 23 Oct 2026 | Claude Code | At the author's request, rewrote the abstract and tightened the report text, restated the equations as numbered display equations, and restyled the slides (white, Times New Roman, three colours) | Every decimal checked again by script against stored data; the author reviews and owns every statement |
| | | | |

Rules for the report:

- The author writes the report text. Exception (23 Oct 2026): the author asked Claude Code to draft
  the report. The report discloses this, and the author reviews and owns every statement.
- AI tools may check reasoning, find errors, and propose edits.
- Every number comes from `results/<run>/analysis/`. Every reference is in `docs/RELATED_WORK.md`
  with a "Checked" entry.
