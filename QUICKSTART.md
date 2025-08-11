# 🚀 Como Executar o Projeto

## Início Rápido (1 comando)

### Windows
```bash
git clone https://github.com/anderson-trizy/hackathon-conecta.git
cd hackathon-conecta
.\start.ps1
```

### Linux/macOS
```bash
git clone https://github.com/anderson-trizy/hackathon-conecta.git
cd hackathon-conecta
chmod +x start.sh
./start.sh
```

## ✅ O que o script faz:

1. **Verifica pré-requisitos** (Python 3.8+, Node.js 16+)
2. **Cria ambiente virtual** Python
3. **Instala dependências** Python (FastAPI, pandas, etc)
4. **Instala dependências** Node.js (React, Vite, etc)
5. **Inicia API** na porta 8000
6. **Inicia Frontend** na porta 3001
7. **Abre navegador** automaticamente

## 🌐 URLs da Aplicação

- **Frontend**: http://localhost:3001
- **API**: http://localhost:8000  
- **Documentação**: http://localhost:8000/docs

## 🔧 Pré-requisitos

- **Python 3.8+**: https://python.org/downloads
- **Node.js 16+**: https://nodejs.org

## 🛑 Como Parar

- Feche as janelas dos terminais
- Ou pressione `Ctrl+C` em cada terminal

## ❗ Problemas?

### Porta ocupada
```bash
# Windows
netstat -ano | findstr :3001
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:3001 | xargs kill
```

### Reinstalar dependências
```bash
# Apagar ambiente virtual
rm -rf .venv
# Executar script novamente  
.\start.ps1
```
