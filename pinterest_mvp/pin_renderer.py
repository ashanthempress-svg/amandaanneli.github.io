from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from PIL import Image, ImageDraw, ImageFont


PIN_SIZE = (1000, 1500)


def _load_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def _wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render_pins(titles: List[str], output_dir: Path, bg_color: str = "#F3E5D7", text_color: str = "#23150F") -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "render_manifest.csv"

    font_title = _load_font(64)
    font_sub = _load_font(34)

    with manifest_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["image_path", "title"])
        writer.writeheader()

        for idx, title in enumerate(titles, start=1):
            img = Image.new("RGB", PIN_SIZE, bg_color)
            draw = ImageDraw.Draw(img)

            lines = _wrap_text(draw, title, font_title, 840)
            y = 220
            for line in lines[:6]:
                draw.text((80, y), line, font=font_title, fill=text_color)
                y += 84

            draw.text((80, 1300), "Save for later", font=font_sub, fill=text_color)

            file_name = f"pin_{idx:03d}.png"
            image_path = output_dir / file_name
            img.save(image_path)
            writer.writerow({"image_path": str(image_path), "title": title})

    return manifest_path
