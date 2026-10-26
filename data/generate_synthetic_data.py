"""
Synthetic data generator for rental-performance-bi.

Creates a fictional dataset for "Serra Cabins Co.", a two-unit short-term
rental operation in a mountain region of Brazil. Every number is generated
from the assumptions below; none comes from a real business.

Usage:
    python data/generate_synthetic_data.py

Output (data/synthetic/):
    bookings.csv, reviews.csv, costs.csv, financing.csv, partner_ledger.csv

Standard library only. A fixed seed makes the output reproducible.
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
START = date(2025, 1, 1)
END = date(2026, 9, 30)
OUT_DIR = Path(__file__).parent / "synthetic"

# --- Assumptions (all fictional) -------------------------------------------
UNITS = {
    "CABIN": {"opens": date(2025, 1, 1), "base_rate": 520.0},
    "CHALET_A": {"opens": date(2026, 3, 1), "base_rate": 610.0},
}
HIGH_SEASON_MONTHS = {6, 7, 8}          # mountain winter
HIGH_SEASON_UPLIFT = 0.40                # +40% nightly rate
WEEKEND_UPLIFT = 0.20                    # Friday and Saturday nights
CHANNELS = [("Airbnb", 0.78, 0.03), ("Direct", 0.15, 0.0), ("Booking", 0.07, 0.15)]
CLEANING_FEE = 150.0                     # charged to the guest per stay
CANCELLATION_RATE = 0.06
REVIEW_RATE = 0.72                       # share of completed stays reviewed
RETURNING_GUEST_RATE = 0.12
ORIGIN_STATES = [("SP", 0.55), ("RJ", 0.18), ("MG", 0.20), ("Other", 0.07)]
REVIEW_THEMES = ["view", "comfort", "cleanliness", "host", "location",
                 "fireplace", "access road", "wifi", "kitchen", "silence"]

MONTHLY_FIXED_COSTS = {                  # per open unit, BRL
    "utilities": 380.0,
    "internet": 120.0,
    "maintenance": 300.0,
    "supplies": 180.0,
    "insurance_and_taxes": 140.0,
}
CLEANING_COST_PER_STAY = 130.0
LAUNDRY_COST_PER_STAY = 45.0

LOAN = {"unit": "CHALET_A", "principal": 280000.0, "monthly_rate": 0.011,
        "months": 120, "first_payment": date(2026, 4, 1)}
PARTNERS = ["Partner A", "Partner B"]


def weighted(options):
    r, acc = random.random(), 0.0
    for value, weight, *rest in options:
        acc += weight
        if r <= acc:
            return (value, *rest) if rest else value
    last = options[-1]
    return (last[0], *last[2:]) if len(last) > 2 else last[0]


def nightly_rate(unit, night):
    rate = UNITS[unit]["base_rate"]
    if night.month in HIGH_SEASON_MONTHS:
        rate *= 1 + HIGH_SEASON_UPLIFT
    if night.weekday() in (4, 5):
        rate *= 1 + WEEKEND_UPLIFT
    return rate


def start_probability(day):
    p = 0.55 if day.weekday() == 4 else 0.12
    if day.month in HIGH_SEASON_MONTHS:
        p += 0.25
    return min(p, 0.95)


def month_starts(first, last):
    d = date(first.year, first.month, 1)
    while d <= last:
        yield d
        d = date(d.year + (d.month // 12), d.month % 12 + 1, 1)


def generate_bookings():
    bookings, seq = [], 1
    for unit, cfg in UNITS.items():
        day = cfg["opens"]
        while day <= END:
            if random.random() < start_probability(day):
                nights = random.choice([2, 2, 2, 3, 3, 4, 5]) if day.weekday() == 4 \
                    else random.choice([1, 2, 2, 3, 4])
                check_out = day + timedelta(days=nights)
                if check_out > END + timedelta(days=1):
                    break
                channel, fee_rate = weighted(CHANNELS)
                lodging = sum(nightly_rate(unit, day + timedelta(days=i)) for i in range(nights))
                gross = round(lodging + CLEANING_FEE, 2)
                platform_fee = round(gross * fee_rate, 2)
                cancelled = random.random() < CANCELLATION_RATE
                bookings.append({
                    "booking_id": f"B{seq:05d}",
                    "unit": unit,
                    "channel": channel,
                    "booking_date": (day - timedelta(days=random.randint(2, 75))).isoformat(),
                    "check_in": day.isoformat(),
                    "check_out": check_out.isoformat(),
                    "nights": nights,
                    "guests": random.choice([2, 2, 2, 3, 4]),
                    "gross_revenue": gross if not cancelled else 0.0,
                    "cleaning_fee": CLEANING_FEE if not cancelled else 0.0,
                    "platform_fee": platform_fee if not cancelled else 0.0,
                    "net_revenue": round(gross - platform_fee, 2) if not cancelled else 0.0,
                    "status": "cancelled" if cancelled else "completed",
                    "returning_guest": random.random() < RETURNING_GUEST_RATE,
                    "origin_state": weighted(ORIGIN_STATES),
                })
                seq += 1
                day = check_out if not cancelled else day + timedelta(days=1)
            else:
                day += timedelta(days=1)
    return bookings


def generate_reviews(bookings):
    reviews = []
    for b in bookings:
        if b["status"] != "completed" or random.random() > REVIEW_RATE:
            continue
        def score():
            return random.choices([5, 4, 3], weights=[82, 15, 3])[0]
        sub = {k: score() for k in ["cleanliness", "accuracy", "check_in",
                                    "communication", "location", "value"]}
        overall = round(sum(sub.values()) / len(sub))
        check_out = date.fromisoformat(b["check_out"])
        reviews.append({
            "booking_id": b["booking_id"],
            "unit": b["unit"],
            "review_date": (check_out + timedelta(days=random.randint(1, 10))).isoformat(),
            "overall": overall,
            **sub,
            "host_response_minutes": random.choice([5, 10, 15, 30, 45, 60, 120]),
            "themes": ";".join(random.sample(REVIEW_THEMES, k=random.randint(1, 3))),
        })
    return reviews


def generate_costs(bookings):
    costs = []
    for unit, cfg in UNITS.items():
        for m in month_starts(cfg["opens"], END):
            for category, amount in MONTHLY_FIXED_COSTS.items():
                costs.append({"month": m.isoformat(), "unit": unit, "category": category,
                              "amount": round(amount * random.uniform(0.85, 1.2), 2)})
            stays = sum(1 for b in bookings if b["unit"] == unit and b["status"] == "completed"
                        and b["check_in"][:7] == m.isoformat()[:7])
            costs.append({"month": m.isoformat(), "unit": unit, "category": "cleaning",
                          "amount": round(stays * CLEANING_COST_PER_STAY, 2)})
            costs.append({"month": m.isoformat(), "unit": unit, "category": "laundry",
                          "amount": round(stays * LAUNDRY_COST_PER_STAY, 2)})
    return costs


def generate_financing():
    p, r, n = LOAN["principal"], LOAN["monthly_rate"], LOAN["months"]
    payment = p * r / (1 - (1 + r) ** -n)          # constant installment
    rows, balance = [], p
    for i, m in enumerate(month_starts(LOAN["first_payment"], END), start=1):
        interest = balance * r
        principal = payment - interest
        balance -= principal
        rows.append({"month": m.isoformat(), "unit": LOAN["unit"], "installment": i,
                     "payment": round(payment, 2), "interest": round(interest, 2),
                     "principal": round(principal, 2), "balance": round(balance, 2)})
    return rows


def generate_partner_ledger():
    rows = []
    for m in month_starts(START, END):
        for partner in PARTNERS:
            if m < UNITS["CHALET_A"]["opens"] and m >= date(2025, 6, 1) and random.random() < 0.5:
                rows.append({"date": m.isoformat(), "partner": partner, "type": "capital_contribution",
                             "amount": round(random.uniform(8000, 25000), -2)})
            if m.month % 3 == 0:
                rows.append({"date": m.isoformat(), "partner": partner, "type": "distribution",
                             "amount": round(-random.uniform(3000, 9000), -2)})
        if random.random() < 0.25:
            rows.append({"date": m.isoformat(), "partner": random.choice(PARTNERS),
                         "type": "expense_paid_on_behalf", "amount": round(random.uniform(300, 2500), 2)})
    return rows


def write_csv(name, rows):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / name, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def main():
    random.seed(SEED)
    bookings = generate_bookings()
    write_csv("bookings.csv", bookings)
    write_csv("reviews.csv", generate_reviews(bookings))
    write_csv("costs.csv", generate_costs(bookings))
    write_csv("financing.csv", generate_financing())
    write_csv("partner_ledger.csv", generate_partner_ledger())


if __name__ == "__main__":
    main()
