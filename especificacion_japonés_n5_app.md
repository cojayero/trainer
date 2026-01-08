# Especificación Detallada

## 1. Visión general del proyecto

- **Nombre provisional de la aplicación**: 日本語N5トレーナー (Nihongo N5 Trainer)
- **Tecnología principal**: Python 3.x, interfaz gráfica con `tkinter` + `ttkbootstrap`.
- **Idioma de la interfaz**: Japonés (toda la UI y contenidos visibles para el alumno estarán en japonés, con apoyo opcional mínimo en español/inglés en comentarios internos o ayudas avanzadas).
- **Objetivo principal**: Proporcionar las competencias necesarias de vocabulario, kanas (hiragana/katakana), kanji básicos, gramática y comprensión lectora para aprobar el examen JLPT N5.
- **Plataforma objetivo**: Escritorio (Windows como prioridad inicial).

## 2. Objetivos pedagógicos (alineados con JLPT N5)

1. **Lectoescritura básica**
   - Dominar todos los hiragana.
   - Dominar todos los katakana.
   - Reconocer y leer correctamente ~100 kanji de nivel N5.

2. **Vocabulario**
   - Aprender y practicar ~800–1000 palabras de uso frecuente en N5 (sustantivos, verbos, adjetivos, expresiones fijas).

3. **Gramática**
   - Dominar las estructuras gramaticales típicas de N5: partículas básicas (は, が, を, に, で, へ, と, も), forma de diccionario, ます, て, ない, adjetivosい/な, etc.

4. **Comprensión lectora y auditiva (opcional)**
   - Comprender frases cortas y textos simples.
   - (Fase 2) Incluir ejercicios con audio para practicar listening.

5. **Estrategia de estudio**
   - Utilizar un sistema de repetición espaciada (SRS) sencillo para repasar vocabulario y kanji.
   - Proporcionar estadísticas de progreso y simulacros de examen N5 (mini tests).

## 3. Perfil de usuario y escenarios de uso

### 3.1. Perfil de usuario

- Estudiante inicial de japonés sin conocimientos previos o con nivel muy básico.
- Edad objetivo: 15+.
- Puede conocer algo de inglés o español, pero la UI principal estará en japonés para fomentar inmersión.

### 3.2. Escenarios de uso

1. El usuario abre la app y selecciona un modo de estudio (kana, vocabulario, kanji, gramática, examen simulado).
2. El usuario realiza sesiones cortas (10–20 minutos) de tarjetas (flashcards) con repetición espaciada.
3. El usuario practica lectura de frases cortas y responde preguntas tipo test.
4. El usuario consulta su progreso (palabras aprendidas, kanji dominados, tiempo de estudio, etc.).

## 4. Módulos funcionales principales

1. **Módulo de autenticación ligera (opcional / Fase 2)**
   - Usuario invitado (sin login) en Fase 1.
   - Más adelante, soporte para múltiples perfiles locales (nombre de usuario y selección rápida).

2. **Pantalla principal (menú de modos)**
   - Botones (en japonés) para:
     - ひらがな練習 (Práctica de Hiragana)
     - カタカナ練習 (Práctica de Katakana)
     - 漢字N5 (Kanji N5)
     - 単語N5 (Vocabulario N5)
     - 文法N5 (Gramática N5)
     - 模擬テスト (Examen simulado)
     - 進捗 (Progreso)
     - 設定 (Configuración)

3. **Módulo de kana (Hiragana / Katakana)**
   - Listados de caracteres con:
     - Carácter grande.
     - Romaji como ayuda opcional (con botón para mostrar/ocultar, 初級者向け).
   - Modos de práctica:
     - Tarjetas: mostrar símbolo → usuario responde romaji/sonido (入力テキスト o selección múltiple).
     - Escritura mental: mostrar romaji → usuario elige el kana correcto.
   - Registro de aciertos y errores para alimentar SRS interno.

4. **Módulo de vocabulario N5**
   - Base de datos de palabras con:
     - Palabra en japonés (kanji + furigana opcional o kana).
     - Lectura (かな).
     - Significado principal (en español o inglés, guardado pero no siempre visible).
     - Tipo de palabra (sustantivo, verbo, adjetivoい/な, expresión, etc.).
     - Etiquetas (kana/kanji, tema: tiempo, familia, escuela, etc.).
   - Modos de práctica:
     - Flashcards japonés → significado.
     - Significado → japonés.
     - Elección múltiple.
     - Escribir lectura (ひらがな入力 / romaji en Fase 1, transición a かな en Fase 2).

5. **Módulo de kanji N5**
   - Lista de ~100 kanji con:
     - Forma del kanji.
     - Lecturas principales (on/kun sencillas).
     - Palabras de ejemplo.
   - Prácticas tipo:
     - Reconocimiento de kanji → lectura.
     - Lectura → selección del kanji correcto.
     - Asociación kanji ↔ significado.

6. **Módulo de gramática N5**
   - Lista de puntos gramaticales con explicación simple en japonés fácil + notas internas en español.
   - Ejemplos de frases por estructura.
   - Ejercicios tipo:
     - Completar huecos (fill-in-the-blank).
     - Seleccionar la partícula correcta.
     - Ordenar palabras para formar frases.

7. **Módulo de examen simulado (模擬テスト)**
   - Generación de tests de ~20–30 preguntas mezcladas (vocabulario, kanji, gramática, lectura).
   - Temporizador opcional.
   - Corrección final con resumen de errores.

8. **Módulo de progreso (進捗)**
   - Estadísticas generales por módulo:
     - N.º de palabras revisadas / dominadas.
     - Porcentaje de aciertos.
     - Tiempo aproximado de estudio (suma de sesiones).
   - Gráficas simples (barras/lineas básicas con `matplotlib` opcional o representaciones textuales).

9. **Módulo de configuración (設定)**
   - Selección de tema de `ttkbootstrap`.
   - Selección de idioma de ayuda secundaria (español / inglés / desactivado).
   - Nivel de dificultad (por ejemplo, más opciones por pregunta, esconder furigana, etc.).
   - Control de SRS (frecuencia de repaso, tamaño de bloque diario de tarjetas).

## 5. Requisitos funcionales detallados

### 5.1. Requisitos generales

- RF-01: La aplicación debe abrir una ventana principal usando `ttkbootstrap` con un tema moderno (por ejemplo, "flatly").
- RF-02: Todos los textos de botones y etiquetas dirigidos al alumno deben estar en japonés.
- RF-03: Debe existir un menú principal con acceso a todos los módulos.
- RF-04: La aplicación debe recordar el progreso del usuario mediante almacenamiento local (SQLite o ficheros JSON) entre sesiones.

### 5.2. Requisitos módulo kana

- RF-KA-01: Debe mostrarse la tabla completa de hiragana y katakana.
- RF-KA-02: El usuario puede seleccionar conjuntos (por filas: あ行, か行, etc.).
- RF-KA-03: En modo flashcard, se muestra un kana grande y el usuario responde.
- RF-KA-04: El sistema calcula acierto/error y almacena la fecha de último repaso.

### 5.3. Requisitos módulo vocabulario

- RF-VO-01: Cargar un listado de vocabulario N5 desde una fuente (CSV/JSON interna).
- RF-VO-02: Permitir filtrado por tema y estado (nuevo, en aprendizaje, dominado).
- RF-VO-03: Mostrar tarjetas con palabra japonesa y, según configuración, lectura y/o significado.
- RF-VO-04: Incluir al menos 2 tipos de ejercicio: flashcards y elección múltiple.

### 5.4. Requisitos módulo kanji

- RF-KA2-01: Cargar lista de kanji con lecturas y ejemplos.
- RF-KA2-02: Permitir repaso tipo tarjeta.
- RF-KA2-03: Integrar progreso con el SRS general.

### 5.5. Requisitos módulo gramática

- RF-GR-01: Listar todos los puntos gramaticales N5.
- RF-GR-02: Para cada punto, mostrar descripción simple y ejemplos.
- RF-GR-03: Generar ejercicios ligados a cada punto (por lo menos 3 ítems por punto).

### 5.6. Requisitos módulo examen simulado

- RF-EX-01: El usuario puede iniciar un examen desde el menú principal.
- RF-EX-02: El examen debe seleccionar preguntas aleatorias de un banco.
- RF-EX-03: Debe mostrar al final el resultado total, tiempo empleado y lista de errores.

### 5.7. Requisitos de progreso y configuración

- RF-PR-01: Mostrar número total de ítems aprendidos (por módulo y global).
- RF-PR-02: Mostrar historial básico de sesiones (fecha, tipo de ejercicio, resultados).
- RF-SE-01: Guardar en configuración: tema visual, idioma de ayuda, dificultad.

## 6. Requisitos no funcionales

1. **Rendimiento**
   - La app debe arrancar en < 3 segundos en un equipo estándar.
   - Cambio entre pantallas sin bloqueos perceptibles.

2. **Usabilidad**
   - Interfaz limpia, pocos elementos por pantalla.
   - Botones grandes y claramente etiquetados.
   - Navegación consistente: botón de regreso al menú principal en todas las pantallas.

3. **Mantenibilidad**
   - Código modular y organizado por paquetes Python.
   - Separación de lógica de negocio, lógica SRS, y capa de UI.

4. **Portabilidad**
   - Desarrollado para Windows, pero manteniendo compatibilidad con otros SO cuando sea posible (Linux/Mac) usando solo dependencias portables.

5. **Persistencia de datos**
   - Uso de SQLite con una sola base de datos local (p.ej. `n5_trainer.db`) o, alternativamente, JSON si se quiere un formato más simple en Fase 1.

## 7. Arquitectura y diseño

### 7.1. Arquitectura general

- Patrón sugerido: MVC simplificado o separación por capas:
  - Capa **UI**: ventanas y frames de `ttkbootstrap`.
  - Capa **lógica de dominio**: manejo de sesiones de estudio, selección de tarjetas, corrección de respuestas.
  - Capa **datos**: acceso a SQLite/JSON, carga de vocabulario, kanji, gramática.

### 7.2. Organización de paquetes Python (propuesta)

- `app/`
  - `__init__.py`
  - `main.py` (punto de entrada)
  - `ui/`
    - `main_window.py` (ventana principal, navegación)
    - `kana_view.py`
    - `vocab_view.py`
    - `kanji_view.py`
    - `grammar_view.py`
    - `exam_view.py`
    - `progress_view.py`
    - `settings_view.py`
  - `core/`
    - `srs.py` (lógica de repetición espaciada)
    - `models.py` (clases de datos: VocabItem, KanjiItem, GrammarPoint, UserProgress, etc.)
    - `exam_engine.py` (generación de exámenes)
  - `data/`
    - `vocab_n5.json`
    - `kanji_n5.json`
    - `grammar_n5.json`
  - `storage/`
    - `database.py` (acceso SQLite o JSON)
    - `settings.py` (configuración de usuario)

### 7.3. Flujo de arranque de la aplicación

1. `main.py` inicializa `ttkbootstrap.Style` y crea la ventana raíz.
2. Se carga la configuración de usuario (tema, idioma de ayuda, etc.).
3. Se instancia el `MainWindow` que administra el cambio entre vistas.
4. Se inicializan los servicios de datos (carga de vocabulario, kanji y gramática).
5. Se muestra el menú principal.

## 8. Diseño de interfaz (a alto nivel)

### 8.1. Menú principal

- Título: 日本語N5トレーナー
- Botones centrados vertical u horizontalmente con `ttkbootstrap.Button`.
- Cada botón abre un `Frame` diferente administrado por un contenedor (por ejemplo, `ttk.Notebook` o un sistema propio de "cambio de pantalla").

### 8.2. Pantallas de práctica (kana, vocabulario, kanji)

Elementos comunes:
- Texto grande con el ítem principal (kana/palabra/kanji).
- Campo o área para respuesta del usuario.
- Botones:
  - 次へ (Siguiente)
  - わからない (No lo sé)
  - 戻る (Volver)
- Barra o etiqueta de progreso (porcentaje, número de tarjetas restantes).

### 8.3. Pantalla de gramática

- Lista lateral de puntos gramaticales.
- Área central con explicación y ejemplos.
- Botón para empezar ejercicios relacionados con el punto seleccionado.

### 8.4. Pantalla de examen simulado

- Pantalla con una pregunta por vez.
- Indicador de número de pregunta actual / total.
- Opción de finalizar examen antes de tiempo.
- Pantalla de resultados al final.

### 8.5. Pantalla de progreso

- Resumen textual y/o gráfico.
- Botones para ver detalles por módulo.

## 9. Modelo de datos (borrador)

### 9.1. Entidades principales

- `VocabItem`
  - `id: int`
  - `word_jp: str`
  - `reading: str`
  - `meaning_es: str`
  - `pos: str` (verb, noun, adj-i, adj-na, etc.)
  - `tags: list[str]`

- `KanjiItem`
  - `id: int`
  - `kanji: str`
  - `readings: list[str]`
  - `meanings_es: list[str]`
  - `examples: list[str]`

- `GrammarPoint`
  - `id: int`
  - `title_jp: str`
  - `description_simple_jp: str`
  - `note_es: str`
  - `examples: list[str]`

- `UserProgress`
  - `user_id: int`
  - `item_type: str` (vocab/kana/kanji/grammar)
  - `item_id: int`
  - `srs_level: int`
  - `last_review: datetime`
  - `right_count: int`
  - `wrong_count: int`

- `Settings`
  - `theme: str`
  - `help_language: str` (es/en/none)
  - `difficulty: str` (easy/normal/hard)

## 10. Lógica de repetición espaciada (SRS) simplificada

- Niveles de SRS (p.ej. 0 a 4).
- Tras una respuesta correcta, subir un nivel (hasta máximo).
- Tras una respuesta incorrecta, bajar de nivel.
- Intervalos de repaso por nivel (ejemplo):
  - Nivel 0: hoy
  - Nivel 1: +1 día
  - Nivel 2: +3 días
  - Nivel 3: +7 días
  - Nivel 4: +14 días
- En cada sesión, seleccionar primero ítems vencidos y luego nuevos ítems si todavía hay capacidad.

## 11. Roadmap por fases

### Fase 1: MVP (mínimo producto viable)

- Implementar estructura básica de proyecto.
- Menú principal y navegación entre vistas.
- Módulo de hiragana + vocabulario básico con flashcards.
- Persistencia sencilla (JSON) para progreso y configuración.

### Fase 2: Ampliación a N5 completo

- Añadir katakana y kanji N5.
- Añadir gramática N5 y ejercicios.
- Implementar SRS básico.
- Introducir exámenes simulados simples.

### Fase 3: Mejora de UX y contenidos

- Añadir estadísticas detalladas y posible soporte de audio.
- Optimizar diseño visual (temas, iconos, etc.).
- Pulir banco de preguntas y vocabulario.

## 12. Criterios de aceptación

- El usuario puede estudiar kana, vocabulario, kanji y gramática desde una misma aplicación.
- La aplicación permite realizar simulacros de examen y muestra resultados.
- El progreso se guarda y se recupera al reiniciar la app.
- Toda la UI dirigida al alumno se muestra en japonés.

---

Este documento sirve como guía de desarrollo. A partir de esta especificación se podrán definir tareas técnicas concretas (historias de usuario) y comenzar la implementación en Python + ttkbootstrap.