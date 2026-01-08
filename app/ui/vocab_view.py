import random

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.core.srs import update_progress_for_item
from app.core.vocab_repository import load_vocab_items, save_vocab_items
from app.storage.settings import load_settings


class VocabView(ttk.Frame):
    """Vista de práctica de vocabulario N5 (versión básica).

    - Lista de palabras.
    - Modo tarjetas: japonés → significado en español.
    """

    def __init__(self, master: ttk.Frame) -> None:
        super().__init__(master)
        settings = load_settings()
        self.help_lang: str = (settings.help_language or "es").lower()
        # Datos completos y vista filtrada
        self.all_items = load_vocab_items()
        self.items = list(self.all_items)
        self.current_index: int | None = None

        self.filter_tag_var: ttk.StringVar | None = None
        self.filter_pos_var: ttk.StringVar | None = None

        self.list_tree: ttk.Treeview | None = None

        self.word_label: ttk.Label | None = None
        self.reading_label: ttk.Label | None = None
        self.answer_entry: ttk.Entry | None = None
        self.feedback_label: ttk.Label | None = None

        self._create_widgets()

    def _create_widgets(self) -> None:
        if self.help_lang == "en":
            header_text = "単語N5 / Vocabulary N5"
        elif self.help_lang == "none":
            header_text = "単語N5"
        else:
            header_text = "単語N5 (Vocabulario N5)"

        header = ttk.Label(
            self,
            text=header_text,
            font=("Yu Gothic UI", 18, "bold"),
        )
        header.pack(side=TOP, pady=10)

        # Botón para añadir nuevo vocabulario
        add_frame = ttk.Frame(self)
        add_frame.pack(fill=X, padx=10)

        if self.help_lang == "en":
            add_text = "新しい単語を追加 / Add word"
        elif self.help_lang == "none":
            add_text = "新しい単語を追加"
        else:
            add_text = "新しい単語を追加 / Añadir palabra"

        add_btn = ttk.Button(
            add_frame,
            text=add_text,
            bootstyle="info-outline",
            command=self._open_add_vocab_dialog,
        )
        add_btn.pack(side=RIGHT)

        if not self.items:
            if self.help_lang == "en":
                msg_text = "単語データがありません (no vocabulary data)"
            elif self.help_lang == "none":
                msg_text = "単語データがありません"
            else:
                msg_text = "単語データがありません (no hay datos de vocabulario)"

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
        test_tab = ttk.Frame(notebook)

        notebook.add(list_tab, text="一覧 / Lista")
        notebook.add(flashcard_tab, text="カード練習 / Tarjetas")
        notebook.add(test_tab, text="テスト / Test")

        self._build_list_tab(list_tab)
        self._build_flashcard_tab(flashcard_tab)
        self._build_test_tab(test_tab)

    def _build_list_tab(self, parent: ttk.Frame) -> None:
        # Filtros sencillos por etiqueta (tag) y tipo de palabra (pos)
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(fill=X, padx=5, pady=5)

        ttk.Label(filter_frame, text="タグ / Etiqueta:").pack(side=LEFT, padx=2)
        all_tags = sorted({t for item in self.all_items for t in item.tags})
        tag_values = ["(all)"] + all_tags
        self.filter_tag_var = ttk.StringVar(value="(all)")
        tag_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_tag_var,
            values=tag_values,
            state="readonly",
            width=12,
        )
        tag_combo.pack(side=LEFT, padx=2)
        tag_combo.bind("<<ComboboxSelected>>", lambda _e: self._apply_filters())

        ttk.Label(filter_frame, text="品詞 / Tipo:").pack(side=LEFT, padx=8)
        all_pos = sorted({item.pos for item in self.all_items if item.pos})
        pos_values = ["(all)"] + all_pos
        self.filter_pos_var = ttk.StringVar(value="(all)")
        pos_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_pos_var,
            values=pos_values,
            state="readonly",
            width=12,
        )
        pos_combo.pack(side=LEFT, padx=2)
        pos_combo.bind("<<ComboboxSelected>>", lambda _e: self._apply_filters())

        self.list_tree = ttk.Treeview(
            parent,
            columns=("jp", "reading", "meaning"),
            show="headings",
            height=10,
        )
        self.list_tree.heading("jp", text="日本語")
        self.list_tree.heading("reading", text="よみかた")
        self.list_tree.heading("meaning", text="意味 (español)")

        self.list_tree.column("jp", width=120)
        self.list_tree.column("reading", width=120)
        self.list_tree.column("meaning", width=220)

        self.list_tree.pack(fill=BOTH, expand=YES, padx=5, pady=5)

        self._refresh_list_tree()

    def _build_flashcard_tab(self, parent: ttk.Frame) -> None:
        if self.help_lang == "en":
            info_text = "カード練習：日本語 → 意味 (English/Spanish)"
        elif self.help_lang == "none":
            info_text = "カード練習：日本語 → 意味"
        else:
            info_text = "カード練習：日本語 → 意味 (español)"

        info = ttk.Label(
            parent,
            text=info_text,
            font=("Yu Gothic UI", 12),
        )
        info.pack(side=TOP, pady=5)

        self.word_label = ttk.Label(
            parent,
            text="?",
            font=("Yu Gothic UI", 32, "bold"),
        )
        self.word_label.pack(pady=10)

        self.reading_label = ttk.Label(
            parent,
            text="",
            font=("Yu Gothic UI", 14),
            bootstyle="secondary",
        )
        self.reading_label.pack(pady=5)

        if self.help_lang == "en":
            entry_help = "意味を英語または母語で入力してください (type the meaning)"
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

    # --- Tab de test tipo elección múltiple ---

    def _build_test_tab(self, parent: ttk.Frame) -> None:
        if self.help_lang == "en":
            info_text = "単語テスト：日本語 → 意味 (4 options)"
        elif self.help_lang == "none":
            info_text = "単語テスト：日本語 → 意味"
        else:
            info_text = "単語テスト：日本語 → 意ma (4 opciones)"

        info = ttk.Label(
            parent,
            text=info_text,
            font=("Yu Gothic UI", 12),
        )
        info.pack(side=TOP, pady=5)

        self.test_word_label = ttk.Label(
            parent,
            text="?",
            font=("Yu Gothic UI", 32, "bold"),
        )
        self.test_word_label.pack(pady=10)

        self.test_reading_label = ttk.Label(
            parent,
            text="",
            font=("Yu Gothic UI", 14),
            bootstyle="secondary",
        )
        self.test_reading_label.pack(pady=5)

        self.test_var = ttk.IntVar(value=-1)
        self.test_options_frame = ttk.Frame(parent)
        self.test_options_frame.pack(pady=5, anchor=NW)

        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)

        check_btn = ttk.Button(
            btn_frame,
            text="答えを確認 / Check",
            bootstyle="success-outline",
            command=self._test_check,
        )
        check_btn.pack(side=LEFT, padx=5)

        next_btn = ttk.Button(
            btn_frame,
            text="次へ / Next",
            bootstyle="secondary-outline",
            command=self._test_next,
        )
        next_btn.pack(side=LEFT, padx=5)

        self.test_feedback_label = ttk.Label(
            parent,
            text="",
            font=("Yu Gothic UI", 11),
            bootstyle="secondary",
        )
        self.test_feedback_label.pack(pady=10, anchor=NW)

        self._test_next()

    # --- Diálogo para añadir vocabulario ---

    def _open_add_vocab_dialog(self) -> None:
        dialog = ttk.Toplevel(self)
        dialog.title("単語追加 / Añadir palabra")

        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=BOTH, expand=YES)

        # Campos básicos
        ttk.Label(frame, text="日本語:").grid(row=0, column=0, sticky=W, pady=2)
        jp_var = ttk.StringVar()
        jp_entry = ttk.Entry(frame, textvariable=jp_var, width=25)
        jp_entry.grid(row=0, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="よみかた:").grid(row=1, column=0, sticky=W, pady=2)
        reading_var = ttk.StringVar()
        reading_entry = ttk.Entry(frame, textvariable=reading_var, width=25)
        reading_entry.grid(row=1, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="意味 (español):").grid(row=2, column=0, sticky=W, pady=2)
        meaning_var = ttk.StringVar()
        meaning_entry = ttk.Entry(frame, textvariable=meaning_var, width=30)
        meaning_entry.grid(row=2, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="品詞 / Tipo:").grid(row=3, column=0, sticky=W, pady=2)
        pos_var = ttk.StringVar()
        pos_entry = ttk.Entry(frame, textvariable=pos_var, width=20)
        pos_entry.grid(row=3, column=1, sticky=W, pady=2)

        ttk.Label(frame, text="タグ (separadas por ';'):").grid(row=4, column=0, sticky=W, pady=2)
        tags_var = ttk.StringVar()
        tags_entry = ttk.Entry(frame, textvariable=tags_var, width=30)
        tags_entry.grid(row=4, column=1, sticky=W, pady=2)

        info_label = ttk.Label(
            frame,
            text="",
            font=("Yu Gothic UI", 9),
            bootstyle="secondary",
        )
        info_label.grid(row=5, column=0, columnspan=2, sticky=W, pady=(4, 2))

        def on_save() -> None:
            word_jp = jp_var.get().strip()
            reading = reading_var.get().strip()
            meaning = meaning_var.get().strip()
            pos = pos_var.get().strip() or "sustantivo"
            tags_text = tags_var.get().strip()
            tags = [t.strip() for t in tags_text.split(";") if t.strip()]

            if not word_jp or not reading or not meaning:
                info_label.configure(
                    text="必須項目が足りません (faltan campos obligatorios)",
                    bootstyle="danger",
                )
                return

            next_id = max((it.id for it in self.all_items), default=0) + 1

            from app.core.models import VocabItem

            new_item = VocabItem(
                id=next_id,
                word_jp=word_jp,
                reading=reading,
                meaning_es=meaning,
                pos=pos,
                tags=tags,
            )

            self.all_items.append(new_item)
            save_vocab_items(self.all_items)

            # Reaplicar filtros y refrescar vista
            self._apply_filters()

            info_label.configure(
                text="単語を保存しました (palabra guardada)",
                bootstyle="success",
            )

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=8, sticky=E)

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

        jp_entry.focus_set()

    def _next_random_item(self) -> None:
        if not self.items:
            return

        self.current_index = random.randrange(len(self.items))
        item = self.items[self.current_index]

        if self.word_label is not None:
            self.word_label.configure(text=item.word_jp)

        if self.reading_label is not None:
            self.reading_label.configure(text=f"よみかた: {item.reading}")

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
        correct_meaning = item.meaning_es.strip().lower()

        is_correct = user_answer == correct_meaning

        if is_correct:
            self.feedback_label.configure(
                text=f"正解です！ ({item.meaning_es})",
                bootstyle="success",
            )
        else:
            self.feedback_label.configure(
                text=f"ちがいます… 正しい答え: {item.meaning_es}",
                bootstyle="danger",
            )

        update_progress_for_item(
            user_id=1,
            item_type="vocab",
            item_id=item.id,
            correct=is_correct,
        )

    # --- Filtros de lista ---

    def _apply_filters(self) -> None:
        tag = self.filter_tag_var.get() if self.filter_tag_var is not None else "(all)"
        pos = self.filter_pos_var.get() if self.filter_pos_var is not None else "(all)"

        filtered = list(self.all_items)

        if tag and tag != "(all)":
            filtered = [it for it in filtered if tag in it.tags]

        if pos and pos != "(all)":
            filtered = [it for it in filtered if it.pos == pos]

        self.items = filtered
        self._refresh_list_tree()

    def _refresh_list_tree(self) -> None:
        if self.list_tree is None:
            return

        for row in self.list_tree.get_children():
            self.list_tree.delete(row)

        for item in self.items:
            self.list_tree.insert("", END, values=(item.word_jp, item.reading, item.meaning_es))

    # --- Lógica del test de elección múltiple ---

    def _test_next(self) -> None:
        if not self.items:
            return

        correct_item = random.choice(self.items)
        distractors_pool = [it for it in self.items if it.id != correct_item.id]
        if len(distractors_pool) < 3:
            # No hay suficientes opciones, usar todo el conjunto
            distractors_pool = self.items

        distractors = random.sample(distractors_pool, min(3, len(distractors_pool)))
        options = distractors + [correct_item]
        random.shuffle(options)

        self.test_current_correct_id = correct_item.id
        self.test_current_options = options

        self.test_word_label.configure(text=correct_item.word_jp)
        self.test_reading_label.configure(text=f"よみかた: {correct_item.reading}")

        for child in self.test_options_frame.winfo_children():
            child.destroy()

        self.test_var.set(-1)
        for idx, opt in enumerate(options):
            rb = ttk.Radiobutton(
                self.test_options_frame,
                text=opt.meaning_es,
                variable=self.test_var,
                value=idx,
                bootstyle="info-toolbutton",
            )
            rb.pack(anchor=NW, pady=2)

        self.test_feedback_label.configure(text="", bootstyle="secondary")

    def _test_check(self) -> None:
        if not getattr(self, "test_current_options", None):
            return

        idx = self.test_var.get()
        if idx < 0 or idx >= len(self.test_current_options):
            return

        selected = self.test_current_options[idx]
        correct_id = self.test_current_correct_id
        is_correct = selected.id == correct_id

        if is_correct:
            msg = f"正解です！ ({selected.meaning_es})"
            style = "success"
        else:
            correct_item = next((it for it in self.test_current_options if it.id == correct_id), None)
            correct_text = correct_item.meaning_es if correct_item else "?"
            msg = f"ちがいます… 正しい答え: {correct_text}"
            style = "danger"

        self.test_feedback_label.configure(text=msg, bootstyle=style)

        update_progress_for_item(
            user_id=1,
            item_type="vocab",
            item_id=correct_id,
            correct=is_correct,
        )
