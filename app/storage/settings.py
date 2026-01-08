from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from app.core.models import Settings


BASE_DIR = Path(__file__).resolve().parents[2]
SETTINGS_FILE = BASE_DIR / "settings.json"


def load_settings() -> Settings:
    if not SETTINGS_FILE.exists():
        return Settings()

    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        return Settings(**data)
    except Exception:
        # Si hay cualquier problema, devolver ajustes por defecto
        return Settings()


def save_settings(settings: Settings) -> None:
    data = {
        "theme": settings.theme,
        "help_language": settings.help_language,
        "difficulty": settings.difficulty,
    }
    SETTINGS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
