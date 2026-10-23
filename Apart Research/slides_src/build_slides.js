// Build "Apart Research/slides.pptx" (10 slides, 16:9).
//   cd "Apart Research/slides_src" && npm install && npm run build
// Every number on the slides comes from the report (Tables 3-5, Appendix C and D), which traces to
// results/<run>/analysis/ and docs/RUN_LOG.md.
const path = require("path");
const pptxgen = require("pptxgenjs");

const OUT = path.join(__dirname, "..", "slides.pptx");
const FIG = path.join(__dirname, "..", "figures");
// Minimalist research theme: white background, Times New Roman, three colours.
//   primary (text, ~60%): charcoal; secondary (structure, ~30%): light grays; accent (~10%): royal blue,
//   used only for key numbers and the highlighted data series.
const HEAD = "Times New Roman";
const BODY = "Times New Roman";
const ACCENT = "1F5FBF";
const COL = {
  ink: "2B2F36", // primary: all main text
  ink2: "2B2F36",
  paper: "FFFFFF", // background; also text on accent or charcoal shapes
  tint: "F3F4F6", // secondary: card fill
  muted: "6B7280", // secondary: captions, footer
  soft: "D1D5DB", // secondary: lines, borders
  bar: "B8BEC7", // secondary: chart bars that are not highlighted
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.author = "Supratik Bhowal";
pres.title = "Who Carries the Cartel?";
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };

const FOOTER = "Who Carries the Cartel?  ·  AI Collusion Research Sprint 2026  ·  Track 1 (Q1.2)";
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: COL.paper },
  objects: [
    { text: { text: FOOTER, options: { x: 0.6, y: 7.0, w: 9, h: 0.3, fontSize: 10, color: COL.muted, fontFace: BODY } } },
    {
      placeholder: {
        options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9, fontSize: 30, bold: true, color: COL.ink, fontFace: HEAD, valign: "middle", align: "left" },
        text: "",
      },
    },
  ],
  slideNumber: { x: 12.3, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: COL.muted, fontFace: BODY },
});
pres.defineSlideMaster({
  title: "TITLE",
  background: { color: COL.paper }, // title and closing slides: no footer
  objects: [
    {
      placeholder: {
        options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9, fontSize: 30, bold: true, color: COL.ink, fontFace: HEAD, valign: "middle", align: "left" },
        text: "",
      },
    },
  ],
  slideNumber: { x: 12.3, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: COL.muted, fontFace: BODY },
});

function text(slide, value, opts) {
  slide.addText(value, Object.assign({ isTextBox: true, fontFace: BODY, color: COL.ink, fontSize: 16, valign: "top", margin: 0 }, opts));
}

function card(slide, x, y, w, h, fill) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill || COL.tint }, line: { color: fill || COL.tint } });
}

function numberBadge(slide, x, y, n, color) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: 0.55, h: 0.55, fill: { color }, line: { color } });
  text(slide, String(n), { x, y, w: 0.55, h: 0.55, fontSize: 18, bold: true, color: COL.paper, align: "center", valign: "middle" });
}

// 1. Title -------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "TITLE" });
  text(s, "AI COLLUSION RESEARCH SPRINT 2026  ·  TRACK 1: MARKETS AND COLLUSION  ·  QUESTION 1.2", { x: 0.6, y: 0.7, w: 12, h: 0.4, fontSize: 13, color: COL.muted, bold: true });
  text(s, "Who Carries the Cartel?", { x: 0.6, y: 1.5, w: 12, h: 1.2, fontSize: 54, bold: true, color: COL.ink, fontFace: HEAD });
  text(s, "LLM price collusion survives agent replacement through the inherited price history", { x: 0.6, y: 2.75, w: 11, h: 0.9, fontSize: 24, color: COL.muted });
  const stats = [
    ["6 of 6", "runs: the same model with the old price history keeps the cartel"],
    ["0.47–0.67", "profit-index loss without the history, by overpricing"],
    ["96%", "of rounds the OLMo-2 entrant repeats its last price"],
  ];
  stats.forEach(([big, small], i) => {
    const x = 0.6 + i * 4.1;
    text(s, big, { x, y: 4.3, w: 3.8, h: 0.8, fontSize: 36, bold: true, color: ACCENT, fontFace: HEAD });
    text(s, small, { x, y: 5.1, w: 3.6, h: 0.9, fontSize: 15, color: COL.ink });
  });
  text(s, "Supratik Bhowal  ·  IEM Kolkata  ·  with Apart Research", { x: 0.6, y: 6.6, w: 9, h: 0.4, fontSize: 15, color: COL.muted });
  s.addNotes(
    "Two AI agents that set prices for two competing firms often learn to keep prices high without being told to. " +
      "We ask what happens when one of them is replaced. Short answer: the cartel survives if the new agent reads the old price history.",
  );
}

// 2. The question --------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("If a firm replaces its AI pricing agent, does collusion end?", { placeholder: "title" });
  text(
    s,
    [
      { text: "AI agents that set prices can reach near-monopoly prices without talking to each other and without an instruction to collude.", options: { breakLine: true } },
      { text: " ", options: { breakLine: true, fontSize: 8 } },
      { text: "Replacing one agent is a natural remedy, and it also happens every time a firm changes its software vendor or model version.", options: { breakLine: true } },
      { text: " ", options: { breakLine: true, fontSize: 8 } },
      { text: "A prompted LLM agent has no memory outside its prompt. So the cartel must be carried by one of three things.", options: {} },
    ],
    { x: 0.6, y: 1.6, w: 5.6, h: 4.5, fontSize: 18, color: COL.ink2 },
  );
  const items = [
    ["The model", "the AI system itself (its weights)", ACCENT],
    ["The price history", "the last 30 rounds of prices that the new agent reads", ACCENT],
    ["The notes", "what the old agent wrote to itself each round", ACCENT],
  ];
  items.forEach(([head, body, color], i) => {
    const y = 1.6 + i * 1.6;
    card(s, 6.8, y, 5.9, 1.35);
    numberBadge(s, 7.05, y + 0.4, i + 1, color);
    text(s, head, { x: 7.85, y: y + 0.22, w: 4.6, h: 0.45, fontSize: 20, bold: true, fontFace: HEAD });
    text(s, body, { x: 7.85, y: y + 0.7, w: 4.6, h: 0.5, fontSize: 15, color: COL.muted });
  });
  s.addNotes("The answer tells a regulator which item a remedy must change: the agent, the data it inherits, or its memory.");
}

// 3. Market and agents ---------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("A simulated two-firm market with LLM pricing agents", { placeholder: "title" });
  text(
    s,
    [
      { text: "Market: ", options: { bold: true } },
      { text: "two firms sell similar products; buyers choose by price (logit Bertrand duopoly, Calvano et al. 2020).", options: { breakLine: true } },
      { text: " ", options: { breakLine: true, fontSize: 8 } },
      { text: "Agents: ", options: { bold: true } },
      { text: "each firm is an open LLM. Each round it sees the rules, its last 30 rounds and its notes, and answers with a price and new notes. The prompt never mentions collusion.", options: { breakLine: true } },
      { text: " ", options: { breakLine: true, fontSize: 8 } },
      { text: "Models: ", options: { bold: true } },
      { text: "Qwen2.5-7B incumbents; Mistral-7B and OLMo-2-7B as other-family entrants.", options: {} },
    ],
    { x: 0.6, y: 1.7, w: 6.2, h: 4.6, fontSize: 18, color: COL.ink2, paraSpaceAfter: 6 },
  );
  // price scale
  card(s, 7.3, 1.6, 5.4, 4.6);
  text(s, "Two benchmarks define the scale", { x: 7.6, y: 1.85, w: 4.9, h: 0.5, fontSize: 18, bold: true, fontFace: HEAD });
  s.addShape(pres.shapes.RECTANGLE, { x: 7.8, y: 3.25, w: 4.4, h: 0.22, fill: { color: COL.soft }, line: { color: COL.soft } });
  s.addShape(pres.shapes.OVAL, { x: 7.7, y: 3.16, w: 0.4, h: 0.4, fill: { color: COL.ink }, line: { color: COL.ink } });
  s.addShape(pres.shapes.OVAL, { x: 11.9, y: 3.16, w: 0.4, h: 0.4, fill: { color: ACCENT }, line: { color: ACCENT } });
  text(s, "Competitive (Nash)\nprice 1.473", { x: 7.5, y: 3.7, w: 2.2, h: 0.8, fontSize: 14, color: COL.ink, bold: true });
  text(s, "Monopoly\nprice 1.925", { x: 10.5, y: 3.7, w: 2.0, h: 0.8, fontSize: 14, color: ACCENT, bold: true, align: "right" });
  text(
    s,
    "Profit index and price index: 0 = competitive level, 1 = monopoly level. A price above the monopoly price gives a price index above 1 but a lower profit index.",
    { x: 7.6, y: 4.7, w: 4.9, h: 1.3, fontSize: 14, color: COL.muted },
  );
  s.addNotes("A profit index near 1 means the two agents behave like a cartel. We report both indices because they disagree when prices overshoot the monopoly price.");
}

// 4. Design --------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Copy every cartel into eight exactly paired worlds", { placeholder: "title" });
  const steps = [
    ["Phase 1", "Two Qwen2.5-7B agents play 100 rounds in 30–40 markets per run."],
    ["Keep cartels", "A market continues only if its profit index in rounds 50–99 is above 0.3."],
    ["Phase 2", "Each kept market is copied into 8 conditions and plays 100 more rounds."],
    ["Compare", "Same random seeds in every copy: differences come only from the replacement. Outcome: rounds 150–199."],
  ];
  steps.forEach(([head, body], i) => {
    const x = 0.6 + i * 3.1;
    card(s, x, 1.5, 2.9, 1.9);
    numberBadge(s, x + 0.2, 1.7, i + 1, COL.ink2);
    text(s, head, { x: x + 0.9, y: 1.78, w: 1.9, h: 0.4, fontSize: 17, bold: true, fontFace: HEAD });
    text(s, body, { x: x + 0.2, y: 2.4, w: 2.55, h: 1.0, fontSize: 14, color: COL.muted });
  });
  const conds = [
    ["Control", "no replacement"],
    ["Placebo", "incumbent told of a replacement; none happens"],
    ["Same + history", "new Qwen agent, reads the last 30 rounds"],
    ["Same, no history", "new Qwen agent, starts blank"],
    ["Same, notes only", "new Qwen agent, gets the old notes only"],
    ["Other + history", "Mistral-7B or OLMo-2-7B, reads the history"],
    ["Other, no history", "other family, starts blank"],
    ["Best-response bot", "maximizes only today's profit (negative control)"],
  ];
  conds.forEach(([head, body], i) => {
    const col = i % 4;
    const row = Math.floor(i / 4);
    const x = 0.6 + col * 3.1;
    const y = 3.75 + row * 1.5;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: 2.9, h: 1.3, rectRadius: 0.1, fill: { color: COL.paper }, line: { color: COL.soft, width: 1 } });
    text(s, head, { x: x + 0.2, y: y + 0.15, w: 2.5, h: 0.4, fontSize: 16, bold: true, color: COL.ink, fontFace: HEAD });
    text(s, body, { x: x + 0.2, y: y + 0.58, w: 2.5, h: 0.7, fontSize: 14, color: COL.muted });
  });
  s.addNotes("Six independent runs, hypotheses fixed in advance, 95% bootstrap intervals over markets. Runs without a stable cartel are reported too.");
}

// 5. Result 1 ------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Result 1: the price history carries the cartel", { placeholder: "title" });
  const labels = ["Control", "Placebo", "Same + history", "Same, notes only", "Same, no history", "Other + history", "Other, no history", "Best-response bot"];
  const values = [0.9, 0.884, 0.876, 0.63, 0.289, 0.199, 0.039, 0.023];
  s.addChart(pres.charts.BAR, [{ name: "Profit index, rounds 150–199", labels, values }], {
    x: 0.6, y: 1.45, w: 7.6, h: 5.3, barDir: "bar", catAxisOrientation: "maxMin",
    chartColors: [COL.ink, COL.bar, ACCENT, COL.bar, COL.bar, COL.bar, COL.bar, COL.bar],
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.000", dataLabelFontSize: 13, dataLabelColor: COL.ink, dataLabelFontFace: "+mn-lt",
    valAxisMinVal: 0, valAxisMaxVal: 1, valAxisLabelFormatCode: "0.0", valAxisLabelFontSize: 12, catAxisLabelFontSize: 14,
    valAxisLabelColor: COL.muted, catAxisLabelColor: COL.ink, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
    valGridLine: { color: "E5E7EB", size: 0.75 }, catGridLine: { style: "none" }, showLegend: false,
    showTitle: true, title: "Run 9: profit index after the replacement (29 markets)", titleFontSize: 15, titleColor: COL.ink, titleFontFace: "+mn-lt",
  });
  card(s, 8.6, 1.6, 4.1, 2.3);
  text(s, "6 of 6", { x: 8.85, y: 1.8, w: 3.7, h: 0.8, fontSize: 40, bold: true, color: ACCENT, fontFace: HEAD });
  text(s, "independent runs: the same model with the history stays at the cartel level; without it, profits fall far.", { x: 8.85, y: 2.65, w: 3.7, h: 1.2, fontSize: 15, color: COL.ink2 });
  card(s, 8.6, 4.15, 4.1, 2.55);
  text(s, "No notice needed", { x: 8.85, y: 4.35, w: 3.7, h: 0.45, fontSize: 18, bold: true, fontFace: HEAD });
  text(s, "In the run without a replacement notice the effect is the same (H1: 0.002). The old notes alone keep part of the cartel (H9: +0.342 over no history).", { x: 8.85, y: 4.85, w: 3.7, h: 1.8, fontSize: 15, color: COL.ink2 });
  s.addNotes("Profit index 0 = competitive, 1 = monopoly. 'Same + history' differs from no replacement by between -0.025 and +0.213 across the six runs.");
}

// 6. Result 2 ------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Result 2: without the history, prices overshoot", { placeholder: "title" });
  s.addImage({ path: path.join(FIG, "fig_trajectories.png"), x: 0.6, y: 1.5, w: 8.4, h: 3.02 });
  text(s, "Run 9, mean over 29 markets per condition. Left: profit index. Right: price index. Dashed line: the replacement at round 100.", { x: 0.6, y: 4.65, w: 8.4, h: 0.6, fontSize: 13, color: COL.muted });
  card(s, 9.4, 1.5, 3.3, 5.2);
  text(s, "1.314", { x: 9.65, y: 1.75, w: 2.9, h: 0.8, fontSize: 40, bold: true, color: ACCENT, fontFace: HEAD });
  text(s, "price index of the entrant without history in run 9 (above the monopoly level of 1)", { x: 9.65, y: 2.6, w: 2.85, h: 1.3, fontSize: 15, color: COL.ink2 });
  text(s, "A monitor that tracks only profits would call this the end of the cartel. Consumers still pay more than the monopoly price.", { x: 9.65, y: 4.1, w: 2.85, h: 2.3, fontSize: 15, color: COL.ink2 });
  text(
    s,
    "Price index of this entrant is above no replacement in 6 of 6 runs (interval above 0 in 5 of 6).",
    { x: 0.6, y: 5.45, w: 8.4, h: 0.8, fontSize: 16, color: COL.ink2, bold: true },
  );
  s.addNotes("The blank entrant has no anchor. It starts high and stays above the monopoly price, so both firms sell less. Only the best-response bot and the Mistral entrant reach competitive prices.");
}

// 7. Result 3 ------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Result 3: the new model's pricing style decides the outcome", { placeholder: "title" });
  const cols = [
    ["Mistral-7B entrant", "21.6–25.5%", "of rounds it repeats its last price", "Breaks the inherited cartel in 4 of 4 runs: profit index 0.55–0.78 below no replacement. It explores, and prices drift down.", COL.ink],
    ["OLMo-2-7B entrant", "96.3–96.8%", "of rounds it repeats its last price", "Keeps the inherited cartel in 2 of 2 runs. Typical note: “Maintain price at $1.93 as it consistently yields profit.”", ACCENT],
  ];
  cols.forEach(([head, big, small, body, color], i) => {
    const x = 0.6 + i * 6.2;
    card(s, x, 1.55, 5.9, 4.6);
    text(s, head, { x: x + 0.3, y: 1.8, w: 5.3, h: 0.5, fontSize: 22, bold: true, fontFace: HEAD });
    text(s, big, { x: x + 0.3, y: 2.45, w: 5.3, h: 0.95, fontSize: 44, bold: true, color, fontFace: HEAD });
    text(s, small, { x: x + 0.3, y: 3.4, w: 5.3, h: 0.4, fontSize: 15, color: COL.muted });
    text(s, body, { x: x + 0.3, y: 4.0, w: 5.3, h: 2.0, fontSize: 16, color: COL.ink2 });
  });
  text(s, "Qwen2.5-7B agents without a replacement repeat their price in 87.7–90.8% of rounds. The price-hold rate can be measured before a model is deployed.", { x: 0.6, y: 6.35, w: 12.1, h: 0.55, fontSize: 15, color: COL.ink2 });
  s.addNotes("'A different model' is not one treatment. A sticky model keeps the inherited prices by inertia; an exploring model drifts to competition.");
}

// 8. Result 4 ------------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Result 4: the surviving prices are anchored, not enforced", { placeholder: "title" });
  const steps = [
    ["Force a cut", "In a copy of the market, one firm's price is forced 10% down for one round."],
    ["Measure the reply", "Does the rival cut more than a profit-maximizing best response would? That excess is the signature of punishment."],
    ["Calibrate", "A myopic agent that cannot punish also follows cuts. Count punishment only above this myopic baseline."],
  ];
  steps.forEach(([head, body], i) => {
    const y = 1.55 + i * 1.6;
    card(s, 0.6, y, 6.4, 1.4);
    numberBadge(s, 0.85, y + 0.42, i + 1, COL.ink2);
    text(s, head, { x: 1.65, y: y + 0.18, w: 5.2, h: 0.4, fontSize: 18, bold: true, fontFace: HEAD });
    text(s, body, { x: 1.65, y: y + 0.6, w: 5.2, h: 0.75, fontSize: 14, color: COL.muted });
  });
  card(s, 7.4, 1.55, 5.3, 4.6);
  text(s, "After calibration", { x: 7.7, y: 1.8, w: 4.7, h: 0.45, fontSize: 18, bold: true, color: COL.ink, fontFace: HEAD });
  text(s, "0 of 13", { x: 7.7, y: 2.35, w: 4.7, h: 0.85, fontSize: 40, bold: true, color: ACCENT, fontFace: HEAD });
  text(s, "audit cells show punishment in each of runs 6, 7 and 8", { x: 7.7, y: 3.2, w: 4.7, h: 0.5, fontSize: 15, color: COL.ink });
  text(s, "1 of 15", { x: 7.7, y: 3.95, w: 4.7, h: 0.85, fontSize: 40, bold: true, color: ACCENT, fontFace: HEAD });
  text(s, "in run 9. The instructed trigger agent (positive control) is detected in runs 4 and 6–9.", { x: 7.7, y: 4.8, w: 4.7, h: 1.0, fontSize: 15, color: COL.ink });
  text(s, "Without calibration, 0–3 cells per run would look like punishment.", { x: 0.6, y: 6.35, w: 12.1, h: 0.5, fontSize: 15, color: COL.ink2, bold: true });
  s.addNotes("The inherited high prices persist because the agents anchor on what they see, not because they threaten a price war.");
}

// 9. Implications --------------------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "TITLE" });
  s.addText("What this means: govern the transcript, not only the agent", { placeholder: "title" });
  const items = [
    ["Competition authorities", "Replacing a colluding pricing system is not a remedy if the shared price history moves with the seat. Remove or redact the history and the notes."],
    ["Market monitors", "A fall in profits is not proof of competition. Compare prices with both the competitive and the monopoly benchmark."],
    ["Auditors", "Calibrate enforcement tests against agents that cannot punish, or ordinary price following looks like a cartel."],
    ["AI safety", "Coordination stored in shared memory, logs or transcripts can outlive the agents that created it."],
  ];
  items.forEach(([head, body], i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.6 + col * 6.2;
    const y = 1.6 + row * 2.6;
    card(s, x, y, 5.9, 2.3);
    text(s, head, { x: x + 0.3, y: y + 0.25, w: 5.3, h: 0.45, fontSize: 20, bold: true, color: ACCENT, fontFace: HEAD });
    text(s, body, { x: x + 0.3, y: y + 0.8, w: 5.3, h: 1.4, fontSize: 16, color: COL.ink });
  });
  s.addNotes("The unit of analysis moves from the agent to the agent and its context.");
}

// 10. Limits and next steps ----------------------------------------------------------------------
{
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addText("Limits, next steps and materials", { placeholder: "title" });
  card(s, 0.6, 1.55, 6.0, 4.9);
  text(s, "Limits", { x: 0.9, y: 1.8, w: 5.4, h: 0.45, fontSize: 20, bold: true, fontFace: HEAD });
  text(
    s,
    [
      { text: "One simulated market, one prompt, 7–14B open models.", options: { bullet: true, breakLine: true } },
      { text: "Only Qwen2.5-7B incumbents kept a stable cartel; two entrant families gave opposite results.", options: { bullet: true, breakLine: true } },
      { text: "The audit tests a one-round reply to a one-round cut.", options: { bullet: true, breakLine: true } },
      { text: "Runs 4–5 ran before the sprint start (disclosed).", options: { bullet: true } },
    ],
    { x: 0.9, y: 2.4, w: 5.4, h: 3.9, fontSize: 15, color: COL.ink2, paraSpaceAfter: 8 },
  );
  card(s, 6.9, 1.55, 5.8, 4.9);
  text(s, "Next steps", { x: 7.2, y: 1.8, w: 5.2, h: 0.45, fontSize: 20, bold: true, fontFace: HEAD });
  text(
    s,
    [
      { text: "More model families; test the price-hold rate as a predictor.", options: { bullet: true, breakLine: true } },
      { text: "Vary the inherited history from 0 to 30 rounds.", options: { bullet: true, breakLine: true } },
      { text: "Multi-round audits; remedies that redact shared memory.", options: { bullet: true } },
    ],
    { x: 7.2, y: 2.4, w: 5.2, h: 2.2, fontSize: 15, color: COL.ink2, paraSpaceAfter: 8 },
  );
  text(s, "Code, data and report:", { x: 7.2, y: 4.75, w: 5.2, h: 0.4, fontSize: 15, bold: true, color: COL.ink });
  text(s, [{ text: "github.com/SSCoderz2123/AI-Collusion-Research-Sprint", options: { hyperlink: { url: "https://github.com/SSCoderz2123/AI-Collusion-Research-Sprint" } } }], { x: 7.2, y: 5.15, w: 5.3, h: 0.4, fontSize: 14, color: ACCENT });
  s.addNotes("All numbers come from stored run data through the analysis code in the repository. The report lists every run, null results and failures.");
}

pres.writeFile({ fileName: OUT }).then((f) => console.log(`wrote ${f}`));
