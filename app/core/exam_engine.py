from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List

from app.core.kanji_repository import load_kanji_items
from app.core.grammar_repository import load_grammar_points
from app.core.vocab_repository import load_vocab_items


@dataclass
class Question:
    id: int
    text: str
    choices: List[str]
    correct_index: int
    source_type: str  # "vocab" | "kanji" | "grammar"
    source_item_id: int


def _build_vocab_questions() -> List[Question]:
    questions: List[Question] = []
    vocab_items = load_vocab_items()
    if len(vocab_items) < 2:
        return questions

    # Usamos el significado principal en español como respuesta
    all_meanings = [v.meaning_es for v in vocab_items]

    q_id = 1
    for item in vocab_items:
        correct = item.meaning_es
        # Generar distractores distintos
        distractors_pool = [m for m in all_meanings if m != correct]
        if len(distractors_pool) < 3:
            continue
        distractors = random.sample(distractors_pool, 3)

        choices = distractors + [correct]
        random.shuffle(choices)
        correct_index = choices.index(correct)

        text = f"【単語】日本語の意味を選んでください：{item.word_jp}（よみ：{item.reading}）"

        questions.append(
            Question(
                id=q_id,
                text=text,
                choices=choices,
                correct_index=correct_index,
                source_type="vocab",
                source_item_id=item.id,
            )
        )
        q_id += 1

    return questions


def _build_kanji_questions(start_id: int) -> List[Question]:
    questions: List[Question] = []
    kanji_items = load_kanji_items()
    if len(kanji_items) < 2:
        return questions

    all_meanings = [k.meanings_es[0] for k in kanji_items if k.meanings_es]

    q_id = start_id
    for item in kanji_items:
        if not item.meanings_es:
            continue
        correct = item.meanings_es[0]
        distractors_pool = [m for m in all_meanings if m != correct]
        if len(distractors_pool) < 3:
            continue
        distractors = random.sample(distractors_pool, 3)

        choices = distractors + [correct]
        random.shuffle(choices)
        correct_index = choices.index(correct)

        readings = ", ".join(item.readings)
        text = f"【漢字】この漢字の意味を選んでください：{item.kanji}（よみ：{readings}）"

        questions.append(
            Question(
                id=q_id,
                text=text,
                choices=choices,
                correct_index=correct_index,
                source_type="kanji",
                source_item_id=item.id,
            )
        )
        q_id += 1

    return questions


def _build_grammar_questions(start_id: int) -> List[Question]:
    questions: List[Question] = []
    points = load_grammar_points()
    if len(points) < 2:
        return questions

    all_titles = [p.title_jp for p in points]

    q_id = start_id
    for p in points:
        if not p.examples:
            continue
        example = random.choice(p.examples)
        correct = p.title_jp

        distractors_pool = [t for t in all_titles if t != correct]
        if len(distractors_pool) < 3:
            continue
        distractors = random.sample(distractors_pool, 3)

        choices = distractors + [correct]
        random.shuffle(choices)
        correct_index = choices.index(correct)

        text = f"【文法】この文で使われている助詞を選んでください：{example}"

        questions.append(
            Question(
                id=q_id,
                text=text,
                choices=choices,
                correct_index=correct_index,
                source_type="grammar",
                source_item_id=p.id,
            )
        )
        q_id += 1

    return questions


def generate_exam(total_questions: int = 20) -> List[Question]:
    """Generar un conjunto mezclado de preguntas para el examen simulado.

    Intenta mezclar vocabulario, kanji y gramática de forma equilibrada.
    """

    vocab_q = _build_vocab_questions()
    kanji_q = _build_kanji_questions(start_id=len(vocab_q) + 1)
    grammar_q = _build_grammar_questions(start_id=len(vocab_q) + len(kanji_q) + 1)

    pool: List[Question] = vocab_q + kanji_q + grammar_q
    random.shuffle(pool)

    if not pool:
        return []

    return pool[: min(total_questions, len(pool))]
