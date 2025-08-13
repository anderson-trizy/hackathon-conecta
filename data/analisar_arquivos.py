import os
import json
from datetime import datetime

def analisar_arquivos_essenciais():
    """Analisa quais arquivos são realmente necessários"""
    
    print("🔍 ANÁLISE DE ARQUIVOS ESSENCIAIS")
    print("=" * 50)
    
    # Arquivos essenciais identificados
    arquivos_essenciais = {
        "DATASOURCE PRINCIPAL": [
            "datasources/consolidated_datasource_enriquecido.json"
        ],
        "DADOS PARA ML/ANÁLISE": [
            "json_exports/produtos_clean.json",
            "json_exports/clientes.json"
        ],
        "DADOS COMPLETOS AIRTABLE": [
            "json_exports/airtable_todos_produtos.json"
        ],
        "DADOS ESTRUTURADOS": [
            "json_exports/personas.json",
            "json_exports/torres.json",
            "json_exports/itens_portfolio.json"
        ],
        "SCRIPTS PRINCIPAIS": [
            "scripts/buscar_todos_produtos_airtable.py",
            "scripts/enriquecer_datasource_airtable.py", 
            "scripts/gerar_produtos_clean.py"
        ]
    }
    
    # Arquivos que podem ser removidos
    arquivos_desnecessarios = {
        "DATASOURCES BACKUP": [
            "datasources/consolidated_datasource.json",
            "datasources/consolidated_datasource_completo.json"
        ],
        "JSON INTERMEDIÁRIOS": [
            "json_exports/airtable_produtos.json",  # Apenas 100 produtos (incompleto)
            "json_exports/airtable_schema.json",   # Schema não usado
            "json_exports/produtos_simplificado.json"  # Versão com metadados desnecessários
        ],
        "SCRIPTS DE DESENVOLVIMENTO": [
            "scripts/buscar_bases_airtable.py",
            "scripts/buscar_produtos_airtable.py", # Busca apenas 100
            "scripts/explorar_base_airtable.py",
            "scripts/investigar_torres.py",
            "scripts/atualizar_datasource_airtable.py",
            "scripts/gerar_produtos_simplificado.py",
            "scripts/testar_estrutura.py",
            "scripts/consulta_llm.py"
        ]
    }
    
    print("✅ ARQUIVOS ESSENCIAIS:")
    total_essenciais = 0
    for categoria, arquivos in arquivos_essenciais.items():
        print(f"\n📁 {categoria}:")
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                size = os.path.getsize(arquivo) / 1024  # KB
                print(f"  ✅ {arquivo} ({size:.0f} KB)")
                total_essenciais += 1
            else:
                print(f"  ❌ {arquivo} (não encontrado)")
    
    print(f"\n❌ ARQUIVOS QUE PODEM SER REMOVIDOS:")
    total_remover = 0
    for categoria, arquivos in arquivos_desnecessarios.items():
        print(f"\n📁 {categoria}:")
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                size = os.path.getsize(arquivo) / 1024  # KB
                print(f"  🗑️ {arquivo} ({size:.0f} KB)")
                total_remover += 1
            else:
                print(f"  ⚪ {arquivo} (já removido)")
    
    print(f"\n📊 RESUMO:")
    print(f"✅ Arquivos essenciais: {total_essenciais}")
    print(f"🗑️ Arquivos para remover: {total_remover}")
    
    # Calcular economia de espaço
    espaco_total = 0
    espaco_remover = 0
    
    for categoria, arquivos in list(arquivos_essenciais.values()) + list(arquivos_desnecessarios.values()):
        for arquivo in arquivos if isinstance(arquivos, list) else [arquivos]:
            if os.path.exists(arquivo):
                size = os.path.getsize(arquivo)
                espaco_total += size
                if arquivo in sum(arquivos_desnecessarios.values(), []):
                    espaco_remover += size
    
    print(f"💾 Espaço total: {espaco_total/1024/1024:.1f} MB")
    print(f"🗑️ Espaço a liberar: {espaco_remover/1024/1024:.1f} MB ({espaco_remover/espaco_total*100:.1f}%)")
    
    return arquivos_desnecessarios

def main():
    arquivos_para_remover = analisar_arquivos_essenciais()
    
    print(f"\n🤔 RECOMENDAÇÃO:")
    print("Manter apenas os arquivos essenciais para:")
    print("• Sistema de recomendação (produtos_clean.json)")  
    print("• Análise de clientes (clientes.json)")
    print("• Dados completos do Airtable (airtable_todos_produtos.json)")
    print("• Datasource principal enriquecido")
    print("• Scripts principais de integração")

if __name__ == "__main__":
    main()
