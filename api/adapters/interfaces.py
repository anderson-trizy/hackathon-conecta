"""
Interfaces abstratas para arquitetura multicloud.
Define contratos que podem ser implementados para Oracle, AWS, Azure, etc.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import pandas as pd


class DataSourceInterface(ABC):
    """Interface para fontes de dados (cloud-agnostic)."""
    
    @abstractmethod
    async def get_clients(self) -> pd.DataFrame:
        """Retorna dados dos clientes."""
        pass
    
    @abstractmethod
    async def get_products(self) -> pd.DataFrame:
        """Retorna dados dos produtos."""
        pass


class MLInterface(ABC):
    """Interface para serviços de ML (cloud-agnostic)."""
    
    @abstractmethod
    async def calculate_similarity(self, client_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calcula similaridade entre clientes."""
        pass
    
    @abstractmethod
    async def recommend_products(self, client_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Gera recomendações de produtos."""
        pass


class StorageInterface(ABC):
    """Interface para armazenamento (cloud-agnostic)."""
    
    @abstractmethod
    async def save_recommendations(self, client_id: str, recommendations: List[Dict[str, Any]]) -> bool:
        """Salva recomendações no storage."""
        pass
    
    @abstractmethod
    async def get_cached_recommendations(self, client_id: str) -> List[Dict[str, Any]]:
        """Busca recomendações em cache."""
        pass
