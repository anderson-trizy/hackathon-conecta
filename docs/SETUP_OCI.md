# 🔧 Setup Completo - Oracle Cloud Infrastructure (OCI)

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Criação de Conta OCI](#criação-de-conta-oci)
3. [Configuração Inicial](#configuração-inicial)
4. [Criação do Compartment](#criação-do-compartment)
5. [Configuração de Rede (VCN)](#configuração-de-rede-vcn)
6. [Configuração de Dynamic Group](#configuração-de-dynamic-group)
7. [Configuração de Políticas](#configuração-de-políticas)
8. [Setup do Data Science](#setup-do-data-science)
9. [Configuração de Chaves API](#configuração-de-chaves-api)
10. [Configuração do Ambiente Local](#configuração-do-ambiente-local)
11. [Teste da Conexão](#teste-da-conexão)
12. [Troubleshooting](#troubleshooting)

---

## 🎯 Pré-requisitos

### Software Necessário

- Python 3.8+ instalado
- Git instalado
- Navegador web atualizado
- Editor de texto/IDE (VSCode recomendado)

### Conhecimentos Básicos

- Conceitos básicos de cloud computing
- Noções de Python
- Familiaridade com terminal/prompt de comando

---

## 🌐 Criação de Conta OCI

### 1. Acesso ao Oracle Cloud

1. Acesse: https://www.oracle.com/cloud/free/
2. Clique em **"Start for free"**
3. Preencha os dados pessoais:
   - Nome completo
   - Email válido
   - País/região
   - Telefone

### 2. Verificação da Conta

1. Confirme o email recebido
2. Complete a verificação por SMS
3. Adicione cartão de crédito (não será cobrado no tier gratuito)

### 3. Primeiro Acesso

1. Faça login no console OCI
2. Anote as informações importantes:
   - **Tenancy OCID**
   - **Region** (ex: us-ashburn-1)
   - **Username** (seu email)

---

## ⚙️ Configuração Inicial

### 1. Navegação no Console

1. Acesse o **OCI Console**: https://cloud.oracle.com/
2. Faça login com suas credenciais
3. Familiarize-se com o menu lateral:
   - **Identity & Security**
   - **Analytics & AI**
   - **Compute**
   - **Storage**

### 2. Verificação de Limites

1. Vá em **Governance & Administration** → **Limits, Quotas and Usage**
2. Verifique os limites disponíveis para:
   - Data Science
   - Compute Instances
   - Block Storage

---

## 📁 Criação do Compartment

### 1. Acesso à Gestão de Compartments

1. No menu lateral: **Identity & Security** → **Compartments**
2. Clique em **"Create Compartment"**

### 2. Configuração do Compartment

```
Name: hackathon-conecta-nstech-2025
Description: Compartment for NStech Hackathon 2025 - ML Recommendation System
Parent Compartment: (root)
```

### 3. Validação

1. Anote o **Compartment OCID** gerado
2. Verifique se o compartment aparece na lista

---

## 🌐 Configuração de Rede (VCN)

### 1. Criação de VCN e Subnet

1. Vá em **Networking** → **Virtual Cloud Networks**
2. Clique em **"Start VCN Wizard"**
3. Selecione **"VCN with Internet Connectivity"**
4. Configure:

```
VCN Name: hackathon-vcn
Compartment: hackathon-conecta-nstech-2025
VCN CIDR Block: 10.0.0.0/16
Public Subnet CIDR Block: 10.0.0.0/24
Private Subnet CIDR Block: 10.0.1.0/24
```

> **⚠️ IMPORTANTE**: Se você receber erro de "CIDR overlaps", isso significa que já existe uma VCN/subnet com esse range. Use CIDRs alternativos:
>
> - **Opção 1**: `10.1.0.0/16` (público: `10.1.0.0/24`, privado: `10.1.1.0/24`)
> - **Opção 2**: `10.2.0.0/16` (público: `10.2.0.0/24`, privado: `10.2.1.0/24`)
> - **Opção 3**: `172.16.0.0/16` (público: `172.16.0.0/24`, privado: `172.16.1.0/24`)

5. Clique em **"Next"** e depois **"Create"**

> **💡 Nota**: O "Networking Quickstart" automaticamente cria a subnet **privada** com um NAT gateway, que é necessária para o Data Science.

---

## 👥 Configuração de Dynamic Group

### 1. Criação do Dynamic Group

1. Vá em **Identity & Security** → **Dynamic Groups**
2. Clique em **"Create Dynamic Group"**
3. Configure:

```
Name: hackathon-datascience-dynamic-group
Description: Dynamic group for Data Science notebook sessions
Compartment: (root)

Matching Rules:
ALL {resource.type = 'datasciencenotebooksession'}
```

> **💡 Explicação**: Dynamic Groups permitem que recursos do OCI (como notebook sessions) assumam identidades e executem ações automaticamente.

---

## 🔐 Configuração de Políticas

### 1. Criação de Política para Data Science

1. Vá em **Identity & Security** → **Policies**
2. Clique em **"Create Policy"**
3. Configure:

```
Name: hackathon-data-science-policy
Description: Policies for Data Science in hackathon compartment
Compartment: (root) ⚠️ IMPORTANTE: Criar no ROOT, mas a política gerencia o compartment filho

Policy Statements:
# Service Policies (obrigatórias)
allow service datascience to use virtual-network-family in tenancy

# Dynamic Group Policies (obrigatórias)
allow dynamic-group hackathon-datascience-dynamic-group to manage data-science-family in tenancy

# User/Administrator Policies
allow group Administrators to manage data-science-family in compartment hackathon-conecta-nstech-2025
allow group Administrators to manage virtual-network-family in compartment hackathon-conecta-nstech-2025
allow group Administrators to manage compute-management-family in compartment hackathon-conecta-nstech-2025
```

> **💡 Explicação**: As políticas devem ser criadas no compartment **root** (tenancy), mas elas concedem permissões para trabalhar **dentro** do compartment `hackathon-conecta-nstech-2025`. Isso é uma prática padrão do OCI.

### 2. Política para Object Storage

```
Name: hackathon-storage-policy
Description: Storage policies for hackathon project
Compartment: (root) ⚠️ IMPORTANTE: Criar no ROOT também

Policy Statements:
allow group Administrators to manage buckets in compartment hackathon-conecta-nstech-2025
allow group Administrators to manage objects in compartment hackathon-conecta-nstech-2025
```

### 📝 Resumo sobre Políticas:

- **Onde criar**: Sempre no compartment **root** (tenancy)
- **O que fazem**: Concedem permissões para trabalhar nos compartments filhos
- **Por que assim**: É o design padrão do OCI - políticas "cascateiam" do root para baixo

### 🔍 Políticas Obrigatórias para Data Science:

1. **Service Policies**: Permitem que o serviço Data Science use a rede
2. **Dynamic Group Policies**: Permitem que notebook sessions executem operações
3. **User Policies**: Permitem que usuários criem e gerenciem recursos

---

## 🧪 Setup do Data Science

### 1. Criação do Projeto Data Science

1. Vá em **Analytics & AI** → **Data Science**
2. Clique em **"Create Project"**
3. Configure:

```
Name: nstech-recommendation-system
Description: ML recommendation system for NStech hackathon
Compartment: hackathon-conecta-nstech-2025
```

### 2. Criação do Notebook Session

1. Dentro do projeto, clique em **"Create Notebook Session"**
2. Configure:

```
Name: nstech-ml-notebook
Compute Shape: VM.Standard2.1 (Always Free eligible)
Block Storage: 50 GB
Compartment: hackathon-conecta-nstech-2025
Subnet: Selecione a subnet PRIVADA criada (hackathon-vcn-private-subnet)
```

> **⚠️ IMPORTANTE**: Use sempre a **subnet privada** para notebook sessions. A subnet pública não funcionará corretamente para Data Science.

### 3. Aguarde a Criação

- Status deve mudar para **"Active"**
- Pode levar 5-10 minutos

---

## 🔑 Configuração de Chaves API

### 1. Geração de Chaves

1. Vá em **Profile** (canto superior direito) → **User Settings**
2. No menu lateral: **API Keys**
3. Clique em **"Add API Key"**
4. Selecione **"Generate API Key Pair"**
5. **IMPORTANTE**: Baixe a chave privada (.pem)

### 2. Configuração Local

1. Crie a pasta para configuração:

```bash
mkdir %USERPROFILE%\.oci
```

2. Crie o arquivo `config` em `%USERPROFILE%\.oci\config`:

```ini
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaxxxxx
fingerprint=xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx
tenancy=ocid1.tenancy.oc1..aaaaaaaxxxxx
region=us-ashburn-1
key_file=C:\Users\SEU_USUARIO\.oci\oci_api_key.pem
```

3. Mova a chave privada para: `%USERPROFILE%\.oci\oci_api_key.pem`

### 3. Obtenção dos OCIDs

- **User OCID**: Profile → User Settings → User Information
- **Tenancy OCID**: Profile → Tenancy Information
- **Fingerprint**: Será mostrado após adicionar a API Key

---

## 💻 Configuração do Ambiente Local

### 1. Instalação do OCI SDK

```bash
pip install oci
pip install ads
pip install oracle-ads[notebook]
```

### 2. Instalação de Dependências Adicionais

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
pip install jupyter notebook
pip install python-dotenv
```

### 3. Criação do Arquivo de Configuração

Crie `.env` na raiz do projeto:

```env
# OCI Configuration
OCI_CONFIG_PROFILE=DEFAULT
OCI_COMPARTMENT_ID=ocid1.compartment.oc1..aaaaaaaxxxxx
OCI_PROJECT_ID=ocid1.datascienceproject.oc1..aaaaaaaxxxxx
OCI_REGION=us-chicago-1

# Local Development
LOCAL_MODE=true
DATA_PATH=./data/
```

---

## 🧪 Teste da Conexão

### 1. Teste Básico do OCI SDK

Crie um arquivo `test_oci_connection.py`:

```python
import oci
from oci.config import from_file

try:
    # Carrega configuração
    config = from_file()

    # Testa conexão com Identity Service
    identity = oci.identity.IdentityClient(config)

    # Lista compartments
    compartments = identity.list_compartments(
        config['tenancy'],
        compartment_id_in_subtree=True
    )

    print("✅ Conexão OCI estabelecida com sucesso!")
    print(f"Compartments encontrados: {len(compartments.data)}")

    # Procura nosso compartment
    for comp in compartments.data:
        if 'hackathon' in comp.name.lower():
            print(f"📁 Compartment encontrado: {comp.name}")
            print(f"   OCID: {comp.id}")

except Exception as e:
    print(f"❌ Erro na conexão: {str(e)}")
    print("Verifique sua configuração em ~/.oci/config")
```

Execute:

```bash
python test_oci_connection.py
```

### 2. Teste do Data Science

```python
import ads
import os
import oci
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configura autenticação
ads.set_auth(auth='api_key', oci_config_location='~/.oci/config')

try:
    # Lista projetos Data Science
    from oci.data_science import DataScienceClient

    config = oci.config.from_file()
    ds_client = DataScienceClient(config)

    projects = ds_client.list_projects(
        compartment_id=os.getenv('OCI_COMPARTMENT_ID')
    )

    print("✅ Data Science conectado com sucesso!")
    print(f"Projetos encontrados: {len(projects.data)}")

except Exception as e:
    print(f"❌ Erro no Data Science: {str(e)}")
```

---

## 🛠️ Troubleshooting

### Problemas Comuns

#### 1. "Authentication failed"

**Causa**: Configuração incorreta de API Keys
**Solução**:

- Verifique se o arquivo `~/.oci/config` está correto
- Confirme se a chave privada está no local indicado
- Valide se o fingerprint está correto

#### 2. "Compartment not found"

**Causa**: OCID do compartment incorreto
**Solução**:

- Vá no console OCI → Compartments
- Copie o OCID correto do compartment criado
- Atualize o arquivo `.env`

#### 3. "Permission denied"

**Causa**: Políticas insuficientes
**Solução**:

- Verifique se as políticas foram criadas corretamente
- Aguarde alguns minutos para propagação
- Confirme se seu usuário tem as permissões necessárias

#### 4. "Service not available in region"

**Causa**: Serviço não disponível na região selecionada
**Solução**:

- Verifique se Data Science está disponível na sua região
- Considere mudar para região com mais serviços (us-ashburn-1)

#### 5. "CIDR overlaps" ao criar VCN/Subnet

**Causa**: Já existe uma VCN ou subnet com o mesmo range de IP
**Solução**:

- Use um CIDR diferente para a nova VCN
- **Opções recomendadas**:
  - `10.1.0.0/16` com subnets `10.1.0.0/24` e `10.1.1.0/24`
  - `10.2.0.0/16` com subnets `10.2.0.0/24` e `10.2.1.0/24`
  - `172.16.0.0/16` com subnets `172.16.0.0/24` e `172.16.1.0/24`
- Para verificar CIDRs existentes: **Networking** → **Virtual Cloud Networks** → liste suas VCNs existentes

#### 6. "Cannot create subnet in public subnet"

**Causa**: Tentativa de criar notebook session em subnet pública
**Solução**:

- Use sempre a **subnet privada** para Data Science
- Verifique se o nome da subnet contém "private" ou "priv"

### Comandos de Diagnóstico

#### Verificar Configuração OCI

```bash
python -c "import oci; print(oci.config.from_file())"
```

#### Listar Regiões Disponíveis

```python
import oci
config = oci.config.from_file()
identity = oci.identity.IdentityClient(config)
regions = identity.list_regions()
for region in regions.data:
    print(f"Region: {region.name} - {region.key}")
```

#### Verificar Limites de Serviço

```python
import oci
config = oci.config.from_file()
limits = oci.limits.LimitsClient(config)
# Lista limites do Data Science
```

---

## 📚 Recursos Adicionais

### Documentação Oficial

- [OCI Documentation](https://docs.oracle.com/en-us/iaas/)
- [Data Science Service](https://docs.oracle.com/en-us/iaas/data-science/)
- [OCI Python SDK](https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/)

### Tutoriais Úteis

- [Getting Started with OCI Data Science](https://docs.oracle.com/en-us/iaas/data-science/using/get-started.htm)
- [OCI Free Tier](https://www.oracle.com/cloud/free/)

### Suporte

- [OCI Community](https://community.oracle.com/hub/)
- [GitHub Issues](https://github.com/oracle/oci-python-sdk/issues)

---

## ✅ Checklist Final

Antes de prosseguir para o desenvolvimento:

### Configuração de Infraestrutura:

- [ ] Conta OCI criada e verificada
- [ ] Compartment `hackathon-conecta-nstech-2025` criado
- [ ] **VCN criada com subnet privada** (obrigatório)
- [ ] **Dynamic Group criado** (obrigatório)
- [ ] **Políticas configuradas corretamente** (service + dynamic group + user)
- [ ] Projeto Data Science criado

### Configuração de Acesso:

- [ ] API Keys geradas e configuradas
- [ ] Arquivo `~/.oci/config` configurado
- [ ] OCI SDK instalado localmente
- [ ] Teste de conexão executado com sucesso
- [ ] Arquivo `.env` configurado no projeto

### Configuração de Notebook (Opcional para desenvolvimento local):

- [ ] Data Science Notebook Session criada
- [ ] Notebook Session em status "Active"

**🎉 Setup OCI Completo!**

Agora você está pronto para desenvolver e executar o sistema de recomendação tanto localmente quanto no ambiente OCI.
