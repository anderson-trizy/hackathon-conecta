# Estatísticas Detalhadas da Base de Dados

## nstech Hackathon - Grupo 10 - Tema 01

### 📊 Resumo Executivo

- **Data de criação**: 09 de agosto de 2025
- **Total de registros**: 200 clientes + 40 itens de portfólio + 130 produtos
- **Cobertura de produtos**: 100% (todos os produtos dos clientes existem na base)
- **Integridade dos dados**: 100% validada

---

## 🏢 Distribuição por Torre de Negócio

| Torre            | Clientes | Percentual | Principais Produtos        |
| ---------------- | -------- | ---------- | -------------------------- |
| Torre Embarcador | 76       | 38.0%      | YMS, TMS Embarcador, DMS   |
| Torre PME        | 74       | 37.0%      | TMS Pequeno/Micro, ERP     |
| Torre IM         | 25       | 12.5%      | Softwares para Seguradoras |
| Torre MG         | 19       | 9.5%       | TMS Médio/Grande, Agro     |
| Torre Mobilidade | 6        | 3.0%       | TMS Passageiros            |

---

## 📏 Distribuição por Porte Empresarial

| Porte   | Clientes | Percentual | Range MRR (R$)   |
| ------- | -------- | ---------- | ---------------- |
| Grande  | 68       | 34.0%      | 25.000 - 150.000 |
| Pequeno | 49       | 24.5%      | 800 - 5.000      |
| Médio   | 47       | 23.5%      | 5.000 - 25.000   |
| Micro   | 36       | 18.0%      | 280 - 800        |

---

## 👤 Distribuição por Persona

| Persona       | Clientes | Percentual | Torres Principais   |
| ------------- | -------- | ---------- | ------------------- |
| Embarcador    | 140      | 70.0%      | Embarcador, PME     |
| Transportador | 35       | 17.5%      | MG, PME, Mobilidade |
| Ressegurador  | 11       | 5.5%       | IM                  |
| Segurador     | 7        | 3.5%       | IM                  |
| Corretor      | 7        | 3.5%       | IM                  |

---

## 🏭 Distribuição Setorial Completa

| Setor                 | Clientes | Percentual |
| --------------------- | -------- | ---------- |
| Transporte Rodoviário | 27       | 13.5%      |
| Seguros               | 24       | 12.0%      |
| Varejo                | 21       | 10.5%      |
| Construção            | 21       | 10.5%      |
| Agronegócio           | 18       | 9.0%       |
| Combustíveis          | 17       | 8.5%       |
| Alimentos             | 17       | 8.5%       |
| E-commerce            | 14       | 7.0%       |
| Autopeças             | 14       | 7.0%       |
| Farmácia              | 10       | 5.0%       |
| Transporte Aéreo      | 4        | 2.0%       |
| Moda                  | 4        | 2.0%       |
| Cosméticos            | 3        | 1.5%       |
| Outros setores        | 6        | 3.0%       |

---

## 💰 Análise Financeira

### MRR por Porte

- **Micro**: Média R$ 450 (280 - 800)
- **Pequeno**: Média R$ 2.800 (800 - 5.000)
- **Médio**: Média R$ 12.500 (5.000 - 25.000)
- **Grande**: Média R$ 55.000 (25.000 - 150.000)

### Top 10 Clientes por MRR

1. Vale S.A. - R$ 120.000 (Mineração)
2. Cargill - R$ 95.000 (Agronegócio)
3. Ultrapar - R$ 92.000 (Combustíveis)
4. CSN - R$ 75.000 (Siderurgia)
5. Ambev - R$ 72.000 (Bebidas)
6. Carrefour Brasil - R$ 68.000 (Varejo)
7. Unilever Brasil - R$ 65.000 (Alimentos)
8. BRF S.A. - R$ 58.000 (Alimentos)
9. Suzano Papel - R$ 48.000 (Papel/Celulose)
10. JBS S.A. - R$ 45.000 (Agronegócio)

---

## 😊 Análise de Satisfação

### Distribuição de Scores

- **5.0**: 7 clientes (3.5%)
- **4.5-4.9**: 34 clientes (17.0%)
- **4.0-4.4**: 78 clientes (39.0%)
- **3.5-3.9**: 58 clientes (29.0%)
- **3.0-3.4**: 23 clientes (11.5%)

### Satisfação por Porte

- **Grande**: 4.12 (média)
- **Médio**: 4.01 (média)
- **Pequeno**: 3.91 (média)
- **Micro**: 3.87 (média)

---

## 📦 Análise de Produtos

### Produtos Mais Utilizados

1. **YMS**: 18 clientes
2. **TMS Embarcador**: 15 clientes
3. **Gestão de Entregas**: 12 clientes
4. **Monitoramento**: 11 clientes
5. **DMS Atacadista/Distribuidor**: 10 clientes

### Produtos por Torre

- **Torre Embarcador**: 67 produtos únicos
- **Torre PME**: 23 produtos únicos
- **Torre MG**: 21 produtos únicos
- **Torre IM**: 15 produtos únicos
- **Torre Mobilidade**: 6 produtos únicos

---

## 🎯 Insights para Recomendação

### Oportunidades de Cross-selling

- **YMS + TMS Embarcador**: Alta correlação (83% dos clientes YMS têm TMS)
- **Gestão de Entregas + Roteirizador**: Complementaridade natural
- **Seguradoras + Resseguros**: Potencial de upselling

### Segmentos de Alto Valor

- **Grandes Embarcadores**: MRR médio R$ 55K, alta adoção de YMS
- **Transportadores Médios/Grandes**: Foco em TMS + Monitoramento
- **PME Embarcadores**: Oportunidade em soluções simplificadas

### Padrões Temporais

- **Novos clientes** (< 12 meses): 18% da base
- **Clientes maduros** (> 60 meses): 31% da base
- **Maior satisfação**: Clientes com 36-60 meses de relacionamento

---

## ✅ Validações Técnicas

### Integridade dos Dados

- ✅ Todos os 200 clientes têm campos obrigatórios
- ✅ IDs sequenciais CLI001-CLI200 sem lacunas
- ✅ 100% dos produtos dos clientes existem na base
- ✅ MRRs dentro dos ranges esperados por porte
- ✅ Scores de satisfação válidos (3.0-5.0)

### Diversidade Representativa

- ✅ 20+ setores econômicos representados
- ✅ Distribuição equilibrada entre torres
- ✅ Casos edge incluídos (micro empresas, setores nicho)
- ✅ Variabilidade realística em tempo de relacionamento

---

_Relatório gerado automaticamente em 09/08/2025_
_Base validada e pronta para algoritmos de ML/AI_
