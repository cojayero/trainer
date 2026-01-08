from __future__ import annotations

from datetime import datetime

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.core.exam_engine import Question, generate_exam
from app.storage.settings import load_settings
from app.core.models import StudySession
from app.storage.sessions import append_session


class ExamView(ttk.Frame):
    """Vista de examen simulado N5.

    - Genera un examen de preguntas mezcladas (vocab, kanji, gramática).
    - Permite responder en formato test (elección múltiple).
    - Al final muestra puntuación y tiempo empleado.
    """

    def __init__(self, master: ttk.Frame) -> None:
        super().__init__(master)
        self.settings = load_settings()
        self.help_lang: str = (self.settings.help_language or "es").lower()
        self.questions: list[Question] = []
        self.current_index: int | None = None
        self.selected_var = ttk.IntVar(value=-1)
        self.start_time: datetime | None = None
        self.correct_count: int = 0
        self.answers: list[int] = []  # índice elegido por el usuario

        self.question_label: ttk.Label | None = None
        self.options_frame: ttk.Frame | None = None
        self.status_label: ttk.Label | None = None
        self.result_label: ttk.Label | None = None

        self._create_widgets()

    def _create_widgets(self) -> None:
        if self.help_lang == "en":
            header_text = "模擬テスト / Mock exam"
        elif self.help_lang == "none":
            header_text = "模擬テスト"
        else:
            header_text = "模擬テスト (Examen simulado)"

        header = ttk.Label(
            self,
            text=header_text,
            font=("Yu Gothic UI", 18, "bold"),
        )
        header.pack(side=TOP, pady=10)

        if self.help_lang == "en":
            info_text = "語彙・漢字・文法の混合問題です。難易度により問題数が変わります。"
        elif self.help_lang == "none":
            info_text = "語彙・漢字・文法の混合問題です。"
        else:
            info_text = "語彙・漢字・文法の混合問題です。難易度により問題数が変わります。"

        info = ttk.Label(
            self,
            text=info_text,
            font=("Yu Gothic UI", 11),
        )
        info.pack(side=TOP, pady=5)

        control_frame = ttk.Frame(self)
        control_frame.pack(pady=5)

        if self.help_lang == "en":
            start_text = "テスト開始 / Start exam"
        elif self.help_lang == "none":
            start_text = "テスト開始"
        else:
            start_text = "テスト開始 / Iniciar examen"

        start_btn = ttk.Button(
            control_frame,
            text=start_text,
            bootstyle="primary",
            command=self._start_exam,
        )
        start_btn.pack(side=LEFT, padx=5)

        self.status_label = ttk.Label(
            self,
            text="",
            font=("Yu Gothic UI", 10),
            bootstyle="secondary",
        )
        self.status_label.pack(pady=5)

        self.question_label = ttk.Label(
            self,
            text="",
            font=("Yu Gothic UI", 14),
            wraplength=700,
            justify=LEFT,
        )
        self.question_label.pack(padx=10, pady=10, anchor=NW)

        self.options_frame = ttk.Frame(self)
        self.options_frame.pack(padx=20, pady=5, anchor=NW)

        nav_frame = ttk.Frame(self)
        nav_frame.pack(pady=10)

        if self.help_lang == "en":
            next_text = "答えを送信 / Next"
            finish_text = "テスト終了 / Finish"
        elif self.help_lang == "none":
            next_text = "答えを送信"
            finish_text = "テスト終了"
        else:
            next_text = "答えを送信 / Siguiente"
            finish_text = "テスト終了 / Finalizar"

        self.next_button = ttk.Button(
            nav_frame,
            text=next_text,
            bootstyle="success-outline",
            command=self._submit_and_next,
            state=DISABLED,
        )
        self.next_button.pack(side=LEFT, padx=5)

        self.finish_button = ttk.Button(
            nav_frame,
            text=finish_text,
            bootstyle="secondary-outline",
            command=self._finish_exam,
            state=DISABLED,
        )
        self.finish_button.pack(side=LEFT, padx=5)

        self.result_label = ttk.Label(
            self,
            text="",
            font=("Yu Gothic UI", 11),
            bootstyle="secondary",
            justify=LEFT,
            wraplength=700,
        )
        self.result_label.pack(padx=10, pady=10, anchor=NW)

    # Lógica del examen

    def _start_exam(self) -> None:
        difficulty = (self.settings.difficulty or "normal").lower()
        if difficulty == "easy":
            total_questions = 10
        elif difficulty == "hard":
            total_questions = 30
        else:
            total_questions = 20

        self.questions = generate_exam(total_questions=total_questions)
        self.answers = []
        self.correct_count = 0
        self.current_index = 0 if self.questions else None
        self.start_time = datetime.now() if self.questions else None

        if not self.questions:
            if self.status_label is not None:
                self.status_label.configure(
                    text="問題を生成できませんでした (no se han podido generar preguntas)",
                    bootstyle="danger",
                )
            return

        if self.status_label is not None:
            self.status_label.configure(
                text=f"問題数：{len(self.questions)}問",
                bootstyle="info",
            )

        if self.result_label is not None:
            self.result_label.configure(text="", bootstyle="secondary")

        self.next_button.configure(state=NORMAL)
        self.finish_button.configure(state=NORMAL)

        self._show_current_question()

    def _show_current_question(self) -> None:
        if self.current_index is None or self.current_index >= len(self.questions):
            return

        q = self.questions[self.current_index]

        if self.question_label is not None:
            self.question_label.configure(text=f"Q{self.current_index + 1}. {q.text}")

        # Limpiar opciones anteriores
        for child in self.options_frame.winfo_children():
            child.destroy()

        self.selected_var.set(-1)

        for i, choice in enumerate(q.choices):
            rb = ttk.Radiobutton(
                self.options_frame,
                text=choice,
                variable=self.selected_var,
                value=i,
                bootstyle="info-toolbutton",
            )
            rb.pack(anchor=NW, pady=2)

    def _submit_and_next(self) -> None:
        if self.current_index is None:
            return

        selected = self.selected_var.get()
        if selected == -1:
            # Nada seleccionado
            if self.status_label is not None:
                if self.help_lang == "en":
                    warn_text = "選択肢を一つ選んでください (choose an option)"
                elif self.help_lang == "none":
                    warn_text = "選択肢を一つ選んでください"
                else:
                    warn_text = "選択肢を一つ選んでください (selecciona una opción)"

                self.status_label.configure(
                    text=warn_text,
                    bootstyle="warning",
                )
            return

        q = self.questions[self.current_index]
        self.answers.append(selected)

        if selected == q.correct_index:
            self.correct_count += 1

        # Siguiente pregunta o finalizar
        self.current_index += 1
        if self.current_index >= len(self.questions):
            self._finish_exam()
        else:
            if self.status_label is not None:
                self.status_label.configure(
                    text=f"Q{self.current_index}/{len(self.questions)}",
                    bootstyle="secondary",
                )
            self._show_current_question()

    def _finish_exam(self) -> None:
        if not self.questions:
            return

        total = len(self.questions)
        now = datetime.now()
        elapsed_sec = 0
        if self.start_time is not None:
            elapsed = now - self.start_time
            elapsed_sec = int(elapsed.total_seconds())

        score_pct = int(self.correct_count * 100 / total)

        # Registrar sesión de examen en el historial
        if self.start_time is not None:
            session = StudySession(
                id=0,
                session_type="exam",
                start_time=self.start_time,
                end_time=now,
                correct_count=self.correct_count,
                total_questions=total,
            )
            append_session(session)

        if self.help_lang == "en":
            summary_lines = [
                f"結果 / Result: {self.correct_count} / {total} 正解 ({score_pct}%)",
                f"時間 / Time: {elapsed_sec} 秒",
                "",
                "間違えた問題 / Incorrect questions:",
            ]
        elif self.help_lang == "none":
            summary_lines = [
                f"結果: {self.correct_count} / {total} 正解 ({score_pct}%)",
                f"時間: {elapsed_sec} 秒",
                "",
                "間違えた問題:",
            ]
        else:
            summary_lines = [
                f"結果 / Resultado: {self.correct_count} / {total} 正解 ({score_pct}%)",
                f"時間 / Tiempo: {elapsed_sec} 秒 (aprox.)",
                "",
                "間違えた問題 / Preguntas falladas:",
            ]

        for idx, (q, ans) in enumerate(zip(self.questions, self.answers), start=1):
            if ans != q.correct_index:
                correct_text = q.choices[q.correct_index]
                user_text = q.choices[ans] if 0 <= ans < len(q.choices) else "(sin respuesta)"
                if self.help_lang == "en":
                    line = (
                        f"Q{idx}: {q.text}\n  あなたの答え / Your answer: {user_text}\n  正解 / Correct: {correct_text}\n"
                    )
                elif self.help_lang == "none":
                    line = (
                        f"Q{idx}: {q.text}\n  あなたの答え: {user_text}\n  正解: {correct_text}\n"
                    )
                else:
                    line = (
                        f"Q{idx}: {q.text}\n  あなたの答え / Tu respuesta: {user_text}\n  正解 / Correcta: {correct_text}\n"
                    )

                summary_lines.append(line)

        if self.result_label is not None:
            self.result_label.configure(
                text="\n".join(summary_lines),
                bootstyle="info",
            )

        # Desactivar navegación
        self.next_button.configure(state=DISABLED)
        self.finish_button.configure(state=DISABLED)

        if self.status_label is not None:
            if self.help_lang == "en":
                end_text = "テスト終了 (exam finished)"
            elif self.help_lang == "none":
                end_text = "テスト終了"
            else:
                end_text = "テスト終了 (examen finalizado)"

            self.status_label.configure(
                text=end_text,
                bootstyle="success",
            )
