"""
🦄 Recommender - Motor de "libros parecidos"

Una vez que sabes qué emociones genera un libro,
busca otros 5 libros que generen CASI LAS MISMAS emociones.

Algoritmo básico:
1. Cargar perfiles de TODOS los 16K libros (pre-calculados)
2. Calcular qué tan parecido es cada uno al que buscas (cosine similarity)
3. Retornar los TOP 5 más parecidos

Cosine similarity:
- Compara dos vectores de 6 dimensiones (las 6 emociones)
- Retorna 0 (nada parecido) a 1 (idéntico)
- Es rápido (milisegundos)

⚠️ IMPORTANTE:
No puedes calcular TODOS los perfiles on-demand.
Son 16K libros × 3-6 minutos cada uno = MESES.

SOLUCIÓN:
1. Pre-calcula los perfiles (batch job, una sola vez)
2. Guarda en caché con cache_manager
3. Carga desde caché (rápido) cuando buscas

El frontend hace: "Busco X" → API carga caché en <100ms → retorna TOP 5
"""

import pandas as pd
import numpy as np
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import os

# ============================================
# CONFIGURACIÓN
# ============================================

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data')
EMOTIONS = ['joy', 'sadness', 'fear', 'surprise', 'anger', 'disgust']
TOP_N = 5

# ============================================
# FUNCIONES HELPER
# ============================================

def load_emotion_profiles() -> pd.DataFrame:
    """
    Carga perfiles emocionales pre-calculados de TODOS los libros.

    Returns:
        DataFrame con columnas: [book_id, title, author, joy, sadness, fear, surprise, anger, disgust]

    Nota importante:
        Estos perfiles deberían estar PRE-CALCULADOS (caché).
        Si no existen, la alternativa es calcularlos on-demand,
        pero eso es LENTO (sería analizar 16K libros = horas).

        Solución recomendada:
        1. Calcularlos una vez (batch job)
        2. Guardarlos en CSV/SQLite
        3. Cargarlos aquí

    TODO para estudiantes:
        - Crear script para pre-calcular perfiles
        - O implementar caché en cache_manager.py
    """
    # TODO: Implementar carga de perfiles
    # Sugerencia: pd.read_csv(f"{DATA_PATH}/emotion_profiles.csv")
    # O consultar base de datos: sqlite3, etc.
    pass


def normalize_profile(profile: Dict[str, float]) -> np.ndarray:
    """
    Normaliza un perfil emocional para cosine similarity.

    Args:
        profile: Dict con 6 emociones

    Returns:
        Array normalizado (tamaño 1)

    Nota:
        Cosine similarity requiere vectores normalizados.
        sklearn.preprocessing.normalize() hace esto automáticamente.
    """
    vector = np.array([profile[emotion] for emotion in EMOTIONS])
    # Normalizar: dividir por la magnitud
    magnitude = np.linalg.norm(vector)
    if magnitude == 0:
        return vector
    return vector / magnitude


def find_similar_profiles(
    input_profile: Dict[str, float],
    all_profiles: pd.DataFrame,
    method: str = "cosine"
) -> np.ndarray:
    """
    Calcula similitud emocional entre un perfil y todos los demás.

    Args:
        input_profile: Perfil emocional del libro buscado
        all_profiles: DataFrame con perfiles de todos los libros
        method: "cosine" o "euclidean"

    Returns:
        Array de similitudes (0 a 1)

    Algoritmo:
        Cosine similarity = cos(θ) entre dos vectores
        - 1.0 = idéntico
        - 0.0 = perpendicular (sin relación)
        - -1.0 = opuesto

    Nota:
        Los estudiantes pueden mejorar:
        - Usar Euclidean distance (es.sqrt de diferencias)
        - Weighted similarity (dar más peso a ciertas emociones)
        - Manhattan distance
    """
    # TODO: Implementar similitud
    # Sugerencia: from sklearn.metrics.pairwise import cosine_similarity
    # input_vector = normalize_profile(input_profile)
    # similarities = cosine_similarity([input_vector], all_vectors)[0]
    pass


def apply_clustering(
    all_profiles: pd.DataFrame,
    n_clusters: int = 10
) -> KMeans:
    """
    Agrupa libros similares en clusters (OPCIONAL).

    Args:
        all_profiles: DataFrame de perfiles
        n_clusters: Número de clusters

    Returns:
        Modelo KMeans entrenado

    Nota:
        Esto es OPCIONAL pero ayuda para:
        - Verificar que el clustering tiene sentido
        - Agrupar por "tipo" de libro (triste, alegre, etc.)
        - Futuro: filtros por cluster

    Mejor usar después de tener perfiles funcionales.
    """
    # TODO: Implementar clustering
    # Sugerencia: from sklearn.cluster import KMeans
    # vectors = all_profiles[EMOTIONS].values
    # kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    # kmeans.fit(vectors)
    pass


def rank_recommendations(
    similarities: np.ndarray,
    book_data: pd.DataFrame,
    top_n: int = 5
) -> List[Dict]:
    """
    Ordena libros por similitud y retorna TOP N.

    Args:
        similarities: Array de similitudes (una por libro)
        book_data: DataFrame con info de libros (title, author, etc.)
        top_n: Número de recomendaciones a retornar

    Returns:
        List of dicts con [title, author, sentiment_score, reason]

    Nota:
        Los estudiantes pueden mejorar:
        - Filtrar por popularity (no recomendar libros obscuros)
        - Diversidad (no recomendar 5 del mismo autor)
        - Rank múltiple (top N de cada cluster)
    """
    # TODO: Implementar ranking
    # Sugerencia:
    # 1. book_data['similarity'] = similarities
    # 2. book_data.sort_values('similarity', ascending=False)
    # 3. Retornar top_n
    pass


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def find_similar_books(
    sentiment_profile: Dict[str, float],
    num_recommendations: int = 5
) -> List[Dict]:
    """
    Encuentra los TOP 5 libros más parecidos emocionalmente.

    Entrada: Un perfil emocional (ej: {joy: 0.75, sadness: 0.2, ...})
    Salida: Los 5 libros con perfil más parecido

    Flujo:
    1. Cargar la base de datos de perfiles (caché)
    2. Convertir el perfil de entrada a vector (6 números)
    3. Calcular distancia coseno vs. todos los 16K libros
    4. Ordenar y retornar TOP 5

    Args:
        sentiment_profile: Dict como este:
            {
                "joy": 0.75,
                "sadness": 0.2,
                "fear": 0.1,
                "surprise": 0.65,
                "anger": 0.05,
                "disgust": 0.08
            }
        num_recommendations: Cuántos retornar (default 5)

    Returns:
        List de dicts:
        [
            {
                "title": "Piranesi",
                "author": "Susanna Clarke",
                "sentiment_score": 0.82,
                "reason": "Similar emotional profile"
            },
            ...
        ]

    ⚠️ CRÍTICO:
    - Necesitas perfiles pre-calculados para TODOS los libros
    - Si no los tienes, esto tardará HORAS
    - Solución: Batch job en Semana 3, guarda en caché, carga aquí

    💡 IMPLEMENTACIÓN PASO A PASO:
    1. load_emotion_profiles() → carga del caché (rápido)
    2. normalize_profile() → convierte dict a vector normalizado
    3. find_similar_profiles() → cosine_similarity
    4. rank_recommendations() → ordena y retorna TOP 5

    🧠 DEBUGGING:
    - print(f"Perfiles cargados: {all_profiles.shape}")
    - print(f"Similitudes: {similarities[:10]}")  # Deberían ser 0-1
    - print(f"Top 5 scores: {np.argsort(similarities)[-5:]}")
    - Si todos son ~0.5, algo está roto

    🎯 CHECKS FINALES:
    - ¿El TOP 1 tiene sense? (debería ser el libro más parecido)
    - ¿Los scores están entre 0 y 1? (si no, normalizate mal)
    - ¿Tardó menos de 100ms? (si tarda más, caché está roto)
    """
    # TODO: USTEDES IMPLEMENTAN ESTO
    print(f"[TODO] Encontrando libros similares...")

    # Estructura esperada:
    # 1. all_profiles = load_emotion_profiles()
    # 2. input_vector = normalize_profile(sentiment_profile)
    # 3. similarities = find_similar_profiles(sentiment_profile, all_profiles)
    # 4. recommendations = rank_recommendations(similarities, all_profiles, num_recommendations)
    # 5. return recommendations

    # PLACEHOLDER - Reemplazar con código real
    return [
        {
            "title": "Piranesi",
            "author": "Susanna Clarke",
            "sentiment_score": 0.82,
            "reason": "Alto impacto emocional similar"
        },
        {
            "title": "The House in the Cerulean Sea",
            "author": "TJ Klune",
            "sentiment_score": 0.78,
            "reason": "Mistura de alegría y contemplación"
        },
        {
            "title": "The Invisible Life of Addie LaRue",
            "author": "V.E. Schwab",
            "sentiment_score": 0.75,
            "reason": "Genera sorpresa y nostalgia"
        },
        {
            "title": "Circe",
            "author": "Madeline Miller",
            "sentiment_score": 0.71,
            "reason": "Reflexión y transformación personal"
        },
        {
            "title": "Mexican Gothic",
            "author": "Silvia Moreno-Garcia",
            "sentiment_score": 0.68,
            "reason": "Suspenso con toques de misterio"
        },
    ][:num_recommendations]


# ============================================
# DEBUGGING / TESTING
# ============================================

if __name__ == "__main__":
    # Test local
    test_profile = {
        "joy": 0.75,
        "sadness": 0.2,
        "fear": 0.1,
        "surprise": 0.65,
        "anger": 0.05,
        "disgust": 0.08,
    }

    recommendations = find_similar_books(test_profile, num_recommendations=5)
    print("Recomendaciones:", recommendations)

    # Deberías ver 5 libros ordenados por similitud
