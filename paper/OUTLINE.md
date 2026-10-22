# Report outline (structure only)

Use the official sprint template. 4–8 pages without references and appendices; 8 is a hard cap.
Abstract ≤ 150 words. Write the text yourself. Put every number from `results/main/analysis/`.

| Section | Pages | Contents | Source |
|---|---|---|---|
| Abstract | – | Question, method in one sentence, main numbers, one-line implication | `analysis/summary.md` |
| 1 Introduction | 0.75 | Replacement as an antitrust remedy; the open gap (organizers' Q1.2); contributions | `docs/RESEARCH_BRIEF.md` |
| 2 Related work | 0.5 | Tran & Yu; Arslan et al.; Gao et al.; Lee; Keppo; Eschenbaum | `docs/RELATED_WORK.md` (checked items only) |
| 3 Method | 1.5 | Market; agents and prompt; phases; branch table; pairing and seeds; audit; controls; statistics | `docs/DESIGN.md`, `docs/PREREGISTRATION.md`, `configs/main.yaml` |
| 4 Results | 2 | A/A value; controls (trigger audit > 0, myopic); phase-1 inclusion count; Fig. 1 trajectories; Fig. 2 paired differences; H1–H5 verdicts; audit table | `analysis/*` |
| 5 Discussion | 0.75 | What carries the cartel; remedy implications; what the audit says about enforcement vs anchoring | – |
| 6 Limitations | 0.5 | Two 7B models; one prompt; one market; 100-round horizon; vLLM determinism; n of kept sessions | – |
| References | – | Only checked papers | – |
| Appendix A | – | Limitations and Dual-Use / Ethical Considerations (required) | – |
| Appendix B | – | Full prompt, config, parse-failure rates, invalid audit events, preexisting-work statement | `succession/prompts.py`, `docs/PREEXISTING_WORK.md` |

Dual-use points to cover: the result could tell a firm how to keep a cartel through a vendor
change (keep the price history); it also tells a regulator what to cut. No evasion method is
published.
