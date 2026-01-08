import random

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.core.kanji_repository import load_kanji_items, save_kanji_items
from app.core.models import KanjiItem
from app.core.srs import update_progress_for_item
from app.storage.settings import load_settings


class KanjiView(ttk.Frame):
    """Vista de práctica de kanji N5 (lista + tarjetas)."""

    def __init__(self, master: ttk.Frame) -> None:
        super().__init__(master)
        settings = load_settings()
        self.help_lang: str = (settings.help_language or "es").lower()
        self.items = load_kanji_items()
        self.current_index: int | None = None

        self.list_tree: ttk.Treeview | None = None

        self.kanji_label: ttk.Label | None = None
        self.readings_label: ttk.Label | None = None
        self.answer_entry: ttk.Entry | None = None
        self.feedback_label: ttk.Label | None = None

        self._create_widgets()

    def _create_widgets(self) -> None:
        if self.help_lang == "en":
            header_text = "漢字N5 / Kanji N5"
        elif self.help_lang == "none":
            header_text = "漢字N5"
        else:
            header_text = "漢字N5 (Kanji N5)"

        header = ttk.Label(
            self,
            text=header_text,
            font=("Yu Gothic UI", 18, "bold"),
        )
        header.pack(side=TOP, pady=10)

        # Botón para añadir nuevos kanji
        add_frame = ttk.Frame(self)
        add_frame.pack(fill=X, padx=10)

        if self.help_lang == "en":
            add_text = "新しい漢字を追加 / Add kanji"
        elif self.help_lang == "none":
            add_text = "新しい漢字を追加"
        else:
            add_text = "新しい漢字を追加 / Añadir kanji"

        add_btn = ttk.Button(
            add_frame,
            text=add_text,
            bootstyle="info-outline",
            command=self._open_add_kanji_dialog,
        )
        add_btn.pack(side=RIGHT)

        if not self.items:
            if self.help_lang == "en":
                msg_text = "漢字データがありません (no kanji data)"
            elif self.help_lang == "none":
                msg_text = "漢字データがありません"
            else:
                msg_text = "漢字データがありません (no hay datos de kanji)"

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
        flashcard_tab = ttk.Frame(notebook)

        notebook.add(list_tab, text="一覧 / Lista")
        notebook.add(flashcard_tab, text="カード練習 / Tarjetas")

        self._build_list_tab(list_tab)
        self._build_flashcard_tab(flashcard_tab)

    def _build_list_tab(self, parent: ttk.Frame) -> None:
        self.list_tree = ttk.Treeview(
            parent,
            columns=("kanji", "readings", "meanings"),
            show="headings",
            height=10,
        )
        self.list_tree.heading("kanji", text="漢字")
        self.list_tree.heading("readings", text="よみかた")
        self.list_tree.heading("meanings", text="意味 (español)")

        self.list_tree.column("kanji", width=80, anchor=CENTER)
        self.list_tree.column("readings", width=160)
        self.list_tree.column("meanings", width=240)

        self.list_tree.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        self._refresh_list_tree()

    def _refresh_list_tree(self) -> None:
        if self.list_tree is None:
            return

        for row in self.list_tree.get_children():
            self.list_tree.delete(row)

        for item in self.items:
            readings = ", ".join(item.readings)
            meanings = ", ".join(item.meanings_es)
            self.list_tree.insert("", END, values=(item.kanji, readings, meanings))

    def _build_flashcard_tab(self, parent: ttk.Frame) -> None:
        if self.help_lang == "en":
            info_text = "カード練習：漢字 → 意味 (meaning)"
        elif self.help_lang == "none":
            info_text = "カード練習：漢字 → 意味"
        else:
            info_text = "カード練習：漢字 → 意味 (español)"

        info = ttk.Label(
            parent,
            text=info_text,
            font=("Yu Gothic UI", 12),
        )
        info.pack(side=TOP, pady=5)

        self.kanji_label = ttk.Label(
            parent,
            text="?",
            font=("Yu Gothic UI", 48, "bold"),
        )
        self.kanji_label.pack(pady=10)

        self.readings_label = ttk.Label(
            parent,
            text="",
            font=("Yu Gothic UI", 14),
            bootstyle="secondary",
        )
        self.readings_label.pack(pady=5)

        if self.help_lang == "en":
            entry_help = "意味を英語または母語で入力してください (type the meaning):"
        elif self.help_lang == "none":
            entry_help = "意味をスペイン語で入力してください"
        else:
            entry_help = "意味をスペイン語で入力してください (escribe el significado en español):"

        entry_label = ttk.Label(
            parent,
            text=entry_help,
            font=("Yu Gothic UI", 10),
        )
        entry_label.pack()

        self.answer_entry = ttk.Entry(parent, width=30)
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

    # --- Diálogo para añadir kanji ---

    def _open_add_kanji_dialog(self) -> None:
        dialog = ttk.Toplevel(self)
        dialog.title("漢字追加 / Añadir kanji")

        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=BOTH, expand=YES)

        ttk.Label(frame, text="漢字:").grid(row=0, column=0, sticky=W, pady=2)
        kanji_var = ttk.StringVar()
        kanji_entry = ttk.Entry(frame, textvariable=kanji_var, width=8)
        kanji_entry.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="よみかた (',' で区切り):").grid(row=1, column=0, sticky=W, pady=2)
        readings_var = ttk.StringVar()
        readings_entry = ttk.Entry(frame, textvariable=readings_var, width=30)
        readings_entry.grid(row=1, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="意味 (español, ';' で区切り):").grid(row=2, column=0, sticky=W, pady=2)
        meanings_var = ttk.StringVar()
        meanings_entry = ttk.Entry(frame, textvariable=meanings_var, width=40)
        meanings_entry.grid(row=2, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="例文 (una por línea):").grid(row=3, column=0, sticky=NW, pady=2)
        examples_text = ttk.Text(frame, width=40, height=4)
        examples_text.grid(row=3, column=1, sticky=W, pady=2)

        info_label = ttk.Label(
            frame,
            text="",
            font=("Yu Gothic UI", 9),
            bootstyle="secondary",
        )
        info_label.grid(row=4, column=0, columnspan=2, sticky=W, pady=(4, 2))

        def on_save() -> None:
            kanji_char = kanji_var.get().strip()
            readings_raw = readings_var.get().strip()
            meanings_raw = meanings_var.get().strip()

            # Aceptar comas japonesas o normales
            readings = [
                r.strip()
                for r in readings_raw.replace("、", ",").split(",")
                if r.strip()
            ]
            meanings_es = [
                m.strip()
                for m in meanings_raw.split(";")
                if m.strip()
            ]

            examples_lines = examples_text.get("1.0", "end").splitlines()
            examples = [ln.strip() for ln in examples_lines if ln.strip()]

            if not kanji_char or not meanings_es:
                info_label.configure(
                    text="必須項目が足りません (faltan campos obligatorios)",
                    bootstyle="danger",
                )
                return

            next_id = max((it.id for it in self.items), default=0) + 1

            new_item = KanjiItem(
                id=next_id,
                kanji=kanji_char,
                readings=readings,
                meanings_es=meanings_es,
                examples=examples,
            )

            self.items.append(new_item)
            save_kanji_items(self.items)

            # Refrescar listado para incluir el nuevo kanji
            self._refresh_list_tree()

            info_label.configure(
                text="漢字を保存しました (kanji guardado)",
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

        kanji_entry.focus_set()

    def _next_random_item(self) -> None:
        if not self.items:
            return

        self.current_index = random.randrange(len(self.items))
        item = self.items[self.current_index]

        if self.kanji_label is not None:
            self.kanji_label.configure(text=item.kanji)

        if self.readings_label is not None:
            readings = ", ".join(item.readings)
            self.readings_label.configure(text=f"よみかた: {readings}")

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

        item = self.items[self.current_index]
        user_answer = self.answer_entry.get().strip().lower()
        # Aceptamos si coincide exactamente con una de las traducciones
        meanings = [m.strip().lower() for m in item.meanings_es]

        is_correct = user_answer in meanings

        if is_correct:
            self.feedback_label.configure(
                text=f"正解です！ ({', '.join(item.meanings_es)})",
                bootstyle="success",
            )
        else:
            self.feedback_label.configure(
                text=f"ちがいます… 正しい答え: {', '.join(item.meanings_es)}",
                bootstyle="danger",
            )

        update_progress_for_item(
            user_id=1,
            item_type="kanji",
            item_id=item.id,
            correct=is_correct,
        )
