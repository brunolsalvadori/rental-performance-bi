# 04 — Dashboard

> Part 1 is reconstructed from my project notes. Part 2 quotes the actual request, translated from Portuguese.

## Part 1 — Production dashboard

### Goal
A dashboard the partners can open from WhatsApp on any phone, with no login and no app to install.

### Prompt
*Summary:* Make the dashboard work when opened from the iPhone Files app and from WhatsApp's built-in viewer. Right now some sections show up empty there.

### What came back
The diagnosis: those viewers silently block JavaScript, so any section drawn by a script stays blank, with no error and no fallback message.

### What I kept, changed or rejected
- **Changed — everything visible is pre-rendered.** A build step writes every KPI, chart (as inline SVG) and table straight into the HTML. JavaScript is kept only as an extra for table search and sorting.
- **Rejected for now — a month filter.** It caused repeated layout and calculation issues in the static setup. I set it aside rather than ship something unreliable.

## Part 2 — Public demo for this repository

### Goal
Show the product to people outside the operation without exposing any real figure, name or review.

### Prompt
> "For the cabin BI, you can use this HTML to create the evidence that's needed." (attached: the production dashboard)

### What came back
A rebuild of the production design (palette, typography, hero illustration, KPI cards, numbered sections) fed by the synthetic generator instead of real data: a financial view and a guest experience view, a unit filter, a table view, screenshots for the README and a page published on GitHub Pages.

### What I kept, changed or rejected
- **Kept — the design, not the data.** The layout came from the real dashboard. No real revenue, cost, loan, partner balance, name, review or listing detail was published.
- **Changed — no chart with two y-axes.** The production chart showing revenue in R$ and margin in % on two axes became two separate charts, which are easier to read correctly.
- **Changed — the demo renders with JavaScript.** Its audience opens it in a desktop or mobile browser, and the unit filter needs to recalculate every KPI. The production rule (pre-render everything) still applies to the partners' version.
- **Approved — publishing the demo on GitHub Pages**, so it opens from a link in the README and on LinkedIn.
</content>
</invoke>
