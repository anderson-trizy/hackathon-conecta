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
    
    config_content = """[DEFAULT]
user=ocid1.user.oc1..your-user-id
fingerprint=your-fingerprint
key_file=~/.oci/private_key.pem
tenancy=ocid1.tenancy.oc1..your-tenancy-id
region=us-ashburn-1
compartment_id=ocid1.compartment.oc1..your-compartment-id

# 🔧 INSTRUÇÕES:
# 1. Substitua os valores acima pelos seus reais
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

def setup_local_environment():
    """Configura ambiente local"""
    print("🏠 CONFIGURANDO AMBIENTE LOCAL")
    print("="*40)
    
    # Dependências básicas
    basic_packages = [
        "pandas>=1.5.0",
        "numpy>=1.21.0", 
        "scikit-learn>=1.1.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0"
    ]
    
    print("📦 Instalando dependências básicas...")
    for package in basic_packages:
        install_package(package)
    
    print("\n✅ Ambiente local configurado com sucesso!")
    print("   Para usar: USE_OCI = False no notebook")

def setup_oci_environment():
    """Configura ambiente OCI"""
    print("☁️  CONFIGURANDO AMBIENTE OCI")
    print("="*40)
    
    # Dependências OCI
    oci_packages = [
        "oracle-ads",
        "oci",
        "oci-cli"
    ]
    
    print("📦 Instalando dependências OCI...")
    success = True
    for package in oci_packages:
        if not install_package(package):
            success = False
    
    if success:
        print("\n📄 Configurando credenciais OCI...")
        if check_oci_config():
            print("✅ Configuração OCI encontrada")
        else:
            create_sample_oci_config()
        
        print("\n✅ Ambiente OCI configurado com sucesso!")
        print("   Para usar: USE_OCI = True no notebook")
        print("   📝 Não esqueça de editar ~/.oci/config com suas credenciais!")
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
