# 03 — KPIs

> Reconstructed from my project notes and the production dashboard. The prompt is summarized, not verbatim.

## Goal
Define each KPI with a formula the partners would accept without debate.

## Prompt
*Summary:* Propose the headline KPIs and their formulas for profitability, occupancy and guest experience, using only what the data can support.

## What came back
A KPI set for profitability, occupancy and guest experience, each with a formula.

## What I kept, changed or rejected
- **Changed — costs split into operating and improvement.** One-off investments in the property (furniture, a water filter, glass for the hot tub) are kept apart from running costs, so they do not distort the operating margin. Margin is computed on operating costs only, and improvements are shown as investment.
- **Changed — bookings are labelled as an estimate where they are one.** The earnings report gives nights and average stay, not a booking count. Bookings are derived as nights ÷ average stay, and the dashboard says so in a footnote rather than presenting it as a literal count.
- **Kept — off-platform stays counted separately.** Direct bookings are added on top of platform numbers and shown as such, so nobody double counts.
- **For this public repository** the KPI set was extended to the standard short-term rental metrics (ADR, RevPAR, NOI, debt service coverage) with formulas in [docs/kpi-definitions.md](../docs/kpi-definitions.md).
</content>
</invoke>
