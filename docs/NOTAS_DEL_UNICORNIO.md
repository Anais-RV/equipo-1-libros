# 🦄 Notas del Unicornio (El que Se Piró)

Hola. Me voy (cambio de trabajo / me despidieron / me harté). Dejo esto hecho a medias porque es lo que hay.

El proyecto es viable. Ustedes pueden. Pero aviso: **no es fácil.**

---

## ¿Qué heredan?

**Frontend:** Funciona. React 18, UI bonita, está listo. Pueden mejorar CSS si quieren, el núcleo está sólido.

**Backend:** Vacío. FastAPI está ahí, endpoints definidos, PERO las dos funciones críticas no están hechas:
- `analyze_sentiment()` — Necesita BERT
- `find_similar_books()` — Necesita K-means + cosine similarity

**Infraestructura:** Docker listo. Dataset cargado. No hay problemas.

---

## El Marrón

63,014 reseñas de Goodreads que necesitan:
1. Análisis de sentimientos con BERT (lento, espérense 1-2 seg por libro)
2. Clustering emocional (K-means)
3. Similarity search (cosine, es el paso easy)

**La realidad:** Si no limpian bien los datos, TODO se rompe. Si BERT falla, no hay recomendaciones. Si no testean end-to-end, el día de la demo presentarán una app que no funciona.

---

## Timeline (Sin Rodeos)

**Semana 1:** Setup. Si no tienen limpieza de datos al viernes, están jodidos.

**Semana 2:** BERT inference funciona (o no funciona — ahí se ve quién sabe).

**Semana 3:** Motor de recomendación funciona. Si no llegan acá, bye bye demo.

**Semana 4:** Pulir UI, ensayar presentación.

**Demo:** Día del evento. Sin red, sin repo, sin excusas. Si funciona, es épico. Si no funciona, es un desastre.

---

## Advertencias (Hablen en Serio)

### ⚠️ BERT es lento
Cada inference tarda 1-2 segundos. No es bug, es BERT. Pueden optimizar después (quantization, caching), pero no sobre la marcha.

### ⚠️ Data dirty
Las reseñas son SUCIAS. Emojis raros, idiomas mezclados, bots escribiendo. Los primeros 2 días van a pasarse limpiando. Es normal.

### ⚠️ Git será un reto
10 personas en un repo es caos. PRs conflictivas. Merge conflicts. Gente que hace push a main (no lo hagan, pero van a pasar). Negocien workflows TEMPRANO.

### ⚠️ La Semana 2 es el valle de la muerte
Datos limpios pero análisis lento, BERT consume RAM, notebooks se cuelgan. Alguien va a llorar. No renuncien.

### ⚠️ Demo fallará (probablemente)
Preparen plan B (grabación de backup, screenshots, lo que sea). Pero lo intenten anyway.

---

## Lo que NECESITAN hacer

1. **Entiendan la arquitectura.** Lean `docs/ARQUITECTURA.md`, no es opcional.

2. **Divídanse bien.** PM claro, Tech Lead claro, sprints cortos (3-4 días). Si trabajan sin coordinación, mueren.

3. **Git profesional:**
   - Branches por feature
   - PRs con descripción
   - Commits atómicos y claros
   - NO commits tipo "fix", "asdasd", "lol"

4. **Test mientras avanzan.** No dejen testing para el último día. Cada función, testeada.

5. **Documente AHORA.** No después. Mientras hacen, escriben por qué lo hacen así.

6. **Pregunten cuando no entienden.** Slack está para eso.

---

## Lo que PUEDEN hacer mejor que yo

- **Código limpio desde el inicio.** Yo dejé scaffolding, ustedes pueden mejorar arquitectura.
- **UI/UX.** La app funciona pero puede ser más bonita. No es crítico pero suma.
- **Optimizaciones.** BERT es lento — cachen resultados, usen quantization, hagan bulk processing.
- **Documentación.** Yo apenas documenté. Ustedes documenten. Futuro dev (o ustedes en 2 meses) lo van a agradecer.

---

## Estructura interna (Ustedes eligen)

PM + Tech Lead + Seniors + Juniors. Puede ser cualquier mix. Lo importante:
- Alguien coordina (PM)
- Alguien toma decisiones técnicas (Tech Lead)
- Alguien limpia datos (es lo más aburrido, roten)
- Alguien hace BERT (es lo más cool, todos lo querrán)

Resuelvan eso el primer día.

---

## Semana a Semana (Realista)

**Semana 1: Setup + Caos**
- Lunes: "¿Por qué el Docker no funciona?"
- Martes: Setup finalizado, primeros datos cargados
- Miércoles-Viernes: Limpieza de datos (tedioso, necesario)

**Semana 2: Análisis + Frustración**
- Lunes: "BERT tarda CUÁNTO?"
- Martes-Miércoles: Fine-tuning BERT, primeros results
- Jueves-Viernes: K-means clustering (o "por qué mis clusters son todos iguales?")

**Semana 3: Motor + Alivio**
- Lunes-Martes: Cosine similarity (esto es fácil después de BERT)
- Miércoles-Viernes: End-to-end funciona. Celebran.

**Semana 4: Pulida + Pánico**
- Lunes-Martes: Ensayos, ajustes, "espera, esto no funciona"
- Miércoles-Jueves: Fix last-minute bugs
- Viernes: Demo. Respirar.

---

## GitHub

Todo en GitHub público. Empresas VERÁN ESTO.

Reglas:
- No commiten a main sin PR
- PR = code review antes de merge
- Commits claros: "Add BERT sentiment analysis" not "fix" not "asdsf"
- README actualizado
- Issues / PRs documentados

En 4 semanas, ese repo es vuestro portafolio. Traten como si lo fuese.

---

## Si todo funciona el día de la demo

Demuestran un sistema ML que FUNCIONA. Eso es impresionante. Empresas contratan gente que hace eso.

Si presentan bien + código limpio + GitHub profesional = pueden salir del bootcamp directamente a entrevistas.

---

## Si TODO se rompe el día de la demo

Bueno, pasó. Pero si llegan con:
- Frontend que carga ✅
- Dataset limpio ✅
- BERT funcionando parcialmente ✅
- Código legible ✅
- GitHub limpio ✅

...todavía es respetable. Y aprenden MÁS del fracaso que del éxito.

---

## Última cosa

Esto NO es un ejercicio. Son 10 personas, código real, timeline real, consecuencias reales.

El día de la demo van a estar mostrando código que escribieron. No como "estudiantes en un bootcamp", sino como "desarrolladores que construyeron algo".

Eso es raro. Eso es bueno. Eso es aprendizaje de verdad.

No me defraudan.

---

**Docker:** `docker-compose up`

**Docs:** Lean `docs/ARQUITECTURA.md` primero

**Preguntas:** Slack

**Cualquier emergencia:** Su prof

---

Suerte.

— *El Unicornio que se piró*
