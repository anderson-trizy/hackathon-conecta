# Arquitetura de Abstração para Text Embeddings - Estratégia Multicloud

## 🎯 **Objetivo**
Criar interfaces abstratas que permitam migração fluida entre OCI Generative AI Text Embeddings e outras soluções (Python local, AWS, Azure, GCP) sem alterar a lógica principal do sistema.

---

## 🏗️ **Padrão de Abstração Implementado**

### **1. Interface Principal - EmbeddingInterface**

```python
# interfaces/embedding_interface.py
from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np

class EmbeddingInterface(ABC):
    """Interface abstrata para serviços de embeddings de texto"""
    
    @abstractmethod
    def get_embedding(self, text: str) -> np.ndarray:
        """Gera embedding para um único texto"""
        pass
    
    @abstractmethod
    def get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Gera embeddings para múltiplos textos"""
        pass
    
    @abstractmethod
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calcula similaridade entre dois embeddings"""
        pass
    
    @abstractmethod
    def find_most_similar(self, target_embedding: np.ndarray, 
                         candidates: List[np.ndarray], top_k: int = 5) -> List[Tuple[int, float]]:
        """Encontra os embeddings mais similares"""
        pass
    
    @abstractmethod
    def cluster_embeddings(self, embeddings: List[np.ndarray], n_clusters: int) -> List[int]:
        """Agrupa embeddings em clusters"""
        pass
```

---

## 🔧 **Implementações Específicas**

### **2. Adapter Oracle OCI (Implementação Atual)**

```python
# adapters/oci_embedding_adapter.py
import oci
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from interfaces.embedding_interface import EmbeddingInterface

class OCIEmbeddingAdapter(EmbeddingInterface):
    """Implementação usando OCI Generative AI"""
    
    def __init__(self, config_path: str = "~/.oci/config"):
        self.config = oci.config.from_file(config_path)
        self.client = oci.generative_ai_inference.GenerativeAiInferenceClient(self.config)
        self.model_id = "cohere.embed-multilingual-v3.0"
        self.compartment_id = self.config.get("compartment_id")
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Gera embedding usando OCI Generative AI"""
        try:
            request = oci.generative_ai_inference.models.EmbedTextDetails(
                inputs=[text],
                serving_mode="ON_DEMAND",
                compartment_id=self.compartment_id,
                model_id=self.model_id
            )
            response = self.client.embed_text(request)
            return np.array(response.data.embeddings[0])
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar embedding OCI: {e}")
    
    def get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Gera múltiplos embeddings em batch (mais eficiente)"""
        try:
            request = oci.generative_ai_inference.models.EmbedTextDetails(
                inputs=texts,
                serving_mode="ON_DEMAND", 
                compartment_id=self.compartment_id,
                model_id=self.model_id
            )
            response = self.client.embed_text(request)
            return [np.array(emb) for emb in response.data.embeddings]
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar embeddings OCI: {e}")
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calcula similaridade coseno"""
        return cosine_similarity([embedding1], [embedding2])[0][0]
    
    def find_most_similar(self, target_embedding: np.ndarray, 
                         candidates: List[np.ndarray], top_k: int = 5) -> List[Tuple[int, float]]:
        """Encontra embeddings mais similares"""
        similarities = []
        for i, candidate in enumerate(candidates):
            sim = self.calculate_similarity(target_embedding, candidate)
            similarities.append((i, sim))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
    
    def cluster_embeddings(self, embeddings: List[np.ndarray], n_clusters: int) -> List[int]:
        """Agrupa embeddings usando K-Means"""
        embeddings_matrix = np.vstack(embeddings)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        return kmeans.fit_predict(embeddings_matrix).tolist()
```

### **3. Adapter Python Local (Fallback/Migração)**

```python
# adapters/python_embedding_adapter.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer  # Alternativa local
from interfaces.embedding_interface import EmbeddingInterface

class PythonEmbeddingAdapter(EmbeddingInterface):
    """Implementação usando bibliotecas Python locais"""
    
    def __init__(self, method: str = "sentence_transformers"):
        self.method = method
        
        if method == "sentence_transformers":
            # Modelo multilíngue similar ao Oracle
            self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        elif method == "tfidf":
            self.vectorizer = TfidfVectorizer(
                max_features=768,  # Mesmo tamanho que Oracle
                stop_words='portuguese',
                ngram_range=(1, 2)
            )
            self._fitted = False
        else:
            raise ValueError(f"Método não suportado: {method}")
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Gera embedding usando método Python escolhido"""
        if self.method == "sentence_transformers":
            return self.model.encode([text])[0]
        elif self.method == "tfidf":
            if not self._fitted:
                # Para TF-IDF, precisa fit primeiro (menos ideal)
                raise RuntimeError("TF-IDF precisa ser treinado com get_embeddings primeiro")
            return self.vectorizer.transform([text]).toarray()[0]
    
    def get_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """Gera múltiplos embeddings"""
        if self.method == "sentence_transformers":
            embeddings = self.model.encode(texts)
            return [emb for emb in embeddings]
        elif self.method == "tfidf":
            if not self._fitted:
                self.vectorizer.fit(texts)
                self._fitted = True
            embeddings = self.vectorizer.transform(texts).toarray()
            return [emb for emb in embeddings]
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calcula similaridade coseno (mesma implementação)"""
        return cosine_similarity([embedding1], [embedding2])[0][0]
    
    def find_most_similar(self, target_embedding: np.ndarray, 
                         candidates: List[np.ndarray], top_k: int = 5) -> List[Tuple[int, float]]:
        """Implementação idêntica ao Oracle"""
        similarities = []
        for i, candidate in enumerate(candidates):
            sim = self.calculate_similarity(target_embedding, candidate)
            similarities.append((i, sim))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
    
    def cluster_embeddings(self, embeddings: List[np.ndarray], n_clusters: int) -> List[int]:
        """Implementação idêntica ao Oracle"""
        embeddings_matrix = np.vstack(embeddings)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        return kmeans.fit_predict(embeddings_matrix).tolist()
```

### **4. Adapter AWS (Futuro)**

```python
# adapters/aws_embedding_adapter.py
import boto3
import numpy as np
from interfaces.embedding_interface import EmbeddingInterface

class AWSEmbeddingAdapter(EmbeddingInterface):
    """Implementação usando AWS Bedrock ou SageMaker"""
    
    def __init__(self, region_name: str = "us-east-1"):
        self.bedrock = boto3.client('bedrock-runtime', region_name=region_name)
        self.model_id = "amazon.titan-embed-text-v1"  # ou Cohere via Bedrock
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Implementação AWS Bedrock"""
        # Implementação específica AWS
        pass
    
    # ... demais métodos seguindo mesma interface
```

### **5. Adapter Azure (Futuro)**

```python
# adapters/azure_embedding_adapter.py
from azure.ai.textanalytics import TextAnalyticsClient
from interfaces.embedding_interface import EmbeddingInterface

class AzureEmbeddingAdapter(EmbeddingInterface):
    """Implementação usando Azure OpenAI Service"""
    
    def __init__(self, endpoint: str, api_key: str):
        self.client = TextAnalyticsClient(endpoint=endpoint, credential=api_key)
    
    # ... implementação Azure específica
```

---

## 🔄 **Factory Pattern para Migração Seamless**

### **6. Factory para Criação de Adapters**

```python
# factories/embedding_factory.py
import os
from typing import Dict, Any
from interfaces.embedding_interface import EmbeddingInterface
from adapters.oci_embedding_adapter import OCIEmbeddingAdapter
from adapters.python_embedding_adapter import PythonEmbeddingAdapter
from adapters.aws_embedding_adapter import AWSEmbeddingAdapter
from adapters.azure_embedding_adapter import AzureEmbeddingAdapter

class EmbeddingFactory:
    """Factory para criar adapters de embedding baseado em configuração"""
    
    @staticmethod
    def create_embedding_service(provider: str = None, **kwargs) -> EmbeddingInterface:
        """Cria serviço de embedding baseado no provider configurado"""
        
        # Prioridade: parâmetro > variável ambiente > padrão
        if provider is None:
            provider = os.getenv('EMBEDDING_PROVIDER', 'oci')
        
        provider = provider.lower()
        
        if provider == 'oci':
            config_path = kwargs.get('config_path', '~/.oci/config')
            return OCIEmbeddingAdapter(config_path=config_path)
            
        elif provider == 'python':
            method = kwargs.get('method', 'sentence_transformers')
            return PythonEmbeddingAdapter(method=method)
            
        elif provider == 'aws':
            region = kwargs.get('region_name', 'us-east-1')
            return AWSEmbeddingAdapter(region_name=region)
            
        elif provider == 'azure':
            endpoint = kwargs.get('endpoint')
            api_key = kwargs.get('api_key')
            if not endpoint or not api_key:
                raise ValueError("Azure requer endpoint e api_key")
            return AzureEmbeddingAdapter(endpoint=endpoint, api_key=api_key)
            
        else:
            raise ValueError(f"Provider não suportado: {provider}")

# Função utilitária para uso simples
def get_embedding_service() -> EmbeddingInterface:
    """Retorna serviço de embedding configurado"""
    return EmbeddingFactory.create_embedding_service()
```

---

## 🚀 **Uso na Aplicação Principal**

### **7. Sistema de Recomendação Cloud-Agnostic**

```python
# core/recommendation_engine.py (CLOUD-AGNOSTIC!)
from factories.embedding_factory import get_embedding_service
from interfaces.embedding_interface import EmbeddingInterface

class RecommendationEngine:
    """Motor de recomendação independente de cloud provider"""
    
    def __init__(self):
        # Injeta o serviço via factory - transparente para a aplicação!
        self.embedding_service: EmbeddingInterface = get_embedding_service()
    
    def analyze_product_overlaps(self, products_df) -> List[Dict]:
        """Identifica sobreposições entre produtos (cloud-agnostic)"""
        descriptions = products_df['descricao'].tolist()
        
        # A implementação não sabe se é Oracle, Python, AWS ou Azure!
        embeddings = self.embedding_service.get_embeddings(descriptions)
        
        overlaps = []
        for i in range(len(embeddings)):
            for j in range(i+1, len(embeddings)):
                similarity = self.embedding_service.calculate_similarity(
                    embeddings[i], embeddings[j]
                )
                if similarity > 0.8:
                    overlaps.append({
                        'produto1': products_df.iloc[i]['nome'],
                        'produto2': products_df.iloc[j]['nome'],
                        'similaridade': similarity
                    })
        
        return overlaps
    
    def get_content_based_recommendations(self, client_id: str, available_products_df) -> Dict:
        """Recomendações baseadas em conteúdo (cloud-agnostic)"""
        # Produtos atuais do cliente
        client_products = self.get_client_products(client_id)
        client_descriptions = [p['descricao'] for p in client_products]
        
        # Embeddings dos produtos do cliente - provider transparente!
        client_embeddings = self.embedding_service.get_embeddings(client_descriptions)
        
        # Embeddings dos produtos disponíveis
        available_descriptions = available_products_df['descricao'].tolist()
        available_embeddings = self.embedding_service.get_embeddings(available_descriptions)
        
        # Calcula similaridade média
        recommendations = []
        for i, available_emb in enumerate(available_embeddings):
            avg_similarity = np.mean([
                self.embedding_service.calculate_similarity(client_emb, available_emb)
                for client_emb in client_embeddings
            ])
            
            recommendations.append({
                'produto': available_products_df.iloc[i]['nome'],
                'score_semantico': avg_similarity,
                'produto_id': available_products_df.iloc[i]['id']
            })
        
        return sorted(recommendations, key=lambda x: x['score_semantico'], reverse=True)
    
    def auto_categorize_products(self, products_df, n_categories: int = 8) -> Dict:
        """Categorização automática (cloud-agnostic)"""
        descriptions = products_df['descricao'].tolist()
        
        # Clustering transparente ao provider!
        embeddings = self.embedding_service.get_embeddings(descriptions)
        clusters = self.embedding_service.cluster_embeddings(embeddings, n_categories)
        
        # Adiciona clusters ao DataFrame
        products_df['categoria_automatica'] = clusters
        
        return {
            'products_with_categories': products_df,
            'n_categories': len(set(clusters))
        }
```

---

## ⚙️ **Configuração de Migração**

### **8. Arquivo de Configuração**

```yaml
# config/embedding_config.yaml
embedding:
  # Configuração atual (Oracle)
  provider: "oci"
  oci:
    config_path: "~/.oci/config"
    model_id: "cohere.embed-multilingual-v3.0"
  
  # Configuração fallback (Python local)
  python:
    method: "sentence_transformers"  # ou "tfidf"
  
  # Configurações futuras
  aws:
    region_name: "us-east-1"
    model_id: "amazon.titan-embed-text-v1"
  
  azure:
    endpoint: "${AZURE_OPENAI_ENDPOINT}"
    api_key: "${AZURE_OPENAI_API_KEY}"
```

### **9. Migração com Variáveis de Ambiente**

```bash
# Configuração atual (Oracle)
export EMBEDDING_PROVIDER=oci

# Para migrar para Python local (zero downtime!)
export EMBEDDING_PROVIDER=python

# Para migrar para AWS
export EMBEDDING_PROVIDER=aws
export AWS_REGION=us-east-1

# Para migrar para Azure
export EMBEDDING_PROVIDER=azure
export AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com/
export AZURE_OPENAI_API_KEY=your-api-key
```

---

## 🧪 **Testes de Compatibilidade**

### **10. Testes para Garantir Migração Seamless**

```python
# tests/test_embedding_compatibility.py
import pytest
from factories.embedding_factory import EmbeddingFactory

class TestEmbeddingCompatibility:
    """Testa compatibilidade entre diferentes providers"""
    
    def test_all_providers_same_interface(self):
        """Todos providers devem implementar a mesma interface"""
        providers = ['oci', 'python']  # , 'aws', 'azure' quando implementados
        
        for provider in providers:
            service = EmbeddingFactory.create_embedding_service(provider)
            
            # Testa métodos obrigatórios
            assert hasattr(service, 'get_embedding')
            assert hasattr(service, 'get_embeddings')
            assert hasattr(service, 'calculate_similarity')
            assert hasattr(service, 'find_most_similar')
            assert hasattr(service, 'cluster_embeddings')
    
    def test_embedding_similarity_consistency(self):
        """Embeddings similares devem dar resultados consistentes"""
        text1 = "Sistema de gestão para transportadoras"
        text2 = "TMS para empresas de logística"
        
        # Testa Oracle vs Python
        oci_service = EmbeddingFactory.create_embedding_service('oci')
        python_service = EmbeddingFactory.create_embedding_service('python')
        
        oci_emb1 = oci_service.get_embedding(text1)
        oci_emb2 = oci_service.get_embedding(text2)
        oci_sim = oci_service.calculate_similarity(oci_emb1, oci_emb2)
        
        python_emb1 = python_service.get_embedding(text1)
        python_emb2 = python_service.get_embedding(text2)
        python_sim = python_service.calculate_similarity(python_emb1, python_emb2)
        
        # Similaridades devem ser correlacionadas (não idênticas, mas similares)
        assert abs(oci_sim - python_sim) < 0.3  # Tolerância para diferenças de modelo
```

---

## 📋 **Checklist de Migração**

### **11. Procedimento de Migração Zero-Downtime**

```python
# scripts/migration_checker.py
class MigrationChecker:
    """Verifica se migração é segura"""
    
    def validate_migration(self, from_provider: str, to_provider: str):
        """Valida se migração é possível"""
        
        # 1. Testa conectividade do novo provider
        try:
            new_service = EmbeddingFactory.create_embedding_service(to_provider)
            test_embedding = new_service.get_embedding("teste de conectividade")
            print(f"✅ {to_provider} conectividade OK")
        except Exception as e:
            print(f"❌ {to_provider} falhou: {e}")
            return False
        
        # 2. Compara qualidade dos embeddings
        sample_texts = [
            "Sistema TMS para transportadoras",
            "Gestão financeira para logística",
            "Plataforma de antecipação de recebíveis"
        ]
        
        old_service = EmbeddingFactory.create_embedding_service(from_provider)
        
        for text in sample_texts:
            old_emb = old_service.get_embedding(text)
            new_emb = new_service.get_embedding(text)
            
            # Verifica se embeddings têm dimensionalidade similar
            if len(old_emb) != len(new_emb):
                print(f"⚠️  Dimensionalidade diferente: {len(old_emb)} vs {len(new_emb)}")
        
        print(f"✅ Migração {from_provider} → {to_provider} validada")
        return True

# Uso
checker = MigrationChecker()
if checker.validate_migration('oci', 'python'):
    os.environ['EMBEDDING_PROVIDER'] = 'python'
    print("🚀 Migração realizada com sucesso!")
```

---

## 🎯 **Benefícios da Arquitetura**

### **✅ Vantagens para nstech:**

1. **Migração Zero-Downtime**: Trocar provider apenas mudando variável de ambiente
2. **Vendor Lock-in Zero**: Não dependemos exclusivamente da Oracle
3. **Testes A/B**: Comparar qualidade entre providers facilmente
4. **Fallback Automático**: Se Oracle falhar, usar Python automaticamente
5. **Evolução Gradual**: Implementar novos providers sem alterar código principal
6. **Compatibilidade Total**: Mesma interface, resultados equivalentes

### **🔄 Exemplo de Migração Real:**

```python
# Hoje (Oracle)
recommendations = recommendation_engine.get_content_based_recommendations(client_id="123")

# Amanhã (Python) - MESMO CÓDIGO, ZERO ALTERAÇÕES!
export EMBEDDING_PROVIDER=python
recommendations = recommendation_engine.get_content_based_recommendations(client_id="123")

# Futuro (AWS) - MESMO CÓDIGO!
export EMBEDDING_PROVIDER=aws
recommendations = recommendation_engine.get_content_based_recommendations(client_id="123")
```

**A aplicação nunca sabe qual provider está sendo usado - é completamente transparente!** 🚀✨

Esta arquitetura garante que investimento no desenvolvimento seja preservado independente de mudanças de estratégia cloud da nstech no futuro!
