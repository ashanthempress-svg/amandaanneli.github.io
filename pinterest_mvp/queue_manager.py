from __future__ import annotations

import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List


def build_publish_queue(
    titles: List[str],
    descriptions: List[str],
    url: str,
    board: str,
    publish_start: datetime,
    interval_hours: int,
    output_path: Path,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["scheduled_time", "board", "title", "description", "url", "status"],
        )
        writer.writeheader()

        for i, title in enumerate(titles):
            description = descriptions[i % len(descriptions)] if descriptions else ""
            scheduled_time = publish_start + timedelta(hours=i * interval_hours)
            writer.writerow(
                {
                    "scheduled_time": scheduled_time.isoformat(),
                    "board": board,
                    "title": title,
                    "description": description,
                    "url": url,
                    "status": "queued",
                }
            )

    return output_path
