# Data dictionary

All tables are synthetic. Currency: BRL. Dates: ISO 8601.

## bookings.csv
| Column | Type | Description |
|---|---|---|
| booking_id | text | Unique booking id |
| unit | text | CABIN or CHALET_A |
| channel | text | Airbnb, Direct or Booking |
| booking_date | date | Date the booking was made |
| check_in / check_out | date | Stay dates (check_out is exclusive) |
| nights | int | Nights booked |
| guests | int | Number of guests |
| gross_revenue | number | Lodging + cleaning fee paid by the guest |
| cleaning_fee | number | Cleaning fee included in gross_revenue |
| platform_fee | number | Fee kept by the channel |
| net_revenue | number | gross_revenue - platform_fee |
| status | text | completed or cancelled (revenue = 0 when cancelled) |
| returning_guest | bool | Guest stayed before |
| origin_state | text | Guest home state |

## reviews.csv
| Column | Type | Description |
|---|---|---|
| booking_id | text | Booking reviewed |
| unit | text | Unit reviewed |
| review_date | date | Date of the review |
| overall | int 1-5 | Overall rating |
| cleanliness, accuracy, check_in, communication, location, value | int 1-5 | Sub-scores |
| host_response_minutes | int | Host response time during the stay |
| themes | text | Semicolon-separated topics mentioned |

## costs.csv
| Column | Type | Description |
|---|---|---|
| month | date | First day of the month |
| unit | text | Unit charged |
| category | text | utilities, internet, maintenance, supplies, insurance_and_taxes, cleaning, laundry |
| amount | number | Cost in the month |

## financing.csv
| Column | Type | Description |
|---|---|---|
| month | date | Installment month |
| unit | text | Unit financed |
| installment | int | Installment number |
| payment | number | Constant installment (interest + principal) |
| interest / principal | number | Split of the payment |
| balance | number | Outstanding balance after payment |

## partner_ledger.csv
| Column | Type | Description |
|---|---|---|
| date | date | Entry month |
| partner | text | Partner A or Partner B |
| type | text | capital_contribution, distribution, expense_paid_on_behalf |
| amount | number | Positive = money in from the partner; negative = money out to the partner |
