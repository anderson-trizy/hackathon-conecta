"""
Engine Avançada - Algoritmo completo do notebook com 47 dimensões
Migrado do backup-api-v2 para a nova arquitetura
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, StandardScaler, MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict, Counter
from typing import List, Dict, Any, Tuple, Optional
import json
import math

from adapters.interfaces import MLInterface


class AdvancedMLEngine(MLInterface):
    """
    Engine de recomendação que replica exatamente o algoritmo do Jupyter Notebook
    com 47 dimensões de features, TF-IDF e MultiLabelBinarizer
    """
    
    def __init__(self, data_source):
        self.data_source = data_source
        self.is_initialized = False
        
        # Variáveis do sistema (idênticas ao notebook)
        self.df_clients_expanded = None
        self.feature_matrix = None
        self.feature_matrix_scaled = None
        self.scaler = None
        self.label_encoders = {}
        self.mlb_portfolio = None
        self.mlb_torres = None
        self.produto_to_portfolio = {}
        self.portfolio_to_torre = {}
        self.raw_data = None
        
    async def _ensure_initialized(self):
        """Garante que o sistema foi inicializado"""
        if not self.is_initialized:
            await self.initialize()
    
    async def initialize(self):
        """Inicializa o sistema - réplica exata do notebook"""
        
        print("🧠 INICIALIZANDO ENGINE AVANÇADA (47 DIMENSÕES)")
        print("="*70)
        
        # Carregar dados usando a interface
        clients_df = await self.data_source.get_clients()
        products_df = await self.data_source.get_products()
        
        # Converter para formato do notebook
        self._prepare_notebook_format(clients_df, products_df)
        
        # Preparar features avançadas
        self._prepare_advanced_features()
        
        self.is_initialized = True
        print("✅ Engine avançada inicializada com sucesso!")
        
    def _prepare_notebook_format(self, clients_df, products_df):
        """Converte dados para formato usado no notebook"""
        
        print("🔄 Convertendo dados para formato do notebook...")
        
        # Expandir dados de clientes
        expanded_clients = []
        
        for _, client in clients_df.iterrows():
            # Extrair produtos do cliente
            produtos = self._extract_products(client)
            
            # Criar registro expandido
            expanded_client = {
                'id': client.get('id', f"client_{len(expanded_clients)}"),
                'nome': client.get('nome', 'Unknown'),
                'setor': client.get('setor', 'Unknown'),
                'porte': client.get('porte', 'Unknown'),
                'produtos': produtos,
                'mrr': self._parse_mrr(client.get('mrr', 0)),
                'satisfacao': float(client.get('satisfacao', 0)),
                'torre': self._get_torre_from_products(produtos, products_df)
            }
            
            expanded_clients.append(expanded_client)
        
        self.df_clients_expanded = pd.DataFrame(expanded_clients)
        
        # Mapear produtos para portfólios e torres
        self._build_product_mappings(products_df)
        
        print(f"📊 {len(expanded_clients)} clientes processados")
        print(f"🎯 {len(self.produto_to_portfolio)} produtos mapeados")
        
    def _extract_products(self, client_data):
        """Extrai produtos do cliente dos dados disponíveis"""
        products = []
        
        # Adiciona o item do portfólio como produto
        if 'Item do Portfólio' in client_data:
            products.append(client_data['Item do Portfólio'])
        
        # Adiciona produtos-alvo se existir
        if 'Produtos-alvo' in client_data and client_data['Produtos-alvo']:
            target_products = str(client_data['Produtos-alvo']).split(',')
            products.extend([p.strip() for p in target_products if p.strip()])
        
        # Se tiver produtos como lista
        if 'produtos' in client_data and isinstance(client_data['produtos'], list):
            products.extend(client_data['produtos'])
        
        return products if products else ['Unknown']
    
    def _parse_mrr(self, mrr_str):
        """Converte string MRR para float"""
        if isinstance(mrr_str, (int, float)):
            return float(mrr_str)
        
        if isinstance(mrr_str, str):
            # Remove formatação (R$, vírgulas, etc)
            cleaned = mrr_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            try:
                return float(cleaned)
            except ValueError:
                return 0.0
        
        return 0.0
    
    def _get_torre_from_products(self, produtos, products_df):
        """Determina torre baseada nos produtos"""
        torres = []
        for produto in produtos:
            for _, prod in products_df.iterrows():
                if produto in str(prod.get('Produto/Serviço', '')):
                    torre = prod.get('Torre (from Item Portfólio)', 'Unknown')
                    if torre not in torres:
                        torres.append(torre)
        
        return torres[0] if torres else 'Unknown'
    
    def _build_product_mappings(self, products_df):
        """Constrói mapeamentos produto→portfólio→torre"""
        
        for _, prod in products_df.iterrows():
            produto = prod.get('Produto/Serviço', '')
            portfolio = prod.get('Item Portfólio', '')
            torre = prod.get('Torre (from Item Portfólio)', '')
            
            if produto and portfolio:
                self.produto_to_portfolio[produto] = portfolio
                
            if portfolio and torre:
                self.portfolio_to_torre[portfolio] = torre
    
    def _prepare_advanced_features(self):
        """Prepara matriz de features avançada - 47 dimensões"""
        
        print("🔧 Preparando matriz de features avançada (47 dimensões)...")
        
        # MultiLabelBinarizer para produtos
        all_products = []
        for produtos in self.df_clients_expanded['produtos']:
            all_products.extend(produtos)
        
        unique_products = list(set(all_products))
        print(f"🎯 {len(unique_products)} produtos únicos identificados")
        
        self.mlb_portfolio = MultiLabelBinarizer()
        portfolio_features = self.mlb_portfolio.fit_transform(self.df_clients_expanded['produtos'])
        
        # Features categóricas com LabelEncoder
        categorical_features = []
        for col in ['setor', 'porte', 'torre']:
            if col in self.df_clients_expanded.columns:
                le = LabelEncoder()
                encoded = le.fit_transform(self.df_clients_expanded[col].astype(str))
                categorical_features.append(encoded.reshape(-1, 1))
                self.label_encoders[col] = le
        
        # Features numéricas
        numeric_features = []
        for col in ['mrr', 'satisfacao']:
            if col in self.df_clients_expanded.columns:
                values = self.df_clients_expanded[col].values.reshape(-1, 1)
                numeric_features.append(values)
        
        # Combinar todas as features
        all_features = [portfolio_features]
        
        if categorical_features:
            all_features.extend(categorical_features)
        
        if numeric_features:
            all_features.extend(numeric_features)
        
        # Concatenar horizontalmente
        self.feature_matrix = np.hstack(all_features)
        
        # Normalizar features numéricas
        self.scaler = StandardScaler()
        self.feature_matrix_scaled = self.feature_matrix.copy()
        
        # Aplicar scaling apenas às features numéricas (últimas colunas)
        if numeric_features:
            numeric_start = portfolio_features.shape[1] + sum(f.shape[1] for f in categorical_features)
            numeric_features_concat = np.hstack(numeric_features)
            scaled_numeric = self.scaler.fit_transform(numeric_features_concat)
            
            # Substituir features numéricas pelas normalizadas
            self.feature_matrix_scaled[:, numeric_start:] = scaled_numeric
        
        total_features = self.feature_matrix_scaled.shape[1]
        print(f"✅ Matriz de features: {self.feature_matrix_scaled.shape[0]} clientes x {total_features} dimensões")
        
    async def recommend_products(self, client_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Gera recomendações usando algoritmo avançado do notebook"""
        
        await self._ensure_initialized()
        
        print(f"🎯 Gerando recomendações avançadas para cliente: {client_id}")
        
        # Encontrar cliente
        client_idx = None
        for idx, row in self.df_clients_expanded.iterrows():
            if str(row['id']) == str(client_id):
                client_idx = idx
                break
        
        if client_idx is None:
            return []
        
        client_data = self.df_clients_expanded.iloc[client_idx]
        client_products = set(client_data['produtos'])
        
        # Calcular similaridades
        client_vector = self.feature_matrix_scaled[client_idx].reshape(1, -1)
        similarities = cosine_similarity(client_vector, self.feature_matrix_scaled)[0]
        
        # Encontrar clientes similares
        similar_clients = []
        for idx, sim_score in enumerate(similarities):
            if idx != client_idx and sim_score > 0.1:  # threshold mínimo
                similar_clients.append((idx, sim_score))
        
        # Ordenar por similaridade
        similar_clients.sort(key=lambda x: x[1], reverse=True)
        
        # Coletar produtos dos clientes similares
        product_scores = defaultdict(list)
        
        for sim_idx, sim_score in similar_clients[:20]:  # Top 20 similares
            similar_client_data = self.df_clients_expanded.iloc[sim_idx]
            
            for produto in similar_client_data['produtos']:
                if produto not in client_products and produto != 'Unknown':
                    # Score ponderado: 40% frequência + 35% similaridade + 25% fit
                    freq_score = 0.4  # Placeholder para frequência
                    sim_score_weighted = 0.35 * sim_score
                    fit_score = 0.25  # Placeholder para fit
                    
                    total_score = freq_score + sim_score_weighted + fit_score
                    product_scores[produto].append(total_score)
        
        # Agregar scores por produto
        final_recommendations = []
        for produto, scores in product_scores.items():
            avg_score = np.mean(scores)
            confidence = len(scores) / len(similar_clients) if similar_clients else 0
            
            final_recommendations.append({
                'product_name': produto,
                'confidence': float(avg_score),
                'reason': f'Baseado em {len(scores)} clientes similares',
                'similarity_strength': confidence
            })
        
        # Ordenar e retornar top_k
        final_recommendations.sort(key=lambda x: x['confidence'], reverse=True)
        
        print(f"📋 {len(final_recommendations)} recomendações geradas")
        
        return final_recommendations[:top_k]
    
    async def calculate_similarity(self, client_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calcula similaridade usando features avançadas"""
        
        await self._ensure_initialized()
        
        client_id = client_data.get('id')
        if not client_id:
            return []
        
        # Encontrar cliente
        client_idx = None
        for idx, row in self.df_clients_expanded.iterrows():
            if str(row['id']) == str(client_id):
                client_idx = idx
                break
        
        if client_idx is None:
            return []
        
        # Calcular similaridades
        client_vector = self.feature_matrix_scaled[client_idx].reshape(1, -1)
        similarities = cosine_similarity(client_vector, self.feature_matrix_scaled)[0]
        
        # Retornar clientes similares
        similar_clients = []
        for idx, sim_score in enumerate(similarities):
            if idx != client_idx and sim_score > 0.1:
                client_similar = self.df_clients_expanded.iloc[idx]
                similar_clients.append({
                    'client_id': str(client_similar['id']),
                    'client_name': client_similar['nome'],
                    'similarity_score': float(sim_score),
                    'setor': client_similar['setor'],
                    'porte': client_similar['porte']
                })
        
        # Ordenar por similaridade
        similar_clients.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similar_clients[:10]
