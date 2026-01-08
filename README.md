# Japanese N5 Trainer (JLPT N5)

Aplicación de escritorio en Python para practicar japonés orientado al examen JLPT N5.

## Características principales

- **Kana (ひらがな / カタカナ)**: tablas completas (gojūon, dakuon, yoon) y modo tarjetas con SRS.
- **Vocabulario N5**: lista filtrable por tipo/tema, tarjetas y test de elección múltiple.
- **Kanji N5**: listado de kanji básicos con lecturas y significados, práctica con tarjetas y alta de nuevos kanji.
- **Gramática**: puntos gramaticales N5 con explicaciones, ejercicios de partículas y alta de nuevos puntos y frases.
- **Examen simulado**: genera tests mezclando vocabulario, kanji y gramática según dificultad.
- **Progreso**: seguimiento SRS por módulo e historial de exámenes.
- **Configuración**: tema visual (ttkbootstrap), idioma de ayuda (es/en/none) y dificultad.

## Requisitos

- Python 3.10+
- Dependencias en `requirements.txt` (incluye `ttkbootstrap`).

Instalación de dependencias (desde la carpeta del proyecto):

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta del proyecto:

```bash
# Activar el entorno virtual si no lo está aún
.\.venv\Scripts\Activate.ps1

# Lanzar la aplicación
python -m app.main
```

## Estructura del proyecto

- `app/main.py`: punto de entrada de la aplicación (ventana principal).
- `app/ui/`: vistas de la interfaz (kana, vocabulario, kanji, gramática, examen, progreso, ajustes).
- `app/core/`: modelos, repositorios de datos, motor de examen y lógica SRS.
- `app/data/`: datos N5 (kana, vocabulario, kanji, gramática).
- `app/storage/`: gestión de ajustes, progreso y sesiones.

## Desarrollo

El proyecto está preparado para usar Git. Para el primer commit y subida a GitHub:

```bash
git add .
git commit -m "Initial project import"
# Añade el remoto (sustituye por tu usuario/repositorio)
git remote add origin https://github.com/TU_USUARIO/japanese-n5-trainer.git
git branch -M main
git push -u origin main
```
