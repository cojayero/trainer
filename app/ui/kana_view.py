import random

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.core.srs import update_progress_for_item
from app.storage.settings import load_settings


HIRAGANA_ROWS = [
    ["あ", "い", "う", "え", "お"],
    ["か", "き", "く", "け", "こ"],
    ["さ", "し", "す", "せ", "そ"],
    ["た", "ち", "つ", "て", "と"],
    ["な", "に", "ぬ", "ね", "の"],
    ["は", "ひ", "ふ", "へ", "ほ"],
    ["ま", "み", "む", "め", "も"],
    ["や", "ゆ", "よ"],
    ["ら", "り", "る", "れ", "ろ"],
    ["わ", "を", "ん"],
    # Dakuon (が行, ざ行, だ行, ば行, ぱ行)
    ["が", "ぎ", "ぐ", "げ", "ご"],
    ["ざ", "じ", "ず", "ぜ", "ぞ"],
    ["だ", "ぢ", "づ", "で", "ど"],
    ["ば", "び", "ぶ", "べ", "ぼ"],
    ["ぱ", "ぴ", "ぷ", "ぺ", "ぽ"],
    # Yoon (きゃ行, しゃ行, ちゃ行, にゃ行, ひゃ行, みゃ行, りゃ行, etc.)
    ["きゃ", "きゅ", "きょ"],
    ["しゃ", "しゅ", "しょ"],
    ["ちゃ", "ちゅ", "ちょ"],
    ["にゃ", "にゅ", "にょ"],
    ["ひゃ", "ひゅ", "ひょ"],
    ["みゃ", "みゅ", "みょ"],
    ["りゃ", "りゅ", "りょ"],
    ["ぎゃ", "ぎゅ", "ぎょ"],
    ["じゃ", "じゅ", "じょ"],
    ["びゃ", "びゅ", "びょ"],
    ["ぴゃ", "ぴゅ", "ぴょ"],
]

KANA_ROMAJI = {
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o",
    "か": "ka",
    "き": "ki",
    "く": "ku",
    "け": "ke",
    "こ": "ko",
    "さ": "sa",
    "し": "shi",
    "す": "su",
    "せ": "se",
    "そ": "so",
    "た": "ta",
    "ち": "chi",
    "つ": "tsu",
    "て": "te",
    "と": "to",
    "な": "na",
    "に": "ni",
    "ぬ": "nu",
    "ね": "ne",
    "の": "no",
    "は": "ha",
    "ひ": "hi",
    "ふ": "fu",
    "へ": "he",
    "ほ": "ho",
    "ま": "ma",
    "み": "mi",
    "む": "mu",
    "め": "me",
    "も": "mo",
    "や": "ya",
    "ゆ": "yu",
    "よ": "yo",
    "ら": "ra",
    "り": "ri",
    "る": "ru",
    "れ": "re",
    "ろ": "ro",
    "わ": "wa",
    "を": "wo",
    "ん": "n",
    # Dakuon
    "が": "ga",
    "ぎ": "gi",
    "ぐ": "gu",
    "げ": "ge",
    "ご": "go",
    "ざ": "za",
    "じ": "ji",
    "ず": "zu",
    "ぜ": "ze",
    "ぞ": "zo",
    "だ": "da",
    "ぢ": "ji",
    "づ": "zu",
    "で": "de",
    "ど": "do",
    "ば": "ba",
    "び": "bi",
    "ぶ": "bu",
    "べ": "be",
    "ぼ": "bo",
    "ぱ": "pa",
    "ぴ": "pi",
    "ぷ": "pu",
    "ぺ": "pe",
    "ぽ": "po",
    # Yoon (combinaciones)
    "きゃ": "kya",
    "きゅ": "kyu",
    "きょ": "kyo",
    "しゃ": "sha",
    "しゅ": "shu",
    "しょ": "sho",
    "ちゃ": "cha",
    "ちゅ": "chu",
    "ちょ": "cho",
    "にゃ": "nya",
    "にゅ": "nyu",
    "にょ": "nyo",
    "ひゃ": "hya",
    "ひゅ": "hyu",
    "ひょ": "hyo",
    "みゃ": "mya",
    "みゅ": "myu",
    "みょ": "myo",
    "りゃ": "rya",
    "りゅ": "ryu",
    "りょ": "ryo",
    "ぎゃ": "gya",
    "ぎゅ": "gyu",
    "ぎょ": "gyo",
    "じゃ": "ja",
    "じゅ": "ju",
    "じょ": "jo",
    "びゃ": "bya",
    "びゅ": "byu",
    "びょ": "byo",
    "ぴゃ": "pya",
    "ぴゅ": "pyu",
    "ぴょ": "pyo",
}


class KanaView(ttk.Frame):
    """Vista de práctica de hiragana.

    - Pestaña 1: tabla de hiragana (ごじゅうおん).
    - Pestaña 2: práctica tipo flashcard (hiragana → romaji).
    """

    def __init__(self, master: ttk.Frame) -> None:
        super().__init__(master)
        settings = load_settings()
        self.help_lang: str = (settings.help_language or "es").lower()
        self.current_char: str | None = None
        self.current_index: int | None = None

        self.all_chars: list[str] = []
        self.group_indices: list[list[int]] = []
        self.current_candidates: list[int] = []

        self.group_var: ttk.StringVar | None = None

        self.kana_label: ttk.Label | None = None
        self.answer_entry: ttk.Entry | None = None
        self.feedback_label: ttk.Label | None = None

        self._create_widgets()

        # Preparar índices globales y grupos por fila para selección de subconjuntos
        self._init_char_indices()

    def _init_char_indices(self) -> None:
        self.all_chars = []
        self.group_indices = []

        idx = 0
        for row in HIRAGANA_ROWS:
            row_indices: list[int] = []
            for _char in row:
                self.all_chars.append(_char)
                row_indices.append(idx)
                idx += 1
            self.group_indices.append(row_indices)

        # Por defecto: todas las posiciones disponibles
        self.current_candidates = list(range(len(self.all_chars)))

    def _create_widgets(self) -> None:
        if self.help_lang == "en":
            header_text = "ひらがな練習 / Hiragana"
        elif self.help_lang == "none":
            header_text = "ひらがな練習"
        else:
            header_text = "ひらがな練習 (Hiragana)"

        header = ttk.Label(
            self,
            text=header_text,
            font=("Yu Gothic UI", 18, "bold"),
        )
        header.pack(side=TOP, pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        table_tab = ttk.Frame(notebook)
        practice_tab = ttk.Frame(notebook)

        notebook.add(table_tab, text="ひらがな表 / Tabla")
        notebook.add(practice_tab, text="カード練習 / Tarjetas")

        self._build_table_tab(table_tab)
        self._build_practice_tab(practice_tab)

    def _build_table_tab(self, parent: ttk.Frame) -> None:
        info = ttk.Label(
            parent,
            text="ひらがな表（ごじゅうおん）",
            font=("Yu Gothic UI", 12),
        )
        info.pack(side=TOP, pady=5)

        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        for row_index, row in enumerate(HIRAGANA_ROWS):
            for col_index, char in enumerate(row):
                btn = ttk.Button(
                    table_frame,
                    text=char,
                    width=4,
                    bootstyle="primary-outline",
                )
                btn.grid(row=row_index, column=col_index, padx=4, pady=4)

    def _build_practice_tab(self, parent: ttk.Frame) -> None:
        if self.help_lang == "en":
            info_text = "カード練習：ひらがな → ローマ字 (romaji)"
        elif self.help_lang == "none":
            info_text = "カード練習：ひらがな → ローマ字"
        else:
            info_text = "カード練習：ひらがな → ローマ字 (romaji)"

        info = ttk.Label(
            parent,
            text=info_text,
            font=("Yu Gothic UI", 12),
        )
        info.pack(side=TOP, pady=5)

        # Selector de fila a practicar
        selector_frame = ttk.Frame(parent)
        selector_frame.pack(pady=5)

        selector_label = ttk.Label(
            selector_frame,
            text="練習する行 / Fila:",
            font=("Yu Gothic UI", 10),
        )
        selector_label.pack(side=LEFT, padx=5)

        labels = [
            "すべて / Todas",
            "あ行",
            "か行",
            "さ行",
            "た行",
            "な行",
            "は行",
            "ま行",
            "や行",
            "ら行",
            "わ行・ん",
            "が行 (だくおん)",
            "ざ行 (だくおん)",
            "だ行 (だくおん)",
            "ば行 (だくおん)",
            "ぱ行 (だくおん)",
            "きゃ行 (拗音)",
            "しゃ行 (拗音)",
            "ちゃ行 (拗音)",
            "にゃ行 (拗音)",
            "ひゃ行 (拗音)",
            "みゃ行 (拗音)",
            "りゃ行 (拗音)",
            "ぎゃ行 (拗音)",
            "じゃ行 (拗音)",
            "びゃ行 (拗音)",
            "ぴゃ行 (拗音)",
        ]

        self.group_var = ttk.StringVar(value=labels[0])
        group_select = ttk.Combobox(
            selector_frame,
            textvariable=self.group_var,
            values=labels,
            state="readonly",
            width=20,
        )
        group_select.pack(side=LEFT, padx=5)
        group_select.bind("<<ComboboxSelected>>", lambda _e: self._on_group_change())

        self.kana_label = ttk.Label(
            parent,
            text="?",
            font=("Yu Gothic UI", 48, "bold"),
        )
        self.kana_label.pack(pady=20)

        if self.help_lang == "en":
            entry_help = "Type in romaji:"
        elif self.help_lang == "none":
            entry_help = "ローマ字で入力してください"
        else:
            entry_help = "ローマ字で入力してください (escribe en romaji):"

        entry_label = ttk.Label(
            parent,
            text=entry_help,
            font=("Yu Gothic UI", 10),
        )
        entry_label.pack()

        self.answer_entry = ttk.Entry(parent, width=20)
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
            command=self._next_random_kana,
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

        # Inicializar primera tarjeta
        self._next_random_kana()

        # Permitir pulsar Enter para comprobar la respuesta
        self.answer_entry.bind("<Return>", lambda _event: self._check_answer())

    def _next_random_kana(self) -> None:
        if not self.all_chars:
            self._init_char_indices()

        # Usar el subconjunto actual de índices (fila seleccionada)
        candidates = self.current_candidates or list(range(len(self.all_chars)))
        self.current_index = random.choice(candidates)
        self.current_char = self.all_chars[self.current_index]

        if self.kana_label is not None:
            self.kana_label.configure(text=self.current_char)

        if self.feedback_label is not None:
            self.feedback_label.configure(text="", bootstyle="secondary")

        if self.answer_entry is not None:
            self.answer_entry.delete(0, END)
            self.answer_entry.focus_set()

    def _on_group_change(self) -> None:
        """Actualizar el subconjunto de kana a practicar según la fila elegida."""

        if self.group_var is None or not self.all_chars or not self.group_indices:
            return

        selected = self.group_var.get()

        # Mapeo 1:1 entre etiquetas y filas de HIRAGANA_ROWS
        if selected.startswith("すべて"):
            self.current_candidates = list(range(len(self.all_chars)))
        else:
            labels_order = [
                "あ行",
                "か行",
                "さ行",
                "た行",
                "な行",
                "は行",
                "ま行",
                "や行",
                "ら行",
                "わ行・ん",
                "が行 (だくおん)",
                "ざ行 (だくおん)",
                "だ行 (だくおん)",
                "ば行 (だくおん)",
                "ぱ行 (だくおん)",
                "きゃ行 (拗音)",
                "しゃ行 (拗音)",
                "ちゃ行 (拗音)",
                "にゃ行 (拗音)",
                "ひゃ行 (拗音)",
                "みゃ行 (拗音)",
                "りゃ行 (拗音)",
                "ぎゃ行 (拗音)",
                "じゃ行 (拗音)",
                "びゃ行 (拗音)",
                "ぴゃ行 (拗音)",
            ]

            try:
                row_idx = labels_order.index(selected)
            except ValueError:
                self.current_candidates = list(range(len(self.all_chars)))
            else:
                if 0 <= row_idx < len(self.group_indices):
                    self.current_candidates = self.group_indices[row_idx][:]
                else:
                    self.current_candidates = list(range(len(self.all_chars)))

        # Al cambiar de fila, mostrar inmediatamente una tarjeta de ese subconjunto
        self._next_random_kana()

    def _check_answer(self) -> None:
        if (
            self.current_char is None
            or self.current_index is None
            or self.answer_entry is None
            or self.feedback_label is None
        ):
            return

        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = KANA_ROMAJI.get(self.current_char, "")

        if not correct_answer:
            return

        is_correct = user_answer == correct_answer

        if is_correct:
            self.feedback_label.configure(
                text=f"正解です！ ({correct_answer})",
                bootstyle="success",
            )
        else:
            self.feedback_label.configure(
                text=f"ちがいます… 正しい答え: {correct_answer}",
                bootstyle="danger",
            )

        # Actualizar progreso SRS para este kana (usuario local id=1)
        update_progress_for_item(
            user_id=1,
            item_type="kana",
            item_id=self.current_index,
            correct=is_correct,
        )
