# 📚 Sistema de Recomendación de Libros

**Status:** ⚠️ En desarrollo — Backend incompleto

---

## Descripción del Proyecto

Sistema ML que recomienda libros basado en análisis de sentimientos emocionales extraídos de 63K+ reseñas de Goodreads.

**Objetivo:** Descubrir libros con alto impacto emocional que los algoritmos estándar no ranking apropiadamente.

**Scope:** 
- Dataset: 16,225 libros | 63,014 reviews
- NLP: BERT para clasificación de emociones (6 clases)
- ML: K-means clustering + cosine similarity
- Frontend: React app para consultas
- Backend: FastAPI API

---

## Estado Actual

### ✅ Completo
- **Frontend:** React 18 con componentes funcionales, UI responsiva
- **Infraestructura:** Docker + docker-compose, dataset cargado, dependencias configuradas
- **API base:** FastAPI con endpoints definidos

### ⚠️ Incompleto
- **Backend:** Dos funciones críticas sin implementar en `backend/main.py`

---

## Qué Falta

**Backend `main.py` - Dos funciones críticas:**

```python
def analyze_sentiment(book_title: str) -> dict:
    """
    TODO: Implementar
    - Cargar dataset
    - Buscar reviews del libro
    - BERT inference → 6 emociones
    - Retornar profile emocional
    """
    
def find_similar_books(sentiment_profile: dict) -> list:
    """
    TODO: Implementar
    - K-means clustering
    - Cosine similarity search
    - Retornar TOP 5 recomendaciones
    """
```

---

## Setup

### Local (recomendado para desarrollo)
```bash
# Terminal 1
cd .
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd backend
python -m uvicorn main:app --reload

# Terminal 2
cd frontend
npm install
npm start
```

### Docker (opcional, para entorno reproducible)
```bash
docker-compose up
```

---

## Estructura

```
.
├── backend/
│   ├── main.py               # API FastAPI (TODO: implementar análisis)
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   └── App.css
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── data/
│   ├── Book_Details.csv
├── archive/
│   └── book_reviews.db
├── requirements.txt          # Dependencias Python únicas del proyecto
└── docs/
    ├── ARQUITECTURA.md
    └── NOTAS_DEL_UNICORNIO.md
```

---

## API

### POST /recommend

**Request:**
```json
{
  "title": "The Midnight Library",
  "description": "Un libro que cambió mi vida"
}
```

**Response (actual - mock):**
```json
{
  "original_book": "The Midnight Library",
  "recommendations": [
    {
      "title": "Piranesi",
      "author": "Susanna Clarke",
      "sentiment_score": 0.78,
      "reason": "Impacto emocional similar"
    }
  ],
  "analysis_summary": "..."
}
```

**Response (deseado):** Mismo formato pero con análisis real de BERT.

---

## Stack

- **Backend:** Python 3.13 + FastAPI
- **Frontend:** React 18
- **ML:** BERT (Transformers) + scikit-learn
- **Data:** Pandas + NumPy
- **DevOps:** Docker

---

## Documentación

- `docs/BRIEF_PARA_ESTUDIANTES.md` — Primeros pasos, troubleshooting, ayuda práctica
- `docs/ARQUITECTURA.md` — Flujo de datos técnico y qué implementar
- `docs/NOTAS_DEL_UNICORNIO.md` — Warnings y timeline realista

---

## Notes

- Dataset: 16K libros, 63K reviews (SQLite + CSV)
- BERT inference puede ser lento (considerar quantization para prod)
- Frontend espera response en formato exacto especificado arriba
- Docker usa port mapping 8000:8000 (backend) y 3000:3000 (frontend)
