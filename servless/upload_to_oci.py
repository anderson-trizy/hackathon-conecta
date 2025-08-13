#!/usr/bin/env python3
"""
📤 Upload to OCI Object Storage
===============================

Script para fazer upload do consolidated_datasource_fresh.json para o bucket OCI.
Integra com o job do Airtable para automatizar o processo completo.
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Importar SDK OCI
try:
    import oci
    from oci.object_storage import ObjectStorageClient
    from oci.object_storage.models import CreateBucketDetails
except ImportError as e:
    print("❌ Erro: SDK OCI não encontrado.")
    print("📦 Instale com: pip install oci")
    sys.exit(1)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('oci_upload.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OCIUploader:
    """Classe para fazer upload de arquivos para OCI Object Storage."""
    
    def __init__(self):
        """Inicializa o cliente OCI."""
        self.load_config()
        self.setup_client()
    
    def load_config(self):
        """Carrega configurações do arquivo .env."""
        # Carregar .env da raiz do projeto
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        
        # Configurações obrigatórias
        self.namespace = os.getenv('OCI_NAMESPACE')
        self.bucket_name = os.getenv('OCI_BUCKET_RECOMMENDATION_NAME')  # Usar bucket de recomendações
        self.region = os.getenv('OCI_REGION')
        self.compartment_id = os.getenv('OCI_COMPARTMENT_ID')
        
        # Configurações de autenticação (opcionais)
        self.config_file = os.getenv('OCI_CONFIG_FILE', '~/.oci/config')
        self.config_profile = os.getenv('OCI_CONFIG_PROFILE', 'DEFAULT')
        
        # Validar configurações obrigatórias
        required_configs = {
            'OCI_NAMESPACE': self.namespace,
            'OCI_BUCKET_RECOMMENDATION_NAME': self.bucket_name,
            'OCI_REGION': self.region,
            'OCI_COMPARTMENT_ID': self.compartment_id
        }
        
        missing_configs = [key for key, value in required_configs.items() if not value]
        if missing_configs:
            logger.error(f"❌ Configurações obrigatórias ausentes no .env: {', '.join(missing_configs)}")
            sys.exit(1)
        
        logger.info(f"✅ Configurações carregadas:")
        logger.info(f"   📁 Namespace: {self.namespace}")
        logger.info(f"   🪣 Bucket: {self.bucket_name}")
        logger.info(f"   🌐 Região: {self.region}")
    
    def setup_client(self):
        """Configura o cliente OCI Object Storage."""
        try:
            # Expandir ~ no caminho do arquivo de configuração
            config_file_path = os.path.expanduser(self.config_file)
            
            # Carregar configuração OCI
            config = oci.config.from_file(config_file_path, self.config_profile)
            config['region'] = self.region
            
            # Criar cliente Object Storage
            self.object_storage_client = ObjectStorageClient(config)
            
            logger.info("✅ Cliente OCI configurado com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar cliente OCI: {e}")
            logger.error("💡 Verifique se o arquivo ~/.oci/config existe e está configurado corretamente")
            sys.exit(1)
    
    def get_file_info(self, file_path):
        """Obtém informações do arquivo a ser enviado."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        file_size = file_path.stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        
        return {
            'path': file_path,
            'size_bytes': file_size,
            'size_mb': round(file_size_mb, 2),
            'name': file_path.name
        }
    
    def upload_file(self, local_file_path, object_name=None):
        """
        Faz upload de um arquivo para o bucket OCI.
        
        Args:
            local_file_path (str): Caminho local do arquivo
            object_name (str): Nome do objeto no bucket (opcional)
        
        Returns:
            dict: Informações do upload realizado
        """
        try:
            # Obter informações do arquivo
            file_info = self.get_file_info(local_file_path)
            
            if not object_name:
                object_name = file_info['name']
            
            logger.info(f"📤 Iniciando upload:")
            logger.info(f"   📄 Arquivo: {file_info['name']}")
            logger.info(f"   📊 Tamanho: {file_info['size_mb']} MB")
            logger.info(f"   🎯 Destino: {object_name}")
            
            # Ler arquivo
            with open(file_info['path'], 'rb') as file_data:
                # Fazer upload
                response = self.object_storage_client.put_object(
                    namespace_name=self.namespace,
                    bucket_name=self.bucket_name,
                    object_name=object_name,
                    put_object_body=file_data,
                    content_type='application/json'
                )
            
            # Informações do upload
            upload_info = {
                'object_name': object_name,
                'bucket_name': self.bucket_name,
                'namespace': self.namespace,
                'etag': response.headers.get('etag'),
                'last_modified': response.headers.get('last-modified'),
                'file_size_mb': file_info['size_mb'],
                'upload_time': datetime.now().isoformat()
            }
            
            logger.info("✅ Upload concluído com sucesso!")
            logger.info(f"   🏷️  ETag: {upload_info['etag']}")
            logger.info(f"   ⏰ Modificado: {upload_info['last_modified']}")
            
            return upload_info
            
        except Exception as e:
            logger.error(f"❌ Erro durante upload: {e}")
            raise
    
    def list_objects(self, prefix=None):
        """Lista objetos no bucket."""
        try:
            response = self.object_storage_client.list_objects(
                namespace_name=self.namespace,
                bucket_name=self.bucket_name,
                prefix=prefix
            )
            
            objects = response.data.objects
            logger.info(f"📋 Objetos no bucket ({len(objects)} encontrados):")
            
            for obj in objects:
                size_mb = obj.size / (1024 * 1024) if obj.size else 0
                logger.info(f"   📄 {obj.name} ({size_mb:.2f} MB)")
            
            return objects
            
        except Exception as e:
            logger.error(f"❌ Erro ao listar objetos: {e}")
            raise

def main():
    """Função principal."""
    print("🚀 Iniciando upload para OCI Object Storage...")
    
    try:
        # Inicializar uploader
        uploader = OCIUploader()
        
        # Caminho do arquivo consolidado
        datasource_file = Path(__file__).parent / 'consolidated_datasource_fresh.json'
        
        if not datasource_file.exists():
            logger.error(f"❌ Arquivo não encontrado: {datasource_file}")
            logger.info("💡 Execute primeiro o job do Airtable: python airtable_datasource_job.py")
            sys.exit(1)
        
        # Gerar nome do objeto com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        object_name = f"datasources/consolidated_datasource_{timestamp}.json"
        
        # Fazer upload
        upload_info = uploader.upload_file(datasource_file, object_name)
        
        # Também fazer upload com nome fixo (última versão)
        latest_object_name = "datasources/consolidated_datasource_latest.json"
        latest_upload_info = uploader.upload_file(datasource_file, latest_object_name)
        
        # Listar arquivos no bucket
        uploader.list_objects(prefix="datasources/")
        
        print("\n🎉 Upload completo!")
        print(f"📤 Arquivos enviados:")
        print(f"   • {object_name}")
        print(f"   • {latest_object_name}")
        print(f"📊 Tamanho: {upload_info['file_size_mb']} MB")
        
        return upload_info
        
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
