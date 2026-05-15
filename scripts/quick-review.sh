#!/usr/bin/env bash
# =============================================================
# quick-review.sh — Validación local antes de hacer un PR
#
# Uso:
#   bash scripts/quick-review.sh
#
# Qué hace:
#   1. Verifica que no hay __pycache__, node_modules, .ipynb
#   2. Comprueba sintaxis Python en todos los .py
#   3. Valida package.json
#   4. Valida docker-compose.yml
#   5. Muestra el estado de Git
# =============================================================

set -e

ERRORS=0
PASS=0

log_pass() { echo "  ✅ $1"; PASS=$((PASS + 1)); }
log_fail() { echo "  ❌ $1"; ERRORS=$((ERRORS + 1)); }
log_info() { echo "     $1"; }
log_step() { echo ""; echo "[ $1 ] $2"; }

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     REVISIÓN RÁPIDA — Proyecto Libros    ║"
echo "╚══════════════════════════════════════════╝"

# ─────────────────────────────────────────────
# 1. Archivos prohibidos
# ─────────────────────────────────────────────
log_step "1/5" "Archivos prohibidos..."

COUNT=$(find . -type d -name "__pycache__" -not -path "./.git/*" 2>/dev/null | wc -l)
if [ "$COUNT" -gt 0 ]; then
    log_fail "__pycache__ encontrado ($COUNT carpeta/s):"
    find . -type d -name "__pycache__" -not -path "./.git/*"
    log_info "Solución: git rm -r --cached '**/__pycache__/'"
else
    log_pass "Sin __pycache__"
fi

COUNT=$(find . -type d -name "node_modules" -not -path "./.git/*" 2>/dev/null | wc -l)
if [ "$COUNT" -gt 0 ]; then
    log_fail "node_modules en el repo — no debe commitearse"
    log_info "Solución: git rm -r --cached frontend/node_modules/"
else
    log_pass "Sin node_modules comprometido"
fi

COUNT=$(find . -name "*.ipynb" -not -path "./.git/*" 2>/dev/null | wc -l)
if [ "$COUNT" -gt 0 ]; then
    log_fail "Notebooks .ipynb encontrados ($COUNT):"
    find . -name "*.ipynb" -not -path "./.git/*"
    log_info "Solución: añade *.ipynb a .gitignore y haz git rm --cached"
else
    log_pass "Sin notebooks .ipynb"
fi

# ─────────────────────────────────────────────
# 2. Sintaxis Python
# ─────────────────────────────────────────────
log_step "2/5" "Sintaxis Python..."

if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    log_info "Python no encontrado, saltando..."
else
    PYTHON_CMD=$(command -v python3 || command -v python)
    PY_ERRORS=0
    PY_FILES=0

    while IFS= read -r f; do
        PY_FILES=$((PY_FILES + 1))
        if ! "$PYTHON_CMD" -m py_compile "$f" 2>/dev/null; then
            log_fail "Error de sintaxis en: $f"
            "$PYTHON_CMD" -m py_compile "$f" 2>&1 || true
            PY_ERRORS=$((PY_ERRORS + 1))
        fi
    done < <(find . -name "*.py" \
        -not -path "./.git/*" \
        -not -path "*/__pycache__/*")

    if [ "$PY_ERRORS" -eq 0 ]; then
        log_pass "Sintaxis Python OK ($PY_FILES archivos revisados)"
    fi
fi

# ─────────────────────────────────────────────
# 3. JSON válidos
# ─────────────────────────────────────────────
log_step "3/5" "JSON válidos..."

if command -v node &> /dev/null; then
    if node -e "JSON.parse(require('fs').readFileSync('frontend/package.json','utf8'))" 2>/dev/null; then
        log_pass "frontend/package.json válido"
    else
        log_fail "frontend/package.json tiene errores JSON"
    fi

    if [ -f "backend/tests/fixtures/mock_books.json" ]; then
        if node -e "JSON.parse(require('fs').readFileSync('backend/tests/fixtures/mock_books.json','utf8'))" 2>/dev/null; then
            log_pass "mock_books.json válido"
        else
            log_fail "mock_books.json tiene errores JSON"
        fi
    fi
else
    log_info "Node.js no encontrado, saltando validación JSON..."
fi

# ─────────────────────────────────────────────
# 4. docker-compose.yml
# ─────────────────────────────────────────────
log_step "4/5" "docker-compose.yml..."

if command -v docker &> /dev/null; then
    if docker compose config --quiet 2>/dev/null; then
        log_pass "docker-compose.yml válido"
    else
        log_fail "docker-compose.yml tiene errores"
        docker compose config 2>&1 || true
    fi

    if [ -f "docker-compose.ci.yml" ]; then
        if docker compose -f docker-compose.ci.yml config --quiet 2>/dev/null; then
            log_pass "docker-compose.ci.yml válido"
        else
            log_fail "docker-compose.ci.yml tiene errores"
        fi
    fi
else
    log_info "Docker no disponible, saltando..."
fi

# ─────────────────────────────────────────────
# 5. Git status
# ─────────────────────────────────────────────
log_step "5/5" "Git status..."

if command -v git &> /dev/null && git rev-parse --git-dir > /dev/null 2>&1; then
    STAGED=$(git diff --cached --name-only 2>/dev/null | wc -l | tr -d ' ')
    UNSTAGED=$(git diff --name-only 2>/dev/null | wc -l | tr -d ' ')
    UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null | wc -l | tr -d ' ')

    log_info "Staged (listos para commit): $STAGED archivo(s)"
    log_info "Modificados sin stagear:     $UNSTAGED archivo(s)"
    log_info "Sin trackear:                $UNTRACKED archivo(s)"
    log_pass "Git OK"
else
    log_info "No es un repositorio git o git no está disponible"
fi

# ─────────────────────────────────────────────
# Resumen final
# ─────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════╗"
if [ "$ERRORS" -eq 0 ]; then
    echo "║  ✅ LISTO para PR  ($PASS checks pasados)   ║"
else
    echo "║  ❌ $ERRORS error(es) — corrígelos antes del PR  ║"
fi
echo "╚══════════════════════════════════════════╝"
echo ""

exit $ERRORS
