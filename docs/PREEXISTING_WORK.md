# Preexisting work disclosure

The sprint rules say: "mark any code you wrote before the sprint as preexisting in the README
and the report". The sprint starts on Friday 23 Oct 2026.

## Preexisting (written on Thu 22 Oct 2026, before the sprint start)

The first version of the experiment harness was written on 22 Oct 2026 with Claude Code,
under the author's direction:

- `succession/` (all modules), `modal_app.py`, `scripts/`, `configs/`, `tests/`
- `CLAUDE.md`, `.claude/rules/`, `docs/`, `paper/OUTLINE.md`

Commit hash of the preexisting state: see `git log` for the commit dated 22 Oct 2026
("Add cartel-succession experiment harness"). Recorded: `d86d384` and `b01d10f` (merged in PR #1), `d34181c` (PR #2).

Pre-sprint setup runs on Modal (22 Oct 2026): the pilot config only (`configs/pilot.yaml`,
4 sessions × 60 rounds), to check the GPU image, determinism and the inclusion rule. See
`docs/RUN_LOG.md`. No main-run result and no report finding come from these runs.

**Main runs before the sprint start.** The main run (`main`) and the replication (`main_mistral`)
ran on 22 Oct 2026, 18:40–23:10 UTC, before the sprint start on Fri 23 Oct 2026 (runs 4–5 in
`docs/RUN_LOG.md`). The report must state this. Analysis of these runs, any further runs, and the
report are sprint work.

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
