# Writing rules (docs, comments, report support material)

Write in ASD-STE100 Simplified Technical English (STE) style:

- Short sentences. One idea per sentence. Active voice.
- Concrete verbs. Use the same term for the same concept every time
  (for example: "profit index", not also "collusion score" or "Delta level").
- No filler, no marketing words ("robust", "seamless", "powerful", "comprehensive", "leverages").
- Give quantities, conditions and units. State cause and result explicitly.
- Define a technical term at first use. Keep abbreviations consistent.
- Instructions use imperative verbs: "Run", "Open", "Check".

Fixed terms in this project:

| Term | Meaning |
|---|---|
| profit index | (profit − Nash profit) / (monopoly profit − Nash profit), mean of both firms |
| incumbent | the agent that stays in the market at the swap |
| entrant | the agent that takes the replaced seat |
| swap round | the first round played by the entrant (round 100 in the main run) |
| branch | one phase-2 condition applied to a copy of a phase-1 session |
| root session | a phase-1 session; the unit of analysis |
| audit | the paired forced-cut test of Tran & Yu (2026) |
| excess response | rival response to a forced cut minus the best-response benchmark |

The sprint report text is the authors' own writing. AI tools may check reasoning, find gaps,
and suggest edits. They do not write report sections (see `docs/AI_USE.md`).
Exception: on 23 Oct 2026 the author asked Claude Code to draft `Apart Research/main3.tex`.
The report discloses this in its AI-use appendix.
