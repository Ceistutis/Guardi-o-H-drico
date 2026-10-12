"""Série estática reproduzível, independente do volume da sessão."""
import csv
from datetime import date, timedelta
from io import StringIO
import random
from app.core.config import SEED


def example_history() -> list[dict]:
    rng = random.Random(SEED)
    return [{"Data": date(2026, 10, 5) + timedelta(days=i),
             "Volume (L)": round(rng.uniform(180, 310), 1)} for i in range(7)]


def filter_history(start: date, end: date) -> list[dict]:
    return [row for row in example_history() if start <= row["Data"] <= end]


def history_csv(rows: list[dict]) -> bytes:
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=["Data", "Volume (L)"], delimiter=";")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8-sig")
