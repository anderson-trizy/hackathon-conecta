"""
API Principal - FastAPI com Engine Avançada (47 dimensões)
Algoritmo completo do notebook migrado do backup-api-v2
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from typing import Dict, Any

from core.advanced_service import AdvancedRecommendationService
from core.advanced_engine import AdvancedMLEngine
from adapters.local.adapters import LocalDataSource, LocalStorage


# Variáveis globais para os serviços
recommendation_service: AdvancedRecommendationService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Configura serviços na inicialização."""
    global recommendation_service
    
    # Configurar adapters baseado no ambiente
    cloud_provider = os.getenv('CLOUD_PROVIDER', 'local')
    
    if cloud_provider == 'oracle':
        # TODO: Implementar OCI adapters
        print("Oracle adapters não implementados ainda, usando local")
        data_source = LocalDataSource('../data/datasources/consolidated_datasource.json')
        ml_engine = AdvancedMLEngine(data_source)
        storage = LocalStorage('./cache')
    else:
        # Usar adapters locais para desenvolvimento
        data_source = LocalDataSource('../data/datasources/consolidated_datasource.json')
        ml_engine = AdvancedMLEngine(data_source)
        storage = LocalStorage('./cache')
    
    # Inicializar serviço avançado
    recommendation_service = AdvancedRecommendationService(
        data_source=data_source,
        ml_engine=ml_engine,
        storage=storage
    )
    
    print(f"API iniciada com provider: {cloud_provider}")
    yield
    
    print("API finalizada")


# Criar aplicação FastAPI
app = FastAPI(
    title="🧠 Sistema de Recomendações Avançado",
    description="API com algoritmo completo do notebook - 47 dimensões, TF-IDF, MultiLabelBinarizer - Oracle Functions Ready",
    version="2.0.0-advanced",
    lifespan=lifespan
)

# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em prod, especificar domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check da aplicação."""
    try:
        if recommendation_service is None:
            return JSONResponse(
                status_code=503,
                content={"status": "unhealthy", "error": "Service not initialized"}
            )
        
        result = await recommendation_service.health_check()
        status_code = 200 if result.get('status') == 'healthy' else 503
        
        return JSONResponse(status_code=status_code, content=result)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "error": str(e)}
        )


@app.get("/")
async def root():
    """Endpoint raiz."""
    return {
        "message": "🧠 Sistema de Recomendações Avançado",
        "version": "2.0.0-advanced",
        "algorithm": "notebook_replica_47_dimensions",
        "features": {
            "dimensions": 47,
            "methods": ["TF-IDF", "MultiLabelBinarizer", "LabelEncoder", "StandardScaler"],
            "scoring": "weighted_40freq_35sim_25fit"
        },
        "cloud_provider": os.getenv('CLOUD_PROVIDER', 'local'),
        "endpoints": {
            "health": "/health",
            "recommendations": "/recommendations/{client_id}",
            "client": "/client/{client_id}",
            "similar": "/similar/{client_id}",
            "analysis": "/analysis/{client_id}"
        }
    }


@app.get("/recommendations/{client_id}")
async def get_recommendations(
    client_id: str, 
    top_k: int = 5, 
    use_cache: bool = True
):
    """Gera recomendações avançadas para um cliente usando algoritmo do notebook."""
    try:
        if recommendation_service is None:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        result = await recommendation_service.get_client_recommendations(
            client_id=client_id,
            top_k=top_k,
            use_cache=use_cache
        )
        
        if not result.get('recommendations'):
            raise HTTPException(status_code=404, detail="No recommendations found")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/client/{client_id}")
async def get_client(client_id: str):
    """Retorna informações do cliente."""
    try:
        if recommendation_service is None:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        client_info = await recommendation_service.get_client_info(client_id)
        
        if not client_info:
            raise HTTPException(status_code=404, detail="Client not found")
        
        return client_info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/similar/{client_id}")
async def get_similar_clients(client_id: str, top_k: int = 10):
    """Retorna análise de clientes similares usando algoritmo avançado."""
    try:
        if recommendation_service is None:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        similar_analysis = await recommendation_service.get_client_similar_analysis(
            client_id=client_id,
            top_k=top_k
        )
        
        return similar_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/debug/{client_id}")
async def debug_client(client_id: str):
    """Debug detalhado do cliente para comparação com notebook."""
    try:
        if recommendation_service is None:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Acessar engine diretamente para debug
        engine = recommendation_service.ml_engine
        
        if not engine.is_initialized:
            await engine.initialize()
        
        # Encontrar dados do cliente
        client_idx = None
        for idx, row in engine.df_clients_expanded.iterrows():
            if str(row['id']) == str(client_id):
                client_idx = idx
                break
        
        if client_idx is None:
            raise HTTPException(status_code=404, detail="Client not found")
        
        target_client_data = engine.df_clients_expanded.iloc[client_idx]
        
        # Calcular similaridades
        similarities = cosine_similarity(engine.feature_matrix_scaled)[client_idx]
        similarities[client_idx] = 0
        
        # Clientes similares
        min_similarity = 0.3
        valid_indices = np.where(similarities >= min_similarity)[0]
        sorted_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]]
        top_similar_indices = sorted_indices[:5]  # Top 5 para debug
        
        similar_clients_debug = []
        for sim_idx in top_similar_indices:
            sim_client = engine.df_clients_expanded.iloc[sim_idx]
            similar_clients_debug.append({
                'id': sim_client['id'],
                'nome': sim_client['nome'],
                'similarity': float(similarities[sim_idx]),
                'setor': sim_client['setor'],
                'porte': sim_client['porte'],
                'produtos': sim_client['produtos']
            })
        
        return {
            'client_id': client_id,
            'client_data': {
                'id': target_client_data['id'],
                'nome': target_client_data['nome'],
                'setor': target_client_data['setor'],
                'porte': target_client_data['porte'],
                'produtos': target_client_data['produtos'],
                'mrr': target_client_data['mrr']
            },
            'feature_matrix_shape': engine.feature_matrix_scaled.shape,
            'total_similar_clients': len(valid_indices),
            'top_similar_clients': similar_clients_debug,
            'algorithm_info': {
                'min_similarity_threshold': min_similarity,
                'feature_dimensions': engine.feature_matrix_scaled.shape[1]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analysis/{client_id}")
async def get_client_analysis(client_id: str):
    """Análise completa do cliente com recomendações e similares."""
    try:
        if recommendation_service is None:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        analysis = await recommendation_service.get_full_client_analysis(client_id)
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/debug/{client_id}")
async def debug_calculations(client_id: str):
    """Debug dos cálculos intermediários para comparar com notebook."""
    try:
        if recommendation_service is None:
            raise HTTPException(status_code=503, detail="Service not initialized")
        
        # Chamar método de debug da engine
        debug_data = await recommendation_service.debug_client_calculations(client_id)
        
        return debug_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"Iniciando servidor em {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
