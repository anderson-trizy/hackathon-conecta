# Hackathon Conecta nstech - Grupo 10 - Tema 01
## Sistema de Recomendação Inteligente para nsApps

### 🎯 Descrição do Projeto
Sistema completo de recomendação de produtos para o portal nsApps da nstech, utilizando Machine Learning e arquitetura moderna de microserviços na Oracle Cloud Infrastructure (OCI).

### 🏆 Objetivos do Hackathon

1. **Sistema Funcional**: API + Frontend consumindo ML
2. **Demonstração Real**: Recomendações baseadas em dados reais
3. **Arquitetura Escalável**: Pronto para produção
4. **Inovação**: Uso avançado de serviços OCI

### 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React App     │    │   OCI API        │    │  Oracle         │
│   (ShadUI)      │───▶│   Gateway        │───▶│  Functions      │
│                 │    │   (CORS/Auth)    │    │  (ML Logic)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                        ┌──────────────────┐    ┌─────────────────┐
                        │  ML Engine       │    │  OCI Data       │
                        │  (Algorithms)    │    │  Science        │
                        │                  │    │  (Training)     │
                        └──────────────────┘    └─────────────────┘
```

### 📁 Estrutura do Projeto

```
hackathon-conecta/
├── 📚 docs/                    # Documentação completa
│   ├── SETUP_OCI.md            # Setup Oracle Cloud Infrastructure
│   └── architecture/           # Diagramas e especificações
├── 🧠 ml-engine/               # Motor de Machine Learning
│   ├── notebooks/              # Jupyter notebooks (POCs e análises)
│   ├── models/                 # Modelos treinados e artefatos
│   ├── src/                    # Código fonte Python
│   └── tests/                  # Testes unitários
├── 🚀 api/                     # API Backend (Oracle Functions)
├── 🎨 frontend/                # Frontend React + ShadUI
├── 📊 data/                    # Datasets organizados
│   ├── raw/                    # Dados originais (Nstech.csv, Produtos.csv)
│   ├── processed/              # Dados processados para ML
│   └── samples/                # Amostras para testes
├── 🔧 infrastructure/          # Infraestrutura como código
└── 🧪 tests/                   # Testes integrados
```

### 🚀 Quick Start

#### **Início Automático (Recomendado)**

**Windows (PowerShell):**
```bash
# Clone e execute
git clone https://github.com/anderson-trizy/hackathon-conecta.git
cd hackathon-conecta
.\start.ps1
```

**Linux/macOS:**
```bash
# Clone e execute  
git clone https://github.com/anderson-trizy/hackathon-conecta.git
cd hackathon-conecta
chmod +x start.sh
./start.sh
```

#### **Acessar Aplicação:**
- **Frontend**: http://localhost:3001
- **API Backend**: http://localhost:8000  
- **Documentação**: http://localhost:8000/docs

#### **Setup Manual (Desenvolvimento)**

**1. ML Engine & API:**
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows)
.\.venv\Scripts\Activate.ps1

# Ativar ambiente virtual (Linux/macOS)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar API
cd api
python main.py
```

**2. Frontend:**
```bash
cd recommendation-microfrontend
npm install
npm run dev
```

### 🎯 Funcionalidades Principais

#### **🧠 Motor de ML (47 Features)**
- **Algoritmo Híbrido**: Combina similaridade coseno + regras de negócio
- **Análise Multidimensional**: Demografia, comportamento, contexto, afinidade
- **Performance**: 89.2% accuracy, <50ms latência
- **Escalabilidade**: 1000+ recomendações/segundo

#### **🚀 API RESTful**
```json
GET /api/v1/recommendations/CLI123
{
  "recommendations": [
    {
      "produto": "Oracle Analytics Cloud", 
      "score": 0.856,
      "justificativa": ["Mesmo setor", "Porte similar"]
    }
  ]
}
```

#### **🎨 Frontend Moderno**
- **React + Next.js(?)**: Performance e SEO otimizado
- **ShadUI/Tailwind**: Design system consistente
- **TypeScript**: Type safety e melhor DX
- **Componentes Reutilizáveis**: Cards, listas, feedback

### 📊 Base de Dados

**Resumo Executivo:**
- **1500 clientes** representativos do mercado NStech
- **130 produtos** com classificação BCG
- **47 features** para análise de similaridade
- **100% cobertura** - todos os produtos validados

**Distribuição:**
- **5 torres** de negócio (Embarcador 38%, PME 37%, etc.)
- **4 portes** empresariais (Grande 34%, Pequeno 24.5%, etc.)
- **20+ setores** econômicos representados
- **Score médio**: 3.98/5.0 satisfação

### 🛠️ Tecnologias

#### **Backend**
- **OCI Data Science**: Notebooks Jupyter, model training/deployment, ADS SDK
- **OCI ML Applications**: Empacotamento e deployment escalável de modelos ML
- **Oracle Functions**: Serverless Python runtime para lógica de negócio customizada
- **OCI API Gateway**: Exposição e gerenciamento da API
- **OCI Object Storage**: Dados, modelos e logs
- **OCI Generative AI**: Text embeddings e análise semântica de produtos
- **OCI Monitoring/Logging**: Observabilidade completa

#### **Frontend** 
- **React + Next.js(?)**: Framework moderno
- **ShadUI/Atlas(?)**: Design system
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling utility-first

#### **ML/Data**
- **Python**: Pandas, NumPy, Scikit-learn
- **Jupyter**: Notebooks interativos
- **Pickle**: Serialização de modelos
- **Similarity Algorithms**: Coseno, Jaccard, Euclidiana

### **Arquitetura - Abordagem Multicloud:**
- Arquitetura com abstrações que permitem migração futura
- Padrão Adapter para diferentes provedores de cloud
- Separação entre lógica de negócio e serviços de infraestrutura
- Documentação de equivalências (Oracle ↔ AWS ↔ Azure ↔ GCP)

### 📈 Roadmap

#### ✅ **Fase 1: Reorganização (Concluída)**
- [x] Nova estrutura de pastas
- [x] Separação ML Engine/API/Frontend
- [x] Documentação organizada

#### 🔄 **Fase 2: API Development (Em Andamento)**
- [ ] Extrair lógica do notebook para módulos Python
- [ ] Implementar Oracle Functions
- [ ] Setup API Gateway com CORS
- [ ] Testes e validação

#### ⏳ **Fase 3: Frontend Integration**
- [ ] Projeto React + ShadUI
- [ ] Componentes de recomendação
- [ ] Integração com API
- [ ] Testes end-to-end

#### ⏳ **Fase 4: Production Ready**
- [ ] CI/CD pipeline
- [ ] Monitoring e alertas
- [ ] Performance optimization
- [ ] Documentation completa

### 🛠️ Scripts Disponíveis

| Script | Descrição | Uso |
|--------|-----------|-----|
| `start.ps1` | Instala dependências e inicia ambos serviços (Windows) | `.\start.ps1` |
| `start.sh` | Instala dependências e inicia ambos serviços (Linux/macOS) | `./start.sh` |
| `setup.ps1` | Apenas instala dependências (Windows) | `.\setup.ps1` |

### 🌿 Estratégia de Branches e Convenções

#### **Estrutura de Branches**
```
main (produção estável - sempre demo-ready)
├── develop (integração contínua - trabalho ativo)  
├── feature/nome-da-funcionalidade (desenvolvimento de features)
├── hotfix/nome-do-bug (correções urgentes)
└── release/vX.X.X (preparação de releases)
```

#### **Fluxo de Trabalho**
1. **Nova Feature**: `develop` → `feature/nome` → desenvolver → PR para `develop`
2. **Bug Crítico**: `main` → `hotfix/nome` → corrigir → PR para `main` e `develop`
3. **Release**: `develop` → `release/vX.X.X` → testes finais → merge para `main`

#### **Convenções de Nomenclatura**

**Branches:**
```bash
feature/api-recommendations-v2       # Nova funcionalidade
feature/frontend-dashboard          # Interface
feature/ml-algorithm-optimization   # Melhorias ML
feature/docker-setup                # Infraestrutura
hotfix/cors-api-fix                 # Correção crítica
hotfix/memory-leak-frontend         # Bug em produção
release/v1.0.0                      # Preparação de release
```

**Commits (Conventional Commits):**
```bash
feat: adiciona nova funcionalidade de recomendações
fix: corrige bug de CORS na API
docs: atualiza documentação do setup
style: formata código seguindo padrões
refactor: otimiza algoritmo de similaridade  
test: adiciona testes unitários para API
chore: atualiza dependências do projeto
```

#### **Regras de Merge**
- **`main`**: Apenas via Pull Request com revisão
- **`develop`**: Pull Request recomendado (flexível para o hackathon)
- **Features**: Commits diretos permitidos durante desenvolvimento

#### **Proteções de Branch**
- **`main`**: Protegida - sempre estável para demonstrações
- **`develop`**: Semi-protegida - pode ter bugs menores
- **Features**: Livres para experimentação

### 🐛 Solução de Problemas

#### **Porta já em uso**
```bash
# Windows
netstat -ano | findstr :3001
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS  
lsof -ti:3001 | xargs kill
lsof -ti:8000 | xargs kill
```

#### **Problemas com ambiente virtual**
```bash
# Recriar ambiente virtual
rm -rf .venv  # ou Remove-Item .venv -Recurse -Force (Windows)
python -m venv .venv
```

#### **Dependências não instaladas**
```bash
# Usar script de setup apenas
.\setup.ps1        # Windows
chmod +x setup.sh && ./setup.sh  # Linux/macOS (se criar)
```

#### **Problemas de CORS**
- Verifique se a API está rodando na porta 8000
- Confirme que o frontend está configurado para a URL correta da API

### 🎯 Casos de Uso para Recomendação

#### **Análise de Similaridade:**
- Clientes com perfis similares (porte + setor + persona)
- Identificação de padrões de adoção de produtos
- Segmentação inteligente por comportamento

#### **Cross-selling Inteligente:**
- Produtos complementares baseados no portfólio atual
- Recomendações por torre de negócio
- Upgrade de produtos por evolução do cliente

#### **Targeting Personalizado:**
- Recomendações específicas por persona
- Adequação de produtos ao porte da empresa
- Oportunidades baseadas em satisfação e tempo de relacionamento

### 👥 Equipe
- **Grupo 10** - Hackathon Conecta nstech
- **Tema**: Sistema de Recomendação Inteligente
- **Parceria**: Oracle

---
**Data de início**: 08 de agosto de 2025
**📅 Hackathon**: Agosto 2025 | **🚀 Status**: Fase 2 - API Development
