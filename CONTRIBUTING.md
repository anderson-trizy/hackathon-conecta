# 🤝 Guia de Contribuição

## 🌿 Estratégia de Branches

### Estrutura Principal
- **`main`** - Código sempre estável, pronto para demonstrações
- **`develop`** - Branch de integração, trabalho ativo do time
- **`feature/*`** - Desenvolvimento de funcionalidades específicas
- **`hotfix/*`** - Correções urgentes em produção
- **`release/*`** - Preparação de versões para produção

### Workflow Recomendado

#### 1. Desenvolvendo Nova Feature
```bash
# Partir sempre da develop atualizada
git checkout develop
git pull origin develop

# Criar branch da feature
git checkout -b feature/nome-descritivo

# Desenvolver e commitar
git add .
git commit -m "feat: implementa funcionalidade X"

# Push e criar Pull Request
git push origin feature/nome-descritivo
# Abrir PR: feature/nome-descritivo → develop
```

#### 2. Correção de Bug Crítico
```bash
# Partir da main para hotfixes
git checkout main
git pull origin main

# Criar branch de hotfix
git checkout -b hotfix/nome-do-bug

# Corrigir e commitar
git add .
git commit -m "fix: corrige bug crítico X"

# Push e PR para main E develop
git push origin hotfix/nome-do-bug
# PR 1: hotfix/nome-do-bug → main
# PR 2: hotfix/nome-do-bug → develop
```

## 📝 Convenções de Commit

### Formato: Conventional Commits
```
tipo(escopo): descrição curta

[corpo opcional]

[rodapé opcional]
```

### Tipos Principais
- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Mudanças na documentação
- **style**: Formatação de código (não altera lógica)
- **refactor**: Refatoração (sem mudança funcional)
- **test**: Adição ou correção de testes
- **chore**: Mudanças de build, dependências, etc.

### Exemplos Práticos
```bash
feat: adiciona endpoint de recomendações personalizadas
fix: corrige bug de CORS na API
docs: atualiza README com instruções de instalação
style: formata código Python seguindo PEP8
refactor: otimiza algoritmo de similaridade coseno
test: adiciona testes unitários para service de recomendação
chore: atualiza dependências do package.json
```

## 🏷️ Convenções de Nomenclatura

### Branches
```bash
# Features - funcionalidades novas
feature/api-recommendations-v2
feature/frontend-user-dashboard  
feature/ml-algorithm-optimization
feature/docker-containerization

# Bugfixes - correções
hotfix/cors-headers-fix
hotfix/memory-leak-frontend
hotfix/database-connection-timeout

# Releases - preparação de versões
release/v1.0.0
release/v1.1.0-beta

# Melhorias técnicas
feature/ci-cd-pipeline
feature/performance-optimization
feature/code-quality-improvements
```

### Pull Requests
- **Título**: Claro e descritivo
- **Descrição**: O que foi implementado e por quê
- **Labels**: `feature`, `bugfix`, `documentation`, `enhancement`
- **Reviewers**: Pelo menos 1 pessoa do time

### Exemplo de PR
```markdown
## 🚀 Feature: Sistema de Recomendações V2

### O que foi implementado
- Novo algoritmo de similaridade com 47 dimensões
- Cache em memória para melhorar performance
- Testes unitários com 90% de cobertura

### Como testar
1. Execute `.\start.ps1`
2. Acesse http://localhost:3001
3. Verifique se as recomendações aparecem

### Checklist
- [x] Código testado localmente
- [x] Documentação atualizada
- [x] Sem conflitos com develop
- [x] Testes passando
```

## 🔍 Code Review

### O que Revisar
- **Funcionalidade**: Código faz o que deveria fazer?
- **Qualidade**: Código legível e bem estruturado?
- **Performance**: Não introduz lentidão desnecessária?
- **Segurança**: Não expõe dados sensíveis?
- **Testes**: Funcionalidade coberta por testes?

### Como Aprovar
- ✅ **Approve**: Código pronto para merge
- 💬 **Comment**: Sugestões opcionais
- ❌ **Request Changes**: Mudanças necessárias antes do merge

## 🚀 Deploy e Releases

### Processo de Release
1. **Feature Complete**: Todas features da sprint em `develop`
2. **Create Release Branch**: `git checkout -b release/v1.1.0`
3. **Final Testing**: Testes integrados, ajustes finais
4. **Merge to Main**: Release pronta para produção
5. **Tag Version**: `git tag v1.1.0`
6. **Merge Back**: Merge da release para `develop`

### Versionamento Semântico
- **MAJOR** (1.0.0): Mudanças que quebram compatibilidade
- **MINOR** (0.1.0): Novas funcionalidades compatíveis
- **PATCH** (0.0.1): Correções de bugs

## ⚡ Dicas para o Hackathon

### Velocidade vs Qualidade
- **Commits frequentes**: Evita perda de trabalho
- **Branches curtas**: Facilita integração
- **Tests básicos**: Pelo menos smoke tests
- **Documentação mínima**: README sempre atualizado

### Colaboração Eficiente
- **Daily standups**: O que fiz, o que farei, impedimentos
- **Pair programming**: Para features complexas
- **Code review rápido**: Máximo 2h para aprovar PRs
- **Demo ready**: Sempre manter `main` demonstrável

## 🆘 Resolução de Conflitos

### Merge Conflicts
```bash
# Atualizar branch com develop
git checkout feature/minha-feature
git merge develop

# Resolver conflitos manualmente
# Commitar resolução
git commit -m "resolve: conflitos com develop"
```

### Emergency Rollback
```bash
# Voltar main para commit anterior
git checkout main
git revert HEAD
git push origin main
```

---
**Lembre-se**: O objetivo é entregar valor rápido mantendo a qualidade. Quando em dúvida, pergunte ao time! 🚀
