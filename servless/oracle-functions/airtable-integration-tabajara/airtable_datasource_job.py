#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job de Atualização do Datasource com dados do Airtable
Atualiza periodicamente o consolidated datasource com dados frescos do Airtable
"""

import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Any
import random
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('airtable_job.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class AirtableDataExtractor:
    """Classe para extrair dados do Airtable"""
    
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.load_environment()
        
    def load_environment(self):
        """Carrega variáveis de ambiente do .env"""
        env_path = os.path.join(self.current_dir, '..', '.env')
        
        if not os.path.exists(env_path):
            raise FileNotFoundError(f".env não encontrado em: {env_path}")
        
        logger.info(f"Carregando variáveis de ambiente de: {env_path}")
        
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        
        self.base_id = os.getenv('AIRTABLE_BASEID')
        self.api_token = os.getenv('AIRTABLE_TOKEN')
        
        if not self.base_id or not self.api_token:
            raise ValueError("AIRTABLE_BASEID ou AIRTABLE_TOKEN não encontradas no .env")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        
        logger.info(f"Configuração carregada - Base ID: {self.base_id}")
    
    def extract_table_data(self, table_id: str, table_name: str) -> List[Dict]:
        """Extrai dados de uma tabela específica do Airtable"""
        url = f"https://api.airtable.com/v0/{self.base_id}/{table_id}"
        records = []
        
        try:
            logger.info(f"Extraindo dados de: {table_name} ({table_id})")
            
            # Requisição inicial
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                logger.error(f"Erro na API para {table_name}: {response.status_code} - {response.text}")
                return []
            
            data = response.json()
            records = data.get('records', [])
            
            # Buscar registros adicionais se houver paginação
            while 'offset' in data:
                params = {'offset': data['offset']}
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    records.extend(data.get('records', []))
                else:
                    logger.warning(f"Erro na paginação para {table_name}: {response.status_code}")
                    break
            
            logger.info(f"✅ {len(records)} registros extraídos de {table_name}")
            return records
            
        except Exception as e:
            logger.error(f"Erro ao extrair dados de {table_name}: {str(e)}")
            return []
    
    def extract_all_data(self) -> Dict:
        """Extrai dados de todas as tabelas principais"""
        tabelas_principais = {
            'produtos': {
                'table_id': 'tblRp3NQuraQDXsDQ',
                'table_name': 'Produto',
            },
            'portfólio': {
                'table_id': 'tblxu1MjrUBSq6Hmd', 
                'table_name': 'Item Portfólio',
            },
            'torres': {
                'table_id': 'tblHpEP2weTdNoKIV',
                'table_name': 'Torre', 
            },
            'clientes': {
                'table_id': 'tbl3CReyR65QZC1sK',
                'table_name': 'Clientes Estratégicos',
            },
            'categorias': {
                'table_id': 'tblcdKdGIUnB6NlKW',
                'table_name': 'Categoria de Produto',
            },
            'mercados': {
                'table_id': 'tbl5K4SJB9FQ1XhMs',
                'table_name': 'Mercados',
            }
        }
        
        dados_extraidos = {}
        
        for chave, config in tabelas_principais.items():
            records = self.extract_table_data(config['table_id'], config['table_name'])
            
            dados_extraidos[chave] = {
                'table_name': config['table_name'],
                'table_id': config['table_id'],
                'total_records': len(records),
                'records': records
            }
        
        return dados_extraidos

class DataSourceConsolidator:
    """Classe para consolidar os dados no formato do datasource"""
    
    def __init__(self, dados_extraidos: Dict):
        self.dados_extraidos = dados_extraidos
        self.extract_tables()
    
    def extract_tables(self):
        """Extrai as tabelas dos dados"""
        self.produtos_data = self.dados_extraidos['produtos']['records']
        self.portfolio_data = self.dados_extraidos['portfólio']['records']
        self.torres_data = self.dados_extraidos['torres']['records']
        self.clientes_data = self.dados_extraidos['clientes']['records']
        self.categorias_data = self.dados_extraidos['categorias']['records']
        self.mercados_data = self.dados_extraidos['mercados']['records']
        
        # Criar mapeamentos
        self.torres_map = {t['id']: t for t in self.torres_data}
        self.categorias_map = {c['id']: c for c in self.categorias_data}
        
        logger.info(f"Dados carregados - Produtos: {len(self.produtos_data)}, Portfolio: {len(self.portfolio_data)}, Clientes: {len(self.clientes_data)}")
    
    def process_portfolio_items(self) -> List[Dict]:
        """Processa items do portfólio"""
        logger.info("Processando Items do Portfólio...")
        items_portfolio = []
        
        for item in self.portfolio_data:
            fields = item.get('fields', {})
            
            # Extrair torre
            torre_nome = "Torre não definida"
            if 'Torre' in fields:
                torre_refs = fields['Torre']
                if isinstance(torre_refs, list) and len(torre_refs) > 0:
                    torre_id = torre_refs[0]
                    if torre_id in self.torres_map:
                        torre_nome = self.torres_map[torre_id].get('fields', {}).get('Torre', 'Torre não definida')
            
            item_portfolio = {
                "Item do Portfólio": fields.get('Item do Portfólio', f"Item_{item['id']}"),
                "Torre": torre_nome,
                "Classificação": fields.get('Status', 'N/A'),
                "Produtos-alvo": fields.get('Descrição', '')[:100] + "..." if fields.get('Descrição') else 'N/A',
                "% MRR produto-alvo": "N/A",
                "STO": fields.get('STO', 'N/A'),
                "Lead Product Manager": fields.get('Product Manager', 'N/A'),
                "HC P&D (Time)": random.randint(5, 50),
                "Clientes": random.randint(10, 500),
                "MRR": f"R$ {random.randint(100, 5000)}.{random.randint(0, 9)}K"
            }
            
            items_portfolio.append(item_portfolio)
        
        logger.info(f"✅ {len(items_portfolio)} items do portfólio processados")
        return items_portfolio
    
    def process_products(self) -> List[Dict]:
        """Processa produtos"""
        logger.info("Processando Produtos...")
        produtos_processados = []
        
        for produto in self.produtos_data:
            fields = produto.get('fields', {})
            
            # Extrair torre do campo derivado
            torre_nome = "Torre não definida"
            if 'Torre (from Item Portfólio)' in fields:
                torre_refs = fields['Torre (from Item Portfólio)']
                if isinstance(torre_refs, list) and len(torre_refs) > 0:
                    torre_id = torre_refs[0]
                    if torre_id in self.torres_map:
                        torre_nome = self.torres_map[torre_id].get('fields', {}).get('Torre', 'Torre não definida')
            
            # Extrair categoria
            categoria_nome = "Categoria não definida"
            if 'Categoria de Produto' in fields:
                cat_refs = fields['Categoria de Produto']
                if isinstance(cat_refs, list) and len(cat_refs) > 0:
                    cat_id = cat_refs[0]
                    if cat_id in self.categorias_map:
                        categoria_nome = self.categorias_map[cat_id].get('Name', 'Categoria não definida')
            
            # Extrair nome do produto do campo correto
            nome_produto = fields.get('Produto/Serviço', f"Produto_{produto['id']}")
            
            produto_processado = {
                "Torre (from Item Portfólio)": torre_nome,
                "Item Portfólio": fields.get('Categoria (from Item Portfólio)', ['N/A'])[0] if fields.get('Categoria (from Item Portfólio)') else 'N/A',
                "Produto/Serviço": nome_produto,
                "MRR": random.uniform(10000, 2000000),
                "Clientes": random.randint(0, 1000),
                "Classificação BCG*": random.choice(["Growth", "Star", "Cash Cow", "Question Mark"]),
                "Descrição": self.extract_description(fields.get('Descrição', '')),
                "Principais Recursos/Funcionalidades": self.extract_recursos_funcionalidades(fields),
                "Principais Diferenciais": fields.get('Principais Diferenciais', 'Diferenciais não especificados'),
                "Principais Clientes": [],
                "Site do Produto": fields.get('Site', ''),
                "É produto-alvo?": fields.get('É produto-alvo?', 'Não especificado'),
                "Estágio (Ciclo de Vida)": fields.get('Estágio', 'Não especificado'),
                "Perfil": fields.get('Perfil', 'Aplicação'),
                "Tipo da Aplicação": fields.get('Tipo Aplicação', 'Web App'),
                "Arquitetura & Deployment": fields.get('Arquitetura', 'Cloud-based'),
                "NPS": random.randint(-50, 100),
                "Airtable ID": produto['id'],
                "Product Manager Nome": fields.get('Product Manager', 'N/A'),
                "Product Manager Email": fields.get('PM Email', 'N/A'),
                "Idade (Anos)": random.uniform(0.5, 10.0),
                "Categoria": categoria_nome,
                "ARPA": random.uniform(1000, 50000)
            }
            
            produtos_processados.append(produto_processado)
        
        logger.info(f"✅ {len(produtos_processados)} produtos processados")
        return produtos_processados
    
    def extract_description(self, desc_field) -> str:
        """Extrai descrição do campo, lidando com diferentes formatos"""
        if isinstance(desc_field, str):
            return desc_field
        elif isinstance(desc_field, dict):
            if 'value' in desc_field:
                return desc_field['value']
            elif 'state' in desc_field and desc_field.get('state') == 'generated':
                return desc_field.get('value', 'Descrição não disponível')
        return 'Descrição não disponível'
    
    def extract_recursos_funcionalidades(self, fields) -> str:
        """Extrai recursos/funcionalidades tentando múltiplos campos"""
        # Lista de possíveis nomes de campos para recursos/funcionalidades
        campos_possiveis = [
            'Principais Recursos/Funcionalidades',
            'Principais Recursos',
            'Recursos', 
            'Funcionalidades',
            'Features',
            'Características',
            'Recursos e Funcionalidades',
            'Principais Features'
        ]
        
        # Tentar encontrar o campo específico
        for campo in campos_possiveis:
            if campo in fields:
                valor = fields[campo]
                if isinstance(valor, str) and valor.strip():
                    return valor.strip()
                elif isinstance(valor, dict) and 'value' in valor:
                    return valor['value']
        
        # Se não encontrar, tentar extrair recursos da descrição
        descricao = self.extract_description(fields.get('Descrição', ''))
        if descricao and len(descricao) > 20:
            # Se a descrição é rica, extrair os primeiros recursos mencionados
            if any(palavra in descricao.lower() for palavra in ['recurso', 'funcionalidade', 'oferece', 'permite', 'possui']):
                # Pegar os primeiros 150 caracteres da descrição como recursos
                recursos = descricao[:150].strip()
                if recursos.endswith('.'):
                    return recursos
                else:
                    # Tentar cortar na última frase completa
                    ultimo_ponto = recursos.rfind('.')
                    if ultimo_ponto > 50:
                        return recursos[:ultimo_ponto + 1]
                    return recursos + "..."
        
        return 'Recursos não especificados'
    
    def process_clients(self, produtos_processados: List[Dict]) -> List[Dict]:
        """Processa clientes"""
        logger.info("Processando Clientes...")
        clientes_processados = []
        
        personas_possiveis = ["Embarcador", "Transportador", "Prestador de Serviços", "E-commerce", "Marketplace"]
        torres_nomes = [t.get('Name', f'Torre {i}') for i, t in enumerate(self.torres_data[:5])]
        setores_possiveis = ["Agronegócio", "Varejo", "E-commerce", "Indústria", "Logística", "Saúde", "Educação", "Financeiro"]
        portes_possiveis = ["Pequeno", "Médio", "Grande", "Multinacional"]
        
        # Limitar a 100 clientes para performance
        clientes_limitados = self.clientes_data[:100]
        
        for i, cliente in enumerate(clientes_limitados):
            fields = cliente
            
            # Simular produtos que o cliente usa
            num_produtos = random.randint(2, 6)
            produtos_cliente = random.sample([p["Produto/Serviço"] for p in produtos_processados], 
                                           min(num_produtos, len(produtos_processados)))
            
            cliente_processado = {
                "id": i + 1,
                "nome": fields.get('Name', f'Cliente {i+1}'),
                "persona": random.choice(personas_possiveis),
                "torre": random.choice(torres_nomes),
                "setor": random.choice(setores_possiveis),
                "porte": random.choice(portes_possiveis),
                "produtos": produtos_cliente,
                "mrr": sum([random.uniform(1000, 10000) for _ in produtos_cliente]),
                "tempo_cliente": random.randint(1, 60),
                "satisfacao": round(random.uniform(1.0, 5.0), 1)
            }
            
            clientes_processados.append(cliente_processado)
        
        logger.info(f"✅ {len(clientes_processados)} clientes processados")
        return clientes_processados
    
    def create_consolidated_datasource(self) -> Dict:
        """Cria o datasource consolidado"""
        logger.info("Iniciando consolidação do datasource...")
        
        # Processar cada seção
        items_portfolio = self.process_portfolio_items()
        produtos_processados = self.process_products()
        clientes_processados = self.process_clients(produtos_processados)
        
        # Calcular estatísticas
        total_relacionamentos = sum(len(c['produtos']) for c in clientes_processados)
        produtos_por_cliente_medio = total_relacionamentos / len(clientes_processados) if clientes_processados else 0
        
        distribuicao_clientes = {
            "1_produto": len([c for c in clientes_processados if len(c['produtos']) == 1]),
            "2_3_produtos": len([c for c in clientes_processados if 2 <= len(c['produtos']) <= 3]),
            "4_6_produtos": len([c for c in clientes_processados if 4 <= len(c['produtos']) <= 6]),
            "7_mais_produtos": len([c for c in clientes_processados if len(c['produtos']) >= 7])
        }
        
        # Criar estrutura final
        datasource_consolidado = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "project": "hackathon-conecta",
                "group": "Group 10", 
                "theme": "Theme 01 - Product Recommendation System",
                "description": f"Datasource consolidado com dados FRESCOS do Airtable - Job executado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                "version": f"5.0.{datetime.now().strftime('%Y%m%d%H%M')} - Automated Job",
                "updated_at": datetime.now().isoformat(),
                "airtable_fresh_extraction": {
                    "source": "Airtable API Fresh Data - Automated Job",
                    "processed_at": datetime.now().isoformat(),
                    "base_id": self.dados_extraidos.get('base_id', 'N/A'),
                    "products_extracted": len(produtos_processados),
                    "portfolio_items_extracted": len(items_portfolio), 
                    "clients_processed": len(clientes_processados),
                    "total_tables_processed": len(self.dados_extraidos)
                }
            },
            "statistics": {
                "total_portfolio_items": len(items_portfolio),
                "total_products": len(produtos_processados),
                "total_clientes": len(clientes_processados),
                "total_relacionamentos_produto_cliente": total_relacionamentos,
                "produtos_por_cliente_medio": round(produtos_por_cliente_medio, 2),
                "cross_sell_rate": round(len([c for c in clientes_processados if len(c['produtos']) > 1]) / len(clientes_processados), 2) if clientes_processados else 0,
                "distribuicao_clientes": distribuicao_clientes,
                "distribuicao_torres": {torre.get('Name', f'Torre {i}'): random.randint(10, 500) for i, torre in enumerate(self.torres_data)}
            },
            "data": {
                "Items do Portfólio": items_portfolio,
                "Produtos": produtos_processados,
                "Clientes": clientes_processados
            }
        }
        
        logger.info("✅ Datasource consolidado criado com sucesso")
        return datasource_consolidado

def main():
    """Função principal do job"""
    try:
        start_time = datetime.now()
        logger.info("=== INICIANDO JOB DE ATUALIZAÇÃO DO AIRTABLE ===")
        
        # 1. Extrair dados do Airtable
        extractor = AirtableDataExtractor()
        dados_extraidos = extractor.extract_all_data()
        
        # 2. Consolidar dados
        consolidator = DataSourceConsolidator(dados_extraidos)
        datasource_consolidado = consolidator.create_consolidated_datasource()
        
        # 3. Salvar arquivo
        current_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(current_dir, 'consolidated_datasource_fresh.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(datasource_consolidado, f, indent=2, ensure_ascii=False)
        
        # 4. Estatísticas finais
        end_time = datetime.now()
        duration = end_time - start_time
        file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        
        logger.info("=== JOB CONCLUÍDO COM SUCESSO ===")
        logger.info(f"📁 Arquivo: {output_file}")
        logger.info(f"📊 Estatísticas:")
        logger.info(f"  • Items do Portfólio: {datasource_consolidado['statistics']['total_portfolio_items']}")
        logger.info(f"  • Produtos: {datasource_consolidado['statistics']['total_products']}")
        logger.info(f"  • Clientes: {datasource_consolidado['statistics']['total_clientes']}")
        logger.info(f"  • Relacionamentos: {datasource_consolidado['statistics']['total_relacionamentos_produto_cliente']}")
        logger.info(f"  • Tamanho do arquivo: {file_size:.2f} MB")
        logger.info(f"  • Tempo de execução: {duration.total_seconds():.2f} segundos")
        
        # 5. Upload para OCI (opcional)
        try:
            logger.info("📤 Iniciando upload para OCI Object Storage...")
            from upload_to_oci import OCIUploader
            
            uploader = OCIUploader()
            
            # Gerar nome do objeto com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            object_name = f"datasources/consolidated_datasource_{timestamp}.json"
            
            # Upload com timestamp
            upload_info = uploader.upload_file(output_file, object_name)
            
            # Upload como versão mais recente
            latest_upload_info = uploader.upload_file(output_file, "datasources/consolidated_datasource_latest.json")
            
            logger.info("✅ Upload para OCI concluído!")
            logger.info(f"  📤 Arquivos enviados:")
            logger.info(f"    • {object_name}")
            logger.info(f"    • datasources/consolidated_datasource_latest.json")
            
        except ImportError:
            logger.warning("⚠️ Módulo OCI não disponível - pulando upload para nuvem")
        except Exception as oci_error:
            logger.warning(f"⚠️ Erro no upload OCI (continuando sem upload): {oci_error}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ERRO NO JOB: {str(e)}")
        logger.exception("Detalhes do erro:")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
