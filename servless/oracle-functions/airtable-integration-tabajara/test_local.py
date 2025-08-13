#!/usr/bin/env python3
"""
🧪 Teste Local da Oracle Function
=================================

Simula uma chamada à Oracle Function localmente para testar o handler.
"""

import json
import io
from func import handler

class MockContext:
    """Mock do contexto da Oracle Function."""
    pass

def test_function():
    """Testa a function localmente."""
    print("🧪 TESTANDO ORACLE FUNCTION LOCALMENTE")
    print("=" * 50)
    
    try:
        # Criar contexto mock
        ctx = MockContext()
        
        # Criar payload de teste (opcional)
        test_payload = {
            "trigger": "manual_test",
            "timestamp": "2025-08-13T04:55:00Z"
        }
        
        # Converter payload para BytesIO
        data = io.BytesIO(json.dumps(test_payload).encode('utf-8'))
        
        print(f"📥 Payload de teste: {json.dumps(test_payload, indent=2)}")
        print("\n🚀 Executando handler...")
        
        # Chamar handler
        response = handler(ctx, data)
        
        # Mostrar resultado
        print(f"\n📤 Status Code: {response.status_code}")
        print(f"📋 Headers: {response.headers}")
        print(f"📄 Response Data:")
        
        # Parsear e formatar resposta
        if response.response_data:
            try:
                response_json = json.loads(response.response_data)
                print(json.dumps(response_json, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print(response.response_data)
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = test_function()
    print(f"\n{'✅ TESTE PASSOU' if success else '❌ TESTE FALHOU'}")
    sys.exit(0 if success else 1)
