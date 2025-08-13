#!/usr/bin/env python3
"""
🔐 OCI Secret Manager
====================

Módulo para gerenciar secrets usando OCI Vault (Key Management Service).
Permite criar, recuperar e atualizar secrets de forma segura na nuvem.
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

try:
    import oci
    from oci.vault import VaultsClient
    from oci.secrets import SecretsClient
    from oci.key_management import KmsVaultClient, KmsManagementClient
    from oci.key_management.models import CreateVaultDetails, CreateKeyDetails, KeyShape
    from oci.vault.models import CreateSecretDetails, SecretContentDetails, Base64SecretContentDetails
except ImportError as e:
    print("❌ Erro: SDK OCI não encontrado.")
    print("📦 Instale com: pip install oci")
    raise e

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OCISecretManager:
    """Classe para gerenciar secrets no OCI Vault."""
    
    def __init__(self, compartment_id: str, vault_id: Optional[str] = None, key_id: Optional[str] = None):
        """
        Inicializa o gerenciador de secrets.
        
        Args:
            compartment_id: OCID do compartment
            vault_id: OCID do vault (opcional, será criado se não fornecido)
            key_id: OCID da chave de criptografia (opcional, será criada se não fornecida)
        """
        self.compartment_id = compartment_id
        self.vault_id = vault_id
        self.key_id = key_id
        self.setup_clients()
    
    def setup_clients(self):
        """Configura os clientes OCI."""
        try:
            # Carregar configuração OCI
            config = oci.config.from_file()
            
            # Criar clientes
            self.vaults_client = VaultsClient(config)
            self.secrets_client = SecretsClient(config)
            self.kms_vault_client = KmsVaultClient(config)
            self.kms_management_client = None  # Será inicializado quando necessário
            
            logger.info("✅ Clientes OCI configurados com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar clientes OCI: {e}")
            raise
    
    def create_vault(self, vault_name: str, vault_type: str = "DEFAULT") -> str:
        """
        Cria um novo vault no OCI.
        
        Args:
            vault_name: Nome do vault
            vault_type: Tipo do vault (DEFAULT ou VIRTUAL_PRIVATE)
        
        Returns:
            OCID do vault criado
        """
        try:
            vault_details = CreateVaultDetails(
                compartment_id=self.compartment_id,
                display_name=vault_name,
                vault_type=vault_type
            )
            
            response = self.kms_vault_client.create_vault(vault_details)
            vault_id = response.data.id
            
            logger.info(f"✅ Vault criado: {vault_name} ({vault_id})")
            self.vault_id = vault_id
            return vault_id
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar vault: {e}")
            raise
    
    def list_vaults(self) -> list:
        """Lista todos os vaults no compartment."""
        try:
            response = self.kms_vault_client.list_vaults(
                compartment_id=self.compartment_id
            )
            
            vaults = []
            for vault in response.data:
                vaults.append({
                    'id': vault.id,
                    'name': vault.display_name,
                    'state': vault.lifecycle_state,
                    'vault_type': vault.vault_type
                })
            
            logger.info(f"📋 Encontrados {len(vaults)} vaults")
            return vaults
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar vaults: {e}")
            raise
    
    def create_key(self, key_name: str, vault_id: str = None) -> str:
        """
        Cria uma chave de criptografia no vault.
        
        Args:
            key_name: Nome da chave
            vault_id: OCID do vault (usa self.vault_id se não fornecido)
        
        Returns:
            OCID da chave criada
        """
        if not vault_id:
            vault_id = self.vault_id
        
        if not vault_id:
            raise ValueError("Vault ID não definido.")
        
        try:
            # Obter endpoint do vault para KMS Management
            vault_response = self.kms_vault_client.get_vault(vault_id)
            management_endpoint = vault_response.data.management_endpoint
            
            # Configurar cliente KMS Management
            config = oci.config.from_file()
            self.kms_management_client = KmsManagementClient(
                config, 
                service_endpoint=management_endpoint
            )
            
            # Criar shape da chave (AES 256-bit)
            key_shape = KeyShape(
                algorithm="AES",
                length=32  # 32 bytes = 256 bits
            )
            
            # Criar detalhes da chave
            key_details = CreateKeyDetails(
                compartment_id=self.compartment_id,
                display_name=key_name,
                key_shape=key_shape
            )
            
            response = self.kms_management_client.create_key(key_details)
            key_id = response.data.id
            
            logger.info(f"✅ Chave criada: {key_name} ({key_id})")
            self.key_id = key_id
            return key_id
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar chave: {e}")
            raise
    
    def list_keys(self, vault_id: str = None) -> list:
        """Lista todas as chaves no vault."""
        if not vault_id:
            vault_id = self.vault_id
            
        if not vault_id:
            raise ValueError("Vault ID não definido.")
        
        try:
            # Obter endpoint do vault
            vault_response = self.kms_vault_client.get_vault(vault_id)
            management_endpoint = vault_response.data.management_endpoint
            
            # Configurar cliente KMS Management
            config = oci.config.from_file()
            kms_client = KmsManagementClient(
                config,
                service_endpoint=management_endpoint
            )
            
            response = kms_client.list_keys(
                compartment_id=self.compartment_id
            )
            
            keys = []
            for key in response.data:
                keys.append({
                    'id': key.id,
                    'name': key.display_name,
                    'state': key.lifecycle_state,
                    'algorithm': key.key_shape.algorithm if key.key_shape else None,
                    'length': key.key_shape.length if key.key_shape else None
                })
            
            logger.info(f"📋 Encontradas {len(keys)} chaves")
            return keys
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar chaves: {e}")
            raise
    
    def create_secret(self, secret_name: str, secret_value: str, description: str = "") -> str:
        """
        Cria um novo secret no vault.
        
        Args:
            secret_name: Nome do secret
            secret_value: Valor do secret
            description: Descrição do secret
        
        Returns:
            OCID do secret criado
        """
        if not self.vault_id:
            raise ValueError("Vault ID não definido. Crie ou defina um vault primeiro.")
        
        if not self.key_id:
            raise ValueError("Key ID não definido. Crie ou defina uma chave primeiro.")
        
        try:
            # Codificar valor em base64
            import base64
            encoded_value = base64.b64encode(secret_value.encode()).decode()
            
            # Criar conteúdo do secret
            secret_content = Base64SecretContentDetails(
                content=encoded_value
            )
            
            # Criar detalhes do secret
            secret_details = CreateSecretDetails(
                compartment_id=self.compartment_id,
                vault_id=self.vault_id,
                key_id=self.key_id,  # Adicionar key_id
                secret_name=secret_name,
                description=description,
                secret_content=secret_content
            )
            
            response = self.vaults_client.create_secret(secret_details)
            secret_id = response.data.id
            
            logger.info(f"✅ Secret criado: {secret_name} ({secret_id})")
            return secret_id
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar secret '{secret_name}': {e}")
            raise
    
    def get_secret(self, secret_id: str) -> str:
        """
        Recupera o valor de um secret.
        
        Args:
            secret_id: OCID do secret
        
        Returns:
            Valor do secret decodificado
        """
        try:
            # Obter versão atual do secret
            response = self.secrets_client.get_secret_bundle(secret_id)
            
            # Decodificar conteúdo
            import base64
            encoded_content = response.data.secret_bundle_content.content
            decoded_value = base64.b64decode(encoded_content).decode()
            
            logger.info(f"✅ Secret recuperado: {secret_id}")
            return decoded_value
            
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar secret '{secret_id}': {e}")
            raise
    
    def list_secrets(self) -> list:
        """Lista todos os secrets no compartment."""
        try:
            response = self.vaults_client.list_secrets(
                compartment_id=self.compartment_id
            )
            
            secrets = []
            for secret in response.data:
                secrets.append({
                    'id': secret.id,
                    'name': secret.secret_name,
                    'state': secret.lifecycle_state,
                    'description': secret.description,
                    'vault_id': secret.vault_id
                })
            
            logger.info(f"📋 Encontrados {len(secrets)} secrets")
            return secrets
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar secrets: {e}")
            raise
    
    def bulk_create_secrets_from_env(self, env_file_path: str) -> Dict[str, str]:
        """
        Cria secrets em lote a partir de um arquivo .env.
        
        Args:
            env_file_path: Caminho para o arquivo .env
        
        Returns:
            Dicionário com nome_variavel -> secret_id
        """
        if not self.vault_id:
            raise ValueError("Vault ID não definido. Crie ou defina um vault primeiro.")
        
        # Ler arquivo .env
        env_vars = {}
        try:
            with open(env_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remover aspas se existirem
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        # Ignorar comentários inline
                        if '#' in value:
                            value = value.split('#')[0].strip()
                        
                        env_vars[key] = value
        
        except Exception as e:
            logger.error(f"❌ Erro ao ler arquivo .env: {e}")
            raise
        
        logger.info(f"📄 Encontradas {len(env_vars)} variáveis no arquivo .env")
        
        # Criar secrets
        created_secrets = {}
        for key, value in env_vars.items():
            if not value:  # Pular variáveis vazias
                continue
                
            try:
                secret_name = f"hackathon-{key.lower().replace('_', '-')}"
                description = f"Variável de ambiente: {key}"
                
                secret_id = self.create_secret(
                    secret_name=secret_name,
                    secret_value=value,
                    description=description
                )
                
                created_secrets[key] = secret_id
                
            except Exception as e:
                logger.warning(f"⚠️ Erro ao criar secret para {key}: {e}")
                continue
        
        logger.info(f"✅ Criados {len(created_secrets)} secrets com sucesso")
        return created_secrets

def main():
    """Função principal para testes e configuração inicial."""
    print("🔐 OCI Secret Manager")
    print("=" * 50)
    
    # Configurações (devem ser fornecidas)
    compartment_id = "ocid1.compartment.oc1..aaaaaaaas3bvztt44hfachktz6gplmkcloyz45rlsl6tjxifuoyak7loa5hq"
    
    try:
        # Inicializar gerenciador
        secret_manager = OCISecretManager(compartment_id)
        
        # Listar vaults existentes
        print("\n📋 Vaults existentes:")
        vaults = secret_manager.list_vaults()
        for vault in vaults:
            print(f"  • {vault['name']} ({vault['state']}) - {vault['id']}")
        
        # Se não houver vaults, criar um
        if not vaults:
            print("\n🔨 Criando novo vault...")
            vault_id = secret_manager.create_vault("hackathon-conecta-vault")
        else:
            # Usar o primeiro vault ativo
            active_vaults = [v for v in vaults if v['state'] == 'ACTIVE']
            if active_vaults:
                secret_manager.vault_id = active_vaults[0]['id']
                print(f"\n✅ Usando vault existente: {active_vaults[0]['name']}")
            else:
                print("\n🔨 Criando novo vault...")
                vault_id = secret_manager.create_vault("hackathon-conecta-vault")
        
        # Verificar/criar chave de criptografia
        print("\n🔑 Verificando chaves de criptografia...")
        try:
            keys = secret_manager.list_keys()
            
            if keys:
                # Usar primeira chave ativa
                active_keys = [k for k in keys if k['state'] == 'ENABLED']
                if active_keys:
                    secret_manager.key_id = active_keys[0]['id']
                    print(f"✅ Usando chave existente: {active_keys[0]['name']}")
                else:
                    print("🔨 Criando nova chave...")
                    key_id = secret_manager.create_key("hackathon-conecta-key")
            else:
                print("🔨 Criando nova chave...")
                key_id = secret_manager.create_key("hackathon-conecta-key")
                
        except Exception as e:
            print(f"⚠️ Erro ao verificar chaves, criando nova: {e}")
            key_id = secret_manager.create_key("hackathon-conecta-key")
        
        # Criar secrets a partir do .env
        print("\n📤 Criando secrets a partir do arquivo .env...")
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        
        if os.path.exists(env_path):
            created_secrets = secret_manager.bulk_create_secrets_from_env(env_path)
            
            print(f"\n🎉 Processo concluído!")
            print(f"✅ {len(created_secrets)} secrets criados no OCI Vault")
            
            # Salvar mapeamento para referência
            mapping_file = 'oci_secrets_mapping.json'
            with open(mapping_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'vault_id': secret_manager.vault_id,
                    'compartment_id': compartment_id,
                    'secrets': created_secrets,
                    'created_at': datetime.now().isoformat()
                }, f, indent=2)
            
            print(f"📄 Mapeamento salvo em: {mapping_file}")
            
        else:
            print(f"❌ Arquivo .env não encontrado: {env_path}")
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
