import random

import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.core.srs import update_progress_for_item
from app.storage.settings import load_settings


KATAKANA_ROWS = [
    ["ア", "イ", "ウ", "エ", "オ"],
    ["カ", "キ", "ク", "ケ", "コ"],
    ["サ", "シ", "ス", "セ", "ソ"],
    ["タ", "チ", "ツ", "テ", "ト"],
    ["ナ", "ニ", "ヌ", "ネ", "ノ"],
    ["ハ", "ヒ", "フ", "ヘ", "ホ"],
    ["マ", "ミ", "ム", "メ", "モ"],
    ["ヤ", "ユ", "ヨ"],
    ["ラ", "リ", "ル", "レ", "ロ"],
    ["ワ", "ヲ", "ン"],
    # Dakuon
    ["ガ", "ギ", "グ", "ゲ", "ゴ"],
    ["ザ", "ジ", "ズ", "ゼ", "ゾ"],
    ["ダ", "ヂ", "ヅ", "デ", "ド"],
    ["バ", "ビ", "ブ", "ベ", "ボ"],
    ["パ", "ピ", "プ", "ペ", "ポ"],
    # Yoon
    ["キャ", "キュ", "キョ"],
    ["シャ", "シュ", "ショ"],
    ["チャ", "チュ", "チョ"],
    ["ニャ", "ニュ", "ニョ"],
    ["ヒャ", "ヒュ", "ヒョ"],
    ["ミャ", "ミュ", "ミョ"],
    ["リャ", "リュ", "リョ"],
    ["ギャ", "ギュ", "ギョ"],
    ["ジャ", "ジュ", "ジョ"],
    ["ビャ", "ビュ", "ビョ"],
    ["ピャ", "ピュ", "ピョ"],
]

KATAKANA_ROMAJI = {
    "ア": "a",
    "イ": "i",
    "ウ": "u",
    "エ": "e",
    "オ": "o",
    "カ": "ka",
    "キ": "ki",
    "ク": "ku",
    "ケ": "ke",
    "コ": "ko",
    "サ": "sa",
    "シ": "shi",
    "ス": "su",
    "セ": "se",
    "ソ": "so",
    "タ": "ta",
    "チ": "chi",
    "ツ": "tsu",
    "テ": "te",
    "ト": "to",
    "ナ": "na",
    "ニ": "ni",
    "ヌ": "nu",
    "ネ": "ne",
    "ノ": "no",
    "ハ": "ha",
    "ヒ": "hi",
    "フ": "fu",
    "ヘ": "he",
    "ホ": "ho",
    "マ": "ma",
    "ミ": "mi",
    "ム": "mu",
    "メ": "me",
    "モ": "mo",
    "ヤ": "ya",
    "ユ": "yu",
    "ヨ": "yo",
    "ラ": "ra",
    "リ": "ri",
    "ル": "ru",
    "レ": "re",
    "ロ": "ro",
    "ワ": "wa",
    "ヲ": "wo",
    "ン": "n",
    # Dakuon
    "ガ": "ga",
    "ギ": "gi",
    "グ": "gu",
    "ゲ": "ge",
    "ゴ": "go",
    "ザ": "za",
    "ジ": "ji",
    "ズ": "zu",
    "ゼ": "ze",
    "ゾ": "zo",
    "ダ": "da",
    "ヂ": "ji",
    "ヅ": "zu",
    "デ": "de",
    "ド": "do",
    "バ": "ba",
    "ビ": "bi",
    "ブ": "bu",
    "ベ": "be",
    "ボ": "bo",
    "パ": "pa",
    "ピ": "pi",
    "プ": "pu",
    "ペ": "pe",
    "ポ": "po",
    # Yoon
    "キャ": "kya",
    "キュ": "kyu",
    "キョ": "kyo",
    "シャ": "sha",
    "シュ": "shu",
    "ショ": "sho",
    "チャ": "cha",
    "チュ": "chu",
    "チョ": "cho",
    "ニャ": "nya",
    "ニュ": "nyu",
    "ニョ": "nyo",
    "ヒャ": "hya",
    "ヒュ": "hyu",
    "ヒョ": "hyo",
    "ミャ": "mya",
    "ミュ": "myu",
    "ミョ": "myo",
    "リャ": "rya",
    "リュ": "ryu",
    "リョ": "ryo",
    "ギャ": "gya",
    "ギュ": "gyu",
    "ギョ": "gyo",
    "ジャ": "ja",
    "ジュ": "ju",
    "ジョ": "jo",
    "ビャ": "bya",
    "ビュ": "byu",
    "ビョ": "byo",
    "ピャ": "pya",
    "ピュ": "pyu",
    "ピョ": "pyo",
}

# Usamos un offset en los IDs para no solapar con hiragana
KATAKANA_ID_OFFSET = 100


class KatakanaView(ttk.Frame):
    """Vista de práctica de katakana (tabla + tarjetas)."""

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

        self._init_char_indices()

    def _init_char_indices(self) -> None:
        self.all_chars = []
        self.group_indices = []

        idx = 0
        for row in KATAKANA_ROWS:
            row_indices: list[int] = []
            for _char in row:
                self.all_chars.append(_char)
                row_indices.append(idx)
                idx += 1
            self.group_indices.append(row_indices)

        self.current_candidates = list(range(len(self.all_chars)))

    def _create_widgets(self) -> None:
        if self.help_lang == "en":
            header_text = "カタカナ練習 / Katakana"
        elif self.help_lang == "none":
            header_text = "カタカナ練習"
        else:
            header_text = "カタカナ練習 (Katakana)"

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

        notebook.add(table_tab, text="カタカナ表 / Tabla")
        notebook.add(practice_tab, text="カード練習 / Tarjetas")

        self._build_table_tab(table_tab)
        self._build_practice_tab(practice_tab)

    def _build_table_tab(self, parent: ttk.Frame) -> None:
        info = ttk.Label(
            parent,
            text="カタカナ表（ごじゅうおん）",
            font=("Yu Gothic UI", 12),
        )
        info.pack(side=TOP, pady=5)

        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=BOTH, expand=YES, padx=20, pady=10)

        for row_index, row in enumerate(KATAKANA_ROWS):
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
            info_text = "カード練習：カタカナ → ローマ字 (romaji)"
        elif self.help_lang == "none":
            info_text = "カード練習：カタカナ → ローマ字"
        else:
            info_text = "カード練習：カタカナ → ローマ字 (romaji)"

        info = ttk.Label(
            parent,
            text=info_text,
            font=("Yu Gothic UI", 12),
        )
        info.pack(side=TOP, pady=5)

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
            "ア行",
            "カ行",
            "サ行",
            "タ行",
            "ナ行",
            "ハ行",
            "マ行",
            "ヤ行",
            "ラ行",
            "ワ行・ン",
            "ガ行 (濁音)",
            "ザ行 (濁音)",
            "ダ行 (濁音)",
            "バ行 (濁音)",
            "パ行 (濁音)",
            "キャ行 (拗音)",
            "シャ行 (拗音)",
            "チャ行 (拗音)",
            "ニャ行 (拗音)",
            "ヒャ行 (拗音)",
            "ミャ行 (拗音)",
            "リャ行 (拗音)",
            "ギャ行 (拗音)",
            "ジャ行 (拗音)",
            "ビャ行 (拗音)",
            "ピャ行 (拗音)",
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

        self._next_random_kana()

        self.answer_entry.bind("<Return>", lambda _event: self._check_answer())

    def _next_random_kana(self) -> None:
        if not self.all_chars:
            self._init_char_indices()

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
        if self.group_var is None or not self.all_chars or not self.group_indices:
            return

        selected = self.group_var.get()

        if selected.startswith("すべて"):
            self.current_candidates = list(range(len(self.all_chars)))
        else:
            labels_order = [
                "ア行",
                "カ行",
                "サ行",
                "タ行",
                "ナ行",
                "ハ行",
                "マ行",
                "ヤ行",
                "ラ行",
                "ワ行・ン",
                "ガ行 (濁音)",
                "ザ行 (濁音)",
                "ダ行 (濁音)",
                "バ行 (濁音)",
                "パ行 (濁音)",
                "キャ行 (拗音)",
                "シャ行 (拗音)",
                "チャ行 (拗音)",
                "ニャ行 (拗音)",
                "ヒャ行 (拗音)",
                "ミャ行 (拗音)",
                "リャ行 (拗音)",
                "ギャ行 (拗音)",
                "ジャ行 (拗音)",
                "ビャ行 (拗音)",
                "ピャ行 (拗音)",
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
        correct_answer = KATAKANA_ROMAJI.get(self.current_char, "")

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

        # Actualizar progreso SRS para este katakana (usuario local id=1)
        update_progress_for_item(
            user_id=1,
            item_type="kana",
            item_id=KATAKANA_ID_OFFSET + self.current_index,
            correct=is_correct,
        )
