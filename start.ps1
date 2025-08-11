# ========================================
# Script de Inicializacao - Hackathon Conecta
# Backend FastAPI + Frontend React
# ========================================

Write-Host "Hackathon Conecta - Sistema de Recomendacoes" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Verificar se Python esta instalado
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python nao encontrado. Por favor, instale o Python 3.8+" -ForegroundColor Red
    Write-Host "   Download: https://python.org/downloads" -ForegroundColor Yellow
    exit 1
}

# Verificar se Node.js esta instalado
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js nao encontrado. Por favor, instale o Node.js 16+" -ForegroundColor Red
    Write-Host "   Download: https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

Write-Host "Pre-requisitos encontrados" -ForegroundColor Green

# Criar ambiente virtual Python se nao existir
if (-not (Test-Path ".venv")) {
    Write-Host "Criando ambiente virtual Python..." -ForegroundColor Cyan
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erro ao criar ambiente virtual" -ForegroundColor Red
        exit 1
    }
}

# Ativar ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Instalar dependencias Python
Write-Host "Instalando dependencias Python..." -ForegroundColor Cyan
pip install --upgrade pip
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt nao encontrado, instalando dependencias basicas..." -ForegroundColor Yellow
    pip install fastapi uvicorn pandas numpy scikit-learn
}

# Instalar dependencias do frontend
Write-Host "Instalando dependencias do Frontend..." -ForegroundColor Cyan
if (Test-Path "recommendation-microfrontend") {
    Set-Location "recommendation-microfrontend"
    npm install
    Set-Location ".."
} else {
    Write-Host "Diretorio recommendation-microfrontend nao encontrado" -ForegroundColor Red
    exit 1
}

Write-Host "" 
Write-Host "Instalacao concluida!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Funcao para iniciar ambos os servicos
Write-Host "Iniciando servicos..." -ForegroundColor Cyan

# Iniciar API em background
Write-Host "Iniciando API FastAPI na porta 8000..." -ForegroundColor Cyan
$apiJob = Start-Job -ScriptBlock {
    Set-Location $args[0]
    & .\.venv\Scripts\Activate.ps1
    $env:PYTHONPATH = "."
    Set-Location "api"
    python main.py
} -ArgumentList (Get-Location)

Start-Sleep 3

# Iniciar Frontend
Write-Host "Iniciando Frontend React na porta 3001..." -ForegroundColor Cyan
Set-Location "recommendation-microfrontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"
Set-Location ".."

Start-Sleep 2

Write-Host ""
Write-Host "Servicos iniciados com sucesso!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Frontend: http://localhost:3001" -ForegroundColor Yellow
Write-Host "API: http://localhost:8000" -ForegroundColor Yellow  
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para parar os servicos:" -ForegroundColor Cyan
Write-Host "   - Feche as janelas do terminal" -ForegroundColor White
Write-Host "   - Ou pressione Ctrl+C em cada terminal" -ForegroundColor White
Write-Host ""
Write-Host "Abrindo navegador..." -ForegroundColor Cyan
Start-Sleep 5
Start-Process "http://localhost:3001"

Write-Host "Sistema pronto para uso!" -ForegroundColor Green
