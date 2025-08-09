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
├── data/                   # Dados do Airtable (Nstech.csv, Produtos.csv)
└── .copilot/              # Instruções e prompts específicos para o Copilot
```

*Outras pastas serão criadas conforme o desenvolvimento avançar.*

### Tecnologias e Arquitetura
**Implementação Atual (Hackathon):**
- Oracle Cloud Infrastructure (OCI)
- Oracle Functions (Serverless)
- OCI Data Science
- OCI Machine Learning Applications
- OCI Generative AI Services
- OCI API Gateway
- Python

**Abordagem Multicloud:**
- Arquitetura com abstrações que permitem migração futura
- Padrão Adapter para diferentes provedores de cloud
- Separação entre lógica de negócio e serviços de infraestrutura
- Documentação de equivalências (Oracle ↔ AWS ↔ Azure ↔ GCP)

### Etapas de Desenvolvimento
1. ✅ Inicialização do projeto e estrutura multicloud
2. ⏳ Análise e estruturação dos dados
3. ⏳ Criação de dados fictícios de clientes
4. ⏳ POC 1: Sistema de recomendação em notebook (OCI Data Science)
5. ⏳ POC 2: Oracle Function com abstração multicloud
6. ⏳ Deploy completo na OCI com documentação de migração

### Equipe
- **Grupo 10** - nstech Hackathon
- **Tema**: Módulo de recomendação para nsApps
- **Parceria**: Oracle

---
**Data de início**: 08 de agosto de 2025
