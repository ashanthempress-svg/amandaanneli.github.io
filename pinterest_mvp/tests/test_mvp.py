import csv
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from pinterest_mvp.copy_generator import generate_pin_copy
from pinterest_mvp.queue_manager import build_publish_queue
from pinterest_mvp.winner_cloner import clone_winners


class TestPinterestMVP(unittest.TestCase):
    def test_generate_pin_copy_counts(self):
        data = generate_pin_copy("https://example.com", "balcony garden", "balcony garden ideas", 8, 4)
        self.assertEqual(len(data.titles), 8)
        self.assertEqual(len(data.descriptions), 4)
        self.assertIn("balcony garden ideas", [t.lower() for t in data.tags])

    def test_queue_builder(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "queue.csv"
            build_publish_queue(
                titles=["A", "B"],
                descriptions=["desc"],
                url="https://example.com",
                board="Board",
                publish_start=datetime.fromisoformat("2026-05-06T12:00:00"),
                interval_hours=12,
                output_path=out,
            )
            with out.open("r", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[1]["scheduled_time"], "2026-05-07T00:00:00")

    def test_clone_winners(self):
        with tempfile.TemporaryDirectory() as td:
            metrics = Path(td) / "metrics.csv"
            metrics.write_text("title,ctr,save_rate\nWinner,0.05,0.06\nLoser,0.01,0.02\n", encoding="utf-8")
            clones = clone_winners(metrics, 0.03, 0.05, 3)
            self.assertEqual(len(clones), 3)
            self.assertTrue(all("Winner" in c for c in clones))


if __name__ == "__main__":
    unittest.main()
