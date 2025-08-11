#!/bin/bash

# ========================================
# Script de Inicialização - Hackathon Conecta
# Backend FastAPI + Frontend React
# ========================================

echo "🚀 Hackathon Conecta - Sistema de Recomendações"
echo "========================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 não encontrado. Por favor, instale o Python 3.8+${NC}"
    echo -e "${YELLOW}   Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv${NC}"
    echo -e "${YELLOW}   MacOS: brew install python3${NC}"
    exit 1
fi

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js não encontrado. Por favor, instale o Node.js 16+${NC}"
    echo -e "${YELLOW}   Ubuntu/Debian: curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt-get install -y nodejs${NC}"
    echo -e "${YELLOW}   MacOS: brew install node${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Pré-requisitos encontrados${NC}"

# Criar ambiente virtual Python se não existir
if [ ! -d ".venv" ]; then
    echo -e "${CYAN}📦 Criando ambiente virtual Python...${NC}"
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Erro ao criar ambiente virtual${NC}"
        exit 1
    fi
fi

# Ativar ambiente virtual
echo -e "${CYAN}🔧 Ativando ambiente virtual...${NC}"
source .venv/bin/activate

# Instalar dependências Python
echo -e "${CYAN}📥 Instalando dependências Python...${NC}"
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo -e "${YELLOW}⚠️  requirements.txt não encontrado, instalando dependências básicas...${NC}"
    pip install fastapi uvicorn pandas numpy scikit-learn
fi

# Instalar dependências do frontend
echo -e "${CYAN}📥 Instalando dependências do Frontend...${NC}"
if [ -d "recommendation-microfrontend" ]; then
    cd recommendation-microfrontend
    npm install
    cd ..
else
    echo -e "${RED}❌ Diretório recommendation-microfrontend não encontrado${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Instalação concluída!${NC}"
echo "========================================"

# Iniciar serviços
echo -e "${CYAN}🚀 Iniciando serviços...${NC}"

# Iniciar API em background
echo -e "${CYAN}📡 Iniciando API FastAPI na porta 8000...${NC}"
export PYTHONPATH="."
(cd api && python3 main.py) &
API_PID=$!

sleep 3

# Iniciar Frontend em background
echo -e "${CYAN}🌐 Iniciando Frontend React na porta 3001...${NC}"
(cd recommendation-microfrontend && npm run dev) &
FRONTEND_PID=$!

sleep 2

echo ""
echo -e "${GREEN}✅ Serviços iniciados com sucesso!${NC}"
echo "========================================"
echo -e "${YELLOW}📱 Frontend: http://localhost:3001${NC}"
echo -e "${YELLOW}🔗 API: http://localhost:8000${NC}"
echo -e "${YELLOW}📖 Docs: http://localhost:8000/docs${NC}"
echo ""
echo -e "${CYAN}❕ Para parar os serviços:${NC}"
echo -e "   kill $API_PID $FRONTEND_PID"
echo -e "   ou pressione Ctrl+C"
echo ""

# Função para cleanup ao sair
cleanup() {
    echo -e "\n${CYAN}🛑 Parando serviços...${NC}"
    kill $API_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

echo -e "${CYAN}🌐 Tentando abrir navegador...${NC}"
sleep 3

# Tentar abrir navegador (funciona no macOS e algumas distros Linux)
if command -v open &> /dev/null; then
    open http://localhost:3001
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3001
else
    echo -e "${YELLOW}Abra manualmente: http://localhost:3001${NC}"
fi

echo -e "${GREEN}🎯 Sistema pronto para uso!${NC}"
echo -e "${BLUE}Pressione Ctrl+C para parar os serviços${NC}"

# Aguardar indefinidamente
wait
