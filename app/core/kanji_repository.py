from __future__ import annotations

import json
from pathlib import Path
from typing import List

from app.core.models import KanjiItem


BASE_DIR = Path(__file__).resolve().parents[2]
KANJI_FILE = BASE_DIR / "app" / "data" / "kanji_n5.json"


def load_kanji_items() -> List[KanjiItem]:
    if not KANJI_FILE.exists():
        return []

    raw = json.loads(KANJI_FILE.read_text(encoding="utf-8"))
    return [
        KanjiItem(
            id=item["id"],
            kanji=item["kanji"],
            readings=item.get("readings", []),
            meanings_es=item.get("meanings_es", []),
            examples=item.get("examples", []),
        )
        for item in raw
    ]


def save_kanji_items(items: List[KanjiItem]) -> None:
    """Guardar la lista completa de kanji en el fichero JSON.

    Se sobrescribe kanji_n5.json con todos los elementos actuales.
    """

    KANJI_FILE.parent.mkdir(parents=True, exist_ok=True)

    data: list[dict] = []
    for item in items:
        data.append(
            {
                "id": item.id,
                "kanji": item.kanji,
                "readings": list(item.readings),
                "meanings_es": list(item.meanings_es),
                "examples": list(item.examples),
            }
        )

    KANJI_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
