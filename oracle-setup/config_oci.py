# 🔧 CONFIGURAÇÃO OCI - NSTECH RECOMMENDATION SYSTEM
"""
Arquivo de configuração para facilitar o setup do OCI.
Credenciais são carregadas de variáveis de ambiente ou arquivo .env
"""

import os
from pathlib import Path

def load_env_file():
    """Carrega variáveis de ambiente de arquivo .env se existir"""
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"')

# Carregar variáveis de ambiente
load_env_file()

# 🌐 CONFIGURAÇÕES GERAIS
OCI_CONFIG = {
    # Namespace do Object Storage (obrigatório)
    "namespace": os.getenv("OCI_NAMESPACE"),
    
    # Bucket para dados e artefatos
    "bucket_name": os.getenv("OCI_BUCKET_NAME"),
    
    # Região OCI
    "region": os.getenv("OCI_REGION"),
}

# 📁 OBJECT STORAGE
OBJECT_STORAGE_CONFIG = {
    # Arquivo de dados principal
    "data_object": os.getenv("DATA_SOURCE_FILE"),
    
    # Arquivo de artefatos do modelo
    "model_artifacts_object": "model_artifacts.pkl",
    
    # Arquivo de configuração de deploy
    "deploy_config_object": "deployment_config.json",
}

# 🧪 DATA SCIENCE PROJECT
DATA_SCIENCE_CONFIG = {
    # ID do compartment (obrigatório)
    "compartment_id": os.getenv("OCI_COMPARTMENT_ID"),
    
    # ID do projeto Data Science (obrigatório)  
    "project_id": os.getenv("OCI_PROJECT_ID"),
    
    # Nome do projeto
    "project_name": os.getenv("PROJECT_NAME"),
}

# 🚀 MODEL DEPLOYMENT
MODEL_DEPLOYMENT_CONFIG = {
    # Nome do modelo deployment
    "display_name": "nstech-recommendation-model",
    
    # Descrição
    "description": "Sistema de Recomendação ML NStech - Hackathon",
    
    # Shape da instância
    "instance_shape": "VM.Standard2.1",
    
    # Configuração de recursos
    "memory_gb": 8,
    "ocpus": 1,
    
    # ID do modelo (será preenchido após criar o modelo)
    "model_id": os.getenv("OCI_MODEL_ID"),
}

# 🔐 CONFIGURAÇÃO DE AUTENTICAÇÃO
AUTH_CONFIG = {
    # Caminho para o arquivo de configuração OCI
    "config_file": os.getenv("OCI_CONFIG_FILE"),
    
    # Profile a ser usado (DEFAULT é o padrão)
    "profile": os.getenv("OCI_CONFIG_PROFILE"),
    
    # Caminho para a chave privada
    "key_file": os.getenv("OCI_KEY_FILE"),
}

# 📊 CONFIGURAÇÕES DO MODELO ML
ML_CONFIG = {
    # Threshold mínimo de similaridade
    "min_similarity": float(os.getenv("SIMILARITY_THRESHOLD")) if os.getenv("SIMILARITY_THRESHOLD") else None,
    
    # Número máximo de recomendações por padrão
    "max_recommendations": int(os.getenv("MAX_RECOMMENDATIONS")) if os.getenv("MAX_RECOMMENDATIONS") else None,
    
    # Taxa de conversão estimada para cálculos de ROI
    "conversion_rate": float(os.getenv("CONVERSION_RATE")) if os.getenv("CONVERSION_RATE") else None,
    
    # MRR médio por produto para cálculos de ROI
    "avg_mrr_per_product": int(os.getenv("AVG_MRR_PER_PRODUCT")) if os.getenv("AVG_MRR_PER_PRODUCT") else None,
    
    # Caminho para dados locais
    "local_data_path": os.getenv("LOCAL_DATA_PATH"),
}

# 🎯 INSTRUÇÕES DE USO
INSTRUCTIONS = """
🔧 COMO CONFIGURAR CREDENCIAIS:

OPÇÃO 1 - ARQUIVO .env (RECOMENDADO):
Crie um arquivo .env na pasta oracle-setup/ com:

OCI_NAMESPACE=seu-namespace-aqui
OCI_BUCKET_NAME=nstech-recommendation-data
OCI_REGION=us-chicago-1
OCI_COMPARTMENT_ID=ocid1.tenancy.oc1..seu-compartment-id
OCI_PROJECT_ID=ocid1.datascienceproject.oc1..seu-project-id
OCI_MODEL_ID=ocid1.datasciencemodel.oc1..seu-model-id
OCI_CONFIG_FILE=~/.oci/config
OCI_CONFIG_PROFILE=DEFAULT
OCI_KEY_FILE=~/.oci/private_key.pem

OPÇÃO 2 - VARIÁVEIS DE AMBIENTE:
export OCI_NAMESPACE=seu-namespace-aqui
export OCI_COMPARTMENT_ID=ocid1.tenancy.oc1..seu-compartment-id
# ... etc

OPÇÃO 3 - ARQUIVO ~/.oci/config:
[DEFAULT]
user=ocid1.user.oc1..seu-user-id
fingerprint=seu-fingerprint
key_file=~/.oci/private_key.pem
tenancy=ocid1.tenancy.oc1..seu-tenancy-id
region=us-chicago-1
compartment_id=ocid1.tenancy.oc1..seu-compartment-id

✅ O arquivo .env é ignorado pelo git automaticamente!
✅ Nunca comite credenciais reais no código!
"""

def validate_config():
    """Valida se as configurações necessárias estão definidas"""
    
    # Primeiro verificar se o arquivo .env existe
    env_file = Path(__file__).parent / '.env'
    if not env_file.exists():
        print("❌ ARQUIVO .env NÃO ENCONTRADO!")
        print("   1. Copie o arquivo: copy .env.template .env")
        print("   2. Edite o .env com suas credenciais reais")
        return False
    
    # Configurações obrigatórias
    required_configs = {
        "OCI_NAMESPACE": OCI_CONFIG["namespace"],
        "OCI_BUCKET_NAME": OCI_CONFIG["bucket_name"],
        "OCI_REGION": OCI_CONFIG["region"],
        "OCI_COMPARTMENT_ID": DATA_SCIENCE_CONFIG["compartment_id"],
        "OCI_PROJECT_ID": DATA_SCIENCE_CONFIG["project_id"],
        "PROJECT_NAME": DATA_SCIENCE_CONFIG["project_name"],
        "DATA_SOURCE_FILE": OBJECT_STORAGE_CONFIG["data_object"],
        "LOCAL_DATA_PATH": ML_CONFIG["local_data_path"]
    }
    
    missing = []
    for key, value in required_configs.items():
        if not value or value == "" or value is None:
            missing.append(key)
    
    if missing:
        print(f"❌ CONFIGURAÇÕES FALTANDO NO ARQUIVO .env:")
        for config in missing:
            print(f"   - {config}")
        print("\n📝 Edite o arquivo .env e adicione todas as configurações obrigatórias")
        return False
    
    print("✅ Todas as configurações obrigatórias estão definidas")
    print("✅ Arquivo .env encontrado e válido")
    return True

if __name__ == "__main__":
    print("🔧 CONFIGURAÇÃO OCI - NSTECH RECOMMENDATION SYSTEM")
    print("="*60)
    print(INSTRUCTIONS)
    
    # Validar configurações
    print("\n🔍 VALIDANDO CONFIGURAÇÕES:")
    validate_config()
    
    print(f"\n📊 CONFIGURAÇÕES ATUAIS:")
    print(f"   Namespace: {OCI_CONFIG['namespace'] or 'NÃO DEFINIDO'}")
    print(f"   Region: {OCI_CONFIG['region']}")
    print(f"   Bucket: {OCI_CONFIG['bucket_name']}")
    print(f"   Compartment ID: {DATA_SCIENCE_CONFIG['compartment_id'][:20] + '...' if DATA_SCIENCE_CONFIG['compartment_id'] else 'NÃO DEFINIDO'}")
    print(f"   Project ID: {DATA_SCIENCE_CONFIG['project_id'][:20] + '...' if DATA_SCIENCE_CONFIG['project_id'] else 'NÃO DEFINIDO'}")
