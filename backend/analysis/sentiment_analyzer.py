import pandas as pd
from typing import Dict
import os
from transformers import pipeline  # ← SIEMPRE AL PRINCIPIO

# ============================================
# CONFIGURACIÓN
# ============================================

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data')
EMOTIONS = ['joy', 'sadness', 'fear', 'surprise', 'anger', 'disgust']

# Cargamos el modelo UNA SOLA VEZ al importar el archivo
'''
print("Cargando modelo BERT... (solo la primera vez)")
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)
print("✅ Modelo cargado")
'''
emotion_classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# ============================================
# FUNCIONES HELPER
# ============================================

def load_book_reviews(book_title: str) -> pd.DataFrame:
    df = pd.read_csv(f"{DATA_PATH}/Book_Details.csv")
    df_reviews = pd.read_csv(f"{DATA_PATH}/reviews_clean.csv")

    book_match = df[df['book_title'].str.lower() == book_title.lower()]

    # Cruzar con reviews
    book_ids = book_match['book_id'].tolist()
    book_reviews = df_reviews[df_reviews['book_id'].isin(book_ids)]

  
    if len(book_reviews) == 0:
        raise ValueError(f"No se encontró el libro: '{book_title}'")

    print(f"✅ Encontradas {len(book_reviews)} reviews para '{book_title}'")
    return book_reviews


def apply_bert_to_reviews(reviews: pd.Series) -> pd.DataFrame:
    classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )

    emotion_labels = EMOTIONS

    results = pd.DataFrame(columns=EMOTIONS)

    for review in reviews:
        output = classifier(
            review,
            candidate_labels=emotion_labels,
            multi_label=False
        )

        row = {label: 0.0 for label in emotion_labels}
        for label, score in zip(output["labels"], output["scores"]):
            row[label] = score

        results.loc[len(results)] = row

    return results


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
    joy     = emotion_df.get('joy',      pd.Series([0])).mean()
    surprise = emotion_df.get('surprise', pd.Series([0])).mean()
    profile['average_sentiment'] = round(float((joy + surprise) / 2), 4)

    return profile


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def analyze_sentiment(book_title: str, test_mode: bool = False) -> Dict[str, float]:
    """
    Analiza qué emociones genera un libro.
    """
    print(f"\n📚 Analizando: '{book_title}'")

    # 1. Cargar reviews del libro
    reviews = load_book_reviews(book_title)

    if len(reviews) < 3:
        raise ValueError(f"'{book_title}' tiene menos de 3 reviews, perfil poco fiable")

    # 2. Modo test: solo procesa 10 reviews para verificar que funciona
    if test_mode:
        reviews = reviews.head(10)
        print(f"⚠️  MODO TEST: procesando solo {len(reviews)} reviews")

    # 3. Aplicar BERT
    print(f"🤖 Aplicando BERT a {len(reviews)} reviews...")
    emotion_scores = apply_bert_to_reviews(reviews['review_content'])

    # 4. Agregar en perfil único
    profile = aggregate_emotion_scores(emotion_scores)

    print(f"\n✅ Perfil emocional de '{book_title}':")
    for emotion, score in profile.items():
        barra = "█" * int(score * 20)
        print(f"   {emotion:<20} {barra} ({score:.2f})")

    return profile


# ============================================
# DEBUGGING / TESTING
# ============================================

if __name__ == "__main__":
    # test_mode=True para probar solo con 10 reviews
    result = analyze_sentiment("The Midnight Library", test_mode=True)
    print("\nPerfil emocional:", result)

    # Cuando esté verificado, cambiar a test_mode=False
    # result = analyze_sentiment("The Midnight Library", test_mode=False)