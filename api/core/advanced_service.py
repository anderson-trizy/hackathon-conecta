"""
Serviço de Recomendação Avançado - Migrado do backup-api-v2
Replica exatamente a lógica do NotebookRecommendationService
Usa CORE ENGINE (cloud-agnostic)
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from adapters.interfaces import DataSourceInterface, StorageInterface
from .advanced_engine import AdvancedMLEngine


class AdvancedRecommendationService:
    """
    Serviço avançado de recomendações que replica o algoritmo do notebook
    com 47 dimensões de features e score ponderado
    """
    
    def __init__(self, 
                 data_source: DataSourceInterface,
                 ml_engine: AdvancedMLEngine, 
                 storage: StorageInterface):
        self.data_source = data_source
        self.ml_engine = ml_engine
        self.storage = storage
        self._initialization_lock = False
    
    async def _ensure_initialized(self):
        """Garante que todos os componentes foram inicializados"""
        if not self._initialization_lock:
            self._initialization_lock = True
            
            # Inicializar engine avançada
            if hasattr(self.ml_engine, 'initialize'):
                await self.ml_engine.initialize()
            
            print("✅ Serviço avançado de recomendações inicializado")
    
    async def get_client_recommendations(self, client_id: str, top_k: int = 5, use_cache: bool = True) -> Dict[str, Any]:
        """
        Gera recomendações avançadas para um cliente
        Replica exatamente o comportamento do NotebookRecommendationService
        """
        
        await self._ensure_initialized()
        
        print(f"🧠 Processando recomendações avançadas para cliente: {client_id}")
        
        # Verificar cache primeiro
        if use_cache:
            cached = await self.storage.get_cached_recommendations(client_id)
            if cached:
                return {
                    'client_id': client_id,
                    'recommendations': cached[:top_k],
                    'source': 'cache',
                    'algorithm': 'advanced_notebook_47_dimensions',
                    'total': len(cached),
                    'timestamp': datetime.now().isoformat()
                }
        
        try:
            # Gerar recomendações usando engine avançada
            recommendations = await self.ml_engine.recommend_products(client_id, top_k)
            
            # Salvar no cache
            if recommendations:
                await self.storage.save_recommendations(client_id, recommendations)
            
            return {
                'client_id': client_id,
                'recommendations': recommendations,
                'source': 'generated',
                'algorithm': 'advanced_notebook_47_dimensions',
                'total': len(recommendations),
                'timestamp': datetime.now().isoformat(),
                'features_used': '47_dimensions_tfidf_mlb',
                'scoring': 'weighted_40freq_35sim_25fit'
            }
            
        except Exception as e:
            print(f"❌ Erro ao gerar recomendações: {str(e)}")
            return {
                'client_id': client_id,
                'recommendations': [],
                'source': 'error',
                'algorithm': 'advanced_notebook_47_dimensions',
                'error': str(e),
                'total': 0,
                'timestamp': datetime.now().isoformat()
            }
    
    async def get_client_similar_analysis(self, client_id: str, top_k: int = 10) -> Dict[str, Any]:
        """
        Análise de clientes similares usando algoritmo avançado
        """
        
        await self._ensure_initialized()
        
        print(f"🔍 Analisando clientes similares para: {client_id}")
        
        try:
            # Buscar clientes similares
            similar_clients = await self.ml_engine.calculate_similarity({'id': client_id})
            
            # Buscar dados do cliente principal
            client_info = await self.get_client_info(client_id)
            
            return {
                'client_id': client_id,
                'client_info': client_info,
                'similar_clients': similar_clients[:top_k],
                'algorithm': 'advanced_cosine_similarity_47_dimensions',
                'total_similar': len(similar_clients),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Erro na análise de similaridade: {str(e)}")
            return {
                'client_id': client_id,
                'similar_clients': [],
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def get_full_client_analysis(self, client_id: str) -> Dict[str, Any]:
        """
        Análise completa do cliente incluindo recomendações e similares
        """
        
        await self._ensure_initialized()
        
        print(f"📊 Análise completa para cliente: {client_id}")
        
        try:
            # Executar análises em paralelo
            client_info = await self.get_client_info(client_id)
            recommendations = await self.get_client_recommendations(client_id, top_k=5, use_cache=False)
            similar_analysis = await self.get_client_similar_analysis(client_id, top_k=10)
            
            return {
                'client_id': client_id,
                'analysis_type': 'full_advanced_analysis',
                'client_info': client_info,
                'recommendations': recommendations,
                'similar_clients_analysis': similar_analysis,
                'algorithm_details': {
                    'engine': 'advanced_notebook_replica',
                    'features': '47_dimensions',
                    'methods': ['TF-IDF', 'MultiLabelBinarizer', 'LabelEncoder', 'StandardScaler'],
                    'scoring': 'weighted_frequency_similarity_fit'
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Erro na análise completa: {str(e)}")
            return {
                'client_id': client_id,
                'analysis_type': 'full_advanced_analysis',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def get_client_info(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Retorna informações detalhadas do cliente"""
        
        try:
            clients_df = await self.data_source.get_clients()
            
            for _, client in clients_df.iterrows():
                if str(client.get('id')) == str(client_id):
                    return {
                        'id': str(client.get('id')),
                        'nome': client.get('nome', 'Unknown'),
                        'setor': client.get('setor', 'Unknown'),
                        'porte': client.get('porte', 'Unknown'),
                        'produtos_atuais': client.get('produtos', []),
                        'mrr': float(client.get('mrr', 0)),
                        'satisfacao': float(client.get('satisfacao', 0)),
                        'torre': client.get('torre', 'Unknown')
                    }
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao buscar informações do cliente: {str(e)}")
            return None
    
    async def health_check(self) -> Dict[str, Any]:
        """Verifica se todos os componentes avançados estão funcionando"""
        
        try:
            await self._ensure_initialized()
            
            clients_df = await self.data_source.get_clients()
            products_df = await self.data_source.get_products()
            
            # Verificar se engine avançada foi inicializada
            engine_status = 'initialized' if hasattr(self.ml_engine, 'is_initialized') and self.ml_engine.is_initialized else 'not_initialized'
            
            return {
                'status': 'healthy',
                'service_type': 'advanced_recommendation_service',
                'algorithm': 'notebook_replica_47_dimensions',
                'data_source': 'ok',
                'ml_engine': engine_status,
                'storage': 'ok',
                'clients_count': len(clients_df),
                'products_count': len(products_df),
                'features': {
                    'dimensions': '47',
                    'methods': ['TF-IDF', 'MultiLabelBinarizer', 'CosineSimilarity'],
                    'scoring': 'weighted_advanced'
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'unhealthy',
                'service_type': 'advanced_recommendation_service',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def debug_client_calculations(self, client_id: str) -> Dict[str, Any]:
        """
        Debug dos cálculos intermediários para comparar com notebook
        """
        try:
            # Obter dados de debug da engine
            debug_data = await self.ml_engine.debug_calculations(client_id)
            
            return {
                "client_id": client_id,
                "debug_data": debug_data,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "client_id": client_id,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
