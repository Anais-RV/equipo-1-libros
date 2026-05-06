"""
🦄 Sentiment Analyzer - El corazón del análisis

Aquí es donde pasa la magia (y el marron). BERT te va a analizar
63K reviews buscando 6 emociones.

ADVERTENCIA: BERT es lento. Muy lento. Como una tortuga en invierno.
- 1 review = 1-2 segundos
- 200 reviews = 3-6 minutos
- No hagas esto on-demand o los usuarios se harán viejos esperando

SOLUCIÓN: Cachear. Ver cache_manager.py.

Emociones que detecta BERT:
- joy (alegría)
- sadness (tristeza)
- fear (miedo)
- surprise (sorpresa)
- anger (ira)
- disgust (repulsión)

Retorna un dict como este:
{
    "joy": 0.75,
    "sadness": 0.2,
    "fear": 0.1,
    "surprise": 0.65,
    "anger": 0.05,
    "disgust": 0.08,
    "average_sentiment": 0.64
}
"""

import pandas as pd
from typing import Dict
import os

# ============================================
# CONFIGURACIÓN
# ============================================

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data')
EMOTIONS = ['joy', 'sadness', 'fear', 'surprise', 'anger', 'disgust']

# ============================================
# FUNCIONES HELPER
# ============================================

def load_book_reviews(book_title: str) -> pd.DataFrame:
    """
    Carga las reviews de un libro específico del dataset.

    Args:
        book_title: Título del libro a buscar

    Returns:
        DataFrame con reviews del libro

    Nota:
        Los estudiantes pueden mejorar:
        - Búsqueda fuzzy (por si el título no es exacto)
        - Case-insensitive search
        - Búsqueda por autor también
    """
    # TODO: Implementar carga del dataset
    # Sugerencia: Usar pandas.read_csv() o sqlite3
    # df = pd.read_csv(f"{DATA_PATH}/Book_Details.csv")
    # book_reviews = df[df['title'].str.lower() == book_title.lower()]
    pass


def apply_bert_to_reviews(reviews: pd.Series) -> pd.DataFrame:
    """
    Aplica modelo BERT pre-entrenado para detectar emociones en cada review.

    Args:
        reviews: Series de textos (reviews)

    Returns:
        DataFrame con scores de 6 emociones para cada review

    Nota:
        Los estudiantes deben:
        - Cargar modelo BERT (transformers library)
        - Hacer inference en cada review (puede ser lento!)
        - Retornar dataframe con columnas: joy, sadness, fear, surprise, anger, disgust
        - Considerar batching para optimizar

    Ejemplo esperado:
        review_text                          joy  sadness  fear  ...
        "This book changed my life!"        0.9   0.1    0.0
        "I couldn't finish it"              0.2   0.8    0.3
    """
    # TODO: Implementar BERT inference
    # Sugerencia: from transformers import pipeline
    # classifier = pipeline("zero-shot-classification")
    # Para cada review, clasificar en las 6 emociones
    pass


def aggregate_emotion_scores(emotion_df: pd.DataFrame) -> Dict[str, float]:
    """
    Agrega los scores de emociones de todas las reviews en un perfil único.

    Args:
        emotion_df: DataFrame con scores de emociones por review

    Returns:
        Dict con promedio de cada emoción

    Ejemplo:
        {
            "joy": 0.75,
            "sadness": 0.25,
            ...
            "average_sentiment": 0.65
        }

    Nota:
        Los estudiantes pueden mejorar:
        - Weighted average (dar más peso a reviews con más votos)
        - Mediana en lugar de media (más robusta a outliers)
        - Standard deviation (qué tan consistentes son los sentimientos)
    """
    # TODO: Implementar agregación
    # Sugerencia: emotion_df.mean()
    pass


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def analyze_sentiment(book_title: str) -> Dict[str, float]:
    """
    Analiza qué emociones genera un libro.

    Flujo:
    1. Buscar las reviews del libro (pueden ser 10 o 200, depende)
    2. Pasar cada una por BERT (LENTO)
    3. Promediar los 6 scores emocionales
    4. Retornar perfil único del libro

    Args:
        book_title: Título exacto del libro

    Returns:
        Dict con 6 emociones + promedio. Ejemplo:
        {
            "joy": 0.75,
            "sadness": 0.2,
            "fear": 0.1,
            "surprise": 0.65,
            "anger": 0.05,
            "disgust": 0.08,
            "average_sentiment": 0.64
        }

    Raises:
        ValueError: "The Midnight Library" no existe o tiene <10 reviews
        Exception: BERT explota (GPU sin memoria, model no cargado, etc.)

    ⚠️ ADVERTENCIAS:
    - BERT tarda 1-2 segundos POR REVIEW
    - 200 reviews = 3-6 MINUTOS (sin caché)
    - Así que: CACHEA TODO con cache_manager.py
    - Si no cacheas, tu demo tardará 10 minutos en cargar

    💡 CONSEJOS:
    1. Primero: load_dataset() → entiende qué columnas tienes
    2. Prueba con 5 reviews solo, no hagas 200 de golpe
    3. print() es tu amigo. Verás dónde se cuelga
    4. Try/except para reviews que rompen BERT
    5. Si BERT falla en medio, cachea lo que tengas + continúa

    🧠 TIPS TÉCNICOS:
    - Usa transformers.pipeline("zero-shot-classification")
    - Batch 5-10 reviews a la vez (más rápido que una por una)
    - Considera quantization o quantized models si tienes tiempo
    - GPU es 10x más rápido que CPU (si tienes)
    """
    # TODO: USTEDES IMPLEMENTAN ESTO
    print(f"[TODO] Analizando sentimientos de '{book_title}'")

    # Estructura esperada:
    # 1. reviews = load_book_reviews(book_title)
    # 2. if len(reviews) < 10: raise ValueError("Not enough reviews")
    # 3. emotion_scores = apply_bert_to_reviews(reviews['text'])
    # 4. profile = aggregate_emotion_scores(emotion_scores)
    # 5. return profile

    # PLACEHOLDER - Reemplazar con código real
    return {
        "joy": 0.75,
        "sadness": 0.2,
        "fear": 0.1,
        "surprise": 0.65,
        "anger": 0.05,
        "disgust": 0.08,
        "average_sentiment": 0.64
    }


# ============================================
# DEBUGGING / TESTING
# ============================================

if __name__ == "__main__":
    # Test local
    result = analyze_sentiment("The Midnight Library")
    print("Perfil emocional:", result)

    # Deberías ver algo como:
    # {
    #     "joy": 0.75,
    #     "sadness": 0.25,
    #     ...
    # }
