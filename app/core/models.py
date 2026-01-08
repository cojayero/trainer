from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Literal


@dataclass
class VocabItem:
    id: int
    word_jp: str
    reading: str
    meaning_es: str
    pos: str
    tags: List[str] = field(default_factory=list)


@dataclass
class KanjiItem:
    id: int
    kanji: str
    readings: List[str]
    meanings_es: List[str]
    examples: List[str] = field(default_factory=list)


@dataclass
class GrammarPoint:
    id: int
    title_jp: str
    description_simple_jp: str
    note_es: str
    examples: List[str] = field(default_factory=list)


ItemType = Literal["vocab", "kana", "kanji", "grammar"]


@dataclass
class UserProgress:
    user_id: int
    item_type: ItemType
    item_id: int
    srs_level: int = 0
    last_review: Optional[datetime] = None
    right_count: int = 0
    wrong_count: int = 0


@dataclass
class Settings:
    theme: str = "flatly"
    help_language: str = "es"  # es/en/none
    difficulty: str = "normal"  # easy/normal/hard


@dataclass
class StudySession:
    id: int
    session_type: Literal["exam"]
    start_time: datetime
    end_time: datetime
    correct_count: int
    total_questions: int
