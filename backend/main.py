"""
🦄 FastAPI Backend - Sistema de Recomendación de Libros

Estructura modular donde:
- analysis/ contiene la lógica ML (BERT, clustering, etc.)
- main.py orquesta y expone API REST

Los estudiantes implementan funciones en:
- analysis/sentiment_analyzer.py → analyze_sentiment()
- analysis/recommender.py → find_similar_books()
- analysis/data_processor.py → carga y limpieza
- analysis/cache_manager.py → persistencia

El frontend (React) consumirá: POST /recommend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Importar funciones de analysis
from analysis.sentiment_analyzer import analyze_sentiment
from analysis.recommender import find_similar_books
from analysis.cache_manager import CacheManager, cache_sentiment

# ============================================
# LOGGING
# ============================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# FASTAPI APP
# ============================================

app = FastAPI(
    title="🦄 Book Recommendation API",
    description="Sistema de recomendación basado en análisis de sentimientos emocionales",
    version="1.0.0"
)

# Permitir CORS para que frontend (localhost:3000) pueda acceder
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache manager
cache = CacheManager()

# ============================================
# MODELOS (Request/Response)
# ============================================

class BookInput(BaseModel):
    """Input: El usuario ingresa un libro que le encantó"""
    title: str
    description: str = "Un libro que me encantó"

class BookRecommendation(BaseModel):
    """Recomendación individual (uno de los TOP 5)"""
    title: str
    author: str
    sentiment_score: float
    reason: str

class RecommendationResponse(BaseModel):
    """Response: Las 5 recomendaciones + resumen"""
    original_book: str
    recommendations: list[BookRecommendation]
    analysis_summary: str

# ============================================
# ENDPOINTS
# ============================================

@app.get("/health")
def health_check():
    """
    Verifica que la API funciona.

    Returns:
        {"status": "ok"}
    """
    logger.info("Health check")
    return {
        "status": "ok",
        "message": "API funcionando correctamente",
        "version": "1.0.0"
    }

@app.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(book: BookInput):
    """
    ENDPOINT PRINCIPAL: Obtiene recomendaciones de libros

    Input:
        {
            "title": "The Midnight Library",
            "description": "Un libro que cambió mi vida"
        }

    Output:
        {
            "original_book": "The Midnight Library",
            "recommendations": [
                {
                    "title": "Piranesi",
                    "author": "Susanna Clarke",
                    "sentiment_score": 0.82,
                    "reason": "Similar emotional impact"
                },
                ...
            ],
            "analysis_summary": "..."
        }

    Flujo:
    1. Valida entrada
    2. Busca en caché (si existe)
    3. Analiza sentimientos del libro (analyze_sentiment)
    4. Encuentra libros similares (find_similar_books)
    5. Retorna top 5 recomendaciones

    Nota para estudiantes:
    - analyze_sentiment() está en analysis/sentiment_analyzer.py (TODO)
    - find_similar_books() está en analysis/recommender.py (TODO)
    - El caché evita recalcular (ver cache_manager.py)
    """

    # Validar entrada
    if not book.title or len(book.title.strip()) == 0:
        logger.warning("Intento de búsqueda con título vacío")
        raise HTTPException(
            status_code=400,
            detail="El título del libro no puede estar vacío"
        )

    try:
        logger.info(f"Procesando búsqueda: '{book.title}'")

        # Paso 1: Intentar obtener del caché
        cached_profile = cache.get_sentiment_profile(book.title)
        if cached_profile:
            logger.info(f"📦 Usando caché para '{book.title}'")
            sentiment_profile = cached_profile
        else:
            # Paso 2: Analizar sentimientos (LENTO)
            logger.info(f"⏳ Analizando sentimientos (sin caché)...")
            sentiment_profile = analyze_sentiment(book.title)
            # Guardar en caché para próxima vez
            cache.save_sentiment_profile(book.title, sentiment_profile)

        # Paso 3: Encontrar libros similares
        logger.info("Buscando libros similares...")
        recommendations = find_similar_books(sentiment_profile, num_recommendations=5)

        # Paso 4: Armar respuesta
        response = RecommendationResponse(
            original_book=book.title,
            recommendations=[
                BookRecommendation(**rec) for rec in recommendations
            ],
            analysis_summary=f"Se analizaron reviews de '{book.title}' para encontrar libros con impacto emocional similar basado en 6 emociones (joy, sadness, fear, surprise, anger, disgust)."
        )

        logger.info(f"✓ Recomendaciones obtenidas: {len(recommendations)} libros")
        return response

    except ValueError as e:
        logger.error(f"Validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error procesando recomendación: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al procesar recomendación: {str(e)}"
        )

@app.get("/data-info")
def get_data_info():
    """
    Información del dataset.

    Retorna:
        - total_books: Número de libros en el dataset
        - total_reviews: Número de reviews analizables
        - emotions: Las 6 emociones que se detectan
        - cache_status: Información del caché actual
    """
    stats = cache.get_cache_stats()

    return {
        "total_books": 16225,
        "total_reviews": 63014,
        "emotions": ["joy", "sadness", "fear", "surprise", "anger", "disgust"],
        "cache": {
            "cached_books": stats["cached_books"],
            "size_mb": f"{stats['total_size_mb']:.2f}"
        },
        "status": "Listo para análisis - Los estudiantes completan sentiment_analyzer.py y recommender.py"
    }

@app.get("/cache-stats")
def get_cache_stats():
    """
    Estadísticas del caché (para debugging).

    Útil para ver cuántos análisis se han cacheado.
    """
    stats = cache.get_cache_stats()
    return {
        "cached_books": stats["cached_books"],
        "total_size_mb": f"{stats['total_size_mb']:.2f}",
        "message": "Ver cache/sentiment_profiles.json para los detalles"
    }

@app.delete("/cache-clear")
def clear_cache():
    """
    Limpia el caché (CUIDADO: borra todos los análisis guardados).

    Útil si cambian el modelo BERT o quieren reanalizar.
    """
    cache.clear_all()
    logger.warning("Caché limpiado")
    return {"message": "Caché limpiado"}

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn
    logger.info("🦄 Iniciando API de Recomendación de Libros...")
    logger.info("Frontend: http://localhost:3000")
    logger.info("API: http://localhost:8000")
    logger.info("Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
