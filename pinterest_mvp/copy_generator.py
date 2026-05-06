from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List


TITLE_PATTERNS = [
    "{keyword}: {benefit}",
    "{number} {keyword} tips for {audience}",
    "How to {outcome} with {keyword}",
    "{keyword} checklist: {benefit}",
    "Easy {keyword} ideas for {audience}",
]

DESCRIPTION_PATTERNS = [
    "Save this for later: {topic} with practical steps and beginner-friendly ideas.",
    "Looking for {keyword}? This guide shows a simple path to {outcome}.",
    "Pin this if you want {benefit} without overwhelm.",
    "A quick read on {topic}, including tools, timing, and easy wins.",
    "Use this as your go-to reference for {keyword} this season.",
]


@dataclass
class PinCopy:
    url: str
    topic: str
    keyword: str
    titles: List[str]
    descriptions: List[str]
    tags: List[str]

    def to_dict(self) -> dict:
        return asdict(self)


def _dedupe(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for item in items:
        key = item.lower().strip()
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def generate_pin_copy(url: str, topic: str, keyword: str, n_titles: int = 10, n_descriptions: int = 5) -> PinCopy:
    benefit = f"better {topic} results"
    audience = "beginners"
    outcome = f"get started with {topic}"

    raw_titles = []
    for i in range(n_titles * 2):
        pattern = TITLE_PATTERNS[i % len(TITLE_PATTERNS)]
        title = pattern.format(
            keyword=keyword.title(),
            benefit=benefit,
            number=5 + (i % 7),
            audience=audience,
            outcome=outcome,
        )
        raw_titles.append(title)

    raw_desc = []
    for i in range(n_descriptions * 2):
        pattern = DESCRIPTION_PATTERNS[i % len(DESCRIPTION_PATTERNS)]
        desc = pattern.format(topic=topic, keyword=keyword, outcome=outcome, benefit=benefit)
        raw_desc.append(desc)

    titles = _dedupe(raw_titles)
    while len(titles) < n_titles:
        titles.append(f"{keyword.title()} idea #{len(titles)+1}")
    titles = titles[:n_titles]

    descriptions = _dedupe(raw_desc)
    while len(descriptions) < n_descriptions:
        descriptions.append(f"Helpful {topic} idea #{len(descriptions)+1}.")
    descriptions = descriptions[:n_descriptions]

    tags = _dedupe([
        keyword,
        topic,
        f"{topic} tips",
        f"{keyword} ideas",
        "pinterest marketing",
        "content strategy",
    ])

    return PinCopy(url=url, topic=topic, keyword=keyword, titles=titles, descriptions=descriptions, tags=tags)
