# 🦄 Arquitectura Técnica

Del Unicornio que se piró. Esto explica cómo todo encaja y qué ustedes tienen que hacer.

---

## Cómo Funciona el Sistema

```
Usuario escribe "The Midnight Library"
    ↓
Frontend (React) → fetch POST /recommend
    ↓
Backend (FastAPI)
├─ analyze_sentiment(book_title)
│  ├─ Buscar reviews del libro
│  ├─ Aplicar BERT → 6 emociones
│  └─ Retornar perfil emocional
├─ find_similar_books(sentiment_profile)
│  ├─ K-means clustering
│  ├─ Cosine similarity
│  └─ Retornar TOP 5
    ↓
Backend devuelve JSON
    ↓
Frontend renderiza recomendaciones bonitas
```

---

## Backend (FastAPI + Python)

**Ubicación:** `backend/main.py`

### Endpoint POST /recommend

**Request:**
```json
{
  "title": "The Midnight Library",
  "description": "Un libro que me encantó"
}
```

**Response esperado:**
```json
{
  "original_book": "The Midnight Library",
  "recommendations": [
    {
      "title": "Piranesi",
      "author": "Susanna Clarke",
      "sentiment_score": 0.78,
      "reason": "Similar emotional impact"
    },
    ...
  ],
  "analysis_summary": "..."
}
```

### Funciones TODO

#### 1. `analyze_sentiment(book_title: str) -> dict`

**Qué recibe:** Título de un libro

**Qué hace:**
1. Buscar todas las reviews del libro en el dataset
2. Limpiar y procesar el texto de cada review
3. Pasar cada review por BERT
4. Extraer 6 emociones: joy, sadness, fear, surprise, anger, disgust
5. Agregar resultados (promedio/suma de scores)

**Qué retorna:**
```python
{
    "book_title": "The Midnight Library",
    "joy": 0.75,
    "sadness": 0.45,
    "fear": 0.10,
    "surprise": 0.65,
    "anger": 0.05,
    "disgust": 0.08
}
```

**Hints:**
- Usá pandas para buscar reviews en el dataset
- Transformers + BERT para clasificación (modelo pre-entrenado está en requirements.txt)
- Agregá resultados de forma sensata (promedio o weighted average)
- BERT es lento, considerá caching si hacés múltiples queries del mismo libro

#### 2. `find_similar_books(sentiment_profile: dict) -> list`

**Qué recibe:** Un perfil emocional (dict con 6 scores)

**Qué hace:**
1. Cargar los perfiles emocionales pre-calculados de TODOS los libros en el dataset
2. Usar cosine similarity para encontrar libros con perfiles similares
3. K-means clustering (opcional pero recomendado)
4. Retornar top 5

**Qué retorna:**
```python
[
    {
        "title": "Piranesi",
        "author": "Susanna Clarke",
        "sentiment_score": 0.78,
        "reason": "Similar emotional profile"
    },
    ...
]
```

**Hints:**
- Scikit-learn tiene `cosine_similarity()` y `KMeans`
- Normalizar los vectors antes de comparar
- El "sentiment_score" es cuánto de similar vs el libro input
- Si no tenés pre-calculados los perfiles de todos los libros, tenés que generarlos (heavy computation)

---

## Frontend (React 18)

**Ubicación:** `frontend/src/`

### Componentes

- **App.jsx** → Contenedor principal, maneja estado (recommendations, loading, error)
- **RecommendationForm.jsx** → Formulario para input del usuario
- **ResultsDisplay.jsx** → Muestra las 5 recomendaciones con scores
- **LoadingSpinner.jsx** → Loading state

### Cómo llama al backend

```javascript
// En App.jsx
const response = await fetch('http://localhost:8000/recommend', {
  method: 'POST',
  body: JSON.stringify({ 
    title: userInput.title,
    description: userInput.description 
  })
});
const data = await response.json();
// Renderizar data.recommendations
```

### Qué pueden mejorar

- CSS (está funcional pero puede ser más bonito)
- Mostrar el perfil emocional del libro (gráficos de las 6 emociones)
- Validaciones de entrada
- UX enhancements (historial, favoritos, etc.)

---

## Docker

**¿Por qué?**

Sin Docker = setup local es lío (Python venv, npm install, rutas de dataset, etc.).

Con Docker = `docker-compose up` y listo.

**docker-compose.yml hace:**
1. Backend en puerto 8000 (contenedor Python)
2. Frontend en puerto 3000 (contenedor Node)
3. Los conecta en red `app-network`
4. Frontend puede hablar a Backend sin problemas

**Para desarrollar localmente:**
```bash
docker-compose up
# Esperar a que arranque
# Frontend: http://localhost:3000
# Backend: http://localhost:8000/health
```

O sin Docker:

```bash
# Terminal 1 — Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload

# Terminal 2 — Frontend
cd frontend
npm install
npm start
```

---

## Stack

- **Backend:** Python 3.11 + FastAPI (framework web) + Uvicorn (servidor ASGI)
- **ML:** PyTorch + Transformers (BERT pre-entrenado) + scikit-learn (K-means, cosine similarity)
- **Frontend:** React 18 + Axios (HTTP client)
- **Data:** Pandas (procesamiento) + NumPy (math) + SQLite (almacenamiento)
- **DevOps:** Docker + docker-compose

---

## Dataset

**Ubicación:** `data/Book_Details.csv` y `data/book_reviews.db`

**Contenido:**
- 16,225 libros únicos
- 63,014 reseñas de Goodreads
- Campos: book_id, title, author, review_text, rating, etc.

**Cómo usarlo:**
```python
import pandas as pd
df = pd.read_csv('data/Book_Details.csv')
reviews_by_book = df[df['title'] == user_input_title]['review_text'].tolist()
```

---

## Qué Implementar (Priority)

### Priority 1 (CRITICAL)
- [ ] Implementar `analyze_sentiment()` en backend
- [ ] Implementar `find_similar_books()` en backend
- [ ] Test que ambas funciones retornan datos correctos
- [ ] Verificar que POST /recommend retorna JSON en formato esperado

### Priority 2 (HIGH)
- [ ] Data cleaning (remove nulls, invalid chars, etc.)
- [ ] BERT inference optimization (caching, quantization)
- [ ] End-to-end testing (fronted → backend → recomendaciones)
- [ ] Clean GitHub (PRs, commits claros, documentación)

### Priority 3 (NICE TO HAVE)
- [ ] UI improvements
- [ ] Visualizar perfiles emocionales
- [ ] Agregar features (búsqueda por autor, filtros, etc.)
- [ ] Performance optimization

---

## Debugging Tips

**Backend:**
- `print()` en main.py aparece en la terminal
- Uvicorn logs muestran requests
- Usa `python -m pdb` para debugging interactivo

**Frontend:**
- DevTools (F12) → Console para logs
- Network tab para ver requests/responses
- React DevTools extension

**Docker:**
- `docker-compose logs backend` → logs del backend
- `docker-compose logs frontend` → logs del frontend
- `docker-compose down` → apagar todo
- `docker-compose up --build` → rebuild si cambias Dockerfile

---

## Que No Olviden

1. Los datos son dirty — limpien bien
2. BERT es lento — optimicen early, no late
3. Git es importante — commits claros, PRs descriptivas
4. Testén todo — no dejen testing para el final
5. Documenten mientras programan — no después

---

Del Unicornio que se piró. Adelante.
