# Job de Atualização do Airtable

Este diretório contém o job automatizado para extrair dados frescos do Airtable e gerar um datasource consolidado atualizado.

## 📁 Arquivos Principais

### `airtable_datasource_job.py` - **SCRIPT PRINCIPAL**

- ✅ Script completo e robusto para extração automática
- 📊 Extrai dados de 6 tabelas principais do Airtable
- 🔄 Consolida no formato padrão do `consolidated_datasource.json`
- 📝 Gera logs detalhados (`airtable_job.log`)
- 📤 **NOVO: Upload automático para OCI Object Storage**
- ⚡ Otimizado para execução periódica

### `upload_to_oci.py` - **UPLOAD PARA NUVEM**

- ☁️ Faz upload automático para OCI Object Storage
- 🪣 Usa bucket configurado no `.env` (nstech-recommendation-data)
- 📅 Cria versão com timestamp e versão "latest"
- 🔧 Configuração automática via SDK OCI
- 📊 Logs detalhados do processo de upload

### `run_complete_job.py` - **JOB COMPLETO**

- 🚀 Executa fluxo completo: Airtable → OCI
- 📤 Extração + Consolidação + Upload automático
- ⏰ Ideal para execução automatizada
- 📈 Relatório completo de execução

### Scripts de Execução:

- `run_airtable_job.py` - Wrapper Python (somente Airtable)
- `run_airtable_job.bat` - Script batch Windows (somente Airtable)
- `run_complete_job.py` - Job completo (Airtable + OCI)
- `run_complete_job.bat` - Script batch completo (Airtable + OCI)
- `upload_manual.py` - Upload manual para OCI

## 🚀 Como Executar

### Execução Manual (Somente Airtable):

```bash
cd servless
python airtable_datasource_job.py
```

### Execução Manual (Airtable + OCI Upload):

```bash
cd servless
python run_complete_job.py
```

### Upload Manual (apenas upload):

```bash
cd servless
python upload_manual.py
```

### Com Wrapper Python:

```bash
cd servless
python run_airtable_job.py
```

### Com Script Batch (Windows):

**Somente Airtable:**

```bash
cd servless
run_airtable_job.bat
```

**Job Completo (Airtable + OCI):**

```bash
cd servless
run_complete_job.bat
```

## ⏰ Agendamento Automático

### Usando Windows Task Scheduler:

1. **Abrir Task Scheduler**

   - Pressione `Win + R`, digite `taskschd.msc`

2. **Criar Tarefa Básica**

   - Action > Create Basic Task
   - Nome: "Airtable Datasource Update"
   - Descrição: "Atualiza datasource com dados frescos do Airtable"

3. **Configurar Trigger**

   - Frequency: Daily (ou conforme necessário)
   - Time: Horário desejado (ex: 02:00 AM)

4. **Configurar Action**

   - Action: Start a program
   - Program: `C:\Users\anderson.marcondes\Documents\dev\hackathon-conecta\servless\run_complete_job.bat`
   - Start in: `C:\Users\anderson.marcondes\Documents\dev\hackathon-conecta\servless`

   **Ou para somente Airtable (sem OCI):**

   - Program: `C:\Users\anderson.marcondes\Documents\dev\hackathon-conecta\servless\run_airtable_job.bat`
   - Start in: `C:\Users\anderson.marcondes\Documents\dev\hackathon-conecta\servless`

### Usando Cron (Linux/Mac):

```bash
# Executar job completo diariamente às 2:00 AM
0 2 * * * cd /path/to/servless && python run_complete_job.py

# Ou somente Airtable (sem OCI)
0 2 * * * cd /path/to/servless && python airtable_datasource_job.py
```

## 📊 Resultado

### Arquivos Gerados:

- **`consolidated_datasource_fresh.json`** - Datasource local atualizado
- **`oci_upload.log`** - Log dos uploads para OCI

### Arquivos na Nuvem (OCI Object Storage):

- **`datasources/consolidated_datasource_YYYYMMDD_HHMMSS.json`** - Versão com timestamp
- **`datasources/consolidated_datasource_latest.json`** - Última versão (sempre atualizada)

### Estrutura dos Dados:

- ✅ **40 Items do Portfólio**
- ✅ **130 Produtos** (com dados completos do Airtable)
- ✅ **100 Clientes** (com relacionamentos simulados)
- ✅ **~390 Relacionamentos** produto-cliente
- ✅ **Metadados** com timestamps e estatísticas

### Logs:

- **`airtable_job.log`** - Log detalhado das execuções do Airtable
- **`oci_upload.log`** - Log detalhado dos uploads para OCI
- **`airtable_job_history.log`** - Histórico de execuções (batch Airtable)
- **`complete_job_history.log`** - Histórico de execuções (batch completo)

## 🔧 Configuração

### Variáveis de Ambiente (.env):

```
# Airtable
AIRTABLE_BASEID=appmmRRZgZ3xSTwB6
AIRTABLE_TOKEN=seu_token_aqui

# OCI Object Storage
OCI_NAMESPACE=seu_namespace
OCI_BUCKET_RECOMMENDATION_NAME=nstech-recommendation-data
OCI_REGION=us-chicago-1
OCI_COMPARTMENT_ID=seu_compartment_id

# OCI Auth (opcionais)
OCI_CONFIG_FILE=~/.oci/config
OCI_CONFIG_PROFILE=DEFAULT
```

### Dependências:

```bash
pip install requests oci
```

## 📈 Monitoramento

### Verificar Execução:

1. **Logs**: Verificar `airtable_job.log` para detalhes
2. **Arquivo**: Verificar timestamp de `consolidated_datasource_fresh.json`
3. **Tamanho**: Arquivo deve ter ~190-300 KB

### Troubleshooting:

- ❌ **Erro de conexão**: Verificar token e base ID no .env
- ❌ **Erro de encoding**: Script já trata encoding UTF-8
- ❌ **Erro de permissão**: Executar com permissões adequadas

## 💡 Uso Recomendado

### Para Desenvolvimento:

- Execute manualmente quando precisar de dados frescos
- Use `run_airtable_job.py` para saída limpa

### Para Produção:

- Configure no Task Scheduler para execução diária/semanal
- Use `run_airtable_job.bat` para máxima compatibilidade
- Monitor logs regularmente

## 🔄 Fluxo do Job

1. **Carrega** variáveis de ambiente (.env)
2. **Conecta** com Airtable API
3. **Extrai** dados das 6 tabelas principais:
   - Produtos (130 registros)
   - Items do Portfólio (40 registros)
   - Torres (9 registros)
   - Clientes Estratégicos (433 registros)
   - Categorias de Produto (52 registros)
   - Mercados (9 registros)
4. **Consolida** dados seguindo estrutura padrão
5. **Gera** arquivo `consolidated_datasource_fresh.json`
6. **Log** estatísticas e tempo de execução

---

**⚡ Tempo de Execução**: ~20-30 segundos  
**📁 Tamanho Final**: ~200-300 KB  
**🔄 Frequência Recomendada**: Diário ou semanal
