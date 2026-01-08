import random

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.core.grammar_repository import load_grammar_points, save_grammar_points
from app.core.srs import update_progress_for_item
from app.storage.settings import load_settings


class GrammarView(ttk.Frame):
    """Vista de gramática N5: lista + ejercicios simples.

    Ejercicios: se muestra una frase ejemplo y se pide al usuario
    escribir la partícula principal que se practica (は, が, を, に, で...).
    """

    def __init__(self, master: ttk.Frame) -> None:
        super().__init__(master)
        settings = load_settings()
        self.help_lang: str = (settings.help_language or "es").lower()
        self.points = load_grammar_points()
        self.current_index: int | None = None
        self.current_example: str | None = None

        self.title_label: ttk.Label | None = None
        self.desc_label: ttk.Label | None = None
        self.example_label: ttk.Label | None = None
        self.answer_entry: ttk.Entry | None = None
        self.feedback_label: ttk.Label | None = None

        self._create_widgets()

    def _create_widgets(self) -> None:
        if self.help_lang == "en":
            header_text = "文法N5 / Grammar N5"
        elif self.help_lang == "none":
            header_text = "文法N5"
        else:
            header_text = "文法N5 (Gramática N5)"

        header = ttk.Label(
            self,
            text=header_text,
            font=("Yu Gothic UI", 18, "bold"),
        )
        header.pack(side=TOP, pady=10)

        # Botón para añadir nuevo punto gramatical
        add_frame = ttk.Frame(self)
        add_frame.pack(fill=X, padx=10)

        if self.help_lang == "en":
            add_text = "文法ポイントを追加 / Add grammar point"
        elif self.help_lang == "none":
            add_text = "文法ポイントを追加"
        else:
            add_text = "文法ポイントを追加 / Añadir gramática"

        add_btn = ttk.Button(
            add_frame,
            text=add_text,
            bootstyle="info-outline",
            command=self._open_add_grammar_dialog,
        )
        add_btn.pack(side=RIGHT)

        if not self.points:
            if self.help_lang == "en":
                msg_text = "文法データがありません (no grammar data)"
            elif self.help_lang == "none":
                msg_text = "文法データがありません"
            else:
                msg_text = "文法データがありません (no hay datos de gramática)"

            msg = ttk.Label(
                self,
                text=msg_text,
                bootstyle="danger",
            )
            msg.pack(pady=20)
            return

        notebook = ttk.Notebook(self)
        notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        list_tab = ttk.Frame(notebook)
        exercise_tab = ttk.Frame(notebook)

        notebook.add(list_tab, text="一覧 / Lista")
        if self.help_lang == "en":
            exercise_label = "練習 / Practice"
        elif self.help_lang == "none":
            exercise_label = "練習"
        else:
            exercise_label = "練習 / Ejercicios"

        notebook.add(exercise_tab, text=exercise_label)

        self._build_list_tab(list_tab)
        self._build_exercise_tab(exercise_tab)

    def _build_list_tab(self, parent: ttk.Frame) -> None:
        tree = ttk.Treeview(
            parent,
            columns=("title", "desc", "note"),
            show="headings",
            height=10,
        )
        tree.heading("title", text="文法ポイント")
        tree.heading("desc", text="説明 (日本語)")
        tree.heading("note", text="Nota (español)")

        tree.column("title", width=80, anchor=CENTER)
        tree.column("desc", width=240)
        tree.column("note", width=260)

        for p in self.points:
            tree.insert("", END, values=(p.title_jp, p.description_simple_jp, p.note_es))

        tree.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    def _build_exercise_tab(self, parent: ttk.Frame) -> None:
        if self.help_lang == "en":
            info_text = "例文を読んで、使われている助詞を入力してください (type the particle)"
        elif self.help_lang == "none":
            info_text = "例文を読んで、使われている助詞を入力してください"
        else:
            info_text = "例文を読んで、使われている助詞を入力してください (escribe la partícula)"

        info = ttk.Label(
            parent,
            text=info_text,
            font=("Yu Gothic UI", 11),
        )
        info.pack(side=TOP, pady=5)

        self.title_label = ttk.Label(
            parent,
            text="",
            font=("Yu Gothic UI", 14, "bold"),
        )
        self.title_label.pack(pady=5)

        self.desc_label = ttk.Label(
            parent,
            text="",
            font=("Yu Gothic UI", 11),
            bootstyle="secondary",
            wraplength=500,
            justify=LEFT,
        )
        self.desc_label.pack(pady=5)

        self.example_label = ttk.Label(
            parent,
            text="",
            font=("Yu Gothic UI", 16),
        )
        self.example_label.pack(pady=10)

        if self.help_lang == "en":
            entry_help = "助詞をひらがなで入力してください (type the particle in hiragana):"
        elif self.help_lang == "none":
            entry_help = "助詞をひらがなで入力してください"
        else:
            entry_help = "助詞をひらがなで入力してください (escribe la partícula en hiragana):"

        entry_label = ttk.Label(
            parent,
            text=entry_help,
            font=("Yu Gothic UI", 10),
        )
        entry_label.pack()

        self.answer_entry = ttk.Entry(parent, width=10)
        self.answer_entry.pack(pady=5)

        button_frame = ttk.Frame(parent)
        button_frame.pack(pady=10)

        check_btn = ttk.Button(
            button_frame,
            text="答えを確認 / Comprobar",
            command=self._check_answer,
            bootstyle="success-outline",
        )
        check_btn.pack(side=LEFT, padx=5)

        next_btn = ttk.Button(
            button_frame,
            text="次へ / Siguiente",
            command=self._next_random_item,
            bootstyle="secondary-outline",
        )
        next_btn.pack(side=LEFT, padx=5)

        self.feedback_label = ttk.Label(
            parent,
            text="",
            font=("Yu Gothic UI", 11),
            bootstyle="secondary",
        )
        self.feedback_label.pack(pady=10)

        self._next_random_item()

        self.answer_entry.bind("<Return>", lambda _event: self._check_answer())

    # --- Diálogo para añadir gramática y frases de ejemplo ---

    def _open_add_grammar_dialog(self) -> None:
        dialog = ttk.Toplevel(self)
        dialog.title("文法ポイント追加 / Añadir gramática")

        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=BOTH, expand=YES)

        ttk.Label(frame, text="助詞・文法ポイント (ej. は, が):").grid(
            row=0, column=0, sticky=W, pady=2
        )
        title_var = ttk.StringVar()
        title_entry = ttk.Entry(frame, textvariable=title_var, width=10)
        title_entry.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="簡単な説明 (日本語):").grid(
            row=1, column=0, sticky=W, pady=2
        )
        desc_var = ttk.StringVar()
        desc_entry = ttk.Entry(frame, textvariable=desc_var, width=40)
        desc_entry.grid(row=1, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="Nota (español):").grid(row=2, column=0, sticky=W, pady=2)
        note_var = ttk.StringVar()
        note_entry = ttk.Entry(frame, textvariable=note_var, width=40)
        note_entry.grid(row=2, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="例文 (una por línea):").grid(
            row=3, column=0, sticky=NW, pady=2
        )
        examples_text = ttk.Text(frame, width=40, height=5)
        examples_text.grid(row=3, column=1, sticky=W, pady=2)

        info_label = ttk.Label(
            frame,
            text="",
            font=("Yu Gothic UI", 9),
            bootstyle="secondary",
        )
        info_label.grid(row=4, column=0, columnspan=2, sticky=W, pady=(4, 2))

        def on_save() -> None:
            title = title_var.get().strip()
            desc = desc_var.get().strip()
            note = note_var.get().strip()
            examples_raw = examples_text.get("1.0", "end").strip()
            examples = [
                line.strip() for line in examples_raw.splitlines() if line.strip()
            ]

            if not title or not desc or not examples:
                info_label.configure(
                    text="必須項目が足りません (faltan campos obligatorios)",
                    bootstyle="danger",
                )
                return

            from app.core.models import GrammarPoint

            next_id = max((p.id for p in self.points), default=0) + 1
            new_point = GrammarPoint(
                id=next_id,
                title_jp=title,
                description_simple_jp=desc,
                note_es=note,
                examples=examples,
            )

            self.points.append(new_point)
            save_grammar_points(self.points)

            info_label.configure(
                text="文法ポイントを保存しました (punto de gramática guardado)",
                bootstyle="success",
            )

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=8, sticky=E)

        save_btn = ttk.Button(
            button_frame,
            text="保存 / Guardar",
            bootstyle="success",
            command=on_save,
        )
        save_btn.pack(side=LEFT, padx=5)

        close_btn = ttk.Button(
            button_frame,
            text="閉じる / Cerrar",
            bootstyle="secondary",
            command=dialog.destroy,
        )
        close_btn.pack(side=LEFT, padx=5)

        title_entry.focus_set()

    def _next_random_item(self) -> None:
        if not self.points:
            return

        self.current_index = random.randrange(len(self.points))
        point = self.points[self.current_index]

        if not point.examples:
            self.current_example = None
        else:
            self.current_example = random.choice(point.examples)

        if self.title_label is not None:
            self.title_label.configure(text=f"文法ポイント: {point.title_jp}")

        if self.desc_label is not None:
            self.desc_label.configure(text=point.description_simple_jp)

        if self.example_label is not None:
            self.example_label.configure(text=self.current_example or "")

        if self.feedback_label is not None:
            self.feedback_label.configure(text="", bootstyle="secondary")

        if self.answer_entry is not None:
            self.answer_entry.delete(0, END)
            self.answer_entry.focus_set()

    def _check_answer(self) -> None:
        if (
            self.current_index is None
            or self.answer_entry is None
            or self.feedback_label is None
        ):
            return

        point = self.points[self.current_index]
        user_answer = self.answer_entry.get().strip()
        correct = point.title_jp.strip()

        is_correct = user_answer == correct

        if is_correct:
            if self.help_lang == "en":
                fb_text = f"正解です！ ({correct})"
            elif self.help_lang == "none":
                fb_text = f"正解です！ ({correct})"
            else:
                fb_text = f"正解です！ ({correct}) - {point.note_es}"

            self.feedback_label.configure(
                text=fb_text,
                bootstyle="success",
            )
        else:
            if self.help_lang == "en":
                fb_text = f"ちがいます… 正しい助詞: {correct}"
            elif self.help_lang == "none":
                fb_text = f"ちがいます… 正しい助詞: {correct}"
            else:
                fb_text = f"ちがいます… 正しい助詞: {correct}  ({point.note_es})"

            self.feedback_label.configure(
                text=fb_text,
                bootstyle="danger",
            )

        update_progress_for_item(
            user_id=1,
            item_type="grammar",
            item_id=point.id,
            correct=is_correct,
        )
