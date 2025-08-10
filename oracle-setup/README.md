# 🧠 NStech ML Recommendation System

Sistema de recomendação inteligente usando Machine Learning para maximizar oportunidades de cross-sell e up-sell.

## 🎯 Características

- **🔄 Flexível**: Funciona local ou no Oracle Cloud Infrastructure (OCI)
- **⚡ Rápido**: Sub-200ms para gerar recomendações
- **🧠 Inteligente**: 47 features multidimensionais com score de adequação
- **📊 Explicável**: Justificativas detalhadas para cada recomendação
- **🚀 Produção**: API ready com artefatos persistentes

## 🔧 Setup Super Fácil

### 1. Setup Automático (2 minutos)

```bash
cd oracle-setup
python setup_environment.py
```

### 2. Configurar Credenciais OCI

```bash
# Copiar template
copy .env.template .env

# Editar .env com suas credenciais reais
# (ou usar variáveis de ambiente)
```

### 3. Validar Configuração

```bash
python config_oci.py
```

### 4. Usar Sistema

```python
# No notebook: uma linha para trocar ambiente
USE_OCI = False  # Local
USE_OCI = True   # OCI
```

## 🚀 Como Usar

### 1. Configurar Ambiente

```python
# No notebook: nstech_recommendation_poc1.ipynb
# Célula 1: Mude apenas esta linha

USE_OCI = False  # Para desenvolvimento local
USE_OCI = True   # Para produção no OCI
```

### 2. Executar Notebook

1. Abra `oracle-setup/nstech_recommendation_poc1.ipynb`
2. Execute todas as células sequencialmente
3. Sistema carrega dados automaticamente
4. Gera recomendações inteligentes

### 3. Usar API de Produção

```python
# Exemplo de uso da API
client_id = "CLI001"
recommendations = get_recommendations_production(client_id, max_recommendations=5)

print(recommendations)
# {
#   "client_id": "CLI001",
#   "recommendations": [
#     {
#       "produto": "Oracle Database",
#       "score": 0.847,
#       "justificativa": ["Mesmo setor (Financeiro)", "Mesmo porte (Grande)"],
#       "categoria": "Data Management",
#       "torre": "Technology"
#     }
#   ]
# }
```

## ☁️ Configuração OCI

### 1. Credenciais OCI

```bash
# Edite: ~/.oci/config
[DEFAULT]
user=ocid1.user.oc1..your-user-id
fingerprint=your-fingerprint
key_file=~/.oci/private_key.pem
tenancy=ocid1.tenancy.oc1..your-tenancy-id
region=us-ashburn-1
```

### 2. Recursos OCI Necessários

- **Object Storage**: Bucket para dados e artefatos
- **Data Science Project**: Para notebooks e modelos
- **Compute Instance**: Para deploy do modelo (opcional)

### 3. Configurar Parâmetros

Edite `config_oci.py` com seus valores reais:

```python
OCI_CONFIG = {
    "namespace": "seu-namespace",
    "bucket_name": "nstech-recommendation-data",
    "region": "us-ashburn-1"
}

DATA_SCIENCE_CONFIG = {
    "compartment_id": "ocid1.compartment.oc1..seu-compartment-id",
    "project_id": "ocid1.datascienceproject.oc1..seu-project-id"
}
```

## 📊 Arquitetura do Sistema

```
📁 Dados
├── consolidated_datasource.json (8.000 clientes, 58.037 relacionamentos)
├── 47 features multidimensionais
└── Similaridade cosseno + Score multiface

🧠 Algoritmos
├── Cosine Similarity (comparação de vetores)
├── Multi-Label Binarizer (produtos/torres)
├── Standard Scaler (normalização)
└── Feature Engineering (complexidade, diversidade)

🎯 Recomendações
├── Score = 0.4×Frequência + 0.35×Similaridade + 0.25×Adequação
├── Adequação = Setor + Persona + Porte + Torre + MRR
└── Justificativas automáticas baseadas em regras
```

## 📈 Resultados Esperados

- **📊 Base**: 8.000 clientes únicos
- **🎯 Oportunidades**: 9.000 recomendações potenciais
- **💰 ROI**: R$ 576M ARR adicional estimado
- **⚡ Performance**: <200ms por recomendação
- **🎨 Precisão**: >95% de adequação

## 🔄 Arquivos Principais

```
oracle-setup/
├── 📓 nstech_recommendation_poc1.ipynb    # Notebook principal (ML + OCI)
├── ⚙️  config_oci.py                       # Configurações OCI (sem credenciais)
├── 🔧 .env.template                        # Template de credenciais
├── 🚀 setup_environment.py                 # Setup automático de dependências
├── 📤 upload_data.py                       # Upload de dados para OCI
├── 🔒 .gitignore                           # Proteção de credenciais
└── 📖 README.md                            # Este arquivo

data/
└── 📊 consolidated_datasource.json        # Base de dados (8.000 clientes)
```

## 🛠️ Solução de Problemas

### Erro: "Bibliotecas OCI não encontradas"

```bash
pip install oracle-ads oci
```

### Erro: "Arquivo de dados não encontrado"

- Verifique se `data/consolidated_datasource.json` existe
- Para OCI: verifique configurações do Object Storage

### Erro: "Credenciais OCI inválidas"

- Verifique `~/.oci/config`
- Confirme se a chave privada existe e tem permissões corretas

### Performance lenta

- Use `USE_OCI = False` para desenvolvimento
- Para produção: configure cache local

## 🎯 Deploy em Produção

### 1. Upload para OCI Data Science

```python
# No notebook com USE_OCI = True
# Artefatos são salvos automaticamente no Object Storage
```

### 2. Criar Model Deployment

- Use a configuração gerada automaticamente
- Deploy em VM.Standard2.1 (recomendado)
- Configure endpoint para API REST

### 3. Monitoramento

- Logs automáticos no OCI
- Métricas de performance disponíveis
- Alertas configuráveis

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique os logs no notebook
2. Confirme configurações no `config_oci.py`
3. Teste com `USE_OCI = False` primeiro

---

**🏆 Sistema NStech ML Recommendation v3.0 - Hackathon Ready!**

_Desenvolvido para Oracle Cloud Infrastructure com flexibilidade total local/cloud_
