# Preexisting work disclosure

The sprint rules say: "mark any code you wrote before the sprint as preexisting in the README
and the report". The sprint starts on Friday 23 Oct 2026.

## Preexisting (written on Thu 22 Oct 2026, before the sprint start)

The first version of the experiment harness was written on 22 Oct 2026 with Claude Code,
under the author's direction:

- `succession/` (all modules), `modal_app.py`, `scripts/`, `configs/`, `tests/`
- `CLAUDE.md`, `.claude/rules/`, `docs/`, `paper/OUTLINE.md`

Commit hash of the preexisting state: see `git log` for the commit dated 22 Oct 2026
("Add cartel-succession experiment harness"). Record it here after merge: `________`.

No experiment was run and no result was produced before the sprint.

## Sprint work (23–25 Oct 2026)

Record here, with commit hashes:

- Pilot and main runs, all data under `results/`.
- Code changes after 23 Oct (list them).
- Analysis, figures, and the report.

## Third-party work used

- Market calibration: Calvano et al. (2020).
- Audit method: Tran & Yu (2026), arXiv 2610.28787. Re-implemented here; no code copied.
- Prompt design informed by Fish et al. (2024) and LLMCartel; text written for this project.
- Models: Qwen2.5-7B-Instruct (Apache 2.0), Mistral-7B-Instruct-v0.3 (Apache 2.0).
- Software: vLLM, Modal, matplotlib, PyYAML.
