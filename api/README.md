# 🧠 API de Recomendações Avançada

## Algoritmo Completo do Notebook (47 Dimensões)

Esta API implementa o algoritmo exato usado no Jupyter Notebook de análise, com todas as funcionalidades avançadas migradas do `backup-api-v2`.

## 🚀 Funcionalidades

### 🎯 **Engine Avançada (AdvancedMLEngine)**
- **47 dimensões de features** com TF-IDF e MultiLabelBinarizer
- **Features categóricas**: Setor, Porte, Torre (LabelEncoder)
- **Features numéricas**: MRR, Satisfação (StandardScaler)
- **Produtos**: Mapeamento produto→portfólio→torre
- **Similaridade**: Algoritmo cosseno avançado

### 📊 **Scoring Ponderado**
- **40%** Frequência de produto
- **35%** Similaridade de cliente
- **25%** Fit do produto

### 🔧 **Serviço Avançado (AdvancedRecommendationService)**
- Recomendações com cache inteligente
- Análise de clientes similares
- Análise completa do cliente
- Health check detalhado

## 📡 **Endpoints**

### Básicos
- `GET /` - Informações da API
- `GET /health` - Status da engine avançada

### Recomendações
- `GET /recommendations/{client_id}?top_k=5&use_cache=true`
- `GET /client/{client_id}` - Informações do cliente
- `GET /similar/{client_id}?top_k=10` - Clientes similares
- `GET /analysis/{client_id}` - **Análise completa**

## 🏃‍♂️ **Como Executar**

```bash
# Navegar para a pasta
cd api

# Ativar ambiente virtual
..\.venv\Scripts\Activate.ps1

# Instalar dependências avançadas
pip install -r requirements.txt

# Executar API
python main.py
```

## 🌐 **URLs**
- **API**: http://127.0.0.1:8000
- **Docs**: http://127.0.0.1:8000/docs
- **Health**: http://127.0.0.1:8000/health

## 🔍 **Exemplo de Uso**

### Recomendações Avançadas
```bash
curl "http://127.0.0.1:8000/recommendations/client_1?top_k=3"
```

**Resposta:**
```json
{
  "client_id": "client_1",
  "recommendations": [
    {
      "product_name": "CRM Advanced",
      "confidence": 0.87,
      "reason": "Baseado em 15 clientes similares",
      "similarity_strength": 0.75
    }
  ],
  "source": "generated",
  "algorithm": "advanced_notebook_47_dimensions",
  "features_used": "47_dimensions_tfidf_mlb",
  "scoring": "weighted_40freq_35sim_25fit"
}
```

### Análise Completa
```bash
curl "http://127.0.0.1:8000/analysis/client_1"
```

**Resposta:**
```json
{
  "client_id": "client_1",
  "analysis_type": "full_advanced_analysis",
  "client_info": {...},
  "recommendations": {...},
  "similar_clients_analysis": {...},
  "algorithm_details": {
    "engine": "advanced_notebook_replica",
    "features": "47_dimensions",
    "methods": ["TF-IDF", "MultiLabelBinarizer", "LabelEncoder", "StandardScaler"],
    "scoring": "weighted_frequency_similarity_fit"
  }
}
```

## 🏗️ **Arquitetura**

```
api/
├── main.py                     # FastAPI principal
├── core/
│   ├── advanced_service.py     # Serviço avançado
│   └── recommendation.py       # Serviço simples (backup)
├── adapters/
│   ├── interfaces.py           # Contratos multicloud
│   └── local/
│       ├── adapters.py         # Adapters simples
│       └── advanced_engine.py  # 🧠 Engine avançada (47D)
└── requirements.txt
```

## 🔄 **Migração do Backup**

Esta API migra **100% da lógica** do `backup-api-v2`:
- ✅ NotebookRecommendationEngine → AdvancedMLEngine
- ✅ NotebookRecommendationService → AdvancedRecommendationService
- ✅ 47 dimensões de features
- ✅ TF-IDF + MultiLabelBinarizer
- ✅ Score ponderado (40/35/25)
- ✅ Algoritmo exato do notebook

## 🌍 **Multicloud Ready**

Mantém compatibilidade para Oracle Functions:
- Interfaces definidas para OCI, AWS, Azure
- Configuração via `CLOUD_PROVIDER` env var
- Oracle Functions entry point preparado

## 📈 **Performance**

- **Cache inteligente** com expiração
- **Inicialização lazy** da engine
- **Features pré-computadas** 
- **Similaridade otimizada** com threshold
