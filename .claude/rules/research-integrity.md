# Research integrity rules

These rules come from the sprint guidelines and the organizers' email of 22 Oct 2026.
A breach can disqualify the project.

1. **No fabricated results.** Report only numbers produced by code in this repository from
   stored run data. Never type a result by hand into the report. Every number in the report
   must trace to a file under `results/<run>/analysis/`.
2. **No fabricated references.** Cite a paper only after a person or tool has opened it.
   Record what was checked in `docs/RELATED_WORK.md`. Do not invent arXiv IDs, authors, titles or quotes.
3. **Disclose prior work.** Code written before the sprint start (Fri 23 Oct 2026) is preexisting.
   List it in `docs/PREEXISTING_WORK.md`, in the README, and in the report. Mark new sprint work by
   commit date.
4. **Disclose AI use.** Log the use of AI tools in `docs/AI_USE.md`. The team is responsible for every
   statement in the report.
5. **Fixed analysis plan.** The hypotheses, inclusion rule, windows and metrics in
   `docs/PREREGISTRATION.md` are fixed before phase 1 runs. A change after that point goes in the
   deviations section of that file, with the date and the reason. Results of an unplanned
   analysis are labelled "exploratory".
6. **Report everything.** Report all branches, null results, parse-failure rates, invalid audit
   events, and the A/A determinism result. Do not drop seeds or sessions outside the inclusion rule.
7. **Positive and negative controls first.** Do not interpret phase 2 until the controls stage and
   the A/A check have run.
8. **Dual use.** The report needs a Limitations and Dual-Use / Ethical Considerations appendix.
   Do not publish prompts or procedures tuned to make collusion harder to detect.
9. **Limits.** Report length is 4–8 pages without references and appendices (8 is a hard cap).
   Abstract ≤ 150 words. Deadline: Sun 25 Oct 2026, 23:59 AoE (Mon 26 Oct, 11:59 UTC).
