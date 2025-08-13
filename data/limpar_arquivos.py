import os

def limpar_arquivos_desnecessarios():
    """Remove arquivos desnecessários mantendo apenas os essenciais"""
    
    print("🧹 LIMPANDO ARQUIVOS DESNECESSÁRIOS")
    print("=" * 50)
    
    # Arquivos que podem ser removidos
    arquivos_para_remover = [
        # Datasources backup
        "datasources/consolidated_datasource.json",
        "datasources/consolidated_datasource_completo.json",
        
        # JSON intermediários
        "json_exports/airtable_produtos.json",  # Apenas 100 produtos (incompleto)
        "json_exports/airtable_schema.json",   # Schema não usado
        "json_exports/produtos_simplificado.json",  # Versão com metadados desnecessários
        
        # Scripts de desenvolvimento/debug
        "scripts/buscar_bases_airtable.py",
        "scripts/buscar_produtos_airtable.py", # Busca apenas 100
        "scripts/explorar_base_airtable.py",
        "scripts/investigar_torres.py",
        "scripts/atualizar_datasource_airtable.py",
        "scripts/gerar_produtos_simplificado.py",
        "scripts/testar_estrutura.py",
        "scripts/consulta_llm.py",
        "scripts/consolidar_datasources.py",  # Não usado mais
        "scripts/enriquecer_dados_empresariais.py",  # Já aplicado
        "scripts/processar_csv_clientes.py",  # Já aplicado
        "scripts/extrair_clientes.py",  # Já aplicado
        "scripts/extrair_personas.py",  # Já aplicado
        "scripts/extrair_torres.py",  # Já aplicado
        "scripts/extrair_itens_portfolio.py"  # Já aplicado
    ]
    
    total_removidos = 0
    espaco_liberado = 0
    
    for arquivo in arquivos_para_remover:
        if os.path.exists(arquivo):
            size = os.path.getsize(arquivo)
            try:
                os.remove(arquivo)
                size_kb = size / 1024
                print(f"🗑️ Removido: {arquivo} ({size_kb:.0f} KB)")
                total_removidos += 1
                espaco_liberado += size
            except Exception as e:
                print(f"❌ Erro ao remover {arquivo}: {e}")
        else:
            print(f"⚪ Já removido: {arquivo}")
    
    print(f"\n📊 RESUMO DA LIMPEZA:")
    print(f"🗑️ Arquivos removidos: {total_removidos}")
    print(f"💾 Espaço liberado: {espaco_liberado/1024/1024:.1f} MB")

def listar_arquivos_restantes():
    """Lista os arquivos que permaneceram"""
    
    print(f"\n✅ ARQUIVOS ESSENCIAIS MANTIDOS:")
    print("=" * 50)
    
    # Listar datasources
    print("\n📊 DATASOURCES:")
    if os.path.exists("datasources"):
        for arquivo in os.listdir("datasources"):
            if arquivo.endswith('.json'):
                size = os.path.getsize(f"datasources/{arquivo}") / 1024
                print(f"  ✅ {arquivo} ({size:.0f} KB)")
    
    # Listar JSON exports essenciais
    print("\n🗂️ JSON EXPORTS:")
    arquivos_essenciais_json = [
        "produtos_clean.json",
        "clientes.json", 
        "airtable_todos_produtos.json",
        "personas.json",
        "torres.json",
        "itens_portfolio.json"
    ]
    
    for arquivo in arquivos_essenciais_json:
        caminho = f"json_exports/{arquivo}"
        if os.path.exists(caminho):
            size = os.path.getsize(caminho) / 1024
            print(f"  ✅ {arquivo} ({size:.0f} KB)")
    
    # Listar scripts essenciais
    print("\n🔧 SCRIPTS:")
    if os.path.exists("scripts"):
        for arquivo in os.listdir("scripts"):
            if arquivo.endswith('.py'):
                size = os.path.getsize(f"scripts/{arquivo}") / 1024
                print(f"  ✅ {arquivo} ({size:.0f} KB)")
    
    # Listar raw
    print("\n📥 RAW:")
    if os.path.exists("raw"):
        for arquivo in os.listdir("raw"):
            size = os.path.getsize(f"raw/{arquivo}") / 1024
            print(f"  ✅ {arquivo} ({size:.0f} KB)")

def main():
    # Limpar arquivos desnecessários
    limpar_arquivos_desnecessarios()
    
    # Listar o que restou
    listar_arquivos_restantes()
    
    print(f"\n🎉 LIMPEZA CONCLUÍDA!")
    print("Mantidos apenas os arquivos essenciais para o hackathon:")
    print("• Datasource principal enriquecido")
    print("• Dados limpos para ML (produtos_clean.json)")
    print("• Dados completos do Airtable")
    print("• Scripts principais de integração")
    print("• Dados estruturados (clientes, personas, torres)")

if __name__ == "__main__":
    main()
