import json

def carregar_datasource():
    """Carrega o datasource enriquecido"""
    with open('datasources/consolidated_datasource_enriquecido.json', 'r', encoding='utf-8') as f:
        datasource = json.load(f)
    return datasource

def criar_mapeamento_torres():
    """Cria mapeamento dos nomes das torres para IDs"""
    torres_mapping = {
        "Torre Embarcador": 1,
        "Torre Fintech": 2, 
        "Torre IM": 3,
        "Torre MG": 4,
        "Torre Mobilidade": 5,
        "Torre PME": 6,
        "Torre Plataforma": 7,
        "Torre VGR": 8
    }
    return torres_mapping

def converter_is_produto_alvo(valor):
    """Converte o valor de 'É produto-alvo?' para 0 ou 1"""
    if not valor:
        return 0
    
    valor_str = str(valor).lower().strip()
    if valor_str in ['sim', 'yes', 'true', '1', 'produto-alvo']:
        return 1
    else:
        return 0

def extrair_torre_id(produto, torres_mapping):
    """Extrai o ID da torre do produto"""
    torre = produto.get('Torre (from Item Portfólio)', '')
    
    if not torre:
        torre = produto.get('Torre', '')
    
    torre = str(torre).strip() if torre else ''
    
    if torre in torres_mapping:
        return torres_mapping[torre]
    
    return 0

def main():
    print("🚀 Gerando JSON limpo de produtos...")
    
    # Carregar dados
    datasource = carregar_datasource()
    torres_mapping = criar_mapeamento_torres()
    
    # Lista limpa de produtos
    produtos_clean = []
    
    produtos = datasource['data']['Produtos']
    
    for produto in produtos:
        produto_obj = {
            "airtable_id": produto.get('Airtable ID', ''),
            "nome": produto.get('Produto/Serviço', ''),
            "quantidade_clientes": produto.get('Clientes', 0),
            "classificacao_bcg": produto.get('Classificação BCG*', ''),
            "is_produto_alvo": converter_is_produto_alvo(produto.get('É produto-alvo?', '')),
            "torre_id": extrair_torre_id(produto, torres_mapping)
        }
        
        produtos_clean.append(produto_obj)
    
    # Salvar JSON limpo
    with open('produtos_clean.json', 'w', encoding='utf-8') as f:
        json.dump(produtos_clean, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON limpo gerado: produtos_clean.json")
    print(f"📊 Total de produtos: {len(produtos_clean)}")

if __name__ == "__main__":
    main()
