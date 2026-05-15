"""
============================================================
🦄 DATA PROCESSOR - VERSION PROFESIONAL
============================================================

Pipeline completo de limpieza para:

1. Book_Details.csv
2. book_reviews.db

Objetivos:
- Detectar idioma correctamente
- Separar inglés / no inglés
- Limpiar texto
- Detectar spam
- Eliminar duplicados
- Generar datasets limpios para BERT

Outputs:
- books_clean.csv
- books_non_english.csv
- reviews_clean.csv
- reviews_discarded.csv

============================================================
"""

# ============================================================
# IMPORTS
# ============================================================

import pandas as pd
import sqlite3
import os
import re

from typing import Tuple
from langdetect import detect, DetectorFactory, LangDetectException

# ============================================================
# CONFIGURACIÓN
# ============================================================

DetectorFactory.seed = 0

BASE_DIR = os.path.dirname(__file__)

DATA_PATH = os.path.join(BASE_DIR, "../../data")
ARCHIVE_PATH = os.path.join(BASE_DIR, "../../archive")

BOOKS_CSV = os.path.join(DATA_PATH, "Book_Details.csv")
REVIEWS_DB = os.path.join(ARCHIVE_PATH, "book_reviews.db")

OUTPUT_DIR = DATA_PATH



# ============================================================
# HELPERS
# ============================================================

def detect_language(text: str) -> str:
    """
    Detecta idioma de forma segura.

    Retorna:
    - en
    - es
    - fr
    - unknown
    """

    if not isinstance(text, str):
        return "unknown"

    text = text.strip()

    # Textos muy cortos fallan mucho
    if len(text) < 15:
        return "unknown"

    try:
        return detect(text)

    except LangDetectException:
        return "unknown"

    except Exception:
        return "unknown"


# ============================================================

def clean_text(text: str) -> str:
    """
    Limpieza de texto para NLP/BERT.
    """

    if not isinstance(text, str):
        return ""

    # lowercase
    text = text.lower()

    # remover URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # remover emails
    text = re.sub(r"\S+@\S+", " ", text)

    # remover emojis
    text = re.sub(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "]+",
        " ",
        text,
        flags=re.UNICODE
    )

    # dejar solo caracteres útiles
    text = re.sub(r"[^a-zA-Z0-9\s.,!?']", " ", text)

    # remover espacios múltiples
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================

def validate_review(text: str, min_length: int = 20):
    """
    Valida reviews.

    Returns:
    (True/False, reason)
    """

    if not isinstance(text, str):
        return False, "not_string"

    text = text.strip()

    if not text:
        return False, "empty"

    if len(text) < min_length:
        return False, "too_short"

    words = text.split()

    if len(words) < 4:
        return False, "too_few_words"

    # detectar spam repetitivo
    unique_ratio = len(set(words)) / len(words)

    if unique_ratio < 0.35:
        return False, "spam_pattern"

    return True, "valid"


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Carga libros y reviews.
    """

    print("\n📚 Cargando datasets...")

    if not os.path.exists(BOOKS_CSV):
        raise FileNotFoundError(f"No existe: {BOOKS_CSV}")

    if not os.path.exists(REVIEWS_DB):
        raise FileNotFoundError(f"No existe: {REVIEWS_DB}")

    # ========================================================
    # LIBROS
    # ========================================================

    books_df = pd.read_csv(BOOKS_CSV)

    # extraer año
    books_df["publication_year"] = (books_df["publication_info"].astype(str).str.extract(r"((?:19|20)\d{2})")[0].astype("Int64"))

    # ========================================================
    # REVIEWS
    # ========================================================

    conn = sqlite3.connect(REVIEWS_DB)

    reviews_df = pd.read_sql(
        "SELECT * FROM book_reviews",
        conn
    )

    conn.close()

    print(f"\n✅ Books loaded: {books_df.shape}")
    print(f"✅ Reviews loaded: {reviews_df.shape}")

    return books_df, reviews_df


# ============================================================
# BOOK PROCESSING
# ============================================================

def preprocess_books(
    books_df: pd.DataFrame
):

    print("\n================================================")
    print("📘 PROCESSING BOOKS")
    print("================================================")

    df = books_df.copy()

    # ========================================================
    # COMBINAR TEXTO
    # ========================================================

    df["combined_text"] = (
        df["book_title"].fillna("") + " " +
        df["book_details"].fillna("")
    )

    # ========================================================
    # DETECTAR IDIOMA
    # ========================================================

    print("\n🌍 Detectando idiomas de libros...")

    df["language"] = df["combined_text"].apply(
        detect_language
    )

    # ========================================================
    # FILTRAR INGLES
    # ========================================================

    english_books_df = df[
        df["language"] == "en"
    ].copy()

    non_english_books_df = df[
        df["language"] != "en"
    ].copy()

    # ========================================================
    # STATS
    # ========================================================

    print("\n📊 Estadísticas libros:")

    print(f"Total libros: {len(df)}")
    print(f"Libros en inglés: {len(english_books_df)}")
    print(f"No inglés: {len(non_english_books_df)}")

    print("\n🌍 Distribución idiomas:")

    print(df["language"].value_counts().head(10))

    print("\nLibros info:")
    df.info()
    print(f"\nLibros describe: {df.describe()}")

    return english_books_df, non_english_books_df


# ============================================================
# PROCESAR RESEÑAS
# ============================================================

def preprocess_reviews(
    reviews_df: pd.DataFrame
):

    print("\n================================================")
    print("🧹 PROCESAR RESEÑAS")
    print("================================================")

    df = reviews_df.copy()

    # ========================================================
    # ELIMINAR NULOS
    # ========================================================

    print("\n🗑 Eliminando reviews nulas...")

    df = df[
        df["review_content"].notna()
    ].copy()

    # ========================================================
    # DETECTAR IDIOMA
    # ========================================================

    print("\n🌍 Detectando idiomas...")

    df["language"] = df["review_content"].apply(
        detect_language
    )

    # ========================================================
    # SEPARAR INGLES / NO INGLES
    # ========================================================

    english_df = df[
        df["language"] == "en"
    ].copy()

    non_english_df = df[
        df["language"] != "en"
    ].copy()

    non_english_df["discard_reason"] = "non_english"

    # ========================================================
    # LIMPIAR TEXO
    # ========================================================

    print("\n🧼 Limpiando texto...")

    english_df["clean_review"] = english_df[
        "review_content"
    ].apply(clean_text)

    # ========================================================
    # DETECTAR PALABRAS SOSPECHOSAMENTE LARGAS
    # ========================================================

    print("\n🔎 Detectando palabras raras...")

    MAX_WORD_LENGTH = 25

    def detectar_palabras_raras(text):

        if not isinstance(text, str):
            return False
        words = text.split()

        for word in words:
           # quitar puntuación básica
            clean_word = re.sub(r"[^a-zA-Z]", "", word)

            if len(clean_word) > MAX_WORD_LENGTH:
                return True

        return False

    # marcar reviews sospechosas
    english_df["palabras_raras"] = english_df["clean_review"].apply(detectar_palabras_raras)

    # contar cuántas hay
    palabras_raras_count = english_df["palabras_raras"].sum()
    total_reviews = len(english_df)

    palabras_raras_porcentage = (
        palabras_raras_count / total_reviews * 100
        if total_reviews > 0 else 0
    )

    print(f"\n🧠 Reviews con palabras raras: {palabras_raras_count}")

    print(f"📊 Porcentaje: {palabras_raras_porcentage:.2f}%")

    # ========================================================
    # ELIMINAR REVIEWS CON PALABRAS RARAS
   #  ========================================================
    
    palabras_raras_df = english_df[english_df["palabras_raras"]].copy()
    palabras_raras_df["discard_reason"] = "palabras_raras"

    # mantener solo reviews limpias
    english_df = english_df[~english_df["palabras_raras"]].copy()

    # ========================================================
    # VALIDAR
    # ========================================================

    print("\n✅ Validando reviews...")

    validation_results = english_df[
        "clean_review"
    ].apply(validate_review)

    english_df["is_valid"] = validation_results.apply(
        lambda x: x[0]
    )

    english_df["discard_reason"] = validation_results.apply(
        lambda x: x[1]
    )

    # ========================================================
    # SEPARAR NO VALIDAS
    # ========================================================

    invalid_reviews_df = english_df[
        ~english_df["is_valid"]
    ].copy()

    valid_reviews_df = english_df[
        english_df["is_valid"]
    ].copy()

    # ========================================================
    # ELIMINAR DUPLICADOS
    # ========================================================

    print("\n🧬 Eliminando duplicados...")

    duplicated_mask = valid_reviews_df.duplicated(
        subset=["clean_review"],
        keep="first"
    )

    duplicates_df = valid_reviews_df[
        duplicated_mask
    ].copy()

    duplicates_df["discard_reason"] = "duplicate"

    valid_reviews_df = valid_reviews_df[
        ~duplicated_mask
    ]

    # ========================================================
    # CONCATENAR DESCARTADAS
    # ========================================================

    discarded_reviews_df = pd.concat([
        non_english_df,
        invalid_reviews_df,
        duplicates_df,
        palabras_raras_df
    ])

    # ========================================================
    # LIMPIEZA FINAL
    # ========================================================

    columns_to_drop = [
        "is_valid"
    ]

    valid_reviews_df = valid_reviews_df.drop(
        columns=columns_to_drop,
        errors="ignore"
    )

    # ========================================================
    # STATS
    # ========================================================

    print("\n📊 Estadísticas reviews:")

    print(f"Originales: {len(reviews_df)}")
    print(f"Válidas: {len(valid_reviews_df)}")
    print(f"Descartadas: {len(discarded_reviews_df)}")

    print("\n🗑 Razones descarte:")

    print(
        discarded_reviews_df["discard_reason"]
        .value_counts()
    )

    print("\n🌍 Distribución idiomas:")

    print(
        df["language"]
        .value_counts()
        .head(10)
    )
    
    print("\nReviews info:")
    df.info()
    print(f"\nReviews describe: {df.describe()}")

    return valid_reviews_df, discarded_reviews_df


# ============================================================
# SAVE FILES
# ============================================================

def save_dataframes(
    books_clean,
    books_non_english,
    reviews_clean,
    reviews_discarded
):
    """
    Guarda todos los CSVs.
    """

    print("\n💾 Guardando archivos...")

    books_clean.to_csv(
        os.path.join(OUTPUT_DIR, "books_clean.csv"),
        index=False,
        encoding="utf-8-sig"
    )

    books_non_english.to_csv(
        os.path.join(OUTPUT_DIR, "books_non_english.csv"),
        index=False,
        encoding="utf-8-sig"
    )

    reviews_clean.to_csv(
        os.path.join(OUTPUT_DIR, "reviews_clean.csv"),
        index=False,
        encoding="utf-8-sig"
    )

    reviews_discarded.to_csv(
        os.path.join(OUTPUT_DIR, "reviews_discarded.csv"),
        index=False,
        encoding="utf-8-sig"
    )

    print("\n✅ Archivos guardados correctamente")


# ============================================================
# STATS
# ============================================================

def get_stats(
    books_clean,
    reviews_clean
):

    print("\n================================================")
    print("📈 DATASET FINAL")
    print("================================================")

    print(f"📚 Books finales: {len(books_clean)}")
    print(f"📝 Reviews finales: {len(reviews_clean)}")

    avg_reviews = len(reviews_clean) / len(books_clean)

    print(f"⭐ Promedio reviews/libro: {avg_reviews:.2f}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # ========================================================
    # LOAD
    # ========================================================

    books_df, reviews_df = load_dataset()

    # ========================================================
    # PROCESS BOOKS
    # ========================================================

    books_clean, books_non_english = preprocess_books(
        books_df
    )

    # ========================================================
    # PROCESS REVIEWS
    # ========================================================

    reviews_clean, reviews_discarded = preprocess_reviews(
        reviews_df
    )

    # ========================================================
    # SAVE
    # ========================================================

    save_dataframes(
        books_clean,
        books_non_english,
        reviews_clean,
        reviews_discarded
    )

    # ========================================================
    # STATS
    # ========================================================

    get_stats(
        books_clean,
        reviews_clean
    )

    print("\n🎉 Pipeline completado correctamente")