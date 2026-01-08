from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from app.core.models import UserProgress


BASE_DIR = Path(__file__).resolve().parents[2]
PROGRESS_FILE = BASE_DIR / "progress.json"
_DATE_FMT = "%Y-%m-%dT%H:%M:%S"


def _serialize_progress_item(p: UserProgress) -> Dict:
    return {
        "user_id": p.user_id,
        "item_type": p.item_type,
        "item_id": p.item_id,
        "srs_level": p.srs_level,
        "last_review": p.last_review.strftime(_DATE_FMT) if p.last_review else None,
        "right_count": p.right_count,
        "wrong_count": p.wrong_count,
    }


def _deserialize_progress_item(data: Dict) -> UserProgress:
    last_review_raw = data.get("last_review")
    last_review = (
        datetime.strptime(last_review_raw, _DATE_FMT) if last_review_raw else None
    )
    return UserProgress(
        user_id=data["user_id"],
        item_type=data["item_type"],
        item_id=data["item_id"],
        srs_level=data.get("srs_level", 0),
        last_review=last_review,
        right_count=data.get("right_count", 0),
        wrong_count=data.get("wrong_count", 0),
    )


def load_all_progress() -> List[UserProgress]:
    if not PROGRESS_FILE.exists():
        return []

    try:
        raw = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        return [_deserialize_progress_item(item) for item in raw]
    except Exception:
        return []


def save_all_progress(items: List[UserProgress]) -> None:
    raw = [_serialize_progress_item(p) for p in items]
    PROGRESS_FILE.write_text(
        json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8"
    )
