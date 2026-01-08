import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.storage.settings import load_settings, save_settings
from app.core.models import Settings


class SettingsView(ttk.Frame):
    """Vista de configuración de la aplicación.

    Permite cambiar:
    - Tema visual (ttkbootstrap).
    - Idioma de ayuda (es/en/none).
    - Dificultad (easy/normal/hard).
    """

    def __init__(self, master: ttk.Frame) -> None:
        super().__init__(master)
        self.settings: Settings = load_settings()

        self.theme_var = ttk.StringVar(value=self.settings.theme)
        self.help_lang_var = ttk.StringVar(value=self.settings.help_language)
        self.difficulty_var = ttk.StringVar(value=self.settings.difficulty)

        self.info_label: ttk.Label | None = None

        self._create_widgets()

    def _create_widgets(self) -> None:
        header = ttk.Label(
            self,
            text="設定 (Configuración / Settings)",
            font=("Yu Gothic UI", 18, "bold"),
        )
        header.pack(side=TOP, pady=10)

        form = ttk.Frame(self)
        form.pack(padx=20, pady=10, anchor=NW)

        # Tema visual
        ttk.Label(form, text="テーマ / Tema:").grid(row=0, column=0, sticky=W, pady=5)
        theme_combo = ttk.Combobox(
            form,
            textvariable=self.theme_var,
            values=[
                "flatly",
                "cosmo",
                "litera",
                "minty",
                "journal",
                "darkly",
            ],
            width=15,
            state="readonly",
        )
        theme_combo.grid(row=0, column=1, sticky=W, pady=5, padx=5)

        # Idioma de ayuda
        ttk.Label(form, text="ヘルプ言語 / Idioma ayuda:").grid(
            row=1, column=0, sticky=W, pady=5
        )
        help_combo = ttk.Combobox(
            form,
            textvariable=self.help_lang_var,
            values=["es", "en", "none"],
            width=10,
            state="readonly",
        )
        help_combo.grid(row=1, column=1, sticky=W, pady=5, padx=5)

        # Dificultad
        ttk.Label(form, text="難易度 / Dificultad:").grid(
            row=2, column=0, sticky=W, pady=5
        )
        diff_combo = ttk.Combobox(
            form,
            textvariable=self.difficulty_var,
            values=["easy", "normal", "hard"],
            width=10,
            state="readonly",
        )
        diff_combo.grid(row=2, column=1, sticky=W, pady=5, padx=5)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=15)

        save_btn = ttk.Button(
            button_frame,
            text="保存 / Guardar",
            bootstyle="success",
            command=self._on_save,
        )
        save_btn.pack(side=LEFT, padx=5)

        self.info_label = ttk.Label(
            self,
            text="設定を変更した後、アプリを再起動してください (reinicia la app tras cambiar el tema)",
            font=("Yu Gothic UI", 9),
            bootstyle="secondary",
        )
        self.info_label.pack(pady=5)

    def _on_save(self) -> None:
        self.settings.theme = self.theme_var.get() or self.settings.theme
        self.settings.help_language = self.help_lang_var.get() or self.settings.help_language
        self.settings.difficulty = self.difficulty_var.get() or self.settings.difficulty

        save_settings(self.settings)

        if self.info_label is not None:
            self.info_label.configure(
                text="設定を保存しました。アプリを再起動してください。 (Configuración guardada; reinicia la app)",
                bootstyle="success",
            )
