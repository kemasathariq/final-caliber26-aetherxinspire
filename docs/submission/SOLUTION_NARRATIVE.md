# INSpire Solution Narrative

**Status:** DRAFT v0.1. Story for the final presentation. Every claim below is either an OBSERVATION from the supplied synthetic dataset, a PROPOSED capability, or marked as not yet shown. Replace PROPOSED items by IMPLEMENTED results only after they are built and validated. The official brief was inspected on 2026-11-04 (`docs/case/CALIBER 2026 - Final Case Brief.pdf`). Open the deck with the brief's title and problem sentence, and keep the umbrella label "integrated supply-chain" second.

## 1. One-sentence story

INSpire is Spare Part Intelligence and Inventory Optimization built as an integrated supply-chain tool: it forecasts where evidence allows, recommends reorder, hold, reduce or monitor actions, and it helps planners decide which parts need attention by testing stock rules against recorded consumption and procurement lead time, and it says clearly where the records, including logistics records, are too thin to decide.

## 2. Narrative arc

**1. The situation (OBSERVATION).** The supplied dataset covers 7,481 spare parts at one plant over 17 months. For 3,656 Stock Items, recorded Min/Max values sit away from recorded stock: 1,380 hold stock above recorded Max and 504 below recorded Min.

**2. What makes the decision hard (OBSERVATION).** Most parts move rarely: 1,220 of 1,930 issued parts were issued in a single month. Maintenance work links to issues for only 20.5 percent of orders. Procurement records show promised dates, not receipts, and 46.7 percent of rows are exact copies. Stock has no date.

**3. What a careless answer would do.** Fit a forecast to sparse history and print a precise reorder point, or call raw stock gaps "excess" and attach a saving. The data cannot support either.

**4. What INSpire does instead (PROPOSED).** It sorts parts into three evidence tiers, 665 policy-testable, 1,265 demand-evidenced, 5,551 with no recorded consumption. For the 665 it replays recorded and proposed Min-Max rules under identical conditions, in two demand views and two procurement views, and shows where the answer depends on the view. Elsewhere it gives descriptive alerts or abstains.

**5. Six capabilities, one workflow (PROPOSED).** Stockout risk, overstock risk, reorder recommendation, slow-moving alert, dynamic inventory parameters, and cost-risk scenarios appear as one chain from data to human decision. An assistant explains stored results, and a planner approves, rejects or defers.

**6. Trust by design.** Simulated results are never called actual stockouts. Parameters are candidates, never optimal. Money appears only with an approved cost set and the word "scenario".

**7. What it needs next.** The case owner's definition of Min/Max, a stock date, receipts, cost parameters. With them, the same structure turns candidates into validated recommendations.

**Key questions (brief p5, p6, must be addressed in the deck).** KQ1: demand predictability for irregular parts is improved by classifying demand, forecasting only where evidence supports it and stating why not elsewhere. KQ2: inventory is optimised dynamically by comparing recorded and proposed Min-Max rules under identical conditions, with stock-level what-if scenarios and cost-risk scenarios under stated assumptions.

## 3. Key messages

| Message | Status |
| --- | --- |
| Recorded stock rules and recorded consumption do not line up in this dataset | OBSERVATION, with caveat that Min/Max meaning is unconfirmed |
| Demand is mostly sparse, so abstention is a feature | OBSERVATION |
| Policy testing runs on 665 materials, with proposed parameters on 228 | IMPLEMENTED, run `RUN-277fc4b966e6`. Simulated, not observed |
| Results are scenarios, not predictions | Design principle |
| Supply-chain scope was investigated: the data has no location, receipt or freight records, so transportation optimisation is a roadmap with a stated data list | OBSERVATION and assessment |
| Cost-risk comparison is ready for assumptions, not for claims | Design principle |

## 4. Claims the team must not make

- A percentage reduction in stockouts or inventory, or any saving.
- "Optimal" parameters.
- Any statement about Chandra Asri performance.
- That recorded Min/Max is wrong, or that stock is "excess".
- That a simulated shortfall happened.
- Any transport time, route, freight cost or logistics saving, or that transportation causes a stock problem.
- That promised procurement interval is delivery or transport time.
- That the official brief asks for transportation. It does not. Supply context answers its "procurement lead time and supply variability" point.
- That Mitem and Mplan show future spare part demand. The case pack diagram says they hold no parts.
- That a part is "obsolete" or "dead stock". Only "potentially obsolete candidate" and "non-moving by recorded issues" (D-21).
- That the solution is machine learning beyond what is built (D-22).

## 5. Questions the jury may ask, and honest answers

| Question | Answer |
| --- | --- |
| Why not a forecasting model for every part? | 1,475 of 1,930 issued parts have two or fewer active months. Fitting would invent precision. We abstain and say why |
| How do you know the recommendations are good? | We can verify the model, not validate it. We test against recorded issues in a held-out replay and show sensitivity. Validation needs stock history and receipts |
| Where is the saving? | Not claimed. Cost parameters are not in the data. Brilian's scenarios show cost differences under stated assumptions |
| Why two demand scenarios? | 863 Movement lines are exact copies of another line. We cannot tell if they are errors, so we show both |
| Why is there no transportation optimisation in a supply-chain solution? | We checked. The six files have one plant, one movement type, one supplier per material and no location, receipt or freight field. A model would need invented routes and costs. We show supply context now and list the data that unlocks allocation and transfers |
| What is your data? | Six supplied workbooks documented as synthetic |
