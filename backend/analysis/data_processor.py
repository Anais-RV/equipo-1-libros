"""
🦄 Data Processor - Lidiando con la data SUCIA

Aquí es donde descubrís por qué el "data cleaning" es el 80% del trabajo.

El dataset tiene:
- Book_Details.csv: 16,225 libros (más o menos limpios)
- book_reviews.db: 63,014 reviews (SUCIAS. Muy sucias.)

La realidad de las reviews:
- Emojis raros: 🤪🎪👻🍆🔞 (sí, eso)
- Idiomas mezclados: "Great book! Me encantó 5/5 ⭐️ 很好"
- Bots: "5 stars" repetido 100 veces
- Nulls, vacías, caracteres especiales
- Spam, publicidad, reviews trolles

Tu misión:
1. Cargar dataset
2. Remover basura
3. Dejar reviews usables para BERT

Estimación realista:
- Entrada: 63,014 reviews
- Salida: ~55,000-60,000 (perdemos 5-12%)
- Es NORMAL. No es tu culpa.

Si pierdes el 50%+, algo está muy mal.
"""

import pandas as pd
import sqlite3
import os
from typing import Tuple
import re

# ============================================
# CONFIGURACIÓN
# ============================================

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data')
ARCHIVE_PATH = os.path.join(os.path.dirname(__file__), '../../archive')
BOOKS_CSV = os.path.join(DATA_PATH, 'Book_Details.csv')
REVIEWS_DB = os.path.join(ARCHIVE_PATH, 'book_reviews.db')

# ============================================
# FUNCIONES HELPER
# ============================================

def clean_text(text: str) -> str:
    """
    Limpia texto de review para procesamiento.

    Operaciones:
    - Convertir a minúsculas
    - Remover URLs
    - Remover caracteres especiales
    - Remover espacios múltiples
    - Remover emojis (opcional)

    Args:
        text: Texto crudo de review

    Returns:
        Texto limpio

    Nota:
        Los estudiantes pueden mejorar:
        - Traducir a inglés (BERT está entrenado en inglés)
        - Remover stopwords
        - Lemmatización/stemming
        - Manejo de emojis (a veces son informativos)
    """
    if not isinstance(text, str):
        return ""

    # Convertir a minúsculas
    text = text.lower()

    # Remover URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remover emojis
    text = re.sub(r'[^\w\s]', ' ', text)

    # Remover espacios múltiples
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def validate_review(review_text: str, min_length: int = 10) -> bool:
    """
    Valida si una review es usable para análisis.

    Criterios:
    - No vacía
    - Longitud mínima (10 caracteres)
    - No es spam/bot

    Args:
        review_text: Texto de review
        min_length: Longitud mínima aceptada

    Returns:
        True si la review es válida

    Nota:
        Los estudiantes pueden mejorar:
        - Detectar spam/bots (reviews idénticas, patrones)
        - Detectar idioma (mantener solo inglés)
        - Score de relevancia
    """
    if not isinstance(review_text, str):
        return False

    if len(review_text.strip()) < min_length:
        return False

    # Más validaciones pueden ir aquí
    return True


# ============================================
# FUNCIONES PRINCIPALES
# ============================================

def load_dataset() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga el dataset completo (libros + reviews).

    Returns:
        Tuple: (books_df, reviews_df)

    books_df columns:
        - book_id
        - title
        - author
        - rating
        - publication_year
        - ...

    reviews_df columns:
        - review_id
        - book_id
        - review_text
        - rating
        - date
        - ...

    Raises:
        FileNotFoundError: Si no existen los archivos

    Nota:
        Los estudiantes deben:
        1. Explorar estructura del dataset
        2. Usar .head(), .info(), .describe()
        3. Identificar columnas relevantes
        4. Detectar valores nulos
    """
    # TODO: Implementar carga
    # Sugerencia:
    # books = pd.read_csv(BOOKS_CSV)
    # Opción A: CSV
    # reviews = pd.read_csv(os.path.join(DATA_PATH, 'reviews.csv'))
    # Opción B: SQLite
    # conn = sqlite3.connect(REVIEWS_DB)
    # reviews = pd.read_sql("SELECT * FROM reviews", conn)
    pass


def preprocess_reviews(
    reviews_df: pd.DataFrame,
    min_review_length: int = 10
) -> pd.DataFrame:
    """
    Limpia y valida reviews.

    Operaciones:
    1. Remover filas con review_text nulo
    2. Limpiar texto (clean_text)
    3. Validar longitud mínima
    4. Remover duplicados

    Args:
        reviews_df: DataFrame con reviews crudas
        min_review_length: Longitud mínima de review

    Returns:
        DataFrame limpio

    Estadísticas esperadas:
        - Entrada: 63,014 reviews
        - Salida: ~55,000-60,000 reviews (después de limpiar)
        - Porcentaje de pérdida: ~5-12% (normal)

    Nota:
        Los estudiantes deben:
        1. Explorar qué se descarta (por qué?)
        2. Documentar cambios
        3. Considerar impacto en análisis
    """
    # TODO: Implementar limpieza
    # Sugerencia:
    # 1. df = reviews_df[reviews_df['review_text'].notna()].copy()
    # 2. df['review_text'] = df['review_text'].apply(clean_text)
    # 3. df = df[df['review_text'].apply(validate_review)]
    # 4. df = df.drop_duplicates(subset=['review_text'])
    pass


def get_book_stats(books_df: pd.DataFrame, reviews_df: pd.DataFrame) -> dict:
    """
    Calcula estadísticas del dataset.

    Args:
        books_df: DataFrame de libros cargado desde Book_Details.csv
        reviews_df: DataFrame de reviews cargado desde book_reviews.db

    Returns:
        Dict con:
        - total_books: número total de libros
        - total_reviews: número total de reviews
        - avg_reviews_per_book: media de reviews por libro
        - books_with_no_reviews: libros sin ninguna review
        - null_reviews: reviews con texto nulo
        - date_range: rango de fechas de las reviews (si existe la columna)
        - rating_distribution: conteo de reviews por puntuación
        - avg_rating: puntuación media de las reviews
    """
    avg_reviews = len(reviews_df) / len(books_df) if len(books_df) > 0 else 0

    # Columnas que pueden variar según el dataset de Kaggle
    review_text_col = next((c for c in ['review_text', 'review'] if c in reviews_df.columns), None)
    rating_col = next((c for c in ['review_rating', 'rating'] if c in reviews_df.columns), None)
    date_col = next((c for c in ['review_date', 'date'] if c in reviews_df.columns), None)
    book_id_col = next((c for c in ['book_id', 'id'] if c in reviews_df.columns), None)

    stats = {
        "total_books": len(books_df),
        "total_reviews": len(reviews_df),
        "avg_reviews_per_book": round(avg_reviews, 2),
        "books_with_no_reviews": (
            len(books_df) - reviews_df[book_id_col].nunique()
            if book_id_col else "N/A (columna book_id no encontrada)"
        ),
        "null_reviews": (
            int(reviews_df[review_text_col].isna().sum())
            if review_text_col else "N/A (columna review_text no encontrada)"
        ),
    }

    if date_col:
        stats["date_range"] = {
            "min": str(reviews_df[date_col].min()),
            "max": str(reviews_df[date_col].max()),
        }

    if rating_col:
        stats["rating_distribution"] = (
            reviews_df[rating_col].value_counts().sort_index().to_dict()
        )
        stats["avg_rating"] = round(reviews_df[rating_col].mean(), 2)

    return stats


# ============================================
# DEBUGGING / TESTING
# ============================================

if __name__ == "__main__":
    # Test local
    print("Cargando dataset...")
    books, reviews = load_dataset()

    print(f"Books shape: {books.shape}")
    print(f"Reviews shape: {reviews.shape}")
    print("\nBooks columns:", books.columns.tolist())
    print("\nReviews columns:", reviews.columns.tolist())

    print("\nLimpiando reviews...")
    reviews_clean = preprocess_reviews(reviews)
    print(f"Reviews después de limpiar: {reviews_clean.shape}")

    print("\nEstadísticas...")
    stats = get_book_stats(books, reviews_clean)
    print(stats)
