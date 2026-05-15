# 📅 Miércoles 7 de Mayo - Primer Día

Bienvenidos. El código heredado es vuestro. Tres semanas largas para hacerlo funcionar. Adelante.

---

## ⏰ Agenda del día

### 09:00-09:15: Intro y setup (15 min)

```bash
git clone <REPO_URL>
cd PFP_Libros
docker-compose up
```

Esperan a que levante sin errores. Si tarda, es normal (primera vez descarga imágenes).

### 09:15-10:00: Lectura (45 min)

**OBLIGATORIO. En orden:**
1. `README.md` (3 min) - Qué es esto
2. `CONTRIBUTING.md` (15 min) - Cómo va a funcionar Semana 1
3. `docs/ARQUITECTURA.md` (10 min) - Cómo encaja todo
4. `backend/analysis/README.md` (15 min) - Qué implementan ustedes

Si no entienden algo, preguntan. No sigan ciego.

### 10:00-10:30: Verificar que todo funciona (30 min)

```bash
# En otra terminal, mientras docker-compose está corriendo

# 1. Backend health check
curl http://localhost:8000/health
# Deberían ver: {"status": "ok"}

# 2. Frontend carga
# Abrir navegador → http://localhost:3000
# Deberían ver: interfaz bonita con icono de libro

# 3. API test
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"title": "The Midnight Library", "description": ""}'
# Deberían ver: 5 libros placeholder (ustedes lo implementarán)
```

Si algo falla aquí, lo arreglamos antes de continuar.

### 10:30-12:00: Explorar el código (90 min)

**Backend:**
- Abrir `backend/analysis/sentiment_analyzer.py` → ver qué hay que hacer
- Abrir `backend/analysis/recommender.py` → ver estructura
- Abrir `backend/analysis/cache_manager.py` → está implementado, entender cómo funciona
- Abrir `backend/main.py` → ver cómo se orquestan los endpoints

**Frontend:**
- Abrir `frontend/src/app/App.jsx` → componente raíz
- Abrir `frontend/src/components/` → ver estructura modular
- Abrir `frontend/src/styles/variables.css` → tema editorial

**Preguntas para responder:**
- ¿De dónde cargan los datos (datasets)?
- ¿Cuántos libros hay? ¿Cuántas reviews?
- ¿Cuáles son las 6 emociones que analizan?
- ¿Cómo funciona el cache?

### 12:00+: Empezar Semana 1

Ver `CONTRIBUTING.md` sección "Semana 1".

---

## ✅ Checklist "Día 1 OK"

Al final del día, deberían poder decir:

- [ ] Docker-compose up funciona sin errores
- [ ] Frontend carga en localhost:3000
- [ ] API responde en localhost:8000/health
- [ ] Leímos toda la documentación sin dormir en clase
- [ ] Entendemos qué hacemos (a grandes rasgos)
- [ ] Git clone → funciona → entendemos estructura
- [ ] Preguntamos lo que no entendemos (eso es bueno)

Si 5+ están checkeadas: **Día 1 = éxito.**

---

## 🚨 Si algo no funciona

**Docker no levanta:**
```
docker ps                    # ¿Hay contenedores?
docker-compose logs          # ¿Qué error?
docker system prune          # Nuclear option
```

**Frontend no carga:**
- Abrir F12 (DevTools) → Console
- ¿Qué error sale?
- Probablemente falta `npm install`

**API no responde:**
- Mira la terminal donde corre `docker-compose up`
- Ves si hay error en backend

**No entienden algo:**
- Preguntan. No asuman. Es código real, puede ser confuso.

---

## 🎯 Objetivo Semana 1

El 11 de mayo:
- ✅ Dataset cargado en Python
- ✅ Reviews limpias (sin nulls, sin basura)
- ✅ Entienden estructura de datos
- ✅ Primer PR abierto (sin miedo, es para aprender)

---

Del Unicornio que se piró. 🦄

No renuncien en el primer día. Es lo más fácil.
