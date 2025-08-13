import io
import json
import logging
from datetime import datetime

from fdk import response
from datasource_service_vault import execute_datasource_update


def handler(ctx, data: io.BytesIO = None):
    """
    Handler da Oracle Function para atualização do datasource.
    
    Executa o job completo de:
    1. Carregamento de credenciais do OCI Vault (seguro)
    2. Extração de dados do Airtable
    3. Consolidação dos dados
    4. Upload para OCI Object Storage
    
    Usa OCI Vault para gestão segura de secrets ao invés de arquivos .env
    """
    logger = logging.getLogger()
    start_time = datetime.now()
    
    try:
        # Log da requisição recebida
        logger.info("🚀 Oracle Function: Iniciando job de atualização do datasource")
        
        # Tentar parsear payload (opcional)
        request_data = {}
        if data:
            try:
                body = json.loads(data.getvalue())
                request_data = body
                logger.info(f"📥 Payload recebido: {json.dumps(request_data, ensure_ascii=False)}")
            except (Exception, ValueError) as ex:
                logger.info(f'⚠️ Payload não é JSON válido: {str(ex)}')
        
        # Executar o job de atualização
        logger.info("🔄 Executando serviço de atualização...")
        result = execute_datasource_update()
        
        # Calcular tempo total
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        # Adicionar informações da function
        result['function_info'] = {
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'total_duration_seconds': total_duration,
            'request_data': request_data
        }
        
        # Log do resultado
        if result['success']:
            logger.info(f"✅ Job concluído com sucesso em {total_duration:.2f}s")
            status_code = 200
        else:
            logger.error(f"❌ Job falhou em {total_duration:.2f}s: {result.get('error', 'Erro desconhecido')}")
            status_code = 500
        
        # Retornar resposta
        return response.Response(
            ctx,
            response_data=json.dumps(result, ensure_ascii=False, indent=2),
            headers={"Content-Type": "application/json"},
            status_code=status_code
        )
        
    except Exception as e:
        error_msg = f"Erro fatal na Oracle Function: {str(e)}"
        logger.error(error_msg)
        
        error_response = {
            'success': False,
            'error': error_msg,
            'function_info': {
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat(),
                'total_duration_seconds': (datetime.now() - start_time).total_seconds()
            }
        }
        
        return response.Response(
            ctx,
            response_data=json.dumps(error_response, ensure_ascii=False, indent=2),
            headers={"Content-Type": "application/json"},
            status_code=500
        )
