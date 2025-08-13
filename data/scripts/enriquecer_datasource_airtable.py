import json
import os
from datetime import datetime

def carregar_dados():
    """Carrega os dados do Airtable e do datasource atual"""
    
    print("📄 Carregando dados do Airtable...")
    with open('airtable_todos_produtos.json', 'r', encoding='utf-8') as f:
        airtable_data = json.load(f)
    
    print("📄 Carregando datasource atual...")
    datasource_path = 'datasources/consolidated_datasource_completo.json'
    with open(datasource_path, 'r', encoding='utf-8') as f:
        datasource = json.load(f)
    
    return airtable_data, datasource

def extrair_valor_campo(fields, campo):
    """Extrai valor de um campo, tratando diferentes estruturas"""
    valor = fields.get(campo, '')
    
    # Se for um dict com 'value', extrair o valor
    if isinstance(valor, dict) and 'value' in valor:
        return valor['value']
    
    # Se for uma lista, pegar o primeiro item
    if isinstance(valor, list) and len(valor) > 0:
        return valor[0]
    
    return valor

def extrair_product_manager_info(fields):
    """Extrai informações do Product Manager"""
    pm_field = fields.get('Product Manager (from Item Portfólio)', [])
    
    if pm_field and isinstance(pm_field, list) and len(pm_field) > 0:
        pm = pm_field[0]
        if isinstance(pm, dict):
            return {
                'nome': pm.get('name', ''),
                'email': pm.get('email', '')
            }
    
    return {'nome': '', 'email': ''}

def calcular_idade_produto(fields):
    """Calcula idade do produto baseado na data de lançamento"""
    idade = fields.get('Idade (Anos)', '')
    if idade:
        return round(idade, 1)
    
    # Se não tiver idade, tentar calcular pela data de lançamento
    data_lancamento = fields.get('Data de Lançamento', '')
    if data_lancamento:
        try:
            from datetime import datetime
            lancamento = datetime.strptime(data_lancamento, '%Y-%m-%d')
            hoje = datetime.now()
            anos = (hoje - lancamento).days / 365.25
            return round(anos, 1)
        except:
            pass
    
    return ''

def extrair_logo_url(fields):
    """Extrai URL do logo do produto"""
    logo_field = fields.get('Logo (Produto)', [])
    if not logo_field:
        logo_field = fields.get('Icon', [])
    
    if logo_field and isinstance(logo_field, list) and len(logo_field) > 0:
        logo = logo_field[0]
        if isinstance(logo, dict) and 'url' in logo:
            return logo['url']
    
    return ''

def criar_mapeamento_produtos_airtable(airtable_data):
    """Cria um mapeamento dos produtos do Airtable por nome"""
    
    print("🗺️ Criando mapeamento de produtos do Airtable...")
    mapeamento = {}
    
    for record in airtable_data['records']:
        fields = record.get('fields', {})
        nome_produto = fields.get('Produto/Serviço', '')
        
        if nome_produto:
            # Extrair informações do Product Manager
            pm_info = extrair_product_manager_info(fields)
            
            # Extrair informações relevantes
            produto_info = {
                'airtable_id': record.get('id', ''),
                'descricao': extrair_valor_campo(fields, 'Descrição'),
                'principais_recursos': extrair_valor_campo(fields, 'Principais Recursos/Funcionalidades'),
                'principais_diferenciais': extrair_valor_campo(fields, 'Principais Diferenciais'),
                'site_produto': fields.get('Site do Produto', ''),
                'eh_produto_alvo': extrair_valor_campo(fields, 'É produto-alvo?'),
                'estagio_ciclo_vida': fields.get('Estágio (Ciclo de Vida)', ''),
                'perfil': fields.get('Perfil', ''),
                'tipo_aplicacao': fields.get('Tipo da aplicação', ''),
                'arquitetura_deployment': fields.get('Arquitetura & Deployment', ''),
                'nps': fields.get('NPS', ''),
                'logo_url': extrair_logo_url(fields),
                'product_manager_nome': pm_info['nome'],
                'product_manager_email': pm_info['email'],
                'idade': calcular_idade_produto(fields),
                'categoria': fields.get('Categoria', ''),
                'mrr': fields.get('MRR', 0),
                'clientes': fields.get('Clientes', 0),
                'classificacao_bcg': fields.get('Classificação BCG*', ''),
                'arpa': fields.get('ARPA', ''),
                'features': fields.get('Features', ''),
                'demo': fields.get('Demo (30-45 min)', ''),
                'pitch': fields.get('Pitch (5 min)', ''),
                'tecnologias': fields.get('Tecnologias Utilizadas', [])
            }
            
            mapeamento[nome_produto] = produto_info
    
    print(f"✅ Mapeamento criado com {len(mapeamento)} produtos do Airtable")
    return mapeamento

def atualizar_produtos_datasource(datasource, mapeamento_airtable):
    """Atualiza os produtos no datasource com informações do Airtable"""
    
    print("🔄 Atualizando produtos no datasource...")
    produtos_atualizados = 0
    produtos_nao_encontrados = []
    
    # Atualizar produtos na seção "Produtos"
    if 'Produtos' in datasource['data']:
        for i, produto in enumerate(datasource['data']['Produtos']):
            nome_produto = produto.get('Produto/Serviço', '')
            
            if nome_produto in mapeamento_airtable:
                airtable_info = mapeamento_airtable[nome_produto]
                
                # Campos para atualizar quando estão vazios ou ausentes
                campos_para_atualizar = {
                    'Airtable ID': airtable_info['airtable_id'],
                    'Descrição': airtable_info['descricao'],
                    'Principais Recursos/Funcionalidades': airtable_info['principais_recursos'],
                    'Principais Diferenciais': airtable_info['principais_diferenciais'],
                    'Site do Produto': airtable_info['site_produto'],
                    'É produto-alvo?': airtable_info['eh_produto_alvo'],
                    'Estágio (Ciclo de Vida)': airtable_info['estagio_ciclo_vida'],
                    'Perfil': airtable_info['perfil'],
                    'Tipo da Aplicação': airtable_info['tipo_aplicacao'],
                    'Arquitetura & Deployment': airtable_info['arquitetura_deployment'],
                    'NPS': airtable_info['nps'],
                    'Logo URL': airtable_info['logo_url'],
                    'Product Manager Nome': airtable_info['product_manager_nome'],
                    'Product Manager Email': airtable_info['product_manager_email'],
                    'Idade (Anos)': airtable_info['idade'],
                    'Categoria': airtable_info['categoria'],
                    'ARPA': airtable_info['arpa'],
                    'Features': airtable_info['features'],
                    'Demo': airtable_info['demo'],
                    'Pitch': airtable_info['pitch']
                }
                
                atualizou_algum_campo = False
                for campo, valor_airtable in campos_para_atualizar.items():
                    # Só atualiza se o campo estiver vazio/ausente e o Airtable tiver valor
                    if valor_airtable and (campo not in produto or not produto[campo] or str(produto[campo]).strip() == ''):
                        produto[campo] = valor_airtable
                        atualizou_algum_campo = True
                
                # Sempre atualizar MRR e Clientes com dados mais recentes
                if airtable_info['mrr']:
                    produto['MRR'] = airtable_info['mrr']
                    atualizou_algum_campo = True
                
                if airtable_info['clientes']:
                    produto['Clientes'] = airtable_info['clientes']
                    atualizou_algum_campo = True
                
                if airtable_info['classificacao_bcg']:
                    produto['Classificação BCG*'] = airtable_info['classificacao_bcg']
                    atualizou_algum_campo = True
                
                if atualizou_algum_campo:
                    produtos_atualizados += 1
                    print(f"  ✅ Atualizado: {nome_produto}")
            
            else:
                produtos_nao_encontrados.append(nome_produto)
    
    print(f"\n📊 Resumo da atualização:")
    print(f"✅ Produtos atualizados: {produtos_atualizados}")
    print(f"⚠️ Produtos não encontrados no Airtable: {len(produtos_nao_encontrados)}")
    
    if produtos_nao_encontrados:
        print(f"\n📋 Produtos não encontrados no Airtable:")
        for produto in produtos_nao_encontrados[:10]:  # Mostra apenas os primeiros 10
            print(f"  - {produto}")
        if len(produtos_nao_encontrados) > 10:
            print(f"  ... e mais {len(produtos_nao_encontrados) - 10} produtos")
    
    return produtos_atualizados

def salvar_datasource_atualizado(datasource, produtos_atualizados):
    """Salva o datasource atualizado"""
    
    # Atualizar metadata
    datasource['metadata']['updated_at'] = datetime.now().isoformat()
    datasource['metadata']['version'] = "4.1.0"
    datasource['metadata']['description'] = f"{datasource['metadata']['description']} - Enriquecido com dados detalhados do Airtable ({produtos_atualizados} produtos atualizados)"
    
    # Adicionar informações sobre a atualização Airtable
    datasource['metadata']['airtable_enrichment'] = {
        'source': 'airtable_todos_produtos.json',
        'processed_at': datetime.now().isoformat(),
        'products_updated': produtos_atualizados,
        'fields_added': [
            'Airtable ID',
            'Descrição',
            'Principais Recursos/Funcionalidades', 
            'Principais Diferenciais',
            'Site do Produto',
            'É produto-alvo?',
            'Estágio (Ciclo de Vida)',
            'Perfil',
            'Tipo da Aplicação',
            'Arquitetura & Deployment',
            'NPS',
            'Logo URL',
            'Product Manager Nome',
            'Product Manager Email',
            'Idade (Anos)',
            'Categoria',
            'ARPA',
            'Features',
            'Demo',
            'Pitch'
        ]
    }
    
    # Salvar arquivo atualizado
    output_path = 'datasources/consolidated_datasource_enriquecido.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(datasource, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Datasource atualizado salvo em: {output_path}")
    return output_path

def mostrar_estatisticas_enriquecimento(datasource):
    """Mostra estatísticas do enriquecimento"""
    
    if 'Produtos' not in datasource['data']:
        return
        
    produtos = datasource['data']['Produtos']
    total_produtos = len(produtos)
    
    # Contar campos preenchidos
    campos_analisados = [
        'Airtable ID', 'Descrição', 'Principais Recursos/Funcionalidades',
        'Principais Diferenciais', 'Site do Produto', 'É produto-alvo?',
        'Estágio (Ciclo de Vida)', 'Perfil', 'Tipo da Aplicação',
        'Arquitetura & Deployment', 'NPS', 'Logo URL', 'Product Manager Nome',
        'Idade (Anos)', 'Categoria'
    ]
    
    estatisticas = {}
    for campo in campos_analisados:
        preenchidos = sum(1 for p in produtos if p.get(campo) and str(p[campo]).strip())
        estatisticas[campo] = {
            'preenchidos': preenchidos,
            'percentual': (preenchidos / total_produtos) * 100
        }
    
    print(f"\n📈 ESTATÍSTICAS DE ENRIQUECIMENTO:")
    print(f"📊 Total de produtos: {total_produtos}")
    print(f"\n📋 Campos enriquecidos:")
    
    for campo, stats in estatisticas.items():
        print(f"  • {campo}: {stats['preenchidos']}/{total_produtos} ({stats['percentual']:.1f}%)")

def main():
    print("🚀 Iniciando enriquecimento do datasource com dados do Airtable")
    print("=" * 70)
    
    try:
        # Carregar dados
        airtable_data, datasource = carregar_dados()
        
        # Criar mapeamento
        mapeamento_airtable = criar_mapeamento_produtos_airtable(airtable_data)
        
        # Atualizar produtos
        produtos_atualizados = atualizar_produtos_datasource(datasource, mapeamento_airtable)
        
        # Salvar resultado
        output_path = salvar_datasource_atualizado(datasource, produtos_atualizados)
        
        # Mostrar estatísticas
        mostrar_estatisticas_enriquecimento(datasource)
        
        print("\n🎉 ENRIQUECIMENTO CONCLUÍDO COM SUCESSO!")
        print(f"📊 Total de produtos atualizados: {produtos_atualizados}")
        print(f"📁 Arquivo salvo em: {output_path}")
        
    except Exception as e:
        print(f"❌ Erro durante o enriquecimento: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
