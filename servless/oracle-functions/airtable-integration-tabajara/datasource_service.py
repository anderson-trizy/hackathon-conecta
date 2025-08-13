#!/usr/bin/env python3
"""
🔄 Serviço de Atualização de Datasource
======================================

Serviço desacoplado para executar o job de extração do Airtable + upload OCI.
Pode ser chamado por Oracle Functions, APIs, cron jobs, etc.
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DatasourceUpdateService:
    """Serviço para atualização do datasource."""
    
    def __init__(self):
        """Inicializa o serviço."""
        self.start_time = datetime.now()
        self.job_id = self.start_time.strftime("%Y%m%d_%H%M%S")
        
    def execute_job(self) -> Dict[str, Any]:
        """
        Executa o job completo de atualização do datasource.
        
        Returns:
            dict: Resultado da execução do job
        """
        try:
            logger.info(f"🚀 Iniciando job de atualização datasource - ID: {self.job_id}")
            
            # 1. Importar e executar extração Airtable
            result_airtable = self._execute_airtable_extraction()
            if not result_airtable['success']:
                return result_airtable
            
            # 2. Executar upload para OCI
            result_oci = self._execute_oci_upload(result_airtable['file_path'])
            
            # 3. Compilar resultado final
            end_time = datetime.now()
            duration = end_time - self.start_time
            
            final_result = {
                'success': result_oci['success'],
                'job_id': self.job_id,
                'start_time': self.start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'duration_seconds': duration.total_seconds(),
                'airtable_result': result_airtable,
                'oci_result': result_oci,
                'statistics': result_airtable.get('statistics', {}),
                'message': 'Job de atualização do datasource concluído com sucesso!' if result_oci['success'] else 'Falha no job de atualização'
            }
            
            logger.info(f"✅ Job concluído - Duração: {duration.total_seconds():.2f}s")
            return final_result
            
        except Exception as e:
            error_msg = f"Erro fatal no job: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            
            return {
                'success': False,
                'job_id': self.job_id,
                'error': error_msg,
                'traceback': traceback.format_exc(),
                'start_time': self.start_time.isoformat(),
                'end_time': datetime.now().isoformat()
            }
    
    def _execute_airtable_extraction(self) -> Dict[str, Any]:
        """Executa a extração dos dados do Airtable."""
        try:
            logger.info("📊 Iniciando extração do Airtable...")
            
            # Configurar .env para o diretório atual
            from dotenv import load_dotenv
            env_file = Path(__file__).parent / '.env'
            if not env_file.exists():
                return {
                    'success': False,
                    'error': f'.env não encontrado em: {env_file}',
                    'stage': 'env_check'
                }
            
            # Carregar .env local
            load_dotenv(env_file)
            logger.info(f"✅ .env carregado de: {env_file}")
            
            # Importar módulos necessários (assumindo que estão no path)
            try:
                sys.path.append(str(Path(__file__).parent.parent))
                from airtable_datasource_job import AirtableDataExtractor, DataSourceConsolidator
            except ImportError as e:
                logger.error(f"Erro ao importar módulos Airtable: {e}")
                return {
                    'success': False,
                    'error': f'Falha ao importar módulos: {e}',
                    'stage': 'import_airtable_modules'
                }
            
            # 1. Extrair dados do Airtable
            extractor = AirtableDataExtractor()
            dados_extraidos = extractor.extract_all_data()
            
            # 2. Consolidar dados
            consolidator = DataSourceConsolidator(dados_extraidos)
            datasource_consolidado = consolidator.create_consolidated_datasource()
            
            # 3. Salvar arquivo
            output_file = Path(__file__).parent.parent / 'consolidated_datasource_fresh.json'
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(datasource_consolidado, f, indent=2, ensure_ascii=False)
            
            file_size_mb = output_file.stat().st_size / (1024 * 1024)
            
            logger.info(f"✅ Extração Airtable concluída - Arquivo: {file_size_mb:.2f} MB")
            
            return {
                'success': True,
                'file_path': str(output_file),
                'file_size_mb': round(file_size_mb, 2),
                'statistics': datasource_consolidado.get('statistics', {}),
                'stage': 'airtable_extraction'
            }
            
        except Exception as e:
            error_msg = f"Erro na extração Airtable: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'stage': 'airtable_extraction'
            }
    
    def _execute_oci_upload(self, file_path: str) -> Dict[str, Any]:
        """Executa o upload para OCI Object Storage."""
        try:
            logger.info("📤 Iniciando upload para OCI...")
            
            # Configurar .env para o diretório atual
            from dotenv import load_dotenv
            env_file = Path(__file__).parent / '.env'
            load_dotenv(env_file)
            
            # Importar módulo OCI
            try:
                sys.path.append(str(Path(__file__).parent.parent))
                from upload_to_oci import OCIUploader
            except ImportError as e:
                logger.warning(f"Módulo OCI não disponível: {e}")
                return {
                    'success': True,  # Não falha o job se OCI não estiver disponível
                    'skipped': True,
                    'reason': 'Módulo OCI não disponível',
                    'stage': 'oci_upload'
                }
            
            # Executar upload
            uploader = OCIUploader()
            
            # Gerar nome do objeto com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            object_name = f"datasources/consolidated_datasource_{timestamp}.json"
            
            # Upload com timestamp
            upload_info = uploader.upload_file(file_path, object_name)
            
            # Upload como versão mais recente
            latest_upload_info = uploader.upload_file(file_path, "datasources/consolidated_datasource_latest.json")
            
            logger.info("✅ Upload OCI concluído!")
            
            return {
                'success': True,
                'uploads': [
                    {
                        'object_name': object_name,
                        'etag': upload_info.get('etag'),
                        'last_modified': upload_info.get('last_modified')
                    },
                    {
                        'object_name': 'datasources/consolidated_datasource_latest.json',
                        'etag': latest_upload_info.get('etag'),
                        'last_modified': latest_upload_info.get('last_modified')
                    }
                ],
                'bucket_name': uploader.bucket_name,
                'namespace': uploader.namespace,
                'stage': 'oci_upload'
            }
            
        except Exception as e:
            error_msg = f"Erro no upload OCI: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'stage': 'oci_upload'
            }

def execute_datasource_update() -> Dict[str, Any]:
    """
    Função pública para executar atualização do datasource.
    Pode ser chamada por qualquer serviço.
    """
    service = DatasourceUpdateService()
    return service.execute_job()

# Para execução direta
if __name__ == "__main__":
    result = execute_datasource_update()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result['success'] else 1)
