# Instruções para o GitHub Copilot - nstech Hackathon

## Contexto do Projeto
Você está trabalhando no desenvolvimento de um sistema de recomendação de produtos para a nstech, uma empresa com mais de 120 produtos organizados em Torres e Itens.

## Diretrizes Específicas

### 1. Arquitetura de Dados
- **Fonte principal**: Dados do Airtable (exportados como CSV)
- **Estrutura**: Torres → Itens → Produtos
- **Relacionamentos**: Clientes → Produtos (baseado em similaridade)

### 2. Tecnologias e Arquitetura
- **Cloud Atual**: Oracle Cloud Infrastructure (OCI) obrigatório para o hackathon
- **AI/ML**: Sempre priorizar serviços Oracle OCI:
  - OCI Data Science
  - OCI ML Applications
  - OCI Generative AI
  - OCI Generative AI Agents
- **Compute**: Oracle Functions (Serverless) - **Python runtime**
- **API**: OCI API Gateway + Oracle Functions
- **Linguagem**: Python (consistência entre notebooks e functions)

**IMPORTANTE - Arquitetura Multicloud:**
- Usar padrões de abstração que permitam migração entre clouds
- Implementar interfaces/adapters para serviços específicos da Oracle
- Documentar equivalências com AWS, Azure, GCP para facilitar migração futura
- Separar lógica de negócio dos serviços de infraestrutura

### 3. Padrões de Desenvolvimento
- **Git**: Conventional Commits
- **Branch principal**: main
- **Estrutura**: Seguir a organização de pastas definida
- **Documentação**: Sempre documentar decisões técnicas

### 4. Sistema de Recomendação

#### 4.1 Implementação Hackathon (Escopo Atual)
- **Algoritmo Principal**: Collaborative Filtering baseado em similaridade entre empresas
- **Abordagem Complementar**: Content-Based Filtering usando características dos produtos/torres
- **Critérios**: Tipo de empresa, segmento, tamanho, produtos já contratados
- **Output**: Lista de produtos recomendados com score de confiança
- **Dados**: Baseado em dados fictícios estruturados do portfólio nstech

#### 4.2 Roadmap Pós-Hackathon (Propostas do Grupo 10)
- **Análise de Sentimento**: 
  - Integração com dados de NPS, CSAT, reviews de clientes
  - Usar OCI Language ou OCI Generative AI para análise de feedback
  - Priorizar produtos com melhor índice de satisfação nas recomendações
  - Analisar comentários sobre concorrentes para positioning

- **Otimização de Preços Dinâmicos**:
  - Sugerir pacotes de produtos com preços otimizados
  - Análise de elasticidade de preços por segmento
  - Recomendações baseadas em margem e competitividade
  - Integração com dados de mercado e concorrência

### 5. Dados de Clientes
- Como não temos dados reais de clientes, criar dados fictícios que façam sentido com:
  - Os itens do portfólio
  - As torres existentes
  - A lógica de negócio da nstech

## Exemplos de Uso

### Prompt para geração de dados:
"Crie dados fictícios de clientes que façam sentido com a estrutura de Torres e Itens da nstech, considerando diferentes tipos de transportadoras"

### Prompt para algoritmo:
"Implemente um algoritmo de recomendação usando serviços Oracle OCI que sugira produtos baseado em empresas similares"

## Restrições e Boas Práticas
- ❌ **Para o hackathon**: Não usar serviços de outras clouds (AWS, Azure, GCP)
- ❌ Não implementar algoritmos complexos do zero se existir serviço Oracle equivalente
- ✅ **Multicloud**: Implementar abstrações que permitam migração futura entre clouds
- ✅ Sempre documentar qual serviço Oracle está sendo usado e por quê
- ✅ Documentar equivalências com outros clouds (AWS Lambda ↔ Oracle Functions)
- ✅ Prever fácil troca da fonte de dados (Airtable API no futuro)
- ✅ Separar lógica de negócio da implementação específica da Oracle
