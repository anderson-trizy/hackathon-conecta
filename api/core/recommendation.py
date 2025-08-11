"""
Core da aplicação - Lógica de negócio independente de cloud.
"""

from typing import List, Dict, Any
from adapters.interfaces import DataSourceInterface, MLInterface, StorageInterface


class RecommendationService:
    """
    Serviço principal de recomendações.
    Cloud-agnostic - funciona com qualquer implementação dos adapters.
    """
    
    def __init__(self, 
                 data_source: DataSourceInterface,
                 ml_engine: MLInterface, 
                 storage: StorageInterface):
        self.data_source = data_source
        self.ml_engine = ml_engine
        self.storage = storage
    
    async def get_recommendations(self, client_id: str, top_k: int = 5, use_cache: bool = True) -> Dict[str, Any]:
        """
        Gera recomendações para um cliente.
        
        Args:
            client_id: ID do cliente
            top_k: Número de recomendações
            use_cache: Se deve usar cache
            
        Returns:
            Dict com recomendações e metadados
        """
        
        # Tentar cache primeiro
        if use_cache:
            cached = await self.storage.get_cached_recommendations(client_id)
            if cached:
                return {
                    'client_id': client_id,
                    'recommendations': cached[:top_k],
                    'source': 'cache',
                    'total': len(cached)
                }
        
        # Gerar novas recomendações
        recommendations = await self.ml_engine.recommend_products(client_id, top_k)
        
        # Salvar no cache
        if recommendations:
            await self.storage.save_recommendations(client_id, recommendations)
        
        return {
            'client_id': client_id,
            'recommendations': recommendations,
            'source': 'generated',
            'total': len(recommendations)
        }
    
    async def get_client_info(self, client_id: str) -> Dict[str, Any]:
        """Retorna informações do cliente."""
        clients_df = await self.data_source.get_clients()
        
        for _, client in clients_df.iterrows():
            if client.get('id') == client_id:
                return {
                    'id': client.get('id'),
                    'nome': client.get('nome'),
                    'setor': client.get('setor'),
                    'porte': client.get('porte'),
                    'produtos_atuais': client.get('produtos', []),
                    'mrr': client.get('mrr', 0),
                    'satisfacao': client.get('satisfacao', 0)
                }
        
        return None
    
    async def get_similar_clients(self, client_id: str) -> List[Dict[str, Any]]:
        """Retorna clientes similares."""
        return await self.ml_engine.calculate_similarity({'id': client_id})
    
    async def health_check(self) -> Dict[str, Any]:
        """Verifica se todos os componentes estão funcionando."""
        try:
            clients_df = await self.data_source.get_clients()
            products_df = await self.data_source.get_products()
            
            return {
                'status': 'healthy',
                'data_source': 'ok',
                'clients_count': len(clients_df),
                'products_count': len(products_df)
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            }
