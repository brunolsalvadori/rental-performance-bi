# 02 — Data model

> Reconstructed from my project notes. The prompt is summarized, not verbatim.

## Goal
Turn scattered sources into a model the dashboard can be rebuilt from every month, without manual fixes.

## Prompt
*Summary:* Read the spreadsheet's revenue, costs and acquisition tabs, plus the Airbnb earnings reports and listing page, and structure them into the data the dashboard needs.

## What came back
A data block with monthly revenue and costs, cost entries, revenue entries by channel, booking statistics, listing metrics and loan totals.

## What I kept, changed or rejected
- **Changed — the partner balance is read, never recomputed.** The partners keep the agreed balance in the spreadsheet, and recomputing it from individual transfers risks a different number. The dashboard reads that field directly.
- **Changed — new months are appended, history is frozen.** Recomputing every month from raw entries brought back date typos that had already been corrected in earlier builds. Each update now adds only the new month.
- **Accepted a limit — reviews come in manually.** The listing page loads dynamically, so only aggregate metrics (rating, review count, highlights) can be read automatically. Review texts and dates are provided by hand.
- **For this public repository** the same logic is expressed as five synthetic tables (bookings, reviews, costs, financing, partner ledger), documented in [docs/data-dictionary.md](../docs/data-dictionary.md).
</content>
</invoke>
