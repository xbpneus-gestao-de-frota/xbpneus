# Tarefas Pendentes - Frontend XBPneus

**Data**: 11 de Outubro de 2025  
**Baseado em**: Relatório de Análise Telas do Frontend (UI/UX)

---

## Situação Atual do Frontend

O relatório de análise revelou que o frontend está em um **estágio intermediário de desenvolvimento**:

### ✅ O Que Está Pronto

1. **Estrutura Sólida**: 49 páginas e 14 componentes reutilizáveis
2. **Autenticação Funcional**: Login e Cadastro implementados e funcionando
3. **Navegação Definida**: Sistema de rotas bem organizado
4. **Telas de Listagem**: ~20 telas com DataTable para exibir dados da API

### ⚠️ O Que Está Faltando

1. **Formulários de CRUD**: As telas de listagem existem, mas os formulários para criar/editar ainda não estão implementados
2. **Páginas de Menu Vazias**: 9 páginas que são apenas placeholders (Financeiro, Compras, Eventos, Relatórios, Configurações)
3. **Dashboards com Dados Reais**: Dashboards existem mas precisam de integração completa com API
4. **Padronização de Cores**: Aplicar o padrão de cores do Login/Cadastro em todas as telas

---

## Tarefas Prioritárias

### 1. Padronizar Cores em Todas as Telas ✅ PRIORIDADE MÁXIMA

**Objetivo**: Aplicar o padrão de cores do Login/Cadastro em todo o sistema.

**Cores do Padrão**:
- Logo/Título: Degradê `#60a5fa` → `#6366f1` → `#7c3aed`
- Botão principal: Degradê `from-blue-400 via-indigo-500 to-purple-600`
- Links: `text-blue-700`
- Inputs focus: `ring-blue-500`
- Texto inputs: `text-blue-900`

**Telas a Padronizar**:
- ✅ Login (já está no padrão)
- ✅ Cadastro (já está no padrão)
- ⚠️ Todos os Dashboards (TransportadorDashboard, DashboardMotorista, DashboardBorracharia, etc.)
- ⚠️ Todas as telas de listagem (VeiculosList, PneusList, OSList, etc.)
- ⚠️ Componentes reutilizáveis (Sidebar, Header, DataTable, etc.)

**Ação**: Criar arquivo de variáveis CSS/Tailwind com as cores padrão e aplicar em todos os componentes.

---

### 2. Implementar Formulários de CRUD

**Objetivo**: Para cada tela de listagem, implementar os formulários de criar e editar.

**Telas que Precisam de Formulários**:

#### Módulo Frota
- [ ] VeiculoForm - Criar/editar veículos
- [ ] PosicaoForm - Criar/editar posições de pneus

#### Módulo Pneus
- [ ] PneuForm - Criar/editar pneus
- [ ] AplicacaoForm - Criar/editar aplicações de pneus

#### Módulo Manutenção
- [ ] OrdemServicoForm - Criar/editar ordens de serviço
- [ ] TesteForm - Criar/editar testes

#### Módulo Estoque
- [ ] MovimentacaoForm - Criar/editar movimentações

#### Módulo IA
- [ ] AnaliseForm - Criar/editar análises
- [ ] GamificacaoForm - Gerenciar gamificação
- [ ] GarantiaForm - Gerenciar garantias

#### Outros Módulos (15+)
- [ ] AlertaForm, CargaForm, EpisForm, etc.

**Modelo de Referência**: Usar os 3 formulários existentes (OSForm, PneuForm, VeiculoForm) como base.

---

### 3. Desenvolver Páginas de Menu (Placeholders)

**Objetivo**: Transformar as 9 páginas vazias em dashboards ou páginas funcionais.

**Páginas a Desenvolver**:

1. **Financeiro** (`/dashboard/financeiro`)
   - Resumo de contas a pagar/receber
   - Gráficos de fluxo de caixa
   - Tabela de lançamentos recentes

2. **Compras** (`/dashboard/compras`)
   - Lista de pedidos de compra
   - Fornecedores
   - Histórico de compras

3. **Eventos** (`/dashboard/eventos`)
   - Calendário de eventos
   - Lista de eventos futuros
   - Notificações

4. **Relatórios** (`/dashboard/relatorios`)
   - Lista de relatórios disponíveis
   - Geração de relatórios personalizados
   - Exportação (PDF, Excel)

5. **Configurações** (`/dashboard/configuracoes`)
   - Configurações do usuário
   - Configurações do sistema
   - Preferências

**Ação**: Priorizar Financeiro e Relatórios, que são mais críticos para gestão.

---

### 4. Consolidar Dashboards

**Problema**: Existem múltiplas páginas de Dashboard:
- TransportadorDashboard
- Dashboard
- DashboardAvancado
- Index

**Objetivo**: Consolidar em uma única experiência de dashboard, usando componentes para exibir diferentes informações com base no perfil/permissões do usuário.

**Ação**: 
1. Escolher um dashboard principal (recomendado: TransportadorDashboard)
2. Migrar funcionalidades dos outros para componentes
3. Remover redundâncias

---

### 5. Integrar Telas com API

**Problema**: Muitos endpoints que as telas tentam consumir não existem ou estão incorretos no backend.

**Ação**:
1. Revisar todas as chamadas de API no frontend
2. Verificar se os endpoints existem no backend
3. Corrigir URLs incorretas
4. Implementar tratamento de erros adequado

**Telas Prioritárias**:
- VeiculosList → `/api/transportador/frota/veiculos/`
- PneusList → `/api/transportador/pneus/pneus/`
- OSList → `/api/transportador/manutencao/ordens-servico/`
- MovimentacoesList → `/api/transportador/estoque/movimentacoes/`

---

## Ordem de Execução Recomendada

### Fase 1: Padronização Visual (1-2 dias)
1. ✅ Criar arquivo de variáveis de cores
2. ✅ Aplicar cores no Sidebar
3. ✅ Aplicar cores no Header
4. ✅ Aplicar cores nos Dashboards
5. ✅ Aplicar cores nas telas de listagem
6. ✅ Aplicar cores nos componentes reutilizáveis

### Fase 2: Funcionalidades de CRUD (3-5 dias)
1. Implementar formulários para Frota (Veículos, Posições)
2. Implementar formulários para Pneus (Pneus, Aplicações)
3. Implementar formulários para Manutenção (OS, Testes)
4. Implementar formulários para Estoque (Movimentações)

### Fase 3: Páginas de Menu (2-3 dias)
1. Desenvolver página Financeiro
2. Desenvolver página Relatórios
3. Desenvolver páginas restantes (Compras, Eventos, Configurações)

### Fase 4: Consolidação e Integração (2-3 dias)
1. Consolidar dashboards
2. Revisar e corrigir integrações com API
3. Testes de ponta a ponta
4. Ajustes finais

---

## Estimativa Total

**Tempo estimado**: 8-13 dias de desenvolvimento

**Prioridade Imediata**: Fase 1 (Padronização Visual) - conforme solicitado pelo usuário

---

## Observações Importantes

1. **Não perder funcionalidades**: Ao consolidar dashboards, garantir que nenhuma funcionalidade seja perdida
2. **Usar formulários existentes como modelo**: Os 3 formulários já implementados (OSForm, PneuForm, VeiculoForm) devem servir de base
3. **Manter consistência**: Todas as telas devem seguir o mesmo padrão visual e de UX
4. **Testar integração**: Cada formulário implementado deve ser testado com a API real
5. **Responsividade**: Garantir que todas as telas funcionem bem em mobile, tablet e desktop

---

**Próximo Passo**: Iniciar Fase 1 - Padronização Visual

