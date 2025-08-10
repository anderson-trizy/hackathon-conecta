# 🚀 SETUP AUTOMÁTICO - NSTECH RECOMMENDATION SYSTEM
"""
Script para configurar automaticamente o ambiente local ou OCI.
Execute com: python setup_environment.py
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Instala um pacote Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado com sucesso")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erro ao instalar {package}")
        return False

def check_oci_config():
    """Verifica se a configuração OCI existe"""
    oci_config_path = Path.home() / ".oci" / "config"
    return oci_config_path.exists()

def create_sample_oci_config():
    """Cria um arquivo de configuração OCI de exemplo"""
    oci_dir = Path.home() / ".oci"
    oci_dir.mkdir(exist_ok=True)
    
    config_content = f"""[DEFAULT]
user={os.getenv('OCI_USER_ID')}
fingerprint={os.getenv('OCI_FINGERPRINT')}
key_file=~/.oci/private_key.pem
tenancy={os.getenv('OCI_TENANCY_ID')}
region={os.getenv('OCI_REGION')}
compartment_id={os.getenv('OCI_COMPARTMENT_ID')}

# 🔧 INSTRUÇÕES:
# 1. Configure as variáveis de ambiente: OCI_USER_ID, OCI_FINGERPRINT, OCI_TENANCY_ID, OCI_REGION, OCI_COMPARTMENT_ID
# 2. Baixe sua chave privada do OCI Console
# 3. Salve a chave em ~/.oci/private_key.pem
# 4. Execute: chmod 600 ~/.oci/private_key.pem (Linux/Mac)
"""
    
    config_path = oci_dir / "config"
    if not config_path.exists():
        with open(config_path, 'w') as f:
            f.write(config_content)
        print(f"📄 Arquivo de configuração OCI criado em: {config_path}")
        print("⚠️  EDITE o arquivo com suas credenciais reais!")
    else:
        print(f"✅ Arquivo de configuração OCI já existe: {config_path}")

def install_basic_packages():
    """Instala pacotes básicos necessários em qualquer ambiente"""
    
    # Poderia remover matplotlib, seaborn, pandas-profiling, que estão no oracle-ads[viz], 
    # mas ocorreu erro ao executar no OCI e então voltamos para oracle-ads)
    basic_packages = [
        "pandas>=1.5.0",
        "numpy>=1.21.0", 
        "scikit-learn>=1.1.0",
        "matplotlib", 
        "seaborn", 
        "plotly"
    ]
    
    print("📦 Instalando dependências básicas...")
    success = True
    for package in basic_packages:
        if not install_package(package):
            success = False
    return success

def setup_local_environment():
    """Configura ambiente local"""
    print("🏠 CONFIGURANDO AMBIENTE LOCAL")
    print("="*40)
    
    if install_basic_packages():
        print("\n✅ Ambiente local configurado com sucesso!")
        print("   Para usar: USE_OCI = False no notebook")

def setup_oci_environment():
    """Configura ambiente OCI"""
    print("☁️  CONFIGURANDO AMBIENTE OCI")
    print("="*40)
    
    # Detectar se estamos no OCI Data Science
    is_oci_datascience = os.environ.get('OCI_RESOURCE_PRINCIPAL_VERSION') is not None
    
    # Instalar básicos primeiro
    if not install_basic_packages():
        print("❌ Erro ao instalar dependências básicas")
        return
    
    # Instalar oracle-ads[viz] e oci
    oci_packages = ['oracle-ads', "oci"]
    
    print("\n📦 Instalando dependências específicas do OCI (inclui visualização)...")
    success = True
    for package in oci_packages:
        if not install_package(package):
            success = False
    
    if success:
        if is_oci_datascience:
            print("\n☁️  MODO OCI DATA SCIENCE DETECTADO")
            print("✅ Autenticação automática via Resource Principal")
            print("✅ Não é necessário configurar credenciais!")
        else:
            print("\n🏠 MODO LOCAL - Configurando credenciais...")
            if check_oci_config():
                print("✅ Configuração OCI encontrada")
            else:
                create_sample_oci_config()
            print("   📝 Não esqueça de editar ~/.oci/config com suas credenciais!")
        
        print("\n✅ Ambiente OCI configurado com sucesso!")
        print("   Para usar: USE_OCI = True no notebook")
    else:
        print("\n❌ Erro na configuração OCI")
        print("   Verifique sua conexão de internet e tente novamente")

def main():
    """Função principal"""
    print("🚀 NSTECH RECOMMENDATION SYSTEM - SETUP")
    print("="*50)
    
    # Detectar ambiente
    print("🔍 Detectando ambiente...")
    
    # Verificar se estamos no OCI Data Science
    is_oci_datascience = os.environ.get('OCI_RESOURCE_PRINCIPAL_VERSION') is not None
    
    if is_oci_datascience:
        print("☁️  Ambiente OCI Data Science detectado")
        setup_oci_environment()
    else:
        print("🏠 Ambiente local detectado")
        
        # Perguntar ao usuário qual ambiente configurar
        print("\n❓ Qual ambiente você quer configurar?")
        print("   1. Local apenas (desenvolvimento)")
        print("   2. OCI apenas (produção)")
        print("   3. Ambos (recomendado)")
        
        choice = input("\nDigite sua escolha (1/2/3): ").strip()
        
        if choice in ['1', '3']:
            setup_local_environment()
        
        if choice in ['2', '3']:
            print("\n" + "="*50)
            setup_oci_environment()
        
        if choice not in ['1', '2', '3']:
            print("❌ Opção inválida. Execute novamente.")
            return
    
    print("\n🎉 SETUP CONCLUÍDO!")
    print("="*50)
    print("📝 PRÓXIMOS PASSOS:")
    print("   1. Abra o notebook nstech_recommendation_poc1.ipynb")
    print("   2. Configure USE_OCI = True/False na primeira célula")
    print("   3. Execute todas as células")
    print("   4. Aproveite as recomendações inteligentes! 🧠")

if __name__ == "__main__":
    main()
