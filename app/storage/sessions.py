from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from app.core.models import StudySession


BASE_DIR = Path(__file__).resolve().parents[2]
SESSIONS_FILE = BASE_DIR / "sessions.json"
_DATE_FMT = "%Y-%m-%dT%H:%M:%S"


def _serialize_session(s: StudySession) -> Dict:
    return {
        "id": s.id,
        "session_type": s.session_type,
        "start_time": s.start_time.strftime(_DATE_FMT),
        "end_time": s.end_time.strftime(_DATE_FMT),
        "correct_count": s.correct_count,
        "total_questions": s.total_questions,
    }


def _deserialize_session(data: Dict) -> StudySession:
    return StudySession(
        id=data.get("id", 0),
        session_type=data.get("session_type", "exam"),
        start_time=datetime.strptime(data["start_time"], _DATE_FMT),
        end_time=datetime.strptime(data["end_time"], _DATE_FMT),
        correct_count=data.get("correct_count", 0),
        total_questions=data.get("total_questions", 0),
    )


def load_sessions() -> List[StudySession]:
    if not SESSIONS_FILE.exists():
        return []

    try:
        raw = json.loads(SESSIONS_FILE.read_text(encoding="utf-8"))
        return [_deserialize_session(item) for item in raw]
    except Exception:
        return []


def save_sessions(sessions: List[StudySession]) -> None:
    raw = [_serialize_session(s) for s in sessions]
    SESSIONS_FILE.write_text(
        json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def append_session(session: StudySession) -> None:
    sessions = load_sessions()
    # Asignar id incremental sencillo
    next_id = max((s.id for s in sessions), default=0) + 1
    session.id = next_id
    sessions.append(session)
    save_sessions(sessions)
