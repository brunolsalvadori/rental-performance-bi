"""
Builds dashboard/index.html from the synthetic CSVs.

Usage:
    python data/generate_synthetic_data.py
    python dashboard/build_dashboard.py

The script reads data/synthetic/*.csv, embeds the rows as JSON into
dashboard/template.html and writes dashboard/index.html. All KPIs are
computed in the browser, so the unit filter recalculates every view.

Standard library only.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "synthetic"
TEMPLATE = Path(__file__).parent / "template.html"
OUTPUT = Path(__file__).parent / "index.html"

NUMERIC = {
    "bookings.csv": {"nights": int, "guests": int, "gross_revenue": float, "cleaning_fee": float,
                     "platform_fee": float, "net_revenue": float},
    "reviews.csv": {"overall": int, "cleanliness": int, "accuracy": int, "check_in": int,
                    "communication": int, "location": int, "value": int,
                    "host_response_minutes": int},
    "costs.csv": {"amount": float},
    "financing.csv": {"installment": int, "payment": float, "interest": float,
                      "principal": float, "balance": float},
    "partner_ledger.csv": {"amount": float},
}


def load(name):
    path = DATA_DIR / name
    if not path.exists():
        raise SystemExit(f"Missing {path}. Run: python data/generate_synthetic_data.py")
    casts = NUMERIC.get(name, {})
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for col, cast in casts.items():
                row[col] = cast(row[col])
            if "returning_guest" in row:
                row["returning_guest"] = row["returning_guest"] == "True"
            rows.append(row)
    return rows


def main():
    data = {
        "company": "Serra Cabins Co.",
        "bookings": load("bookings.csv"),
        "reviews": load("reviews.csv"),
        "costs": load("costs.csv"),
        "financing": load("financing.csv"),
        "partnerLedger": load("partner_ledger.csv"),
    }
    html = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    OUTPUT.write_text(html.replace("/*__DATA__*/null", payload), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
