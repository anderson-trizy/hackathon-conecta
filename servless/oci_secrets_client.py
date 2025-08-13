"""
OCI Secrets Client - Cliente simplificado para Oracle Functions
Recupera secrets do OCI Vault para uso em Oracle Functions
"""

import oci
import json
import logging
import base64
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCISecretsClient:
    """Cliente simplificado para recuperar secrets do OCI Vault"""
    
    def __init__(self, config_path: str = None, profile: str = "DEFAULT"):
        """
        Inicializar cliente OCI Secrets
        
        Args:
            config_path: Caminho para arquivo de configuração OCI (opcional)
            profile: Profile do arquivo de configuração (padrão: DEFAULT)
        """
        try:
            # Configurar cliente OCI
            if config_path:
                self.config = oci.config.from_file(config_path, profile)
            else:
                # Para Oracle Functions, usar signer de instância
                self.config = oci.config.from_file(profile_name=profile)
            
            # Cliente para secrets
            self.secrets_client = oci.secrets.SecretsClient(self.config)
            
            # Carregar mapeamento de secrets
            self.secrets_mapping = self._load_secrets_mapping()
            
            logger.info("✅ OCI Secrets Client inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar OCI Secrets Client: {str(e)}")
            raise
    
    def _load_secrets_mapping(self) -> Dict[str, str]:
        """Carregar mapeamento de secrets do arquivo JSON"""
        try:
            with open('oci_secrets_mapping.json', 'r', encoding='utf-8') as f:
                mapping_data = json.load(f)
                return mapping_data.get('secrets', {})
        except FileNotFoundError:
            logger.warning("⚠️ Arquivo oci_secrets_mapping.json não encontrado")
            return {}
        except Exception as e:
            logger.error(f"❌ Erro ao carregar mapeamento: {str(e)}")
            return {}
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        """
        Recuperar valor de um secret específico
        
        Args:
            secret_name: Nome da variável de ambiente (ex: 'OCI_NAMESPACE')
            
        Returns:
            Valor do secret ou None se não encontrado
        """
        try:
            # Buscar OCID do secret no mapeamento
            secret_ocid = self.secrets_mapping.get(secret_name)
            if not secret_ocid:
                logger.warning(f"⚠️ Secret '{secret_name}' não encontrado no mapeamento")
                return None
            
            # Recuperar conteúdo do secret
            secret_bundle = self.secrets_client.get_secret_bundle(secret_ocid)
            secret_content = secret_bundle.data.secret_bundle_content
            
            # Decodificar conteúdo Base64
            if hasattr(secret_content, 'content'):
                decoded_content = base64.b64decode(secret_content.content).decode('utf-8')
                logger.info(f"✅ Secret '{secret_name}' recuperado com sucesso")
                return decoded_content
            else:
                logger.warning(f"⚠️ Conteúdo do secret '{secret_name}' está vazio")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar secret '{secret_name}': {str(e)}")
            return None
    
    def get_all_secrets(self) -> Dict[str, str]:
        """
        Recuperar todos os secrets mapeados
        
        Returns:
            Dicionário com todos os secrets disponíveis
        """
        secrets = {}
        
        for secret_name in self.secrets_mapping.keys():
            value = self.get_secret(secret_name)
            if value:
                secrets[secret_name] = value
        
        logger.info(f"✅ Recuperados {len(secrets)} secrets")
        return secrets
    
    def get_secrets_for_function(self) -> Dict[str, str]:
        """
        Recuperar secrets essenciais para Oracle Function
        
        Returns:
            Dicionário com secrets necessários para a função
        """
        essential_secrets = [
            'OCI_NAMESPACE',
            'OCI_BUCKET_AGENT_NAME', 
            'OCI_BUCKET_RECOMMENDATION_NAME',
            'OCI_REGION',
            'OCI_COMPARTMENT_ID',
            'DATA_SOURCE_FILE'
        ]
        
        secrets = {}
        for secret_name in essential_secrets:
            value = self.get_secret(secret_name)
            if value:
                secrets[secret_name] = value
        
        logger.info(f"✅ Recuperados {len(secrets)} secrets essenciais para Function")
        return secrets

# Função de conveniência para Oracle Functions
def get_oci_secrets() -> Dict[str, str]:
    """
    Função de conveniência para Oracle Functions
    Retorna todos os secrets necessários
    """
    try:
        client = OCISecretsClient()
        return client.get_secrets_for_function()
    except Exception as e:
        logger.error(f"❌ Erro ao recuperar secrets: {str(e)}")
        return {}

# Exemplo de uso
if __name__ == "__main__":
    print("🔐 OCI Secrets Client - Teste")
    print("=" * 50)
    
    # Criar cliente
    client = OCISecretsClient()
    
    # Testar recuperação de um secret específico
    print("\n🧪 Teste: Recuperar secret específico")
    namespace = client.get_secret('OCI_NAMESPACE')
    if namespace:
        print(f"✅ OCI_NAMESPACE: {namespace}")
    
    # Recuperar secrets essenciais
    print("\n📋 Secrets essenciais para Oracle Function:")
    essential_secrets = client.get_secrets_for_function()
    for name, value in essential_secrets.items():
        print(f"  • {name}: {value[:20]}{'...' if len(value) > 20 else ''}")
    
    print(f"\n🎉 Total: {len(essential_secrets)} secrets recuperados")
