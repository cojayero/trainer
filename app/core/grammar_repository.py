from __future__ import annotations

import json
from pathlib import Path
from typing import List

from app.core.models import GrammarPoint


BASE_DIR = Path(__file__).resolve().parents[2]
GRAMMAR_FILE = BASE_DIR / "app" / "data" / "grammar_n5.json"


def load_grammar_points() -> List[GrammarPoint]:
    if not GRAMMAR_FILE.exists():
        return []

    raw = json.loads(GRAMMAR_FILE.read_text(encoding="utf-8"))
    return [
        GrammarPoint(
            id=item["id"],
            title_jp=item["title_jp"],
            description_simple_jp=item["description_simple_jp"],
            note_es=item.get("note_es", ""),
            examples=item.get("examples", []),
        )
        for item in raw
    ]


def save_grammar_points(points: List[GrammarPoint]) -> None:
    """Guardar la lista completa de puntos gramaticales en grammar_n5.json."""

    GRAMMAR_FILE.parent.mkdir(parents=True, exist_ok=True)

    raw = []
    for p in points:
        raw.append(
            {
                "id": p.id,
                "title_jp": p.title_jp,
                "description_simple_jp": p.description_simple_jp,
                "note_es": p.note_es,
                "examples": list(p.examples),
            }
        )

    GRAMMAR_FILE.write_text(
        json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8"
    )
