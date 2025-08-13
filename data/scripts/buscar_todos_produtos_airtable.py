import requests
import json
import os
from dotenv import load_dotenv

def buscar_todos_produtos():
    """
    Busca TODOS os dados da tabela Produto no Airtable usando paginação
    """
    
    # Carregar variáveis de ambiente do .env na raiz do projeto
    load_dotenv(dotenv_path='../.env')
    
    # Configurações
    AIRTABLE_TOKEN = os.getenv('AIRTABLE_TOKEN')
    BASE_ID = "appmmRRZgZ3xSTwB6"  # ID da base Portfólio
    TABLE_NAME = "Produto"  # Nome da tabela
    
    if not AIRTABLE_TOKEN:
        print("❌ Token do Airtable não encontrado!")
        return
    
    print(f"🔑 Token encontrado: {AIRTABLE_TOKEN[:10]}...")
    print(f"📊 Base ID: {BASE_ID}")
    print(f"📋 Tabela: {TABLE_NAME}")
    
    # URL da API para buscar registros da tabela
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Buscar TODOS os registros usando paginação
    todos_produtos = []
    offset = None
    pagina = 1
    
    try:
        print("🔍 Iniciando busca completa com paginação...")
        
        while True:
            print(f"📄 Processando página {pagina}...")
            
            # Parâmetros da requisição
            params = {}
            if offset:
                params['offset'] = offset
            
            response = requests.get(url, headers=headers, params=params)
            
            print(f"   📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Pegar registros desta página
                records_pagina = data.get('records', [])
                todos_produtos.extend(records_pagina)
                
                print(f"   ✅ {len(records_pagina)} produtos na página {pagina}")
                print(f"   📊 Total acumulado: {len(todos_produtos)} produtos")
                
                # Verificar se há mais páginas
                offset = data.get('offset')
                if not offset:
                    print("   🏁 Última página alcançada!")
                    break
                
                pagina += 1
                
            else:
                print(f"❌ Erro na página {pagina}: {response.status_code}")
                print(f"Resposta: {response.text}")
                break
        
        print(f"\n🎯 BUSCA COMPLETA FINALIZADA!")
        print(f"✅ Total de produtos encontrados: {len(todos_produtos)}")
        
        # Exibir informações dos produtos
        print(f"\n📋 Lista dos {len(todos_produtos)} produtos:")
        print("=" * 60)
        
        for i, record in enumerate(todos_produtos, 1):
            record_id = record.get('id', 'ID não disponível')
            fields = record.get('fields', {})
            
            # Extrair campos principais
            nome = fields.get('Produto/Serviço', 'Nome não disponível')
            mrr = fields.get('MRR', 0)
            clientes = fields.get('Clientes', 0)
            torre = fields.get('Torre (from Item Portfólio)', ['N/A'])
            item_portfolio = fields.get('Item Portfólio', ['N/A'])
            classificacao_bcg = fields.get('Classificação BCG*', 'N/A')
            estagio = fields.get('Estágio (Ciclo de Vida)', 'N/A')
            
            print(f"📦 Produto {i}: {nome}")
            print(f"   ID: {record_id}")
            print(f"   MRR: R$ {mrr:,.2f}" if isinstance(mrr, (int, float)) else f"   MRR: {mrr}")
            print(f"   Clientes: {clientes}")
            print(f"   Torre: {torre[0] if torre and torre[0] != 'N/A' else 'N/A'}")
            print(f"   Item Portfólio: {item_portfolio[0] if item_portfolio and item_portfolio[0] != 'N/A' else 'N/A'}")
            print(f"   BCG: {classificacao_bcg}")
            print(f"   Estágio: {estagio}")
            print()
        
        # Salvar dados completos
        dados_completos = {
            'total_records': len(todos_produtos),
            'records': todos_produtos,
            'metadata': {
                'base_id': BASE_ID,
                'table_name': TABLE_NAME,
                'total_pages_processed': pagina
            }
        }
        
        nome_arquivo = 'airtable_todos_produtos.json'
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_completos, f, ensure_ascii=False, indent=2)
        
        print(f"📄 Dados completos salvos em: {nome_arquivo}")
        
        # Estatísticas detalhadas
        if todos_produtos:
            print(f"\n📊 ESTATÍSTICAS DETALHADAS:")
            print(f"💡 Total de produtos: {len(todos_produtos)}")
            
            # Contar campos únicos
            all_fields = set()
            for record in todos_produtos:
                all_fields.update(record['fields'].keys())
            
            print(f"💡 Total de campos únicos disponíveis: {len(all_fields)}")
            
            # Top 15 campos mais populares
            field_count = {}
            for field in all_fields:
                count = sum(1 for r in todos_produtos if field in r['fields'])
                field_count[field] = count
            
            print(f"\n📈 Top 15 campos mais populares:")
            top_fields = sorted(field_count.items(), key=lambda x: x[1], reverse=True)[:15]
            for field, count in top_fields:
                percentage = (count / len(todos_produtos)) * 100
                print(f"   - {field}: {count}/{len(todos_produtos)} ({percentage:.1f}%)")
            
            # Estatísticas de MRR e Clientes
            mrrs = []
            clientes_total = []
            for record in todos_produtos:
                fields = record['fields']
                if 'MRR' in fields and isinstance(fields['MRR'], (int, float)):
                    mrrs.append(fields['MRR'])
                if 'Clientes' in fields and isinstance(fields['Clientes'], (int, float)):
                    clientes_total.append(fields['Clientes'])
            
            if mrrs:
                mrr_total = sum(mrrs)
                print(f"\n💰 MRR Total: R$ {mrr_total:,.2f}")
                print(f"📊 MRR Médio: R$ {mrr_total/len(mrrs):,.2f}")
                print(f"🔝 Maior MRR: R$ {max(mrrs):,.2f}")
            
            if clientes_total:
                clientes_soma = sum(clientes_total)
                print(f"👥 Total de Clientes: {clientes_soma:,}")
                print(f"📊 Média de Clientes por Produto: {clientes_soma/len(clientes_total):,.0f}")
                print(f"🔝 Produto com mais Clientes: {max(clientes_total):,}")
        
        return dados_completos
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Script Completo - Buscar TODOS os Produtos do Airtable")
    print("=" * 60)
    produtos = buscar_todos_produtos()
    
    if produtos:
        print("\n🎉 BUSCA COMPLETA FINALIZADA COM SUCESSO!")
        print(f"📊 Total de produtos capturados: {produtos['total_records']}")
    else:
        print("\n💥 Falha na busca completa dos produtos")
