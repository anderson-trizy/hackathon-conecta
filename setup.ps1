# ========================================
# CONFIGURACAO RAPIDA - HACKATHON CONECTA
# ========================================

Write-Host "Configuracao Rapida do Projeto" -ForegroundColor Green

# Este script apenas instala as dependencias sem iniciar os servicos

# Verificar pre-requisitos
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python nao encontrado" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js nao encontrado" -ForegroundColor Red  
    exit 1
}

# Setup Python
if (-not (Test-Path ".venv")) {
    Write-Host "Criando ambiente virtual..." -ForegroundColor Cyan
    python -m venv .venv
}

Write-Host "Ativando ambiente virtual..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

Write-Host "Instalando dependencias Python..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt

# Setup Frontend
Write-Host "Instalando dependencias Frontend..." -ForegroundColor Cyan
Set-Location "recommendation-microfrontend"
npm install
Set-Location ".."

Write-Host "Configuracao concluida!" -ForegroundColor Green
Write-Host ""
Write-Host "Para iniciar o projeto:" -ForegroundColor Yellow
Write-Host "   .\start.ps1" -ForegroundColor White
