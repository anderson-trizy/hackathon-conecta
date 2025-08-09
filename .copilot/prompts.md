# Prompts Específicos para o Projeto

## 1. Análise de Dados
```
Analise os arquivos Nstech.csv e Produtos.csv da nstech. Identifique:
- Estrutura hierárquica: Torres → Itens → Produtos
- Relacionamentos entre entidades
- Campos-chave para o sistema de recomendação
- Possíveis sobreposições de funcionalidades entre produtos

Contexto: Sistema de recomendação usando Oracle OCI para empresa com 120+ produtos
```

## 2. Geração de Dados de Clientes
```
Baseado na estrutura de Torres e Itens da nstech, crie um dataset fictício de clientes com:
- Diferentes tipos de transportadoras (pequeno, médio, grande porte)
- Segmentos variados (operadores logísticos, transportador FTL, etc.)
- Relacionamento cliente → produtos que faça sentido com a lógica de negócio
- Pelo menos 100 clientes fictícios para treinar o modelo

Use os nichos-alvo e produtos dos itens como referência para criar relacionamentos realistas.
```

## 3. Arquitetura Oracle OCI com Aderência Multicloud
```
Projete uma arquitetura usando serviços Oracle OCI que:
- Implemente o sistema de recomendação usando Oracle Functions
- Use abstrações/interfaces que permitam migração futura para outras clouds
- Documente equivalências: Oracle Functions ↔ AWS Lambda ↔ Azure Functions
- Separe lógica de negócio dos serviços específicos da Oracle
- Use padrões de design que facilitem a portabilidade

Serviços Oracle + Equivalências:
- Oracle Functions ↔ AWS Lambda ↔ Azure Functions
- OCI API Gateway ↔ AWS API Gateway ↔ Azure API Management
- OCI Object Storage ↔ AWS S3 ↔ Azure Blob Storage
- OCI Data Science ↔ AWS SageMaker ↔ Azure ML Studio

Criar interfaces abstratas para: Storage, ML Services, Serverless Functions
```

## 4. Algoritmo de Recomendação
```
Implemente um sistema de recomendação para a nstech usando Oracle OCI que:
- Use collaborative filtering baseado em similaridade de clientes
- Considere: tipo de empresa, segmento, tamanho, produtos já contratados
- Retorne top N produtos recomendados com score de confiança
- Seja eficiente para 120+ produtos e centenas de clientes

Exemplo: Cliente A e B são pequenas transportadoras, A tem produtos X,Y,Z do item "Serviços Financeiros", B tem apenas X,Y → recomendar Z para B
```

## 5. Oracle Function para Recomendação (Python)
```
Crie uma Oracle Function em Python que:
- Use o runtime Python 3.9+ do Oracle Functions
- Receba ID do cliente como parâmetro
- Execute o algoritmo de recomendação usando pandas/numpy
- Retorne JSON com produtos recomendados e scores
- Seja otimizada para cold start (imports mínimos)
- Use OCI SDK para acessar dados/modelos
- Integre com OCI API Gateway

Estrutura: func.py, requirements.txt, func.yaml
Endpoint via API Gateway: GET /recommend?client_id=123

Otimizações Python:
- Use imports condicionais quando possível
- Cache modelos/dados em variáveis globais
- Minimize dependências em requirements.txt
```

## 7. Padrão de Abstração Multicloud
```
Implemente um padrão de abstração que permita migração entre clouds:

1. **Interface de Storage**:
   - Atual: OCI Object Storage
   - Futuro: AWS S3, Azure Blob, GCP Cloud Storage

2. **Interface de ML**:
   - Atual: OCI Data Science + Generative AI
   - Futuro: AWS SageMaker, Azure ML, GCP Vertex AI

3. **Interface de Serverless**:
   - Atual: Oracle Functions
   - Futuro: AWS Lambda, Azure Functions, GCP Cloud Functions

4. **Interface de API Gateway**:
   - Atual: OCI API Gateway
   - Futuro: AWS API Gateway, Azure API Management

Estrutura sugerida:
```python
# interfaces/storage.py
class StorageInterface:
    def upload_data(self, data, path): pass
    def download_data(self, path): pass

# adapters/oci_storage.py
class OCIStorageAdapter(StorageInterface):
    # Implementação específica Oracle
```

Documentar mapeamento completo de migração Oracle → AWS/Azure/GCP
```

## 8. Roadmap Pós-Hackathon (Propostas Grupo 10)
```
Desenvolva propostas técnicas detalhadas para evoluções futuras:

### Análise de Sentimento Integrada
- Como integrar dados de NPS, CSAT, reviews de clientes
- Arquitetura para análise contínua de feedback usando OCI Language
- Pipeline para processar comentários e avaliar satisfação por produto
- Machine Learning para identificar padrões de satisfação por segmento
- Dashboard para acompanhar índices de recomendação vs satisfação

### Sistema de Preços Dinâmicos
- Integração com dados de mercado e concorrência
- Algoritmos de elasticidade de preços por segmento de cliente
- Recomendações de produtos considerando margem vs competitividade
- Análise de bundles/pacotes com maior valor percebido
- A/B testing para validar estratégias de pricing

### Arquitetura Evolutiva
- Como expandir a Oracle Function atual para suportar essas funcionalidades
- Novos serviços OCI necessários (Document AI, Vision, etc.)
- Estratégia de dados para capturar feedback em tempo real
- Integração com sistemas CRM/ERP da nstech

Contexto: Apresentar roadmap técnico convincente para continuidade pós-hackathon
```
```
Desenvolva propostas técnicas detalhadas para evoluções futuras:

### Análise de Sentimento Integrada
- Como integrar dados de NPS, CSAT, reviews de clientes
- Arquitetura para análise contínua de feedback usando OCI Language
- Pipeline para processar comentários e avaliar satisfação por produto
- Machine Learning para identificar padrões de satisfação por segmento
- Dashboard para acompanhar índices de recomendação vs satisfação

### Sistema de Preços Dinâmicos
- Integração com dados de mercado e concorrência
- Algoritmos de elasticidade de preços por segmento de cliente
- Recomendações de produtos considerando margem vs competitividade
- Análise de bundles/pacotes com maior valor percebido
- A/B testing para validar estratégias de pricing

### Arquitetura Evolutiva
- Como expandir a Oracle Function atual para suportar essas funcionalidades
- Novos serviços OCI necessários (Document AI, Vision, etc.)
- Estratégia de dados para capturar feedback em tempo real
- Integração com sistemas CRM/ERP da nstech

Contexto: Apresentar roadmap técnico convincente para continuidade pós-hackathon
```
```
Implemente um padrão de abstração que permita migração entre clouds:

1. **Interface de Storage**:
   - Atual: OCI Object Storage
   - Futuro: AWS S3, Azure Blob, GCP Cloud Storage

2. **Interface de ML**:
   - Atual: OCI Data Science + Generative AI
   - Futuro: AWS SageMaker, Azure ML, GCP Vertex AI

3. **Interface de Serverless**:
   - Atual: Oracle Functions
   - Futuro: AWS Lambda, Azure Functions, GCP Cloud Functions

4. **Interface de API Gateway**:
   - Atual: OCI API Gateway
   - Futuro: AWS API Gateway, Azure API Management

Estrutura sugerida:
```python
# interfaces/storage.py
class StorageInterface:
    def upload_data(self, data, path): pass
    def download_data(self, path): pass

# adapters/oci_storage.py
class OCIStorageAdapter(StorageInterface):
    # Implementação específica Oracle
```

Documentar mapeamento completo de migração Oracle → AWS/Azure/GCP
```
