# KPI definitions

Lodging revenue = gross_revenue - cleaning_fee (completed bookings only).
Available nights = days the unit was open in the period.

| KPI | Formula | Why it matters |
|---|---|---|
| Occupancy rate | nights sold / available nights | Demand health by season |
| ADR | lodging revenue / nights sold | Pricing power |
| RevPAR | lodging revenue / available nights | Combines price and occupancy |
| Net revenue by channel | sum(net_revenue) by channel | True value of each channel after fees |
| NOI | sum(net_revenue) - sum(costs) | Operating profit per unit |
| Debt service coverage | NOI / sum(financing.payment) | Can the unit pay its loan? Target > 1.2 |
| Cost per occupied night | sum(costs) / nights sold | Efficiency of operations |
| Partner balance | contributions + expenses paid on behalf - distributions, per partner | Basis for settlements |
| Average overall rating | mean(reviews.overall) | Headline guest satisfaction |
| Share of 5-star reviews | reviews with overall = 5 / all reviews | Platform ranking driver |
| Review rate | reviews / completed bookings | Engagement after the stay |
| Median host response time | median(host_response_minutes) | Communication quality |
| Returning guest rate | completed bookings with returning_guest / completed bookings | Loyalty |
| Cancellation rate | cancelled / all bookings | Revenue risk |
| Lead time | mean(check_in - booking_date) | Planning horizon for pricing |
| Length of stay | mean(nights) | Cleaning and pricing strategy |
