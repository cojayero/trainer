from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List

from app.core.models import VocabItem


BASE_DIR = Path(__file__).resolve().parents[2]
VOCAB_JSON_FILE = BASE_DIR / "app" / "data" / "vocab_n5.json"
VOCAB_CSV_FILE = BASE_DIR / "app" / "data" / "vocab_n5.csv"


def _load_from_json() -> List[VocabItem]:
    if not VOCAB_JSON_FILE.exists():
        return []

    raw = json.loads(VOCAB_JSON_FILE.read_text(encoding="utf-8"))
    return [
        VocabItem(
            id=item["id"],
            word_jp=item["word_jp"],
            reading=item["reading"],
            meaning_es=item["meaning_es"],
            pos=item.get("pos", ""),
            tags=item.get("tags", []),
        )
        for item in raw
    ]


def _load_from_csv() -> List[VocabItem]:
    if not VOCAB_CSV_FILE.exists():
        return []

    items: List[VocabItem] = []
    with VOCAB_CSV_FILE.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                item_id = int(row.get("id", "0") or 0)
            except ValueError:
                continue

            tags_raw = row.get("tags", "") or ""
            tags = [t.strip() for t in tags_raw.split(";") if t.strip()]

            items.append(
                VocabItem(
                    id=item_id,
                    word_jp=row.get("word_jp", ""),
                    reading=row.get("reading", ""),
                    meaning_es=row.get("meaning_es", ""),
                    pos=row.get("pos", ""),
                    tags=tags,
                )
            )

    return items


def load_vocab_items() -> List[VocabItem]:
    """Cargar vocabulario N5.

    Si existe vocab_n5.csv, se prioriza (permite un listado grande N5).
    En caso contrario, se usa vocab_n5.json como conjunto mínimo.
    """

    csv_items = _load_from_csv()
    if csv_items:
        return csv_items

    return _load_from_json()


def save_vocab_items(items: List[VocabItem]) -> None:
    """Guardar la lista completa de vocabulario en vocab_n5.csv.

    Si el fichero CSV no existe, se creará con encabezados estándar.
    """

    VOCAB_CSV_FILE.parent.mkdir(parents=True, exist_ok=True)

    with VOCAB_CSV_FILE.open("w", encoding="utf-8", newline="") as f:
        fieldnames = ["id", "word_jp", "reading", "meaning_es", "pos", "tags"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            writer.writerow(
                {
                    "id": item.id,
                    "word_jp": item.word_jp,
                    "reading": item.reading,
                    "meaning_es": item.meaning_es,
                    "pos": item.pos,
                    "tags": ";".join(item.tags),
                }
            )
