from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from copy_generator import generate_pin_copy
from queue_manager import build_publish_queue
from winner_cloner import clone_winners


OUTPUT_DIR = Path("pinterest_mvp/output")
COPY_FILE_DEFAULT = OUTPUT_DIR / "pin_copy.json"


def cmd_generate_copy(args: argparse.Namespace) -> None:
    pin_copy = generate_pin_copy(
        url=args.url,
        topic=args.topic,
        keyword=args.keyword,
        n_titles=args.n_titles,
        n_descriptions=args.n_descriptions,
    )
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = Path(args.out_file)
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(pin_copy.to_dict(), f, ensure_ascii=False, indent=2)
    print(f"Saved copy to {out_file}")


def _load_copy(copy_file: Path) -> dict:
    with copy_file.open("r", encoding="utf-8") as f:
        return json.load(f)


def cmd_render(args: argparse.Namespace) -> None:
    data = _load_copy(Path(args.copy_file))
    try:
        from pin_renderer import render_pins
    except ModuleNotFoundError as exc:
        if exc.name == "PIL":
            raise SystemExit(
                "Rendering requires Pillow. Install with: pip install -r pinterest_mvp/requirements.txt"
            )
        raise

    manifest = render_pins(
        titles=data["titles"],
        output_dir=OUTPUT_DIR,
        bg_color=args.bg_color,
        text_color=args.text_color,
    )
    print(f"Rendered pins. Manifest: {manifest}")


def cmd_queue(args: argparse.Namespace) -> None:
    data = _load_copy(Path(args.copy_file))
    publish_start = datetime.fromisoformat(args.publish_start)
    queue_path = build_publish_queue(
        titles=data["titles"],
        descriptions=data["descriptions"],
        url=data["url"],
        board=args.board,
        publish_start=publish_start,
        interval_hours=args.interval_hours,
        output_path=Path(args.out_file),
    )
    print(f"Queue saved to {queue_path}")


def cmd_clone_winners(args: argparse.Namespace) -> None:
    clones = clone_winners(
        metrics_file=Path(args.metrics_file),
        ctr_threshold=args.ctr_threshold,
        save_threshold=args.save_threshold,
        variants=args.variants,
    )
    out = {"titles": clones}
    out_file = Path(args.out_file)
    with out_file.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(clones)} cloned titles to {out_file}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pinterest MVP toolkit")
    sub = parser.add_subparsers(required=True)

    g = sub.add_parser("generate-copy")
    g.add_argument("--url", required=True)
    g.add_argument("--topic", required=True)
    g.add_argument("--keyword", required=True)
    g.add_argument("--n-titles", type=int, default=10)
    g.add_argument("--n-descriptions", type=int, default=5)
    g.add_argument("--out-file", default=str(COPY_FILE_DEFAULT))
    g.set_defaults(func=cmd_generate_copy)

    r = sub.add_parser("render")
    r.add_argument("--copy-file", default=str(COPY_FILE_DEFAULT))
    r.add_argument("--bg-color", default="#F3E5D7")
    r.add_argument("--text-color", default="#23150F")
    r.set_defaults(func=cmd_render)

    q = sub.add_parser("queue")
    q.add_argument("--copy-file", default=str(COPY_FILE_DEFAULT))
    q.add_argument("--board", required=True)
    q.add_argument("--publish-start", required=True, help="ISO datetime, e.g. 2026-05-06T12:00:00")
    q.add_argument("--interval-hours", type=int, default=12)
    q.add_argument("--out-file", default=str(OUTPUT_DIR / "publish_queue.csv"))
    q.set_defaults(func=cmd_queue)

    c = sub.add_parser("clone-winners")
    c.add_argument("--metrics-file", required=True)
    c.add_argument("--ctr-threshold", type=float, default=0.03)
    c.add_argument("--save-threshold", type=float, default=0.05)
    c.add_argument("--variants", type=int, default=5)
    c.add_argument("--out-file", default=str(OUTPUT_DIR / "cloned_copy.json"))
    c.set_defaults(func=cmd_clone_winners)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
