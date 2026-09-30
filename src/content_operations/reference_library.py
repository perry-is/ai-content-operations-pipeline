"""Synthetic reference library used for linking and overlap checks."""

import json
import re
from pathlib import Path


def load_library(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def recommend(source: dict, library: list[dict]) -> list[dict]:
    source_text = " ".join((source.get("topic", ""), source.get("canonical_title", ""), source.get("transcript", ""), source.get("show_notes", "")))
    terms = {word for word in re.findall(r"[a-z0-9]+", source_text.lower()) if len(word) >= 4}
    ranked = []
    for item in library:
        item_terms = {word for value in item.get("search_terms", []) for word in re.findall(r"[a-z0-9]+", value.lower())}
        overlap = terms.intersection(item_terms)
        if overlap:
            ranked.append((len(overlap), item))
    return [item for _, item in sorted(ranked, key=lambda pair: (-pair[0], pair[1]["content_id"]))[:3]]
