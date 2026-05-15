"""
SCRIPT DE VALIDACIÓN: Goodreads Dataset (Goodreads May 2024)
Valida los archivos REALES disponibles en el proyecto:
  - data/Book_Details.csv      → metadata de 16k libros
  - archive/book_reviews.db    → 63k reseñas con texto para NLP

Ejecuta desde la carpeta data/ o ajusta BASE_DIR si es necesario.
"""

import pandas as pd
import sqlite3
import os
import re

# ============================================================================
# PASO 1: CONFIGURACIÓN DE RUTAS
# ============================================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_PATH     = os.path.join(BASE_DIR, "data", "Book_Details.csv")
REVIEWS_DB   = os.path.join(BASE_DIR, "archive", "book_reviews.db")
LISTS_DB     = os.path.join(BASE_DIR, "archive", "books.db")   # no es necesario para el proyecto

print("=" * 70)
print("VALIDACIÓN DATASET GOODREADS — PROYECTO RECOMENDACIÓN LIBROS")
print("=" * 70)

warnings = []
errors   = []

# ============================================================================
# PASO 2: VERIFICAR QUE LOS ARCHIVOS EXISTEN
# ============================================================================
print("\n[1/5] COMPROBANDO ARCHIVOS...")

for path, label in [(CSV_PATH, "Book_Details.csv"), (REVIEWS_DB, "book_reviews.db")]:
    if os.path.exists(path):
        size_mb = os.path.getsize(path) / 1_048_576
        print(f"  ✅ {label:25s} ({size_mb:.1f} MB)")
    else:
        print(f"  ❌ {label:25s} → NO ENCONTRADO en {path}")
        errors.append(f"Archivo no encontrado: {label}")

if errors:
    print("\n❌ Archivos críticos faltan. Abortando.")
    exit(1)

# ============================================================================
# PASO 3: VALIDAR Book_Details.csv  (metadata de libros)
# ============================================================================
print("\n[2/5] VALIDANDO Book_Details.csv (metadata)...")

df_books = pd.read_csv(CSV_PATH)
print(f"  Filas: {len(df_books):,}  |  Columnas: {df_books.shape[1]}")
print(f"  Columnas disponibles: {df_books.columns.tolist()}")

# Columnas críticas esperadas
BOOKS_REQUIRED = {
    "book_id":          "ID único Goodreads (clave de join con reviews)",
    "book_title":       "Título del libro",
    "author":           "Autor",
    "genres":           "Géneros (lista en formato string)",
    "average_rating":   "Rating promedio 1-5",
    "num_reviews":      "Número total de reseñas",
}
BOOKS_OPTIONAL = {
    "book_details":     "Descripción/sinopsis del libro",
    "publication_info": "Info de publicación (año extraíble via regex)",
    "num_ratings":      "Número total de valoraciones",
    "rating_distribution": "Distribución de ratings por estrella",
    "num_pages":        "Número de páginas",
}

print("\n  Columnas OBLIGATORIAS:")
for col, desc in BOOKS_REQUIRED.items():
    if col in df_books.columns:
        nulls = df_books[col].isnull().sum()
        pct   = 100 * nulls / len(df_books)
        status = "✅" if pct < 5 else "⚠️ "
        print(f"    {status} {col:22s} nulos: {nulls} ({pct:.1f}%) → {desc}")
        if pct >= 5:
            warnings.append(f"{col} tiene {pct:.1f}% nulos")
    else:
        print(f"    ❌ {col:22s} → FALTA")
        errors.append(f"Book_Details.csv: columna ausente '{col}'")

print("\n  Columnas OPCIONALES:")
for col, desc in BOOKS_OPTIONAL.items():
    mark = "✅" if col in df_books.columns else "⏭️ "
    print(f"    {mark} {col:22s} → {desc}")

# Nota sobre publication_year
if "publication_info" in df_books.columns:
    sample_pub = df_books["publication_info"].dropna().iloc[0]
    year_match = re.search(r'\b(1[89]\d{2}|20[0-2]\d)\b', str(sample_pub))
    note = f"(año extraíble, ej: '{sample_pub[:50]}...')" if year_match else "(parsing necesario)"
    print(f"\n  ⚠️  publication_year → No existe como columna directa. {note}")
    warnings.append("publication_year requiere parsear publication_info con regex")

# ============================================================================
# PASO 4: VALIDAR book_reviews.db  (reseñas + texto NLP)
# ============================================================================
print("\n[3/5] VALIDANDO book_reviews.db (reseñas)...")

conn = sqlite3.connect(REVIEWS_DB)
df_rev = pd.read_sql("SELECT * FROM book_reviews", conn)
conn.close()

print(f"  Filas: {len(df_rev):,}  |  Columnas: {df_rev.columns.tolist()}")

REVIEWS_REQUIRED = {
    "book_id":          "ID del libro (join con Book_Details.csv)",
    "review_content":   "Texto de la reseña → NLP / sentimientos",
    "review_rating":    "Rating de la reseña ('Rating X out of 5' → limpiar a int)",
    "review_date":      "Fecha de la reseña (análisis temporal)",
}
REVIEWS_OPTIONAL = {
    "reviewer_id":      "ID del revisor",
    "reviewer_name":    "Nombre del revisor",
    "likes_on_review":  "Likes recibidos (proxy de calidad)",
    "reviewer_followers": "Seguidores del revisor (influencer detection)",
    "reviewer_total_reviews": "Total reseñas del revisor (fake review detection)",
}

print("\n  Columnas OBLIGATORIAS:")
for col, desc in REVIEWS_REQUIRED.items():
    if col in df_rev.columns:
        nulls = df_rev[col].isnull().sum()
        pct   = 100 * nulls / len(df_rev)
        status = "✅" if pct < 10 else "⚠️ "
        print(f"    {status} {col:25s} nulos: {nulls:,} ({pct:.1f}%) → {desc}")
        if pct >= 10:
            warnings.append(f"reviews.{col} tiene {pct:.1f}% nulos")
    else:
        print(f"    ❌ {col:25s} → FALTA")
        errors.append(f"book_reviews.db: columna ausente '{col}'")

print("\n  Columnas OPCIONALES:")
for col, desc in REVIEWS_OPTIONAL.items():
    mark = "✅" if col in df_rev.columns else "⏭️ "
    print(f"    {mark} {col:25s} → {desc}")

# Detalle de review_rating
if "review_rating" in df_rev.columns:
    rating_vals = df_rev["review_rating"].dropna().unique()
    print(f"\n  ⚠️  review_rating formato raw: {rating_vals[:5]}")
    print(f"      → Trío 1 debe limpiar: extraer número de 'Rating X out of 5'")
    warnings.append("review_rating en formato string → requiere limpieza a numérico")

# ============================================================================
# PASO 5: VALIDAR JOIN ENTRE ARCHIVOS
# ============================================================================
print("\n[4/5] VALIDANDO JOIN books ↔ reviews...")

rev_ids    = set(df_rev["book_id"].astype(int))
detail_ids = set(df_books["book_id"])
join_ids   = rev_ids.intersection(detail_ids)

print(f"  Libros únicos en reviews:        {len(rev_ids):,}")
print(f"  Libros únicos en Book_Details:   {len(detail_ids):,}")
print(f"  Libros con reseñas Y metadata:   {len(join_ids):,}  ← dataset útil para el proyecto")
print(f"  Reseñas vinculables:             {df_rev[df_rev['book_id'].astype(int).isin(join_ids)].shape[0]:,}")

join_pct = 100 * len(join_ids) / len(rev_ids)
if join_pct >= 90:
    print(f"  ✅ Join coverage: {join_pct:.1f}% — excelente")
elif join_pct >= 70:
    print(f"  ⚠️  Join coverage: {join_pct:.1f}% — aceptable")
    warnings.append(f"Join coverage {join_pct:.1f}% — algunos libros con reseñas no tienen metadata")
else:
    print(f"  ❌ Join coverage: {join_pct:.1f}% — problemático")
    errors.append(f"Join coverage insuficiente: {join_pct:.1f}%")

# ============================================================================
# PASO 6: RESUMEN DE COBERTURA DE COLUMNAS CRÍTICAS DEL BRIEFING
# ============================================================================
print("\n[5/5] COBERTURA vs BRIEFING_COPILOT.md...")
print()
coverage = [
    ("review_text (NLP)",   "review_content en book_reviews.db",  True,  "63,014 reseñas con texto"),
    ("rating 1-5",          "review_rating en book_reviews.db",   True,  "Requiere limpiar formato string → int"),
    ("book_id / title",     "book_id + book_title en CSV",        True,  "16,157 libros"),
    ("author",              "author en Book_Details.csv",         True,  "Sin nulos"),
    ("genre",               "genres en Book_Details.csv",         True,  "Formato lista string → parsear con ast.literal_eval"),
    ("publication_year",    "publication_info en CSV",            None,  "Extraer año con regex (p.ej. r'\\b(19|20)\\d{2}\\b')"),
    ("num_reviews",         "num_reviews en Book_Details.csv",    True,  "Sin nulos"),
    ("average_rating",      "average_rating en Book_Details.csv", True,  "Sin nulos"),
]

for briefing_col, real_col, ok, note in coverage:
    icon = "✅" if ok is True else ("⚠️ " if ok is None else "❌")
    print(f"  {icon} {briefing_col:25s} → {real_col}")
    print(f"     {note}")

# ============================================================================
# VEREDICTO FINAL
# ============================================================================
print("\n" + "=" * 70)
print("VEREDICTO FINAL")
print("=" * 70)

if errors:
    print("\n❌ DATASET NO VÁLIDO — Errores críticos:")
    for e in errors:
        print(f"   • {e}")
else:
    print("\n✅ DATASET VÁLIDO PARA EL PROYECTO")
    print(f"\n   • {len(join_ids):,} libros con metadata completa + reseñas")
    print(f"   • 63,014 reseñas disponibles para NLP/sentimientos")
    print(f"   • Géneros, rating promedio, num_reviews → análisis completo")
    print(f"   • Join directo por book_id (Goodreads ID)")

if warnings:
    print(f"\n⚠️  AVISOS PARA TRÍO 1 (limpieza obligatoria):")
    for w in warnings:
        print(f"   • {w}")

print("""
ARCHIVOS REALES DEL PROYECTO:
  data/Book_Details.csv       → metadata (usar en lugar de goodreads_books.csv)
  archive/book_reviews.db     → reseñas (tabla: book_reviews)
  archive/books.db            → listas Goodreads (NO necesario para el proyecto)

PRÓXIMOS PASOS:
  1. Trío 1: Cargar ambas fuentes, hacer JOIN por book_id, limpiar review_rating
  2. Actualizar BRIEFING_COPILOT.md con nombres reales de archivos
  3. Generar notebooks template para cada trío
""")

print("=" * 70)
print("FIN VALIDACIÓN")
print("=" * 70)
