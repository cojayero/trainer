import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.storage.settings import load_settings
from app.ui.kana_view import KanaView
from app.ui.katakana_view import KatakanaView
from app.ui.vocab_view import VocabView
from app.ui.kanji_view import KanjiView
from app.ui.grammar_view import GrammarView
from app.ui.exam_view import ExamView
from app.ui.progress_view import ProgressView
from app.ui.settings_view import SettingsView


class MainWindow(ttk.Frame):
    """Ventana principal con menú en japonés y contenedor de vistas.

    La interfaz de usuario está en japonés; el código y comentarios pueden
    incluir español para facilitar el mantenimiento.
    """

    def __init__(self, master: ttk.Window) -> None:
        super().__init__(master)
        self.master = master
        self.settings = load_settings()
        self.pack(fill=BOTH, expand=YES)

        self._create_widgets()

    def _create_widgets(self) -> None:
        # Frame superior para título
        header = ttk.Frame(self)
        header.pack(side=TOP, fill=X, pady=10)
        help_lang = (self.settings.help_language or "es").lower()

        if help_lang == "en":
            title_text = "日本語N5トレーナー / Japanese N5 Trainer"
        elif help_lang == "none":
            title_text = "日本語N5トレーナー"
        else:
            title_text = "日本語N5トレーナー / Entrenador N5 de japonés"

        title_label = ttk.Label(
            header,
            text=title_text,
            font=("Yu Gothic UI", 20, "bold"),
        )
        title_label.pack(side=TOP, pady=5)

        # Frame central dividido en menú lateral + área de contenido
        body = ttk.Frame(self)
        body.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Menú lateral
        menu_frame = ttk.Frame(body)
        menu_frame.pack(side=LEFT, fill=Y)

        # Área de contenido donde se mostrarán las vistas
        self.content_frame = ttk.Frame(body, bootstyle="secondary")
        self.content_frame.pack(side=LEFT, fill=BOTH, expand=YES, padx=10)

        # Botones de menú (en japonés)
        if help_lang == "en":
            buttons = [
                ("ひらがな練習 / Hiragana", self.show_kana_view),
                ("カタカナ練習 / Katakana", self.show_katakana_view),
                ("漢字N5 / Kanji N5", self.show_kanji_view),
                ("単語N5 / Vocabulary N5", self.show_vocab_view),
                ("文法N5 / Grammar N5", self.show_grammar_view),
                ("模擬テスト / Mock exam", self.show_exam_view),
                ("進捗 / Progress", self.show_progress_view),
                ("設定 / Settings", self.show_settings_view),
            ]
        elif help_lang == "none":
            buttons = [
                ("ひらがな練習", self.show_kana_view),
                ("カタカナ練習", self.show_katakana_view),
                ("漢字N5", self.show_kanji_view),
                ("単語N5", self.show_vocab_view),
                ("文法N5", self.show_grammar_view),
                ("模擬テスト", self.show_exam_view),
                ("進捗", self.show_progress_view),
                ("設定", self.show_settings_view),
            ]
        else:
            buttons = [
                ("ひらがな練習 (Hiragana)", self.show_kana_view),
                ("カタカナ練習 (Katakana)", self.show_katakana_view),
                ("漢字N5 (Kanji N5)", self.show_kanji_view),
                ("単語N5 (Vocabulario N5)", self.show_vocab_view),
                ("文法N5 (Gramática N5)", self.show_grammar_view),
                ("模擬テスト (Examen simulado)", self.show_exam_view),
                ("進捗 (Progreso)", self.show_progress_view),
                ("設定 (Configuración)", self.show_settings_view),
            ]

        for text, command in buttons:
            btn = ttk.Button(menu_frame, text=text, command=command, width=16)
            btn.pack(side=TOP, fill=X, pady=3)

        # Vista inicial
        if help_lang == "en":
            welcome = "ようこそ！ 日本語N5トレーナーへ。\n左のメニューから学習モードを選んでください。(Choose a mode from the left menu.)"
        elif help_lang == "none":
            welcome = "ようこそ！ 日本語N5トレーナーへ。\n左のメニューから学習モードを選んでください。"
        else:
            welcome = "ようこそ！ 日本語N5トレーナーへ。\n左のメニューから学習モードを選んでください。(Elige un modo en el menú de la izquierda.)"

        self._show_placeholder(welcome)

    # Métodos para cambiar de vista (por ahora simples placeholders)
    def _clear_content(self) -> None:
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _show_placeholder(self, message: str) -> None:
        self._clear_content()
        label = ttk.Label(
            self.content_frame,
            text=message,
            justify=LEFT,
            font=("Yu Gothic UI", 14),
        )
        label.pack(padx=20, pady=20, anchor=NW)

    def show_kana_view(self) -> None:
        self._clear_content()
        view = KanaView(self.content_frame)
        view.pack(fill=BOTH, expand=YES)

    def show_katakana_view(self) -> None:
        self._clear_content()
        view = KatakanaView(self.content_frame)
        view.pack(fill=BOTH, expand=YES)

    def show_kanji_view(self) -> None:
        self._clear_content()
        view = KanjiView(self.content_frame)
        view.pack(fill=BOTH, expand=YES)

    def show_vocab_view(self) -> None:
        self._clear_content()
        view = VocabView(self.content_frame)
        view.pack(fill=BOTH, expand=YES)

    def show_grammar_view(self) -> None:
        self._clear_content()
        view = GrammarView(self.content_frame)
        view.pack(fill=BOTH, expand=YES)

    def show_exam_view(self) -> None:
        self._clear_content()
        view = ExamView(self.content_frame)
        view.pack(fill=BOTH, expand=YES)

    def show_progress_view(self) -> None:
        self._clear_content()
        view = ProgressView(self.content_frame)
        view.pack(fill=BOTH, expand=YES)

    def show_settings_view(self) -> None:
        self._clear_content()
        view = SettingsView(self.content_frame)
        view.pack(fill=BOTH, expand=YES)
