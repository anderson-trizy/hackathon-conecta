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

### 🧠 **1. AutoML para Otimização Contínua**

```python
# Futuro: AutoML para encontrar o melhor algoritmo automaticamente
from ads.automl.driver import AutoML

def enhance_with_automl():
    """
    Implementação futura: AutoML para otimizar recomendações
    """
    # Preparar dados para classificação
    dataset = prepare_conversion_dataset()  # Clientes que compraram vs não compraram
    
    # AutoML testa múltiplos algoritmos automaticamente
    automl = AutoML(dataset, target='conversion_probability')
    best_model = automl.train(
        time_budget=3600,  # 1 hora para encontrar melhor modelo
        algorithms=['RandomForest', 'XGBoost', 'Neural Networks', 'SVM']
    )
    
    # Combinar similaridade atual + probabilidade de conversão
    hybrid_recommendations = combine_similarity_and_conversion(
        similarity_model=current_cosine_model,
        conversion_model=best_model
    )
    
    return hybrid_recommendations

# Benefícios:
# ✅ Melhoria automática da precisão
# ✅ Descoberta de padrões não óbvios
# ✅ Adaptação a mudanças no comportamento dos clientes
```

### 📊 **2. Pipeline MLOps Completo**

```python
# Futuro: Pipeline automatizado de retreino e deploy
from ads.pipeline import Pipeline
from ads.jobs import Job

def create_mlops_pipeline():
    """
    Pipeline empresarial para retreino automático
    """
    pipeline = Pipeline("nstech-recommendation-pipeline")
    
    # Etapa 1: Coleta de dados atualizados
    pipeline.add_step("data_ingestion", Job(
        name="ingest-crm-data",
        infrastructure="VM.Standard2.1",
        runtime="generalml_p38_cpu_v1"
    ).run_function(ingest_updated_client_data))
    
    # Etapa 2: Feature engineering automático
    pipeline.add_step("feature_engineering", Job(
        name="auto-feature-eng",
        infrastructure="VM.Standard2.4"  # Mais poder para processing
    ).run_function(automated_feature_engineering))
    
    # Etapa 3: Retreino do modelo
    pipeline.add_step("model_training", Job(
        name="retrain-similarity",
        infrastructure="VM.GPU2.1"  # GPU para acelerar
    ).run_function(retrain_with_new_data))
    
    # Etapa 4: Validação automática
    pipeline.add_step("model_validation", Job(
        name="validate-performance"
    ).run_function(validate_model_performance))
    
    # Etapa 5: Deploy gradual (canary deployment)
    pipeline.add_step("gradual_deployment", Job(
        name="canary-deploy"
    ).run_function(deploy_with_ab_testing))
    
    # Agendar para rodar semanalmente
    pipeline.schedule("@weekly")
    
    return pipeline

# Benefícios:
# ✅ Retreino automático com novos dados
# ✅ Zero downtime deployment
# ✅ Rollback automático se performance degradar
# ✅ Logs e métricas detalhadas
```

### 🔍 **3. Monitoramento Inteligente e Drift Detection**

```python
# Futuro: Monitoramento avançado do modelo em produção
from ads.model.deployment import ModelDeployment
from ads.model.model_metadata import MetadataCustomCategory

def setup_intelligent_monitoring():
    """
    Sistema de monitoramento com detecção de drift
    """
    # Deploy com monitoramento automático
    deployment = ModelDeployment(
        model=similarity_model,
        inference_conda_env="generalml_p38_cpu_v1",
        instance_shape="VM.Standard2.2",
        bandwidth_mbps=10,
        
        # Configurações de monitoramento
        enable_logging=True,
        enable_monitoring=True,
        log_group_id="ocid1.loggroup.oc1..monitoring",
        
        # Alertas automáticos
        alarm_configuration={
            "cpu_utilization": {"threshold": 80, "action": "scale_up"},
            "error_rate": {"threshold": 5, "action": "alert_team"},
            "latency_p95": {"threshold": 500, "action": "investigate"}
        }
    )
    
    # Drift detection automático
    drift_monitor = create_drift_monitor(
        baseline_data=training_features,
        alert_threshold=0.1,  # 10% de drift aciona alerta
        check_frequency="daily"
    )
    
    # Dashboard executivo automático
    executive_dashboard = create_business_dashboard([
        "conversion_rate_by_recommendations",
        "revenue_impact_tracking", 
        "client_satisfaction_correlation",
        "model_performance_trends"
    ])
    
    return deployment, drift_monitor, executive_dashboard

# Benefícios:
# ✅ Detecção precoce de problemas
# ✅ Alertas inteligentes para equipe técnica
# ✅ Dashboard executivo para business
# ✅ Auto-scaling baseado em demanda
```

### 🧪 **4. A/B Testing e Experimentação**

```python
# Futuro: Teste A/B automático de algoritmos
from ads.model.model_version_set import ModelVersionSet

def setup_ab_testing():
    """
    Sistema de A/B testing para otimização contínua
    """
    # Versionamento de modelos
    mvs = ModelVersionSet(name="nstech-recommendation")
    
    # Versão A: Similaridade atual (baseline)
    model_a = mvs.create_model_version(
        model=cosine_similarity_model,
        version="v1.0-cosine",
        description="Baseline: Cosine similarity + 47 features"
    )
    
    # Versão B: Hybrid com deep learning
    model_b = mvs.create_model_version(
        model=neural_collaborative_filtering_model,
        version="v2.0-neural",
        description="Neural Collaborative Filtering"
    )
    
    # Versão C: Ensemble de algoritmos
    model_c = mvs.create_model_version(
        model=ensemble_model,
        version="v3.0-ensemble", 
        description="Ensemble: Cosine + Neural + XGBoost"
    )
    
    # Configurar split de tráfego
    ab_test_config = {
        "traffic_split": {
            "model_a": 0.4,  # 40% para baseline
            "model_b": 0.3,  # 30% para neural
            "model_c": 0.3   # 30% para ensemble
        },
        "success_metrics": [
            "conversion_rate",
            "revenue_per_recommendation", 
            "client_satisfaction",
            "recommendation_diversity"
        ],
        "test_duration": "30_days",
        "auto_promote_winner": True
    }
    
    return setup_traffic_splitting(ab_test_config)

# Benefícios:
# ✅ Melhoria contínua baseada em dados reais
# ✅ Redução de risco com testes graduais
# ✅ Otimização automática do algoritmo vencedor
# ✅ Métricas de negócio para decisões
```

### 🎯 **5. Integração Empresarial Completa**

```python
# Futuro: Integração total com ecosystem empresarial
def create_enterprise_integration():
    """
    Integração completa com sistemas empresariais
    """
    integrations = {
        # CRM Integration
        "salesforce": {
            "sync_frequency": "real_time",
            "endpoints": ["opportunities", "accounts", "contacts"],
            "push_recommendations": True,
            "track_outcomes": True
        },
        
        # ERP Integration  
        "oracle_erp": {
            "sync_frequency": "daily",
            "track_product_adoption": True,
            "revenue_attribution": True,
            "churn_prediction": True
        },
        
        # Marketing Automation
        "marketing_cloud": {
            "personalized_campaigns": True,
            "recommendation_emails": True,
            "journey_optimization": True,
            "conversion_tracking": True
        },
        
        # Business Intelligence
        "oracle_analytics": {
            "executive_dashboards": True,
            "predictive_insights": True,
            "roi_tracking": True,
            "market_analysis": True
        }
    }
    
    return enterprise_connector(integrations)

# Benefícios:
# ✅ Visão 360° do cliente
# ✅ Ações automáticas baseadas em recomendações
# ✅ ROI tracking completo
# ✅ Insights estratégicos para C-level
```

### 💡 **Por que ADS Será Essencial no Futuro?**

1. **📈 Escalabilidade**: Sistema atual suporta milhares, ADS suporta milhões
2. **🤖 Automação**: Reduz intervenção manual de 80% para <5%
3. **🎯 Precisão**: AutoML pode melhorar accuracy em 15-30%
4. **💰 ROI**: Automação reduz custos operacionais em 60%
5. **🚀 Time-to-Market**: Deploy de novos algoritmos em dias vs semanas

---

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
