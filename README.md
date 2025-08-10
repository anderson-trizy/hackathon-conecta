# nstech Hackathon - Grupo 10 - Tema 01
## Módulo de Recomendação para nsApps

### Descrição do Projeto
Sistema de recomendação de produtos para o portal nsApps da nstech, utilizando recursos de AI da Oracle Cloud Infrastructure (OCI).

### Objetivo
Desenvolver um módulo que recomende produtos aos clientes baseado em:
- Tipo de cliente
- Persona
- Segmento de atuação
- Tamanho da empresa
- Produtos já utilizados por empresas similares

### Estrutura do Projeto
```
.
├── data/                   # Dados consolidados e estruturados do Airtable (Nstech.csv, Produtos.csv)
│   └── consolidated_datasource.json  # Base principal com 200 clientes
├── STATISTICS.md           # Estatísticas detalhadas da base de dados
└── .copilot/              # Instruções e prompts específicos para o Copilot
```

*Outras pastas serão criadas conforme o desenvolvimento avançar.*

### 📊 Base de Dados Consolidada

**Resumo Executivo:**
- **200 clientes fictícios** representativos do mercado nstech
- **40 itens de portfólio** organizados por torre de negócio  
- **130 produtos reais** mapeados com MRR e classificação BCG
- **100% de cobertura** - todos os produtos dos clientes existem na base
- **Validação completa** de integridade e consistência dos dados

**Distribuição Equilibrada:**
- 5 torres de negócio (Embarcador 38%, PME 37%, IM 12.5%, MG 9.5%, Mobilidade 3%)
- 4 portes empresariais (Grande 34%, Pequeno 24.5%, Médio 23.5%, Micro 18%)
- 20+ setores econômicos representados
- Score médio de satisfação: 3.98/5.0

> 📋 **Estatísticas completas disponíveis em [STATISTICS.md](./STATISTICS.md)**

### 🎯 Casos de Uso para Recomendação

#### **Análise de Similaridade:**
- Clientes com perfis similares (porte + setor + persona)
- Identificação de padrões de adoção de produtos
- Segmentação inteligente por comportamento

#### **Cross-selling Inteligente:**
- Produtos complementares baseados no portfólio atual
- Recomendações por torre de negócio
- Upgrade de produtos por evolução do cliente

#### **Targeting Personalizado:**
- Recomendações específicas por persona
- Adequação de produtos ao porte da empresa
- Oportunidades baseadas em satisfação e tempo de relacionamento

### Tecnologias e Arquitetura
**Implementação Atual (Hackathon):**
- **OCI Data Science**: Notebooks Jupyter, model training/deployment, ADS SDK
- **OCI ML Applications**: Empacotamento e deployment escalável de modelos ML
- **Oracle Functions**: Serverless Python runtime para lógica de negócio customizada
- **OCI Generative AI**: Text embeddings e análise semântica de produtos
- **OCI API Gateway**: Exposição e gerenciamento da API
- **OCI Object Storage**: Dados, modelos e logs
- **OCI Monitoring/Logging**: Observabilidade completa

**Abordagem Multicloud:**
- Arquitetura com abstrações que permitem migração futura
- Padrão Adapter para diferentes provedores de cloud
- Separação entre lógica de negócio e serviços de infraestrutura
- Documentação de equivalências (Oracle ↔ AWS ↔ Azure ↔ GCP)

### Etapas de Desenvolvimento
1. ✅ **Inicialização do projeto e estrutura multicloud**
   - Configuração da arquitetura com abstrações para múltiplos clouds
   - Documentação de equivalências Oracle ↔ AWS ↔ Azure ↔ GCP

2. ✅ **Análise e estruturação dos dados**
   - Consolidação de dados Airtable (Nstech.csv + Produtos.csv)
   - Estruturação de 40 itens de portfólio e 130 produtos reais
   - Enriquecimento com screenshots e dados contextuais
   - Criação de processos funcionais e nichos de mercado

3. ✅ **Criação de base de clientes diversificada**
   - Geração de 200 clientes fictícios representativos
   - Distribuição equilibrada por torres, portes e setores
   - Mapeamento correto com produtos reais da base
   - Validação completa de consistência e qualidade

4. ⏳ **POC 1: Sistema de recomendação em notebook (OCI Data Science)**
   - Algoritmos de similaridade entre clientes
   - Análise de padrões de adoção de produtos
   - Matriz de recomendações baseada em ML

5. ⏳ **POC 2: API híbrida com ML Applications + Oracle Functions**
   - ML Applications: API de similaridade e scoring de produtos
   - Oracle Functions: Lógica de negócio e regras customizadas
   - Integração com OCI Generative AI para embeddings
   - Testes de performance e escalabilidade

6. ⏳ **Deploy completo na OCI com documentação de migração**
   - Pipeline CI/CD completo
   - Monitoramento e observabilidade
   - Guias de migração para outros clouds

### Equipe
- **Grupo 10** - nstech Hackathon
- **Tema**: Módulo de recomendação para nsApps
- **Parceria**: Oracle

---
**Data de início**: 08 de agosto de 2025
