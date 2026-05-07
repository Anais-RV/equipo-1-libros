# 🦄 Cómo contribuir (Instrucciones del Unicornio)

Esto no es un proyecto normal. Es un **simulacro de startup**: código abandonado, timeline ajustado, presión real.

Bienvenidos. No es fácil.

## Lo primero

Lean esto en este orden:
1. **README.md** - Qué es el proyecto
2. **docs/BRIEF_PARA_ESTUDIANTES.md** - Primeros pasos y troubleshooting (léanlo en serio)
3. **docs/ARQUITECTURA.md** - Cómo encaja todo técnicamente
4. **backend/analysis/README.md** - Qué implementar exactamente

Tardarán 45 minutos. Merecen la pena.

## Setup

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
# Deberían ver: "API running on http://localhost:8000"

# Frontend (otra terminal)
cd frontend
npm install
npm start
# Deberían ver: http://localhost:3000 (con placeholder)
```

**Verificar que funciona:**
```bash
curl http://localhost:8000/health
# {"status": "ok", ...}

curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"title": "The Midnight Library", "description": "test"}'
# Deberías ver 5 libros placeholder (ustedes lo implementarán)
```

## Semana 1: Setup (7-11 mayo)

### Tareas
- [ ] Clonar repo y setup funciona (docker-compose up)
- [ ] Leer toda la documentación (sí, toda)
- [ ] Explorar dataset: `python backend/analysis/data_processor.py`
- [ ] Ver qué columnas tienes, cuántos nulls, qué se ve dirty
- [ ] Empezar a limpiar reviews

### Comandos útiles
```python
# En Jupyter o Python:
from analysis.data_processor import load_dataset, preprocess_reviews

books, reviews = load_dataset()
print(books.shape)       # (16225, ?)
print(reviews.shape)     # (63014, ?)

print(books.columns)
print(reviews.columns)

# Ver qué tan sucia está la data
print(reviews['review_text'].head())
print(reviews['review_text'].isnull().sum())
```

### Señales de alerta
- ❌ Docker no funciona → Pedir ayuda. Es crítico.
- ❌ Dataset no carga → Chequeá paths, encoding
- ❌ Reviews vacías en exceso → Revisá clean_text()

## Semana 2: BERT (12-18 mayo - El valle de la muerte)

### Tareas
- [ ] Cargar modelo BERT
- [ ] Test en 10 reviews (verificar que funciona)
- [ ] Implementar `apply_bert_to_reviews()`
- [ ] Implementar `analyze_sentiment()`
- [ ] Ver que cacheá resultados

### Comandos
```python
# Test BERT
from transformers import pipeline

classifier = pipeline("zero-shot-classification")
review = "This book changed my life!"
EMOTIONS = ['joy', 'sadness', 'fear', 'surprise', 'anger', 'disgust']

result = classifier(review, EMOTIONS)
print(result)
# {'sequence': 'This book changed my life!', 
#  'labels': ['joy', 'surprise', ...],
#  'scores': [0.98, 0.01, ...]}
```

### Señales de alerta
- ❌ BERT tarda 1 minuto en 10 reviews → Es normal (pero después cachea)
- ❌ Faltan memoria → Reduce batch size o desactiva GPU (`CUDA_VISIBLE_DEVICES=""`)
- ⚠️ Scores no suma a 1 → BERT retorna scores, no probabilidades (está bien)
- ❌ Cache no funciona → Revisá `cache_manager.py`

## Semana 3: Recomendación + Top 5 (19-25 mayo)

### Tareas
- [ ] Pre-calcular perfiles de TOP 100-1000 libros
- [ ] Implementar `find_similar_books()` con cosine similarity
- [ ] Verificar que TOP 5 tiene sense
- [ ] Cachear todo

### Comandos
```python
# Pre-calcular perfiles (batch job)
from analysis.sentiment_analyzer import analyze_sentiment
from analysis.cache_manager import CacheManager

cache = CacheManager()

# Loop por los TOP 100 libros
for i, book_title in enumerate(books['title'].head(100)):
    print(f"[{i+1}/100] Analizando {book_title}...")
    profile = analyze_sentiment(book_title)
    # Ya cachea automáticamente
    
    if i % 10 == 0:
        stats = cache.get_cache_stats()
        print(f"  Cache: {stats['cached_books']} libros")
```

### Señales de alerta
- ❌ Cosine similarity retorna >1 o <-1 → Normalizaste mal
- ❌ TOP 5 no tiene sense → Revisá los datos o la normalización
- ⚠️ Tarda 5 segundos en buscar → Cache está roto
- ❌ Demo falla → Probablemente no cacheaste los perfiles

## Semana Final: Pulida + Demo (26-28 mayo)

### Tareas
- [ ] Fix bugs que aparecieron
- [ ] Testing end-to-end
- [ ] Ensayo de demo (CRÍTICO - practiquen 3+ veces)
- [ ] Documentación final (sí, esto importa)
- [ ] Screenshots + grabación de respaldo (demo falla a veces)

### Demo
```bash
# Día de demo
docker-compose up
# Frontend en http://localhost:3000
# Buscar "The Midnight Library"
# Ver las 5 recomendaciones
# Que funcione sin Internet
```

## Git Professional

No negotiable. Ustedes ven esto en el repo del 28.

```bash
# NO hagas esto
git commit -m "fix"
git commit -m "asdasd"
git push -f

# Haz esto
git checkout -b feature/bert-sentiment-analysis
# ... codigo ...
git add backend/analysis/sentiment_analyzer.py
git commit -m "Implement BERT inference for 6 emotions"
git push origin feature/bert-sentiment-analysis
# → Abrir PR, review, merge
```

**Commits claros:**
- "Add BERT sentiment analysis"
- "Implement cosine similarity for recommendations"
- "Fix cache loading bug"
- "Add docstrings to data_processor"

**NO:**
- "fix"
- "lol"
- "asdasd"
- "work in progress"

## Debugging

Cuando algo no funciona:

```python
# 1. Prints por doquier
print(f"[PUNTO 1] Llegué acá")
print(f"[DATOS] Shape: {df.shape}")
print(f"[RESULTADO] {output}")

# 2. Local testing
cd backend
python analysis/sentiment_analyzer.py
# Deberías ver el output o traceback

# 3. API logs
# Mira la terminal donde corre uvicorn
# Ves qué error retorna

# 4. Frontend console
# F12 → Console
# ¿Qué error da la llamada a /recommend?
```

## Checklist pre-demo (Viernes 28 de mayo)

- [ ] Docker compose up funciona
- [ ] Frontend carga en localhost:3000
- [ ] API responde en localhost:8000/health
- [ ] POST /recommend retorna recomendaciones (no placeholder)
- [ ] Buscar "The Midnight Library" tarda <1 segundo
- [ ] Frontend muestra 5 libros con scores
- [ ] Todo el repo está limpio (no hay .ipynb, no hay __pycache__)
- [ ] Git history tiene commits claros (no "fix", no "asdasd")
- [ ] README está actualizado
- [ ] Documentación tiene info real (no placeholders)

Si falla 1-2 cosas: respetable. Es realista.
Si falla 5+: bueno, aprenderán más del fracaso que del éxito.

## Si se rompe TODO

Respuesta del Unicornio: "Pasó. Así es."

Pero si llegan con:
- Frontend que carga ✅
- Dataset limpio ✅
- BERT funcionando en algo ✅
- Código legible ✅
- Git limpio ✅

...es respetable. Y hayan aprendido MÁS que si hubiese funcionado todo.

## Últimas palabras

Esto es código real. Ustedes no son "estudiantes haciendo ejercicios".
Son desarrolladores que construyeron un sistema ML.

Eso no es pequeño.

No me defraudan.

---

Del Unicornio que se piró. Adelante. 🦄
