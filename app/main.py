import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.ui.main_window import MainWindow
from app.storage.settings import load_settings


def main() -> None:
    settings = load_settings()
    theme_name = settings.theme or "flatly"

    app = ttk.Window(themename=theme_name)
    app.title("日本語N5トレーナー")
    app.geometry("900x600")

    MainWindow(app)

    app.mainloop()


if __name__ == "__main__":
    main()
