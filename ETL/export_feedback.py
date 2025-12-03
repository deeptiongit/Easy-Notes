from __future__ import annotations

import argparse
import csv
import os
from datetime import datetime

from database.database import FeedbackSessionLocal, init_feedback_db
from database.models import FeedbackData


def parse_args():
    parser = argparse.ArgumentParser(description="Export feedback data to CSV using local DB")

    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Limit number of rows (0 = no limit)"
    )
    parser.add_argument(
        "--since",
        help="ISO datetime to filter rows after (e.g. 2024-01-01T00:00:00)"
    )
    parser.add_argument(
        "--out",
        default="feedback_export.csv",
        help="Destination CSV file path",
    )

    return parser.parse_args()


def export_to_csv(out_path: str, limit: int = 0, since: str | None = None) -> int:
    # Create output directory if needed
    out_dir = os.path.dirname(out_path)
    os.makedirs(out_dir if out_dir else ".", exist_ok=True)

    init_feedback_db()

    db = FeedbackSessionLocal()

    try:
        query = db.query(FeedbackData).order_by(FeedbackData.date.asc())

        # Filter by datetime
        if since:
            try:
                dt = datetime.fromisoformat(since)
                query = query.filter(FeedbackData.date >= dt)
            except ValueError:
                print(f"WARN: Invalid --since value '{since}'. Expected ISO format. Ignoring filter.")

        # Apply limit
        if limit > 0:
            query = query.limit(limit)

        rows = query.all()

        # Write CSV
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "document_id", "ocr_text", "doc_type", "date"])

            for r in rows:
                writer.writerow([
                    r.id,
                    r.document_id,
                    r.ocr_text,
                    r.doc_type,
                    r.date.isoformat() if r.date else ""
                ])

        print(f"✔ Wrote {len(rows)} rows to: {out_path}")
        return 0

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return 1

    finally:
        db.close()


def main():
    args = parse_args()
    return export_to_csv(args.out, args.limit, args.since)


if __name__ == "__main__":
    raise SystemExit(main())
