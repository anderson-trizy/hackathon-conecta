# Datasources Essenciais - Hackathon Conecta ✨

## 📁 Estrutura Otimizada (6.5 MB - 10 arquivos essenciais)

### **📊 Datasources** (`datasources/`)

- `consolidated_datasource_enriquecido.json` - **DATASOURCE PRINCIPAL** com 2,755 clientes + 130 produtos do Airtable (1.3 MB)

### **🗂️ JSON Exports** (`json_exports/`)

**🎯 Arquivos Principais para o Hackathon:**

- `produtos_clean.json` - **ARQUIVO PRINCIPAL** - 130 produtos com campos essenciais para ML (26 KB)
- `clientes.json` - 2,755 clientes estruturados com IDs relacionais (287 KB)

**📊 Dados Completos:**

- `airtable_todos_produtos.json` - 130 produtos completos do Airtable com 116 campos cada (4.8 MB)

**🔗 Dados Estruturados:**

- `personas.json` - 7 personas únicas do sistema
- `torres.json` - 8 torres únicas do sistema
- `itens_portfolio.json` - 40 itens do portfólio com classificações

### **🔧 Scripts Essenciais** (`scripts/`)

- `buscar_todos_produtos_airtable.py` - Busca todos os 130 produtos do Airtable (7 KB)
- `enriquecer_datasource_airtable.py` - Enriquece datasource com dados do Airtable (13 KB)
- `gerar_produtos_clean.py` - Gera JSON limpo com campos essenciais (2 KB)

### **📥 Raw Data** (`raw/`)

- `Nstech.csv`, `Produtos.csv`, `ClientexProduto_Embarcador.csv` - Dados originais (91 KB)

## 🎯 Como Usar

### Para Sistema de Recomendação (ML)

```json
// Use: json_exports/produtos_clean.json
[
	{
		"airtable_id": "recoxWFftbDV8rJ2j",
		"nome": "Trizy - TSM",
		"quantidade_clientes": 91,
		"classificacao_bcg": "Growth",
		"is_produto_alvo": 1,
		"torre_id": 1
	}
]
```

### Para Análise de Clientes

```json
// Use: json_exports/clientes.json
[
	{
		"id": 1,
		"nome": "Cliente XYZ",
		"persona_id": 2,
		"torre_id": 1
	}
]
```

### Regenerar Dados (se necessário)

```bash
cd scripts
python buscar_todos_produtos_airtable.py  # Buscar do Airtable
python enriquecer_datasource_airtable.py  # Enriquecer datasource
python gerar_produtos_clean.py           # Gerar lista limpa
```

## 📊 Estatísticas dos Dados

### **Produtos (130 total)**

- **Produtos-alvo**: 64 (49.2%)
- **Classificação BCG**: Migrar (39.2%), Growth (31.5%), MVP (8.5%)
- **Por Torre**: Torre Embarcador (33.1%), Torre VGR (18.5%), Torre PME (15.4%)

### **Clientes (2,755 total)**

- **Por Torre**: Torre Embarcador (88.1%), Torre IM (6.1%), Torre PME (4.7%)
- **Por Persona**: Embarcador (88.2%), Seguradora (6.0%), Transportador Pequeno (4.3%)

### **Airtable Integration**

- **Base**: Portfolio (appmmRRZgZ3xSTwB6)
- **Total MRR**: R$ 87.8M
- **Cobertura**: 100% Airtable ID, 99.2% Produto-alvo, 96.2% Estágio

## 🔗 Mapeamento de IDs

### Torres (torre_id)

1. Torre Embarcador | 2. Torre Fintech | 3. Torre IM | 4. Torre MG
2. Torre Mobilidade | 6. Torre PME | 7. Torre Plataforma | 8. Torre VGR

### Personas (persona_id)

1. Corretor | 2. Embarcador | 3. Ressegurador | 4. Seguradora
2. Transportador | 6. Transportador M/G | 7. Transportador Pequeno

## 🚀 Status do Projeto

**Versão 4.1.0 - OTIMIZADO** (Agosto 2025)

- ✅ **6.7 MB removidos** (13.2 MB → 6.5 MB)
- ✅ **20 arquivos removidos** - mantidos apenas essenciais
- ✅ **Integração Airtable completa**
- ✅ **Dados prontos para ML**
- ✅ **Sistema de recomendação pronto**

---

_Estrutura otimizada para máxima performance no hackathon_ 🏆
