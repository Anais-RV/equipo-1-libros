import pandas as pd
from typing import Dict
import os
from transformers import pipeline  # ← SIEMPRE AL PRINCIPIO
from rapidfuzz import process, fuzz

# ============================================
# CONFIGURACIÓN
# ============================================

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data')
EMOTIONS = ['joy', 'sadness', 'fear', 'surprise', 'anger', 'disgust']

# Umbral mínimo de similitud para fuzzy matching (0-100)
FUZZY_THRESHOLD = 70

# Cargamos el modelo UNA SOLA VEZ al importar el archivo
print("Cargando modelo BERT... (solo la primera vez)")
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)
print("✅ Modelo cargado")


# ============================================
# FUZZY SEARCH
# ============================================

def fuzzy_find_book(query: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Busca un libro por título o por autor usando fuzzy matching
    (tolerante a errores tipográficos y sin distinción de mayúsculas).

    Devuelve las filas del DataFrame que coincidan.
    """
    query = query.strip()

    # --- 1. Búsqueda por título ---
    titles = df['book_title'].dropna().unique().tolist()
    best_title = process.extractOne(
        query,
        titles,
        scorer=fuzz.token_sort_ratio,   # robusto ante palabras reordenadas
        score_cutoff=FUZZY_THRESHOLD
    )

    if best_title:
        matched_title, score, _ = best_title
        print(f"📖 Título encontrado: '{matched_title}' (similitud: {score}%)")
        return df[df['book_title'].str.lower() == matched_title.lower()]

    # --- 2. Búsqueda por autor (si no encontró título) ---
    if 'author' in df.columns:
        authors = df['author'].dropna().unique().tolist()
        best_author = process.extractOne(
            query,
            authors,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=FUZZY_THRESHOLD
        )

        if best_author:
            matched_author, score, _ = best_author
            print(f"✍️  Autor encontrado: '{matched_author}' (similitud: {score}%)")
            return df[df['author'].str.lower() == matched_author.lower()]

    # --- 3. Sin coincidencias ---
    return pd.DataFrame()


# ============================================
# FUNCIONES HELPER
# ============================================

def load_book_reviews(query: str) -> tuple[pd.DataFrame, str]:
    """
    Carga las reviews de un libro buscando por título o autor.
    Devuelve (reviews_df, nombre_encontrado).
    """
    df = pd.read_csv(f"{DATA_PATH}/books_clean.csv")
    df_reviews = pd.read_csv(f"{DATA_PATH}/reviews_clean.csv")

    # Fuzzy search sobre el catálogo
    book_match = fuzzy_find_book(query, df)

    if book_match.empty:
        # Sugerimos las 3 opciones más parecidas para ayudar al usuario
        titles = df['book_title'].dropna().unique().tolist()
        suggestions = process.extract(
            query,
            titles,
            scorer=fuzz.token_sort_ratio,
            limit=3
        )
        hint = ", ".join(f"'{s[0]}'" for s in suggestions)
        raise ValueError(
            f"No se encontró '{query}' en el catálogo.\n"
            f"   ¿Quisiste decir? → {hint}"
        )

    # Nombre canónico para los mensajes
    found_name = book_match['book_title'].iloc[0]

    # Cruzar con reviews
    book_ids = book_match['book_id'].tolist()
    book_reviews = df_reviews[df_reviews['book_id'].isin(book_ids)]

    if len(book_reviews) == 0:
        raise ValueError(f"Se encontró '{found_name}' pero no tiene reviews disponibles.")

    print(f"✅ Encontradas {len(book_reviews)} reviews para '{found_name}'")
    return book_reviews, found_name


def apply_bert_to_reviews(reviews: pd.Series) -> pd.DataFrame:
    results = []

    for review in reviews:
        
        output = emotion_classifier(
            review,
            truncation = True,
            max_length = 512)   # BERT tiene límite de tokens
        row = {item['label']: item['score'] for item in output[0]}
        results.append(row)
        
     
    return pd.DataFrame(results).fillna(0.0)


def aggregate_emotion_scores(emotion_df: pd.DataFrame) -> Dict[str, float]:
    """
    Agrega los scores de emociones de todas las reviews en un perfil único.
    """
    profile = {}

    for emotion in EMOTIONS:
        if emotion in emotion_df.columns:
            profile[emotion] = round(float(emotion_df[emotion].mean()), 4)
        else:
            profile[emotion] = 0.0

    # El modelo j-hartmann también devuelve 'neutral', la incluimos si existe
    if 'neutral' in emotion_df.columns:
        profile['neutral'] = round(float(emotion_df['neutral'].mean()), 4)

    # Sentiment general: media entre joy y surprise (emociones positivas)
    joy      = emotion_df.get('joy',      pd.Series([0])).mean()
    surprise = emotion_df.get('surprise', pd.Series([0])).mean()
    profile['average_sentiment'] = round(float((joy + surprise) / 2), 4)

    return profile


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def analyze_sentiment(query: str, test_mode: bool = False) -> Dict[str, float]:
    """
    Analiza qué emociones genera un libro.
    Acepta el título con errores tipográficos o el nombre del autor.
    """
    print(f"\n📚 Buscando: '{query}'")

    # 1. Cargar reviews (con fuzzy search incluido)
    reviews, found_name = load_book_reviews(query)

    if len(reviews) < 3:
        raise ValueError(f"'{found_name}' tiene menos de 3 reviews, perfil poco fiable")

    # 2. Modo test: solo procesa 10 reviews para verificar que funciona
    if test_mode:
        reviews = reviews.head(10)
        print(f"⚠️  MODO TEST: procesando solo {len(reviews)} reviews")

    # 3. Aplicar BERT
    print(f"🤖 Aplicando BERT a {len(reviews)} reviews...")
    emotion_scores = apply_bert_to_reviews(reviews['review_content'])

    # 4. Agregar en perfil único
    profile = aggregate_emotion_scores(emotion_scores)

    print(f"\n✅ Perfil emocional de '{found_name}':")
    for emotion, score in profile.items():
        barra = "█" * int(score * 20)
        print(f"   {emotion:<20} {barra} ({score:.2f})")

    return profile


# ============================================
# DEBUGGING / TESTING
# ============================================

if __name__ == "__main__":
    # Pruebas con errores tipográficos intencionales
    result = analyze_sentiment("Zodiak", test_mode=True)  # sin guion
    result = analyze_sentiment("Heydi", test_mode=True)                     # typo
    result = analyze_sentiment("Jack Canfield", test_mode=True)                             # por autor