# Sistema de Recomendação - Microfrontend

Microfrontend desenvolvido com Vite + React + TypeScript + ShadUI para o sistema de recomendações de produtos.

## 🚀 Características

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: ShadUI/UI (Radix UI + Tailwind CSS)
- **Arquitetura**: Microfrontend (preparado para Module Federation)
- **API Integration**: Integração com API de recomendações

## 📁 Estrutura do Projeto

```
src/
├── components/
│   ├── ui/              # Componentes base do ShadUI
│   ├── RecommendationWidget.tsx  # Widget principal
│   └── ProductDetailModal.tsx    # Modal de detalhes
├── services/
│   └── recommendationService.ts  # Service para API
├── types/
│   └── recommendation.ts        # Tipos TypeScript
├── lib/
│   └── utils.ts                # Utilitários
└── index.css                   # Estilos globais
```

## 🔧 Instalação e Desenvolvimento

### Pré-requisitos

- Node.js 18+
- npm ou yarn

### Instalação

```bash
cd recommendation-microfrontend
npm install
```

### Desenvolvimento

```bash
npm run dev
```

O microfrontend estará disponível em: `http://localhost:3001`

### Build de Produção

```bash
npm run build
```

## 🔗 Uso

### Como Microfrontend Independente

Acesse: `http://localhost:3001?clientId=400`

### Parâmetros da URL

- `clientId`: ID do cliente para buscar recomendações (obrigatório)

### Exemplo de Integração

```html
<!-- Incorporar em outro site -->
<iframe
	src="http://localhost:3001?clientId=400"
	width="100%"
	height="800px"
></iframe>
```

## 📊 Funcionalidades

### Widget de Recomendações

- **Carregamento Dinâmico**: Busca recomendações via API
- **Cards Responsivos**: Layout adaptável para diferentes telas
- **Hover Effects**: Interações visuais nos cards
- **Loading States**: Estados de carregamento e erro
- **Badges**: Indicadores visuais de recomendação e score

### Modal de Detalhes

- **Abas Organizadas**: Visão Geral, Funcionalidades, Casos de Sucesso, Recursos
- **Informações Detalhadas**: Especificações técnicas, benefícios, stories
- **Ações**: Agendar reunião, solicitar demo, download de materiais
- **Design Responsivo**: Funciona em desktop e mobile

## 🎨 Design System

Utiliza o **Atlas Design System** baseado em:

- **ShadUI/UI**: Componentes acessíveis e personalizáveis
- **Radix UI**: Primitivos de componentes
- **Tailwind CSS**: Sistema de estilos utilitário
- **Lucide React**: Ícones consistentes

## 🔌 API Integration

### Endpoint Principal

```
GET http://127.0.0.1:8002/recommendations/{clientId}
```

### Estrutura de Resposta Esperada

```json
{
	"client_id": "400",
	"recommendations": [
		{
			"id": "prod-1",
			"name": "Nome do Produto",
			"description": "Descrição do produto",
			"score": 0.85,
			"category": "Categoria",
			"segment": "Segmento"
		}
	],
	"total_recommendations": 3,
	"status": "success"
}
```

## 🔮 Futuras Implementações

### Module Federation

- Configuração para Module Federation com Webpack
- Exposição de componentes para outros microfrontends
- Shared dependencies otimizadas

### Funcionalidades Adicionais

- Sistema de autenticação
- Personalização de tema por portal
- Analytics e tracking
- Cache de recomendações
- Filtros e ordenação avançada

## 🛠️ Desenvolvimento

### Comandos Disponíveis

```bash
npm run dev      # Modo desenvolvimento
npm run build    # Build de produção
npm run preview  # Preview do build
npm run lint     # Linting do código
```

### Variáveis de Ambiente

```env
# .env.local
VITE_API_BASE_URL=http://127.0.0.1:8002
```

## 🧪 Testes

```bash
# Adicionar futuramente
npm run test
npm run test:e2e
```

## 📝 Notas de Implementação

1. **API Mock**: Algumas informações são mockadas temporariamente (images, similarCompaniesCount, etc.)
2. **Error Handling**: Implementado tratamento básico de erros de API
3. **Loading States**: Estados de carregamento para melhor UX
4. **Responsive Design**: Funciona em desktop, tablet e mobile
5. **Accessibility**: Componentes seguem padrões de acessibilidade do Radix UI

## 🤝 Contribuição

1. Clone o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto é propriedade da NStech.
