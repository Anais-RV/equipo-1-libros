# 🐳 Docker Explicado — Lo que Necesitan Saber

*(Nota del unicornio que se piró: si no entienden Docker en la primera semana, es normal. Yo tampoco, por eso dejé esto documentado. Suerte.)*

---

## 🚀 PRIMER PASO: Instalar Docker Desktop

**Si no lo tienen aún, comiencen por acá. No pueden hacer nada sin esto.**

### Windows (Lo más probable)

1. **Descargen Docker Desktop:** https://www.docker.com/products/docker-desktop
2. **Ejecuten el instalador** (.exe que bajaron)
3. **Acepten TODOS los permisos** que pide (importante)
4. **Reinicien la máquina** (sí, obligatorio. No lo salten.)
5. **Abran Docker Desktop** (icono en aplicaciones o bandeja de tareas)
   - Busquen la ballena azul 🐳
   - Esperen a que diga "Docker Desktop is running"
   - Puede tardar 1-2 minutos la primera vez

**Verificar que funciona:**
```bash
# Abran PowerShell y corran:
docker --version
# Deberían ver algo como: Docker version 24.0.0, build xxxxx
```

Si ven un error "Cannot connect to Docker daemon":
- Abran Docker Desktop (icono en taskbar, esquina inferior derecha)
- Esperen 30 segundos
- Reintenten el comando

### macOS

1. **Descargen Docker Desktop:** https://www.docker.com/products/docker-desktop (versión Mac Intel o Apple Silicon según su chip)
2. **Ejecuten el .dmg** y arrastren Docker a Applications
3. **Abran Docker** desde Applications
4. **Acepten el password** si pide (es necesario para VM)

```bash
# Verificar en terminal:
docker --version
```

### Linux (Si alguien usa)

```bash
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Iniciar servicio:
sudo systemctl start docker
sudo systemctl enable docker
```

---

## ¿Qué es Docker?

Docker es **una caja de seguridad virtual** donde vive todo lo que necesita el proyecto:
- Python 3.13 (sí, específicamente 3.13, no 3.12 ni 3.11)
- Node 18 (también específico, porque los detalles importan)
- BERT, Torch, todas las librerías pesadas (que pesan MUCHO)
- Configuración exacta (que tardé semanas en que funcionara)

**Ustedes editan el código en su máquina. Docker lo ejecuta dentro de la caja. Así su sistema está protegido.**

*Traducción: no carguen BERT en su máquina directamente o llorarán.*

---

## ¿Por qué Docker? (Una historia real)

### Lo que pasó sin Docker (el dolor)
```
Yo: "Listo, instalé BERT"
Mi compu: *comienza a arder*
RAM: 0.2GB disponible
Compu: ¿Quieres instalar más? Toma 2GB de swap.
Yo: "¿Por qué todo es tan lento?"
Compu: Porque instalaste 47GB de dependencias de ML.
Mi vida: destruida.
```

### Lo que pasa con Docker (salvación)
```
Ustedes: docker-compose up
Docker: "Yo manejo todo adentro de mi caja"
Su compu: Limpia. Feliz. Sin BERT contaminando el sistema.
Su vida: salvada.
```

---

## Las 4 razones por las que Docker existe (y yo lo uso)

### 1️⃣ Aislamiento (es decir, no contaminar tu compu)
**Sin Docker:** 
- Instalan BERT, torch, transformers → 47GB de dependencias
- Instalan Node → más cosas
- Python 3.13, esperen en realidad necesito 3.12 → conflictos
- Tu compu: "¿Quién soy? ¿Para qué sirvo?"

**Con Docker:**
- Toda la basura vive DENTRO del contenedor
- Tu compu: "Estoy limpia y feliz"
- Cuando cierras Docker: `docker-compose down` → adiós basura, código sigue en Git ✅

### 2️⃣ Consistencia (el "funciona en mi máquina" nunca más)
**Problema real que me pasó:**
```
Yo: "Funciona. Lo subo a GitHub"
Ustedes clonan: "No funciona"
Yo: "¿Qué? Para mí funciona..."
Ustedes: "Tienes Python 3.13, yo 3.12"
Yo: *cara de sufrimiento*
```

**Solución Docker:**
Todos tienen Python 3.13 exacto. Node 18 exacto. BERT exacto. Fin.
Si funciona en tu máquina = funciona en la de TODOS.

### 3️⃣ Reproducibilidad (para que en 2030 alguien sepa qué hacer)
En 6 meses, otro dev clona el repo y hace `docker-compose up`.
Funciona igual. Sin "ah, necesitas instalar X versión de Y en tu máquina antes de que el cometa golpee la tierra".

GitHub es tu fuente de verdad. Docker garantiza que funcione.

### 4️⃣ Profesional (así trabaja la industria real)
Startups, empresas, todo usa Docker. Si quieren trabajar en un equipo real después del bootcamp, esto ES lo que van a hacer.
Sin Docker = atraso de 5 años.

---

## ¿Cómo lo usan? (La parte práctica, sin dolor)*

*Sin dolor porque ya lo sufrí yo.*

---

## Cómo lo usan (paso a paso)

### Primer día (Jueves 7 de mayo)

```bash
# 1. Clonan
git clone https://github.com/Anais-RV/equipo-1-libros.git
cd equipo-1-libros

# 2. Levantan Docker (ejecuta TODO el proyecto de una vez)
docker-compose up

# Esperen 2-3 minutos a que levante
# (Sí, 2-3 minutos. Docker descarga imágenes. Es normal.)
# 
# Verán cosas raras en la terminal. IGNORE. Es normal.
# Busquen ESTAS líneas sin errores rojos:
# ✅ backend_1 | Uvicorn running on http://0.0.0.0:8000
# ✅ frontend_1 | webpack compiled...

# Si ven "error" en rojo: pregunten en Discord. No intenten "arreglarlo".

# 3. Abran navegador
# http://localhost:3000  ← Frontend (el formulario bonito)
# http://localhost:8000/docs  ← API docs (Swagger, para curiosos)

# 4. Trabajen normalmente
# - Editen código en VSCode (en su máquina, no dentro de Docker)
# - Docker lo ejecuta automáticamente
# - Los cambios se ven al instante (gracias a los volúmenes)
# - NO NECESITAN recargar Docker para ver cambios

# Sí, es magia. Pero es magia buena.
```

### Cada sesión (Lunes-Viernes, el ritual)

```bash
# MAÑANA (09:00): Despertar Docker
docker-compose up
# (Espera 30 seg a que esté listo)
# Café mientras tanto.

# TODO EL DÍA: Trabajan normalmente
# - Editan archivos en VSCode
# - Git commit/push (código sigue en tu máquina Y en GitHub)
# - Docker ejecuta en vivo en el fondo
# - No necesitan tocar Docker nunca más

# TARDE (18:00): Apagar Docker
Ctrl+C  (en la terminal de Docker)
docker-compose down
# (El contenedor muere, Docker se apaga, su máquina vuelve a la normalidad)
# (Pero el código que escribieron sigue en su máquina + Git)

# MAÑANA SIGUIENTE: Repetir sin miedo
# El código NO desapareció. Docker no es destructor de código.
```

---

## La verdad incómoda sobre Docker

**Primer día:** "¿Por qué tarda tanto?"

**Día 3:** "Funciona. No entiendo por qué, pero funciona."

**Semana 2:** "Ahh, entiendo. Es magia."

**Semana 4:** "Docker es mi amigo."

Es normal no entender Docker completamente al principio. Yo tampoco lo entendía. Pero FUNCIONA. Y eso es lo que importa.

---

## Qué entienden cuando hacen esto

### Editan código (su máquina local)
```python
# backend/analysis/sentiment_analyzer.py
def analyze_sentiment(text):
    # Ustedes escriben acá
    pass
```

### Docker lo ejecuta (dentro del contenedor)
```
Docker ejecuta el código ↓
Backend responde en http://localhost:8000
Frontend lo ve en http://localhost:3000
```

### Lo guardan
```bash
git add .
git commit -m "Implement sentiment analysis"
git push origin feature/sentiment
```

**El código VIVE en su máquina + Git. Docker es solo la ejecución.**

---

## Errores comunes (y soluciones que NO son magia)

### "Port 8000 already in use"
```
Mensaje: "Error: Port 8000 already in use"
Significado: Alguien ya levantó Docker en otra terminal
Solución 1: Cierra la otra terminal (Ctrl+C, docker-compose down)
Solución 2: "Profe, mi compañero y yo estamos en la misma máquina"
Entonces: Usen puertos diferentes (pero pregunten primero, no improvisen)
```

### "Cannot connect to Docker daemon"
```
Mensaje: "Cannot connect to Docker daemon"
Significado: Docker Desktop no está corriendo
Causa real: Olvidaron abrir Docker Desktop
Solución:
  1. Abre Docker Desktop (icono en aplicaciones, la ballena azul)
  2. Espera 30 segundos (es lento)
  3. Reintenta: docker-compose up
  4. Profit
```

### "Module not found: transformers" (o cualquier librería)
```
Mensaje: "ModuleNotFoundError: No module named 'transformers'"
Significado: Docker no instaló las dependencias correctamente
Causa real: A veces pasa. No es culpa de ustedes.
Solución:
  1. Ctrl+C (parar Docker)
  2. docker-compose down (apagar todo)
  3. docker-compose up --build (reinstalar desde cero)
  4. Esperar (5-10 minutos, no es rápido)
  5. Si sigue fallando: preguntar en Discord
```

### "BERT is SOOO SLOW / my RAM is dying"
```
Mensaje: "Esto tarda 2 segundos por libro..."
Significado: Correcto. BERT es lento. Es NORMAL.
Causa real: BERT es un modelo de 330M parámetros. No es un if statement.
Solución:
  ✅ Paciencia. Coffee break. Meditación.
  ✅ Usen cache (ya está implementado)
  ❌ NO intenten "optimizar" BERT en Semana 2
  ❌ NO cierren Docker porque "está lento"
  
La Semana 2 va a ser lenta. Todos lo sabemos. Respiren.
```

### "Everything is broken and I hate Docker"
```
Mensaje: "NOTHING WORKS. DOCKER IS BROKEN. I HATE THIS."
Significado: Docker está funcionando bien. Es el cansancio hablando.
Solución real:
  1. Descansar 15 minutos
  2. Tomar agua
  3. Intentar de nuevo
  4. Si sigue fallando: Discord
  
Nunca debería estar enojado con Docker. Docker no tiene sentimientos.
```

---

## Checklist cada mañana

- [ ] Docker Desktop abierto (ballena en tareas)
- [ ] `docker-compose up` corriendo
- [ ] Backend responde: `curl http://localhost:8000/health`
- [ ] Frontend carga: http://localhost:3000
- [ ] Cero errores rojos en la terminal

Si todo ✅ = a trabajar.

---

## Lo más importante (en serio)

**Docker NO es mágico. Es una herramienta. Una herramienta que me salvó la vida.**

**Lo que necesitan hacer:**

- ✅ Mañana: `docker-compose up`
- ✅ Todo el día: Trabajen normal (editen código, hagan commits)
- ✅ Tarde: `Ctrl+C` y `docker-compose down`
- ✅ Código se guarda en Git (no desaparece, está a salvo)
- ✅ Mañana siguiente: Repetir sin miedo

**Lo que NO necesitan hacer:**

- ❌ Entender cómo funciona Docker por dentro (todavía)
- ❌ Instalar nada en su máquina manualmente
- ❌ "Optimizar" Docker (déjenlo en paz)
- ❌ Paniquear cuando ven errores raros en la terminal (ignórenlos)

**Lo más importante de todo:**

No renuncien en Semana 2 cuando Docker + BERT les consuma RAM y todo sea lento.

Eso es normal. Yo lloré. Ustedes también van a llorar. Pero funciona.

---

## ¿Preguntas?

Discord → #equipo-1

Cualquier cosa que no entienda o no funcione: **pregunten sin miedo**.

No hay preguntas estúpidas. Docker confunde a todos al principio.

Yo creé este proyecto y sigo confundido por Docker. Pero funciona.

---

## Analogía final (la verdadera)

Docker es como una **máquina virtual portable** que vive en su máquina.

- **Adentro:** Todo funciona exacto (Python 3.13, Node 18, BERT, todo perfecto)
- **Afuera:** Su compu está intacta (sin BERT, sin 47GB de dependencias)
- **El código:** Vive en su máquina + Git (no desaparece)
- **Docker:** Es solo el "execute button"

**Flujo de verdad:**

```
Ustedes escriben código en VSCode
           ↓
Docker lo ejecuta en la caja
           ↓
Funciona en su navegador (localhost:3000)
           ↓
Lo guardan en Git
           ↓
Cierran Docker (Ctrl+C, docker-compose down)
           ↓
El código sigue en su máquina, intacto
           ↓
Mañana: repetir
```

Fin. 🚀

---

*Del unicornio que se piró. Si algún día trabajan con Docker en un equipo real, van a entender por qué estoy aquí recomendándolo. Docker no es opcional. Es supervivencia.*