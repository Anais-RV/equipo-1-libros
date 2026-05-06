# ============================================================================
# SETUP ENTORNO VIRTUAL - Proyecto Final Data Analyst
# ============================================================================
# Uso: .\setup_venv.ps1
# ============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SETUP: Entorno Virtual" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Paso 1: Crear o reutilizar entorno virtual
if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "`n[1/3] Reutilizando entorno virtual existente: .venv" -ForegroundColor Yellow
    Write-Host "✅ Entorno virtual encontrado" -ForegroundColor Green
}
else {
    Write-Host "`n[1/3] Creando entorno virtual .venv..." -ForegroundColor Yellow
    python -m venv .venv

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Error creando entorno virtual" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
}

# Paso 2: Activar entorno virtual
Write-Host "`n[2/3] Activando entorno virtual..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error activando entorno virtual" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Entorno virtual activado" -ForegroundColor Green

# Paso 3: Instalar requirements
Write-Host "`n[3/3] Instalando requirements..." -ForegroundColor Yellow
Write-Host "(Esto puede tardar 5-10 minutos por torch)" -ForegroundColor DarkYellow
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error instalando requirements" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Requirements instalados" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETADO" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nProximos pasos:" -ForegroundColor Yellow
Write-Host "1. El entorno virtual ya está activado" -ForegroundColor White
Write-Host "2. Verifica con: python --version" -ForegroundColor White
Write-Host "3. Abre Jupyter: jupyter notebook" -ForegroundColor White
Write-Host "4. Navega a: notebooks/" -ForegroundColor White
