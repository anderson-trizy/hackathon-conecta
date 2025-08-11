"""
Engine FINAL SIMPLIFICADA - Baseada no algoritmo que funciona 100%
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict, Counter
from typing import List, Dict, Any, Tuple
import json

class AdvancedMLEngine:
    """Engine baseada no algoritmo validado que funciona"""
    
    def __init__(self, data_source):
        self.data_source = data_source
        self.is_initialized = False
        self.raw_data = None
        self.df_clients = None
        self.feature_matrix_scaled = None
        self.similarity_matrix = None

    async def initialize(self):
        """Inicializa com algoritmo validado"""
        print("🧠 INICIALIZANDO ENGINE VALIDADA")
        
        # Carregar dados
        self.raw_data = await self.data_source.get_raw_data()
        
        # Expandir clientes
        clients = self.raw_data['data']['Clientes']
        self.df_clients = pd.DataFrame(clients)
        
        print(f"📊 Clientes carregados: {len(self.df_clients)}")
        
        # Criar features exatamente como no script validado
        self._create_features()
        
        # Calcular similaridade
        self.similarity_matrix = cosine_similarity(self.feature_matrix_scaled)
        
        self.is_initialized = True
        print("✅ Engine inicializada com algoritmo validado")

    def _create_features(self):
        """Cria features exatamente como no script validado"""
        
        df = self.df_clients
        
        # 1. Features categóricas
        categorical_features = {}
        categorical_columns = ['persona', 'torre', 'setor', 'porte']
        for col in categorical_columns:
            if col in df.columns:
                le = LabelEncoder()
                categorical_features[f'{col}_encoded'] = le.fit_transform(df[col].fillna('Unknown'))
        
        # 2. Features numéricas
        numerical_features = {}
        if 'mrr' in df.columns:
            mrr_values = pd.to_numeric(df['mrr'], errors='coerce').fillna(0)
            numerical_features['mrr_log'] = np.log1p(mrr_values)
        
        if 'tempo_cliente' in df.columns:
            tempo_values = pd.to_numeric(df['tempo_cliente'], errors='coerce').fillna(0)
            numerical_features['tempo_cliente_norm'] = tempo_values / 60
        
        if 'satisfacao' in df.columns:
            satisfacao_values = pd.to_numeric(df['satisfacao'], errors='coerce').fillna(3.0)
            numerical_features['satisfacao'] = satisfacao_values
        
        # 3. Mapeamentos produto -> portfólio -> torre
        produto_to_portfolio = {}
        portfolio_to_torre = {}
        df_produtos_map = pd.DataFrame(self.raw_data['data']['Produtos'])
        df_portfolio_map = pd.DataFrame(self.raw_data['data']['Items do Portfólio'])
        
        for _, produto in df_produtos_map.iterrows():
            produto_nome = produto.get('Produto/Serviço', '')
            portfolio_item = produto.get('Item Portfólio', '')
            if produto_nome and portfolio_item:
                produto_to_portfolio[produto_nome] = portfolio_item
        
        for _, portfolio in df_portfolio_map.iterrows():
            portfolio_nome = portfolio.get('Item do Portfólio', '')
            torre = portfolio.get('Torre', '')
            if portfolio_nome and torre:
                portfolio_to_torre[portfolio_nome] = torre
        
        # 4. Features de portfólio (multi-hot)
        portfolio_items_per_client = []
        for _, client in df.iterrows():
            client_portfolios = set()
            produtos = client.get('produtos', [])
            if isinstance(produtos, list):
                for produto in produtos:
                    if produto in produto_to_portfolio:
                        client_portfolios.add(produto_to_portfolio[produto])
            portfolio_items_per_client.append(list(client_portfolios))
        
        mlb_portfolio = MultiLabelBinarizer()
        portfolio_matrix = mlb_portfolio.fit_transform(portfolio_items_per_client)
        
        # 5. Features de torres (multi-hot)
        torres_per_client = []
        for _, client in df.iterrows():
            client_torres = set()
            produtos = client.get('produtos', [])
            if isinstance(produtos, list):
                for produto in produtos:
                    if produto in produto_to_portfolio:
                        portfolio_item = produto_to_portfolio[produto]
                        if portfolio_item in portfolio_to_torre:
                            client_torres.add(portfolio_to_torre[portfolio_item])
            torres_per_client.append(list(client_torres))
        
        mlb_torres = MultiLabelBinarizer()
        torres_matrix = mlb_torres.fit_transform(torres_per_client)
        
        # 6. Features de complexidade
        complexity_features = {}
        complexity_features['num_produtos'] = [len(client.get('produtos', [])) for client in df.to_dict('records')]
        complexity_features['num_portfolios'] = [len(portfolios) for portfolios in portfolio_items_per_client]
        complexity_features['num_torres'] = [len(torres) for torres in torres_per_client]
        
        def calculate_diversity(items_list):
            if not items_list:
                return 0
            counts = Counter(items_list)
            total = sum(counts.values())
            entropy = -sum((count/total) * np.log2(count/total) for count in counts.values())
            return entropy
        
        diversity_scores = []
        for produtos in [client.get('produtos', []) for client in df.to_dict('records')]:
            portfolios = [produto_to_portfolio.get(produto, 'Unknown') for produto in produtos]
            diversity_scores.append(calculate_diversity(portfolios))
        
        complexity_features['portfolio_diversity'] = diversity_scores
        
        # 7. Consolidar features
        all_features = []
        
        for feature_name, values in categorical_features.items():
            all_features.append(values.reshape(-1, 1))
        
        for feature_name, values in numerical_features.items():
            all_features.append(np.array(values).reshape(-1, 1))
        
        for feature_name, values in complexity_features.items():
            all_features.append(np.array(values).reshape(-1, 1))
        
        all_features.append(portfolio_matrix)
        all_features.append(torres_matrix)
        
        feature_matrix = np.hstack(all_features)
        
        # 8. Normalização
        scaler = StandardScaler()
        n_categorical = sum(1 for _ in categorical_features.values())
        n_numerical = sum(1 for _ in numerical_features.values())
        n_complexity = sum(1 for _ in complexity_features.values())
        n_non_binary = n_categorical + n_numerical + n_complexity
        
        self.feature_matrix_scaled = feature_matrix.copy()
        if n_non_binary > 0:
            self.feature_matrix_scaled[:, :n_non_binary] = scaler.fit_transform(feature_matrix[:, :n_non_binary])
        
        print(f"📐 Matriz de features: {self.feature_matrix_scaled.shape}")

    async def recommend_products(self, client_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Gera recomendações com algoritmo validado"""
        
        if not self.is_initialized:
            await self.initialize()
        
        print(f"🎯 Recomendações para cliente: {client_id}")
        
        # Encontrar cliente
        client_idx = None
        for idx, row in self.df_clients.iterrows():
            if str(row['id']) == str(client_id):
                client_idx = idx
                break
        
        if client_idx is None:
            return []
        
        target_client_data = self.df_clients.iloc[client_idx]
        target_products = set(target_client_data.get('produtos', []))
        
        # Calcular similaridades
        similarities = self.similarity_matrix[client_idx]
        similarities[client_idx] = 0
        
        # Encontrar clientes similares
        min_similarity = 0.3
        valid_indices = np.where(similarities >= min_similarity)[0]
        sorted_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]]
        top_indices = sorted_indices[:20]
        
        # Coletar produtos candidatos
        product_candidates = defaultdict(list)
        
        for sim_idx in top_indices:
            similar_client = self.df_clients.iloc[sim_idx]
            similar_products = set(similar_client.get('produtos', []))
            new_products = similar_products - target_products
            
            for product in new_products:
                if product and product != 'Unknown':
                    # Score de adequação
                    fit_score = 0.0
                    if target_client_data.get('setor') == similar_client.get('setor'):
                        fit_score += 0.3
                    if target_client_data.get('porte') == similar_client.get('porte'):
                        fit_score += 0.2
                    if target_client_data.get('persona') == similar_client.get('persona'):
                        fit_score += 0.25
                    if target_client_data.get('torre') == similar_client.get('torre'):
                        fit_score += 0.15
                    
                    product_candidates[product].append({
                        'similarity': similarities[sim_idx],
                        'fit_score': fit_score
                    })
        
        # Calcular scores finais
        product_scores = {}
        for product, occurrences in product_candidates.items():
            frequency_score = len(occurrences) / len(top_indices)
            avg_similarity = np.mean([occ['similarity'] for occ in occurrences])
            avg_fit_score = np.mean([occ['fit_score'] for occ in occurrences])
            
            final_score = (
                frequency_score * 0.4 +
                avg_similarity * 0.35 +
                avg_fit_score * 0.25
            )
            
            product_scores[product] = final_score
        
        # Ordenar produtos
        sorted_products = sorted(
            product_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Resultado final
        final_recommendations = []
        for product, score in sorted_products[:top_k]:
            recommendation = {
                'product_name': product,
                'confidence': score,
                'reason': f"Baseado em clientes similares",
                'similarity_strength': score,
                'avg_similarity': score,
                'avg_fit_score': score
            }
            final_recommendations.append(recommendation)
        
        print(f"✅ {len(final_recommendations)} recomendações geradas")
        return final_recommendations
    
    async def find_similar_clients(self, client_data: Dict[str, Any], top_k: int = 10) -> List[Dict[str, Any]]:
        """Método de compatibilidade"""
        return []
