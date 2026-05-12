"""
Servidor FastAPI mínimo para CI/CD health checks.

Este archivo REEMPLAZA main.py en entornos de integración continua.
No usa BERT, torch ni datasets reales — solo responde con mock data.

Endpoints disponibles:
    GET  /health     → estado del servidor
    GET  /           → info básica
    POST /recommend  → devuelve libros mock
"""

import json
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Book Recommendation API — CI Mode",
    description="Servidor stub para health checks en CI/CD. Sin ML.",
    version="ci"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar mock data desde el mismo directorio que este archivo
_HERE = os.path.dirname(os.path.abspath(__file__))
_MOCK_PATH = os.path.join(_HERE, "mock_books.json")

with open(_MOCK_PATH, encoding="utf-8") as _f:
    MOCK_BOOKS: list = json.load(_f)


# ────────────────────────────────────────
# Modelos
# ────────────────────────────────────────

class BookInput(BaseModel):
    title: str
    author: str = ""


# ────────────────────────────────────────
# Endpoints
# ────────────────────────────────────────

@app.get("/health")
def health():
    """Health check — usado por Docker y CI."""
    return {
        "status": "ok",
        "mode": "ci",
        "books_loaded": len(MOCK_BOOKS)
    }


@app.get("/")
def root():
    return {
        "message": "Book Recommendation API",
        "mode": "ci_stub",
        "status": "running",
        "docs": "/docs"
    }


@app.post("/recommend")
def recommend(book: BookInput):
    """Devuelve recomendaciones mock (sin ML real)."""
    return {
        "query": {
            "title": book.title,
            "author": book.author
        },
        "recommendations": MOCK_BOOKS,
        "mode": "ci_mock",
        "note": "Datos de prueba — el servidor real usa BERT"
    }
