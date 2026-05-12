# Scripts — Guía de Uso

Herramientas para desarrollo local y validación antes de hacer PRs.

---

## quick-review.sh

Replica localmente los mismos checks que corre el CI de GitHub Actions.
**Ejecútalo antes de cada PR para evitar fallos sorpresa.**

```bash
bash scripts/quick-review.sh
```

**Qué verifica:**

| # | Check | Por qué |
|---|-------|---------|
| 1 | Sin `__pycache__`, `node_modules`, `.ipynb` | No deben estar en el repo |
| 2 | Sintaxis Python válida (todos los `.py`) | Detecta errores antes de push |
| 3 | `package.json` es JSON válido | CI falla si está roto |
| 4 | `docker-compose.yml` sin errores | El health check lo necesita |
| 5 | Estado de Git | Resumen de qué está pendiente |

---

## Pre-commit Hook

Se ejecuta **automáticamente antes de cada `git commit`**.
Rechaza el commit si hay archivos prohibidos o errores de sintaxis Python.

### Instalar (una sola vez, después de clonar)

**Linux / Mac / WSL / Git Bash:**
```bash
cp scripts/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

**Windows (PowerShell):**
```powershell
Copy-Item scripts\hooks\pre-commit .git\hooks\pre-commit
```

### Verificar que está instalado

```bash
ls -la .git/hooks/pre-commit
```

### Saltarse el hook (solo en emergencias)

```bash
git commit --no-verify -m "mensaje"
```

---

## Health Check local con Docker

Levanta el backend con datos mock (sin BERT, sin dataset real).
Útil para probar que la API arranca correctamente.

```bash
# Levantar
docker compose -f docker-compose.ci.yml up

# En otra terminal, verificar:
curl http://localhost:8000/health
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"title": "1984", "author": "George Orwell"}'

# Parar
docker compose -f docker-compose.ci.yml down
```

---

## CI en GitHub Actions

Los workflows se activan automáticamente en cada PR:

| Workflow | Archivo | Qué hace | Tiempo aprox. |
|----------|---------|----------|---------------|
| CI Validación | `.github/workflows/ci.yml` | Sintaxis Python/JS + lint Dockerfiles | ~30s |
| Health Check | `.github/workflows/health-check.yml` | Build imagen CI + verifica API | ~60s |

### Por qué hay dos Dockerfiles

| Archivo | Cuándo se usa | Contiene |
|---------|--------------|---------|
| `backend/Dockerfile` | Producción | Todas las dependencias (torch, BERT...) |
| `backend/Dockerfile.ci` | CI solamente | Solo fastapi + uvicorn (~20s de build) |

---

## Errores comunes

**`__pycache__ encontrado`**
```bash
git rm -r --cached backend/__pycache__/
# Y asegúrate de tener __pycache__/ en .gitignore
```

**`*.ipynb encontrado`**
```bash
git rm --cached notebooks/mi_analisis.ipynb
echo "*.ipynb" >> .gitignore
git add .gitignore
```

**Error de sintaxis Python**
```bash
python -m py_compile backend/analysis/mi_archivo.py
```
