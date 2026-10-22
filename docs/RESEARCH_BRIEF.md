# Research brief: Cartel succession

**Working title:** Cartel Succession: Does LLM price collusion survive replacing an agent?
**Sprint:** Apart Research AI Collusion Research Sprint, 23–25 Oct 2026. Track 1, question 1.2.
**Author:** Supratik Bhowal (solo).

## Question

After two LLM pricing agents reach supra-competitive prices, one agent is replaced.

1. Does the profit index return to its pre-swap level?
2. Which part carries the cartel: the model, or the price history the entrant inherits?
3. After the swap, is the high price enforced (a cut is punished) or only anchored?

## Why it is open

The organizers state that no replacement study exists for LLM agents. A literature check on
22 Oct 2026 found close work, but no test of this question:

- Tran & Yu (2026, arXiv 2610.28787): paired forced-deviation audit; no agent replacement.
- Arslan et al. (2026, arXiv 2609.35402): partner persistence vs re-pairing for trained agents.
- Gao et al. (2026, arXiv 2609.05279): agent swap test in cooperative teams, not collusion.
- Eschenbaum et al. (2022): re-matching breaks Q-learning collusion.

## Policy relevance

If the cartel returns when the entrant inherits the history, replacing a pricing algorithm is
not a remedy unless the shared price history is also cut. If the cartel does not return,
replacement is a remedy. Both outcomes inform antitrust remedies for algorithmic pricing.

## Method summary

1. Market: two-firm logit Bertrand game (a=2, a0=0, μ=0.25, cost=1). Nash price 1.473,
   monopoly price 1.925.
2. Agents: Qwen2.5-7B-Instruct (incumbent family) and Mistral-7B-Instruct-v0.3 (other family),
   served by vLLM on Modal L4 GPUs. Temperature 0.7. Last 30 rounds of history plus own notes.
3. Phase 1: 20 sessions × 100 rounds. Keep sessions by the pre-registered rule.
4. Phase 2: copy each kept session into 7 branches at round 100 and play 100 more rounds.
5. Audit: at the end of each branch, force a 10% price cut in a paired copy and measure the
   rival's response against a best-response benchmark.
6. Controls: A/A determinism check; myopic prompt (placebo); instructed trigger strategy
   (positive control for the audit); best-response bot entrant (negative control).

Details: `docs/PREREGISTRATION.md`, `docs/DESIGN.md`.

## Budget

About 8–10 L4 GPU hours, about $8–15 of the $50 Modal credit (estimate; see
`docs/RUNNING_ON_MODAL.md`).
