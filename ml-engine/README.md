# ML Engine - NStech Recommendation System

## 📋 Visão Geral

Este módulo contém toda a lógica de Machine Learning para o sistema de recomendação da NStech.

## 📁 Estrutura Atual

```
ml-engine/
├── notebooks/          # ✅ Jupyter notebooks para análise e prototipagem
│   └── nstech_recommendation_poc1.ipynb
├── models/            # ✅ Modelos treinados e artefatos
│   └── model_artifacts.pkl
├── src/               # ✅ Código fonte Python
│   ├── config_oci.py      # Configuração OCI
│   ├── setup_environment.py  # Setup do ambiente
│   ├── upload_data.py     # Upload de dados
│   └── __init__.py        # Package marker
├── requirements.txt   # ✅ Dependências Python
├── config.yaml       # ✅ Configurações do ML
└── README.md         # ✅ Esta documentação
```

## 📁 Expansão Futura (Just-In-Time)

As seguintes estruturas serão criadas **quando necessárias** na Fase 2:

### src/ (Módulos ML - Fase 2)

- `recommender.py`: Lógica principal de recomendação
- `data_processor.py`: Processamento de dados
- `feature_engineering.py`: Engenharia de features
- `model_trainer.py`: Treinamento de modelos

### tests/ (Fase 2+)

- `test_recommender.py`: Testes do sistema de recomendação
- `test_data_processor.py`: Testes de processamento
- Criada quando implementarmos testes automatizados

## 🚀 Quick Start

### 1. Instalação

```bash
cd ml-engine
pip install -r requirements.txt
```

### 2. Executar Notebook

```bash
jupyter notebook notebooks/nstech_recommendation_poc1.ipynb
```

### 3. Usar como módulo (Fase 2)

```python
from ml_engine.src.recommender import NSTechRecommender

recommender = NSTechRecommender()
recommendations = recommender.get_recommendations("CLI123", limit=5)
```

## 🔧 Funcionalidades

- **Algoritmo Híbrido**: Combina múltiplas abordagens de recomendação
- **47 Features**: Análise multidimensional de clientes e produtos
- **Similarity Matrix**: Matriz de similaridade pré-computada
- **Feedback Loop**: Sistema de aprendizado contínuo

## 📊 Performance

- **Accuracy**: 89.2% (teste interno)
- **Latência**: <50ms para recomendações
- **Throughput**: 1000+ recomendações/segundo

## 📝 Notebooks Disponíveis

- ✅ `nstech_recommendation_poc1.ipynb`: POC principal e sistema completo
- ⏳ `data_exploration.ipynb`: Análise exploratória dos dados (Fase 2)
- ⏳ `model_training.ipynb`: Treinamento e avaliação de modelos (Fase 2)
