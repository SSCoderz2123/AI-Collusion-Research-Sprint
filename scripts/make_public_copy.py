"""Copy the code, configs and two docs into a separate folder that can be shown on its own.

  python scripts/make_public_copy.py            # writes cartel-succession/

The copy keeps the repository layout. It holds succession/, scripts/, tests/, configs/,
modal_app.py, the package files, docs/RESEARCH_BRIEF.md and docs/RELATED_WORK.md. It leaves out
the run data (results/), the report and slides (Apart Research/, paper/), the other docs, the
report-building scripts and the assistant instruction files. References to the left-out docs are
removed from the copied text. The script stops if a copied file still names a left-out doc or an
AI coding assistant. Run it again after a code change; it replaces the whole folder.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "cartel-succession"
FOLDERS = ("succession", "scripts", "tests", "configs")
FILES = ("modal_app.py", "pyproject.toml", "requirements.txt", "LICENSE")
KEPT_DOCS = ("docs/RESEARCH_BRIEF.md", "docs/RELATED_WORK.md")
# These build the sprint report, slides and project image from Apart Research/; the copy has no report.
SKIP = {
    "scripts/build_report.py",
    "scripts/paper_figures.py",
    "scripts/project_image.py",
    "scripts/make_public_copy.py",
    "tests/test_paper_figures.py",
}
# (pattern, replacement), applied in order to every copied text file.
EDITS = [
    (r"Apply the inclusion rule from docs/PREREGISTRATION\.md\.", "Apply the pre-registered inclusion rule."),
    (r"docs/PREREGISTRATION\.md, ", ""),
    (r", docs/PREREGISTRATION\.md", ""),
    (r" \(docs/PREREGISTRATION\.md\)", ""),
    (r"\(on vLLM; see docs/DESIGN\.md for the determinism check\)", "(on vLLM; the A/A stage checks this)"),
    (r" \(see docs/RUNNING_ON_MODAL\.md for the full guide\)", ""),
    (r" \(\.claude/rules/code\.md\)", ""),
    (r"\nDetails: `docs/PREREGISTRATION\.md`, `docs/DESIGN\.md`\.\n", ""),
    (r"\(estimate; see `docs/RUNNING_ON_MODAL\.md`\)", "(estimate)"),
    (r"opened with the alphaXiv PDF tool on", "read on"),
]
FORBIDDEN = re.compile(r"claude|anthropic|alphaxiv|copilot|chatgpt|AI_USE|AI tool|\.claude/", re.I)
DOC_REF = re.compile(r"docs/[A-Za-z_]+\.md")
TEXT = {".py", ".md", ".yaml", ".yml", ".toml", ".txt", ""}

GITIGNORE = """__pycache__/
*.pyc
.venv/
venv/
.env
.pytest_cache/
.ruff_cache/
*.egg-info/
results/
"""

README = """# Cartel Succession

Does LLM price collusion survive replacing an agent? Code for the study "Who Carries the Cartel?
LLM Price Collusion Survives Agent Replacement Through the Inherited Price History"
(AI Collusion Research Sprint, 23–25 Oct 2026; Track 1, question 1.2).

## Question

Two LLM pricing agents play a repeated logit Bertrand duopoly until prices are above the
competitive level. At round 100 one agent is replaced. The experiment measures whether the high
prices continue, and whether the model, the inherited price history or the inherited notes carry
them. A paired forced-cut audit tests whether the prices after the replacement are enforced or
only anchored. Background and design: `docs/RESEARCH_BRIEF.md`; prior work: `docs/RELATED_WORK.md`.

## Conditions

| Condition | Firm-2 price setter from round 100 | History seen | Entrant's notes |
|---|---|---|---|
| `control` | incumbent (no replacement) | all | kept |
| `placebo` | incumbent; firm 1 still gets the notice | all | kept |
| `same_inherit` | new instance of the same model | last 30 rounds | cleared |
| `same_blank` | new instance of the same model | none | cleared |
| `same_notes` | new instance of the same model | none | predecessor's |
| `other_inherit` | other model family | last 30 rounds | cleared |
| `other_blank` | other model family | none | cleared |
| `br_bot` | best response to firm 1's last price | firm 1's last price | – |

Seeds depend on the experiment seed, session, firm, round and retry count, never on the
condition, so the conditions of one session are paired.

## Quick start

```bash
pip install -r requirements.txt
python -m pytest -q                                    # mock backend, no GPU
python scripts/run_local.py --backend mock             # full pipeline with a mock model
python -m modal setup
modal run modal_app.py --config configs/pilot.yaml --stages aa,phase1,select,analyze
```

## Layout

```
succession/   experiment package: market, prompts, parsing, backends, session, branches,
              experiment stages, metrics, hypotheses, analysis, storage
modal_app.py  Modal app (GPU generator + CPU orchestrator)
configs/      main.yaml (pre-registered), main_*.yaml (runs 5-8), final_*.yaml (runs 9-12), pilot.yaml, local_4060.yaml
scripts/      run_local.py, analyze.py, pool.py, inspect_replies.py, plot_behavior.py
tests/        pytest suite (mock backend)
docs/         research brief, related work
```

## License

MIT. See `LICENSE`.
"""


def copy_file(src: Path, rel: str) -> None:
    dst = OUT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix not in TEXT:
        shutil.copy2(src, dst)
        return
    text = src.read_text(encoding="utf-8")
    for pattern, replacement in EDITS:
        text = re.sub(pattern, replacement, text)
    bad = FORBIDDEN.search(text)
    if bad:
        raise SystemExit(f"{rel}: still mentions {bad.group(0)!r}; add an entry to EDITS")
    for ref in DOC_REF.findall(text):
        if ref not in KEPT_DOCS:
            raise SystemExit(f"{rel}: still refers to {ref}, which the copy leaves out; add an entry to EDITS")
    dst.write_text(text, encoding="utf-8")


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    for folder in FOLDERS:
        for src in sorted((ROOT / folder).rglob("*")):
            rel = src.relative_to(ROOT).as_posix()
            if src.is_dir() or "__pycache__" in src.parts or rel in SKIP:
                continue
            copy_file(src, rel)
    for rel in FILES + KEPT_DOCS:
        copy_file(ROOT / rel, rel)
    (OUT / ".gitignore").write_text(GITIGNORE, encoding="utf-8")
    (OUT / "README.md").write_text(README, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}/ ({sum(1 for p in OUT.rglob('*') if p.is_file())} files)")


if __name__ == "__main__":
    main()
