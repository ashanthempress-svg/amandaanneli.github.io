from __future__ import annotations

import csv
from pathlib import Path
from typing import List


def clone_winners(metrics_file: Path, ctr_threshold: float, save_threshold: float, variants: int) -> List[str]:
    winners: List[str] = []

    with metrics_file.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ctr = float(row.get("ctr", 0) or 0)
            save_rate = float(row.get("save_rate", 0) or 0)
            title = row.get("title", "").strip()
            if title and ctr >= ctr_threshold and save_rate >= save_threshold:
                winners.append(title)

    clones: List[str] = []
    for title in winners:
        for i in range(1, variants + 1):
            clones.append(f"{title} | Variation {i}")

    return clones
