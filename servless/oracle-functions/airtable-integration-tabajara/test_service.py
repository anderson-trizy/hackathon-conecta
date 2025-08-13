#!/usr/bin/env python3
"""
🧪 Teste do Serviço Desacoplado
==============================

Testa apenas o serviço de atualização de datasource, sem Oracle Function.
"""

import json
from datasource_service import execute_datasource_update

def main():
    """Testa o serviço desacoplado."""
    print("🧪 TESTANDO SERVIÇO DE ATUALIZAÇÃO DATASOURCE")
    print("=" * 55)
    
    try:
        # Executar serviço
        result = execute_datasource_update()
        
        # Mostrar resultado
        print(f"\n📊 RESULTADO:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Resumo
        if result['success']:
            stats = result.get('statistics', {})
            print(f"\n✅ JOB CONCLUÍDO COM SUCESSO!")
            print(f"⏱️  Duração: {result.get('duration_seconds', 0):.2f}s")
            if stats:
                print(f"📄 Produtos: {stats.get('total_products', 'N/A')}")
                print(f"📋 Portfolio: {stats.get('total_portfolio_items', 'N/A')}")
                print(f"👥 Clientes: {stats.get('total_clientes', 'N/A')}")
        else:
            print(f"\n❌ JOB FALHOU: {result.get('error', 'Erro desconhecido')}")
        
        return result['success']
        
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
