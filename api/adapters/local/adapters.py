"""
Adapter local para desenvolvimento.
Carrega dados do JSON consolidado.
"""

import os
import json
import pandas as pd
from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

from adapters.interfaces import DataSourceInterface, MLInterface, StorageInterface


class LocalDataSource(DataSourceInterface):
    """Carrega dados do arquivo JSON local."""
    
    def __init__(self, data_path: str = None):
        if data_path is None:
            # Usar path absoluto baseado na localização atual
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            self.data_path = os.path.join(project_root, "data", "consolidated_datasource.json")
        else:
            self.data_path = data_path
        self._data_cache = None
    
    def _load_data(self) -> Dict[str, Any]:
        """Carrega e cacheia dados JSON."""
        if self._data_cache is None:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self._data_cache = json.load(f)
        return self._data_cache
    
    async def get_clients(self) -> pd.DataFrame:
        """Retorna DataFrame com clientes."""
        data = self._load_data()
        clients = data['data']['Clientes']
        return pd.DataFrame(clients)
    
    async def get_products(self) -> pd.DataFrame:
        """Retorna DataFrame com produtos."""
        data = self._load_data()
        products = data['data']['Produtos']
        return pd.DataFrame(products)
    
    async def get_raw_data(self) -> Dict[str, Any]:
        """Retorna dados brutos completos para compatibilidade com notebook."""
        return self._load_data()


class LocalMLEngine(MLInterface):
    """
    Motor ML local simplificado - DEPRECATED
    Use AdvancedMLEngine no core/ para funcionalidade completa
    """
    
    def __init__(self, data_source: DataSourceInterface):
        self.data_source = data_source
        self._similarity_cache = None
        self._clients_cache = None
        print("⚠️  USANDO ENGINE SIMPLES - Para funcionalidade avançada use AdvancedMLEngine")
    
    async def _get_similarity_matrix(self) -> np.ndarray:
        """Calcula matriz de similaridade entre clientes."""
        if self._similarity_cache is None:
            clients_df = await self.data_source.get_clients()
            self._clients_cache = clients_df
            
            # Features simples para início
            features = []
            for _, client in clients_df.iterrows():
                feature_vector = [
                    len(client.get('produtos', [])),  # Num produtos
                    client.get('mrr', 0),             # MRR
                    client.get('satisfacao', 0),      # Satisfação
                    client.get('tempo_cliente', 0),   # Tempo cliente
                ]
                
                # One-hot encoding para setor
                setores = ['Atacado/Distribuição', 'Logística', 'E-commerce', 'Indústria', 'Saúde']
                for setor in setores:
                    feature_vector.append(1 if client.get('setor') == setor else 0)
                
                # One-hot encoding para porte
                portes = ['Pequeno', 'Médio', 'Grande']
                for porte in portes:
                    feature_vector.append(1 if client.get('porte') == porte else 0)
                
                features.append(feature_vector)
            
            # Normalizar e calcular similaridade
            scaler = StandardScaler()
            features_normalized = scaler.fit_transform(features)
            self._similarity_cache = cosine_similarity(features_normalized)
        
        return self._similarity_cache
    
    async def calculate_similarity(self, client_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Encontra clientes similares."""
        similarity_matrix = await self._get_similarity_matrix()
        clients_df = await self.data_source.get_clients()
        
        # Encontrar índice do cliente
        client_id = client_data.get('id')
        client_idx = None
        for idx, row in clients_df.iterrows():
            if row.get('id') == client_id:
                client_idx = idx
                break
        
        if client_idx is None:
            return []
        
        # Top 5 clientes similares
        similarities = similarity_matrix[client_idx]
        similar_indices = np.argsort(similarities)[::-1][1:6]  # Excluir ele mesmo
        
        similar_clients = []
        for idx in similar_indices:
            client = clients_df.iloc[idx]
            similar_clients.append({
                'id': client.get('id'),
                'nome': client.get('nome'),
                'similarity_score': float(similarities[idx]),
                'setor': client.get('setor'),
                'produtos': client.get('produtos', [])
            })
        
        return similar_clients
    
    async def recommend_products(self, client_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Gera recomendações baseadas em clientes similares."""
        clients_df = await self.data_source.get_clients()
        products_df = await self.data_source.get_products()
        
        # Encontrar cliente target
        target_client = None
        for _, client in clients_df.iterrows():
            if client.get('id') == client_id:
                target_client = client
                break
        
        if target_client is None:
            return []
        
        # Produtos que o cliente já tem
        current_products = set(target_client.get('produtos', []))
        
        # Encontrar clientes similares
        similar_clients = await self.calculate_similarity({'id': client_id})
        
        # Coletar produtos dos similares
        recommended_products = {}
        for similar in similar_clients:
            similarity_score = similar['similarity_score']
            for produto in similar['produtos']:
                if produto not in current_products:
                    if produto not in recommended_products:
                        recommended_products[produto] = 0
                    recommended_products[produto] += similarity_score
        
        # Ordenar por score e pegar top_k
        sorted_products = sorted(recommended_products.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for produto, score in sorted_products[:top_k]:
            # Buscar info do produto
            product_info = None
            for _, prod in products_df.iterrows():
                if prod.get('Produto/Serviço') == produto:
                    product_info = prod
                    break
            
            recommendations.append({
                'produto': produto,
                'score': float(score),
                'portfolio': product_info.get('Item Portfólio') if product_info is not None else 'N/A',
                'torre': product_info.get('Torre') if product_info is not None else 'N/A'
            })
        
        return recommendations


class LocalStorage(StorageInterface):
    """Implementação local de storage usando arquivos."""
    
    def __init__(self, cache_dir: str = "./cache"):
        self.cache_dir = cache_dir
        import os
        os.makedirs(cache_dir, exist_ok=True)
    
    async def save_recommendations(self, client_id: str, recommendations: List[Dict[str, Any]]) -> bool:
        """Salva recomendações no cache local."""
        try:
            import json
            import os
            from datetime import datetime
            
            cache_file = os.path.join(self.cache_dir, f"{client_id}.json")
            
            cache_data = {
                'client_id': client_id,
                'recommendations': recommendations,
                'timestamp': datetime.now().isoformat(),
                'expires_at': (datetime.now().timestamp() + 3600)  # 1 hora
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Erro ao salvar cache: {e}")
            return False
    
    async def get_cached_recommendations(self, client_id: str) -> List[Dict[str, Any]]:
        """Busca recomendações no cache local."""
        try:
            import json
            import os
            from datetime import datetime
            
            cache_file = os.path.join(self.cache_dir, f"{client_id}.json")
            
            if not os.path.exists(cache_file):
                return []
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Verificar se expirou
            if datetime.now().timestamp() > cache_data.get('expires_at', 0):
                os.remove(cache_file)
                return []
            
            return cache_data.get('recommendations', [])
        except Exception as e:
            print(f"Erro ao buscar cache: {e}")
            return []
