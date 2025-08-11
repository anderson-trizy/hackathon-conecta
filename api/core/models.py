"""
Tipos e modelos compartilhados.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class ClientModel(BaseModel):
    id: str
    nome: str
    setor: str
    porte: str
    produtos: List[str] = []
    mrr: float = 0.0
    satisfacao: float = 0.0


class ProductModel(BaseModel):
    nome: str
    categoria: str
    compatibilidade: List[str] = []


class RecommendationModel(BaseModel):
    product_name: str
    confidence: float
    reason: str


class RecommendationRequest(BaseModel):
    client_id: str
    top_k: int = 5
    use_cache: bool = True


class RecommendationResponse(BaseModel):
    client_id: str
    recommendations: List[RecommendationModel]
    source: str  # 'cache' ou 'generated'
    total: int
    timestamp: Optional[str] = None
