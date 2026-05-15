# 📖 Brief para Estudiantes — Lean Esto Primero

Hola. Bienvenidos al proyecto.

Esto es CÓDIGO REAL. No es un ejercicio de escuela. El "unicornio" que empezó esto se fue (por razones), y ustedes heredan el caos. Pero organizado.

---

## Lo que heredan (honestamente)

**Lo que FUNCIONA:**
- ✅ Frontend: React bonito, componentes listos, UI responsiva
- ✅ Backend: FastAPI con endpoints, estructura clara
- ✅ Data: 63K reviews limpias (bueno, limpiables)
- ✅ Docker: Levanta sin problemas

**Lo que NO funciona:**
- ❌ El análisis de sentimientos (BERT — ustedes lo implementan)
- ❌ Las recomendaciones (K-means + cosine — ustedes lo implementan)

**Lo importante:** NO hay que empezar de cero. Hay templates. Hay arquitectura. Hay claridad.

---

## La verdad sin rodeos

**BERT tarda.** Cada libro = 1-2 segundos. No es bug, es BERT. Lo van a odiar la Semana 2.

**Los datos son sucios.** Emojis raros, idiomas mezclados, bots. Primer día: limpiar datos (tedioso pero necesario).

**Semana 2 es hard.** Todo lento, RAM al máximo, gente frustrada. No renuncien. Pasa siempre.

**Git será complicado.** 10 personas en un repo = conflictos. Negocien workflows YA.

---

## Primeros pasos (Hoy — Jueves 7 de mayo)

### 1️⃣ Clonan el repo

```bash
git clone https://github.com/Anais-RV/equipo-1-libros.git
cd equipo-1-libros
```

### 2️⃣ Leen documentación (en orden, 45 min)

```
README.md (5 min)
  ↓
docs/ARQUITECTURA.md (10 min)
  ↓
docs/NOTAS_DEL_UNICORNIO.md (10 min)
  ↓
backend/analysis/README.md (10 min)
  ↓
CONTRIBUTING.md (10 min)
```

**No salten pasos.** Cada doc construye sobre el anterior.

### 3️⃣ Levantan el proyecto

```bash
docker-compose up
```

Esperen 2-3 minutos a que levante.

### 4️⃣ Verifican que funciona

**Terminal nueva (mientras Docker corre):**

```bash
# Backend está vivo?
curl http://localhost:8000/health

# Deberían ver:
# {"status": "ok", "timestamp": "2026-05-07T..."}

# API responde?
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"title": "The Midnight Library", "description": ""}'

# Deberían ver 5 libros placeholder (ustedes lo harán real)
```

**Frontend funciona?**
- Abran http://localhost:3000 en navegador
- Deberían ver formulario bonito + icono de libro

### 5️⃣ Cierran y respiran

```bash
# En la terminal de Docker:
Ctrl+C

# Limpian:
docker-compose down
```

---

## Estructura de carpetas (Guía rápida)

```
equipo-1-libros/
│
├── README.md                      ← Qué es el proyecto (técnico)
├── CONTRIBUTING.md                ← Plan semanal + setup
├── BRIEF_PARA_ESTUDIANTES.md      ← Esto (ayuda + troubleshooting)
│
├── backend/
│   ├── main.py                    ← API FastAPI (endpoints listos)
│   ├── requirements.txt            ← Dependencias Python
│   ├── Dockerfile                 ← Cómo Docker corre backend
│   │
│   └── analysis/                  ← Aquí implementan USTEDES
│       ├── README.md              ← Qué hacer exactamente
│       ├── sentiment_analyzer.py  ← TODO: BERT (semana 2)
│       ├── recommender.py         ← TODO: cosine similarity (semana 3)
│       ├── data_processor.py      ← TODO: cargar/limpiar datos (semana 1)
│       └── cache_manager.py       ← LISTO (no tocar)
│
├── frontend/
│   ├── src/
│   │   ├── app/App.jsx            ← Componente principal
│   │   ├── components/            ← RecommendationForm, ResultsDisplay, etc.
│   │   └── styles/                ← Variables CSS, temas
│   ├── package.json               ← Dependencias Node
│   ├── Dockerfile                 ← Cómo Docker corre frontend
│   └── public/index.html          ← HTML raíz
│
├── data/
│   ├── goodreads_reviews.csv      ← 63K reviews (AQUÍ trabajan)
│   └── books.csv                  ← 16K libros
│
├── docs/
│   ├── ARQUITECTURA.md            ← Flujo técnico detallado
│   └── NOTAS_DEL_UNICORNIO.md     ← Warnings del que se fue
│
└── docker-compose.yml             ← Cómo Docker levanta todo
```

---

## ⚠️ Problemas comunes (y soluciones)

### Docker no arranca

```bash
# Primero: ¿está Docker Desktop corriendo?
# (Busca la ballena en la bandeja de tareas)

# Si no está, ábrelo y espera 30 seg

# Si sigue sin funcionar:
docker-compose up --build

# Si aún falla, nuclear option:
docker system prune -a
docker-compose up
```

### "Port 8000 already in use"

Alguien más usa ese puerto.

```bash
# Mata el proceso:
lsof -i :8000  # (Mac/Linux)
netstat -ano | findstr :8000  # (Windows)

# Luego mata el proceso por ID:
kill -9 <PID>
# O en Windows:
taskkill /PID <PID> /F

# Reintenta:
docker-compose up
```

### "Cannot connect to Docker daemon"

Docker no está corriendo o no está instalado.

```bash
# Verifica:
docker --version

# Si no está instalado:
# Descarga e instala Docker Desktop desde:
# https://www.docker.com/products/docker-desktop

# Si está instalado pero no corre:
# Abre Docker Desktop (icono en tu aplicaciones)
```

### Frontend carga pero "Cannot reach backend"

Backend no está respondiendo.

```bash
# Verifica que Docker está corriendo:
docker-compose ps
# Deberías ver dos servicios (backend, frontend) en "Up"

# Si backend está rojo:
docker-compose logs backend
# Busca error en los logs

# Si ves "Address already in use":
# Ve arriba ("Port 8000 already in use")
```

### "Module not found: analysis.sentiment_analyzer"

Path de imports está mal.

```bash
# Verifica que estás en la carpeta correcta:
pwd
# Deberías estar en: /app/backend (dentro de Docker)

# O si trabajas local (sin Docker):
cd backend
python -c "from analysis import sentiment_analyzer"
```

---

## 📋 Comandos útiles por semana

### Semana 1: Data (7-11 mayo)

```python
# Explorar dataset
from analysis.data_processor import load_dataset

books, reviews = load_dataset()

# ¿Qué columnas tengo?
print(books.columns.tolist())
print(reviews.columns.tolist())

# ¿Cuántos nulls?
print(reviews.isnull().sum())

# ¿Qué data es "dirty"?
print(reviews['review_text'].head(10))

# Ver estadísticas
print(reviews['review_text'].str.len().describe())
```

### Semana 2: BERT (12-18 mayo)

```python
# Test BERT en una review
from transformers import pipeline

classifier = pipeline("zero-shot-classification", 
                     model="facebook/bart-large-mnli")

review = "This book changed my life! Amazing!"
EMOTIONS = ['joy', 'sadness', 'fear', 'surprise', 'anger', 'disgust']

result = classifier(review, EMOTIONS, multi_class=True)
print(result)
# {'sequence': '...', 'labels': ['joy', 'surprise', ...], 'scores': [...]}
```

### Semana 3: Recomendaciones (19-25 mayo)

```python
# Test cosine similarity
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Vector emocional de un libro
book1_emotions = np.array([0.9, 0.1, 0.05, 0.3, 0.0, 0.0])
book2_emotions = np.array([0.85, 0.05, 0.1, 0.35, 0.0, 0.02])

similarity = cosine_similarity([book1_emotions], [book2_emotions])[0][0]
print(f"Similarity: {similarity:.2f}")  # Entre 0 y 1
```

---

## 🚀 Git profesional (Desde el primer commit)

### Reglas básicas

```bash
# NUNCA pusheen directo a main
# SIEMPRE usen branches

# Crear branch para tu feature:
git checkout -b feature/cargar-dataset

# Trabajo, commits claros:
git add backend/analysis/data_processor.py
git commit -m "Add dataset loading and validation"

# Push a tu branch:
git push origin feature/cargar-dataset

# En GitHub: Abren PR, describen qué hicieron, alguien revisa
# Una vez aprobado: merge a dev (no a main)
```

### Commit messages que NO son vergüenza

```bash
# ✅ BUENOS:
git commit -m "Implement BERT sentiment analysis for reviews"
git commit -m "Fix cosine similarity calculation edge case"
git commit -m "Add caching decorator for sentiment profiles"

# ❌ MALOS:
git commit -m "fix"
git commit -m "asdasd"
git commit -m "lol"
git commit -m "updates"
```

---

## 🐛 Debugging tips

### "¿Por qué mi código falla?"

1. **Mirar el error completo** (no ignore el traceback)
2. **Googlear el error** (ChatGPT es tu amigo)
3. **Testear en partes** (no corran 10K reviews de una)
4. **Usa print/logging** para ver qué pasa
5. **Pregunten en Discord** si llevan 30 min stuck

### "¿Cómo veo qué hace mi código?"

```python
# Opción 1: Print statements (rápido pero feo)
print(f"Debug: {variable}")

# Opción 2: Logging (profesional)
import logging
logging.debug(f"Variable is {variable}")

# Opción 3: Python debugger (el plus ultra)
import pdb
pdb.set_trace()  # Se pausa acá, pueden inspeccionar todo
```

---

## 📚 Recursos útiles

- **BERT docs:** https://huggingface.co/transformers/
- **scikit-learn:** https://scikit-learn.org/ (K-means, cosine similarity)
- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **Pandas:** https://pandas.pydata.org/ (data processing)

---

## Timeline (Sin mentiras)

| Semana | Tarea | Dificultad | Riesgo |
|--------|-------|-----------|--------|
| 1 (7-11 mayo) | Setup + limpiar datos | 🟢 Media | Data dirty |
| 2 (12-18 mayo) | BERT + clustering | 🔴 HARD | RAM + tiempo |
| 3 (19-25 mayo) | Motor de recomendaciones | 🟢 Media | Cosine bugs |
| 4 (26-28 mayo) | Pulida + ensayos | 🟢 Media | Pánico |

---

## Si el día de la demo funciona TODO ✅

Muestran un sistema ML que FUNCIONA. Eso es impresionante. Empresas contratan gente que hace eso.

Presentan en GitHub: código limpio, commits profesionales, README actualizado = **diferenciador de CV.**

## Si el día de la demo se rompe TODO ❌

Pasó. Pero si llegan con:
- ✅ Frontend que carga
- ✅ Dataset limpio
- ✅ BERT funcionando (aunque sea parcial)
- ✅ Código legible
- ✅ GitHub limpio

...es respetable. Aprenden MÁS del fracaso que del éxito.

---

## Última cosa

Esto NO es un ejercicio. Es código real. Timeline real. Consecuencias reales.

El 28 de mayo van a estar presentando CÓDIGO QUE ESCRIBIERON. No como "estudiantes", sino como "desarrolladores".

Eso es raro. Eso es bueno. Eso es aprendizaje de verdad.

No me defraudan.

---

## Checklist "Hoy todo funciona"

- [ ] Docker Desktop está corriendo
- [ ] `docker-compose up` levanta sin errores
- [ ] `curl http://localhost:8000/health` responde
- [ ] Frontend carga en http://localhost:3000
- [ ] Leyeron toda la documentación (sí, toda)
- [ ] Saben qué implementar (ver `backend/analysis/README.md`)
- [ ] Están en Discord #equipo-1
- [ ] Preguntaron algo al Tech Lead (empiezan así)

---

**Preguntas técnicas:** Discord `#equipo-1`  
**Emergencias:** Pregunta a tu Tech Lead  
**Para empezar AHORA:** `docker-compose up`

¡Adelante! 🚀

— *La profesora que los cuida (y cree en ustedes)*
