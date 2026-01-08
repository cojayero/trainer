import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from app.storage.progress import load_all_progress
from app.storage.settings import load_settings
from app.storage.sessions import load_sessions


class ProgressView(ttk.Frame):
    """Vista de resumen de progreso (kana, vocabulario, etc.)."""

    def __init__(self, master: ttk.Frame) -> None:
        super().__init__(master)
        settings = load_settings()
        self.help_lang: str = (settings.help_language or "es").lower()
        self._create_widgets()

    def _create_widgets(self) -> None:
        if self.help_lang == "en":
            header_text = "進捗 / Progress"
        elif self.help_lang == "none":
            header_text = "進捗"
        else:
            header_text = "進捗 (Progreso)"

        header = ttk.Label(
            self,
            text=header_text,
            font=("Yu Gothic UI", 18, "bold"),
        )
        header.pack(side=TOP, pady=10)

        if self.help_lang == "en":
            info_text = "学習状況の概要 / Study progress overview"
        elif self.help_lang == "none":
            info_text = "学習状況の概要"
        else:
            info_text = "学習状況の概要 / Resumen del estado de estudio"

        info = ttk.Label(
            self,
            text=info_text,
            font=("Yu Gothic UI", 11),
        )
        info.pack(side=TOP, pady=5)

        progress_items = load_all_progress()

        # Agregar estadísticas por tipo de ítem
        stats_by_type: dict[str, dict[str, int]] = {}
        for p in progress_items:
            t = p.item_type
            if t not in stats_by_type:
                stats_by_type[t] = {
                    "count": 0,
                    "learned": 0,
                    "right": 0,
                    "wrong": 0,
                }
            stats_by_type[t]["count"] += 1
            stats_by_type[t]["right"] += p.right_count
            stats_by_type[t]["wrong"] += p.wrong_count
            if p.srs_level >= 2:
                stats_by_type[t]["learned"] += 1

        # Tabla simple de estadísticas
        table = ttk.Treeview(
            self,
            columns=("tipo", "items", "aprendidos", "aciertos", "fallos"),
            show="headings",
            height=5,
        )
        if self.help_lang == "en":
            table.heading("tipo", text="種類 / Type")
            table.heading("items", text="項目数 / Items")
            table.heading("aprendidos", text="習得済み / Learned")
            table.heading("aciertos", text="正解数 / Correct")
            table.heading("fallos", text="不正解数 / Wrong")
        elif self.help_lang == "none":
            table.heading("tipo", text="種類")
            table.heading("items", text="項目数")
            table.heading("aprendidos", text="習得済み")
            table.heading("aciertos", text="正解数")
            table.heading("fallos", text="不正解数")
        else:
            table.heading("tipo", text="種類 / Tipo")
            table.heading("items", text="項目数 / Nº ítems")
            table.heading("aprendidos", text="習得済み / Aprendidos")
            table.heading("aciertos", text="正解数 / Aciertos")
            table.heading("fallos", text="不正解数 / Fallos")

        table.column("tipo", width=120)
        table.column("items", width=100, anchor=CENTER)
        table.column("aprendidos", width=120, anchor=CENTER)
        table.column("aciertos", width=100, anchor=CENTER)
        table.column("fallos", width=100, anchor=CENTER)

        if self.help_lang == "en":
            type_labels = {
                "kana": "かな / Kana",
                "vocab": "単語 / Vocab",
                "kanji": "漢字",
                "grammar": "文法",
            }
        elif self.help_lang == "none":
            type_labels = {
                "kana": "かな",
                "vocab": "単語",
                "kanji": "漢字",
                "grammar": "文法",
            }
        else:
            type_labels = {
                "kana": "かな (Kana)",
                "vocab": "単語 (Vocab)",
                "kanji": "漢字",
                "grammar": "文法",
            }

        total_items = 0
        total_learned = 0

        for t, s in stats_by_type.items():
            label = type_labels.get(t, t)
            table.insert(
                "",
                END,
                values=(
                    label,
                    s["count"],
                    s["learned"],
                    s["right"],
                    s["wrong"],
                ),
            )
            total_items += s["count"]
            total_learned += s["learned"]

        table.pack(fill=X, padx=10, pady=10)

        if self.help_lang == "en":
            summary_text = f"合計 / Total: {total_learned} / {total_items} 項目 習得済み (learned)"
        elif self.help_lang == "none":
            summary_text = f"合計: {total_learned} / {total_items} 項目 習得済み"
        else:
            summary_text = f"合計 / Total: {total_learned} / {total_items} 項目 習得済み (aprendidos)"

        summary = ttk.Label(
            self,
            text=summary_text,
            font=("Yu Gothic UI", 11, "bold"),
        )
        summary.pack(pady=5)

        # Historial básico de sesiones de examen
        sessions = load_sessions()
        if sessions:
            if self.help_lang == "en":
                hist_title = "最近の模擬テスト履歴 / Recent mock exams"
            elif self.help_lang == "none":
                hist_title = "最近の模擬テスト履歴"
            else:
                hist_title = "最近の模擬テスト履歴 / Historial reciente de exámenes"

            hist_label = ttk.Label(
                self,
                text=hist_title,
                font=("Yu Gothic UI", 11, "bold"),
            )
            hist_label.pack(pady=(15, 5))

            hist_table = ttk.Treeview(
                self,
                columns=("fecha", "duracion", "puntuacion"),
                show="headings",
                height=5,
            )

            if self.help_lang == "en":
                hist_table.heading("fecha", text="日時 / Date")
                hist_table.heading("duracion", text="時間 / Time (s)")
                hist_table.heading("puntuacion", text="得点 / Score")
            elif self.help_lang == "none":
                hist_table.heading("fecha", text="日時")
                hist_table.heading("duracion", text="時間 (秒)")
                hist_table.heading("puntuacion", text="得点")
            else:
                hist_table.heading("fecha", text="日時 / Fecha")
                hist_table.heading("duracion", text="時間 / Tiempo (s)")
                hist_table.heading("puntuacion", text="得点 / Puntuación")

            hist_table.column("fecha", width=180)
            hist_table.column("duracion", width=110, anchor=CENTER)
            hist_table.column("puntuacion", width=130, anchor=CENTER)

            # Mostrar las últimas 10 sesiones (más recientes primero)
            recent = sorted(sessions, key=lambda s: s.start_time, reverse=True)[:10]
            for s in recent:
                start_str = s.start_time.strftime("%Y-%m-%d %H:%M")
                duration = int((s.end_time - s.start_time).total_seconds())
                score = f"{s.correct_count}/{s.total_questions}"
                hist_table.insert("", END, values=(start_str, duration, score))

            hist_table.pack(fill=X, padx=10, pady=5)
