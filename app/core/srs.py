from __future__ import annotations

from datetime import datetime
from typing import List

from app.core.models import UserProgress, ItemType
from app.storage.progress import load_all_progress, save_all_progress


def _update_single_progress(item: UserProgress, correct: bool, now: datetime) -> None:
    """Actualizar un registro de progreso según si la respuesta ha sido correcta.

    Lógica SRS simplificada basada solo en nivel y fecha.
    """

    if correct:
        item.srs_level = min(item.srs_level + 1, 4)
        item.right_count += 1
    else:
        item.srs_level = max(item.srs_level - 1, 0)
        item.wrong_count += 1

    item.last_review = now


def update_progress_for_item(
    user_id: int,
    item_type: ItemType,
    item_id: int,
    correct: bool,
    now: datetime | None = None,
) -> None:
    """Actualizar (o crear) el progreso para un ítem concreto.

    - `user_id`: identificador del usuario (por ahora 1 en modo local).
    - `item_type`: "kana", "vocab", "kanji" o "grammar".
    - `item_id`: identificador interno del ítem.
    - `correct`: True si la respuesta fue correcta.
    """

    if now is None:
        now = datetime.now()

    items: List[UserProgress] = load_all_progress()

    match = next(
        (p for p in items if p.user_id == user_id and p.item_type == item_type and p.item_id == item_id),
        None,
    )

    if match is None:
        match = UserProgress(
            user_id=user_id,
            item_type=item_type,
            item_id=item_id,
        )
        items.append(match)

    _update_single_progress(match, correct=correct, now=now)

    save_all_progress(items)
