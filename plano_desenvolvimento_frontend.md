# Plano de Desenvolvimento Frontend - Sistema XBPneus

## 1. Análise do Padrão de Cores e Design Existente

Com base na análise dos arquivos do frontend, o sistema XBPneus utiliza o seguinte padrão de cores e design:

### Paleta de Cores Principal

*   **Fundo Principal:** `#0b1220` (azul escuro quase preto)
*   **Texto Principal:** `#e5e7eb` (cinza claro)
*   **Sidebar:** `#1A237E` (azul índigo escuro)
*   **Gradiente Principal:** `linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)` (azul claro → azul → roxo)
*   **Botão de Ação Negativa:** `#DC2626` (vermelho)
*   **Hover Sidebar:** `#3949AB` (azul índigo médio)
*   **Item Ativo Sidebar:** Gradiente `from-blue-400 via-indigo-500 to-purple-600`

### Componentes de UI

*   **Framework:** React com Vite
*   **Estilização:** Tailwind CSS
*   **Ícones:** Lucide React
*   **Roteamento:** React Router DOM
*   **Layout:** Sidebar fixa com conteúdo principal responsivo

### Estrutura de Navegação

O sistema atualmente possui os seguintes itens de navegação no sidebar:

1.  Início (Dashboard)
2.  Frota
3.  Pneus
4.  Estoque
5.  Manutenção
6.  IA - Análise
7.  Financeiro
8.  Compras
9.  Eventos
10. Relatórios
11. Configurações
12. Empresas
13. Filiais

## 2. Módulos e Funcionalidades a Serem Desenvolvidos

Com base na análise dos endpoints não conectados, os seguintes módulos e funcionalidades precisam ser desenvolvidos no frontend:

### 2.1. Módulos de Usuário (Novos Perfis)

Estes módulos representam diferentes tipos de usuários do sistema e devem ter seus próprios dashboards e funcionalidades:

1.  **Borracharia**
    *   Login
    *   Perfil
    *   Dashboard específico
2.  **Motorista**
    *   Login
    *   Perfil
    *   Dashboard específico
3.  **Recapadora**
    *   Login
    *   Perfil
    *   Dashboard específico
4.  **Revenda**
    *   Login
    *   Perfil
    *   Dashboard específico

### 2.2. Funcionalidades Detalhadas do Módulo Transportador

Estas são funcionalidades adicionais dentro do módulo transportador que precisam de telas no frontend:

#### 2.2.1. Alertas (Expandido)

*   **Telas Existentes:** Lista de Alertas
*   **Novas Telas:**
    *   Configuração de Alertas
    *   Histórico de Alertas
    *   Tipos de Alertas

#### 2.2.2. Almoxarifado (Expandido)

*   **Telas Existentes:** Lista de Almoxarifados, Locais de Estoque
*   **Novas Telas:**
    *   Inventários
    *   Itens de Inventário
    *   Requisições
    *   Itens de Requisição
    *   Movimentações de Almoxarifado

#### 2.2.3. Auditoria (Expandido)

*   **Telas Existentes:** Logs de Auditoria
*   **Novas Telas:**
    *   Logs de Acesso
    *   Logs de Alteração
    *   Sessões
    *   Configurações de Auditoria

#### 2.2.4. Cargas (Expandido)

*   **Telas Existentes:** Lista de Cargas
*   **Novas Telas:**
    *   Tipos de Cargas
    *   Itens de Cargas
    *   Manifestos de Cargas
    *   Rastreamento de Cargas

#### 2.2.5. Clientes (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Clientes
    *   Detalhes do Cliente
    *   Contatos de Clientes
    *   Formulário de Cadastro/Edição de Cliente

#### 2.2.6. Combustível (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Postos de Combustível
    *   Abastecimentos
    *   Consumo Mensal
    *   Formulário de Cadastro/Edição de Posto
    *   Formulário de Registro de Abastecimento

#### 2.2.7. Compliance (Expandido)

*   **Telas Existentes:** Documentos de Compliance
*   **Novas Telas:**
    *   Normas de Compliance
    *   Auditorias de Compliance
    *   Não Conformidades
    *   Planos de Ação de Compliance

#### 2.2.8. Configurações (Expandido)

*   **Telas Existentes:** Configurações Gerais
*   **Novas Telas:**
    *   Configurações do Sistema
    *   Parâmetros da Empresa
    *   Perfis de Usuários
    *   Permissões Customizadas
    *   Catálogo de Modelos de Veículos
    *   Mapa de Posições de Pneus
    *   Operações de Configurações
    *   Medidas por Posição
    *   Pressões Recomendadas
    *   Catálogo de Pneus XBRI

#### 2.2.9. Contratos (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Contratos
    *   Detalhes do Contrato
    *   Aditivos de Contratos
    *   Formulário de Cadastro/Edição de Contrato

#### 2.2.10. Custos (Novo Módulo)

*   **Novas Telas:**
    *   Categorias de Custos
    *   Lista de Custos
    *   Custo por Km
    *   Formulário de Cadastro/Edição de Custo

#### 2.2.11. Dashboards (Expandido)

*   **Telas Existentes:** Dashboard Principal
*   **Novas Telas:**
    *   Métricas do Dashboard
    *   Dashboards Personalizados
    *   Widgets
    *   KPIs

#### 2.2.12. Documentos (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Documentos
    *   Detalhes do Documento
    *   Upload de Documentos
    *   Visualização de Documentos

#### 2.2.13. Empresas e Filiais (Expandido)

*   **Telas Existentes:** Lista de Empresas, Lista de Filiais
*   **Novas Telas:**
    *   Detalhes da Empresa
    *   Detalhes da Filial
    *   Formulário de Cadastro/Edição de Empresa
    *   Formulário de Cadastro/Edição de Filial

#### 2.2.14. Entregas (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Entregas
    *   Detalhes da Entrega
    *   PODs (Proof of Delivery)
    *   Ocorrências de Entregas
    *   Tentativas de Entregas
    *   Formulário de Cadastro/Edição de Entrega

#### 2.2.15. EPIs (Expandido)

*   **Telas Existentes:** Lista de EPIs
*   **Novas Telas:**
    *   Tipos de EPIs
    *   Entregas de EPIs
    *   Fichas de EPIs

#### 2.2.16. Estoque (Expandido)

*   **Telas Existentes:** Produtos, Movimentações, Categorias
*   **Novas Telas:**
    *   Saldos de Estoque
    *   Previsões de Demanda
    *   Curva ABC

#### 2.2.17. Faturamento (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Faturas
    *   Detalhes da Fatura
    *   Itens de Fatura
    *   Notas Fiscais de Faturamento
    *   Formulário de Cadastro/Edição de Fatura

#### 2.2.18. Ferramentas (Expandido)

*   **Telas Existentes:** Lista de Ferramentas
*   **Novas Telas:**
    *   Empréstimos de Ferramentas
    *   Manutenção de Ferramentas
    *   Calibração de Ferramentas

#### 2.2.19. Fornecedores (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Fornecedores
    *   Detalhes do Fornecedor
    *   Contatos de Fornecedores
    *   Formulário de Cadastro/Edição de Fornecedor

#### 2.2.20. IA - Análise (Expandido)

*   **Telas Existentes:** Nova Análise, Histórico, Gamificação, Garantias, Chatbot, Relatórios
*   **Novas Telas:**
    *   Análises de IA (lista completa)
    *   Detalhes da Análise
    *   Gamificação (detalhes)
    *   Garantias (detalhes)

#### 2.2.21. Integrações (Expandido)

*   **Telas Existentes:** Lista de Integrações
*   **Novas Telas:**
    *   Integrações Externas
    *   Logs de Integrações
    *   Webhooks Configurados
    *   Credenciais de API

#### 2.2.22. Loja (Novo Módulo)

*   **Novas Telas:**
    *   Categorias de Produtos da Loja
    *   Produtos da Loja
    *   Pedidos
    *   Itens de Pedido
    *   Movimentações da Loja

#### 2.2.23. Manutenção (Expandido)

*   **Telas Existentes:** Ordens de Serviço, Itens de OS, Checklists, Planos Preventiva, Histórico
*   **Novas Telas:**
    *   OS (lista completa)
    *   Testes Pós-Manutenção

#### 2.2.24. Motorista Externo (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Motoristas Externos
    *   Detalhes do Motorista Externo
    *   Alocações de Motorista
    *   Formulário de Cadastro/Edição de Motorista Externo

#### 2.2.25. Motorista Interno (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Motoristas Internos
    *   Detalhes do Motorista Interno
    *   Vínculos de Motorista
    *   Jornadas de Trabalho
    *   Mensagens para Motoristas
    *   Alertas de Motoristas
    *   Formulário de Cadastro/Edição de Motorista Interno

#### 2.2.26. Multas (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Multas
    *   Detalhes da Multa
    *   Recursos de Multas
    *   Pontuação CNH
    *   Formulário de Cadastro/Edição de Multa

#### 2.2.27. Notas Fiscais (Expandido)

*   **Telas Existentes:** Notas Fiscais
*   **Novas Telas:**
    *   Notas Fiscais (lista completa)
    *   Itens de Nota Fiscal
    *   Impostos de Nota Fiscal
    *   Anexos de Nota Fiscal

#### 2.2.28. Notificações (Novo Módulo)

*   **Novas Telas:**
    *   Canais de Notificação
    *   Lista de Notificações
    *   Templates de Notificação
    *   Preferências de Notificação

#### 2.2.29. Pagamentos (Novo Módulo)

*   **Novas Telas:**
    *   Contas a Pagar
    *   Contas a Receber
    *   Pagamentos Realizados
    *   Formulário de Cadastro/Edição de Pagamento

#### 2.2.30. Peças (Expandido)

*   **Telas Existentes:** Lista de Peças
*   **Novas Telas:**
    *   Categorias de Peças
    *   Estoque de Peças
    *   Movimentações de Peças
    *   Fornecedores de Peças

#### 2.2.31. Pneus (Expandido)

*   **Telas Existentes:** Lista de Pneus, Aplicações, Eventos
*   **Novas Telas:**
    *   (Todas as telas já estão conectadas)

#### 2.2.32. Rastreamento (Novo Módulo)

*   **Novas Telas:**
    *   Posições de Rastreamento
    *   Cercas Eletrônicas
    *   Violações de Cercas
    *   Histórico de Rastreamento

#### 2.2.33. Relatórios (Expandido)

*   **Telas Existentes:** Relatórios
*   **Novas Telas:**
    *   Templates de Relatórios
    *   Relatórios Agendados
    *   Relatórios Gerados
    *   Dashboards Personalizados

#### 2.2.34. Rotas (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Rotas
    *   Detalhes da Rota
    *   Pontos de Rota
    *   Rotas Otimizadas
    *   Formulário de Cadastro/Edição de Rota

#### 2.2.35. Seguros (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Seguradoras
    *   Apólices de Seguro
    *   Sinistros
    *   Formulário de Cadastro/Edição de Seguradora
    *   Formulário de Cadastro/Edição de Apólice

#### 2.2.36. Telemetria (Novo Módulo)

*   **Novas Telas:**
    *   Dispositivos de Telemetria
    *   Leituras de Telemetria
    *   Alertas de Telemetria

#### 2.2.37. Treinamentos (Expandido)

*   **Telas Existentes:** Lista de Treinamentos
*   **Novas Telas:**
    *   Cursos de Treinamento
    *   Treinamentos Realizados
    *   Certificados de Treinamento
    *   Instrutores de Treinamento

#### 2.2.38. Viagens (Novo Módulo)

*   **Novas Telas:**
    *   Lista de Viagens
    *   Detalhes da Viagem
    *   Cargas da Viagem
    *   Paradas da Viagem
    *   Formulário de Cadastro/Edição de Viagem

### 2.3. Módulos de Relatórios (Novos Endpoints)

*   **Novas Telas:**
    *   Relatório de Giro de Estoque
    *   Relatório de Custos por OS
    *   Relatório de Custos por Posição
    *   Relatório de Medições por Posição

## 3. Estratégia de Desenvolvimento

Para garantir a eficiência e a qualidade do desenvolvimento, a seguinte estratégia será adotada:

### 3.1. Priorização de Módulos

Os módulos serão priorizados com base na sua importância para o negócio e na complexidade de implementação:

1.  **Alta Prioridade (Essenciais para o Negócio):**
    *   Empresas e Filiais (Expandido)
    *   Motorista Interno
    *   Motorista Externo
    *   Clientes
    *   Fornecedores
    *   Viagens
    *   Entregas
    *   Combustível
    *   Multas
    *   Contratos
    *   Custos
    *   Pagamentos
    *   Rastreamento

2.  **Média Prioridade (Importantes para Operação):**
    *   Almoxarifado (Expandido)
    *   Estoque (Expandido)
    *   Manutenção (Expandido)
    *   Peças (Expandido)
    *   Ferramentas (Expandido)
    *   EPIs (Expandido)
    *   Treinamentos (Expandido)
    *   Documentos
    *   Notificações
    *   Seguros
    *   Rotas
    *   Telemetria

3.  **Baixa Prioridade (Complementares):**
    *   Cargas (Expandido)
    *   Alertas (Expandido)
    *   Auditoria (Expandido)
    *   Compliance (Expandido)
    *   Configurações (Expandido)
    *   Dashboards (Expandido)
    *   Faturamento
    *   IA - Análise (Expandido)
    *   Integrações (Expandido)
    *   Loja
    *   Notas Fiscais (Expandido)
    *   Relatórios (Expandido)

4.  **Módulos de Usuário (Novos Perfis):**
    *   Borracharia
    *   Motorista
    *   Recapadora
    *   Revenda

### 3.2. Padrão de Desenvolvimento de Telas

Todas as novas telas seguirão o seguinte padrão:

1.  **Layout Consistente:**
    *   Uso do componente `LayoutTransportador` para manter a sidebar e o header
    *   Uso do componente `PageHeader` para títulos de página
    *   Uso do componente `DataTable` para listagens
    *   Uso de modais para formulários de cadastro/edição

2.  **Estilização:**
    *   Manter a paleta de cores existente
    *   Usar Tailwind CSS para estilização
    *   Usar Lucide React para ícones
    *   Aplicar gradientes onde apropriado (botões de ação, títulos)

3.  **Funcionalidades Padrão:**
    *   Listagem com paginação
    *   Busca e filtros
    *   Ordenação de colunas
    *   Exportação de dados (CSV, Excel, PDF)
    *   Formulários de cadastro/edição com validação
    *   Confirmação de exclusão
    *   Mensagens de sucesso/erro

4.  **Integração com Backend:**
    *   Adicionar endpoints ao arquivo `frontend/src/api/config.js`
    *   Criar funções de chamada de API no arquivo apropriado em `frontend/src/api/`
    *   Usar hooks do React para gerenciar estado e efeitos colaterais
    *   Implementar tratamento de erros e loading states

### 3.3. Componentes Reutilizáveis

Para acelerar o desenvolvimento, os seguintes componentes reutilizáveis serão criados ou aprimorados:

1.  **FormModal:** Modal genérico para formulários de cadastro/edição
2.  **ConfirmDialog:** Diálogo de confirmação para ações destrutivas
3.  **StatusBadge:** Badge para exibir status (ativo, inativo, pendente, etc.)
4.  **DateRangePicker:** Seletor de intervalo de datas
5.  **SearchBar:** Barra de busca com debounce
6.  **FilterPanel:** Painel de filtros lateral
7.  **StatsCard:** Card para exibir estatísticas
8.  **ChartWidget:** Widget para exibir gráficos
9.  **FileUploader:** Componente para upload de arquivos
10. **ImageViewer:** Visualizador de imagens

### 3.4. Estrutura de Arquivos

A estrutura de arquivos do frontend será organizada da seguinte forma:

```
frontend/src/
├── api/
│   ├── config.js (endpoints centralizados)
│   ├── auth.js
│   ├── transportador.js
│   ├── borracharia.js
│   ├── motorista.js
│   ├── recapadora.js
│   ├── revenda.js
│   └── ...
├── components/
│   ├── common/ (componentes reutilizáveis)
│   ├── forms/ (formulários específicos)
│   ├── modals/ (modais)
│   ├── ui/ (componentes de UI básicos)
│   ├── Header.jsx
│   ├── Sidebar.jsx
│   ├── LayoutTransportador.jsx
│   └── ...
├── pages/
│   ├── auth/ (login, cadastro)
│   ├── transportador/
│   │   ├── dashboard/
│   │   ├── frota/
│   │   ├── pneus/
│   │   ├── estoque/
│   │   ├── manutencao/
│   │   ├── ia/
│   │   ├── financeiro/
│   │   ├── compras/
│   │   ├── eventos/
│   │   ├── relatorios/
│   │   ├── configuracoes/
│   │   ├── empresas/
│   │   ├── filiais/
│   │   ├── clientes/
│   │   ├── fornecedores/
│   │   ├── viagens/
│   │   ├── entregas/
│   │   ├── combustivel/
│   │   ├── multas/
│   │   ├── contratos/
│   │   ├── custos/
│   │   ├── pagamentos/
│   │   ├── rastreamento/
│   │   ├── motorista-interno/
│   │   ├── motorista-externo/
│   │   ├── almoxarifado/
│   │   ├── pecas/
│   │   ├── ferramentas/
│   │   ├── epis/
│   │   ├── treinamentos/
│   │   ├── documentos/
│   │   ├── notificacoes/
│   │   ├── seguros/
│   │   ├── rotas/
│   │   ├── telemetria/
│   │   ├── cargas/
│   │   ├── alertas/
│   │   ├── auditoria/
│   │   ├── compliance/
│   │   ├── dashboards/
│   │   ├── faturamento/
│   │   ├── integracoes/
│   │   ├── loja/
│   │   └── notas-fiscais/
│   ├── borracharia/
│   ├── motorista/
│   ├── recapadora/
│   ├── revenda/
│   └── ...
├── hooks/ (hooks customizados)
├── utils/ (funções utilitárias)
├── App.jsx
├── main.jsx
└── index.css
```

## 4. Cronograma de Desenvolvimento (Estimativa)

Considerando a complexidade e a quantidade de módulos a serem desenvolvidos, o cronograma estimado é o seguinte:

### Fase 1: Planejamento e Setup (1 dia)

*   Análise detalhada dos endpoints do backend
*   Criação de componentes reutilizáveis
*   Setup da estrutura de arquivos
*   Atualização do arquivo `config.js` com todos os endpoints

### Fase 2: Desenvolvimento de Módulos de Alta Prioridade (5-7 dias)

*   Empresas e Filiais (Expandido)
*   Motorista Interno
*   Motorista Externo
*   Clientes
*   Fornecedores
*   Viagens
*   Entregas
*   Combustível
*   Multas
*   Contratos
*   Custos
*   Pagamentos
*   Rastreamento

### Fase 3: Desenvolvimento de Módulos de Média Prioridade (5-7 dias)

*   Almoxarifado (Expandido)
*   Estoque (Expandido)
*   Manutenção (Expandido)
*   Peças (Expandido)
*   Ferramentas (Expandido)
*   EPIs (Expandido)
*   Treinamentos (Expandido)
*   Documentos
*   Notificações
*   Seguros
*   Rotas
*   Telemetria

### Fase 4: Desenvolvimento de Módulos de Baixa Prioridade (5-7 dias)

*   Cargas (Expandido)
*   Alertas (Expandido)
*   Auditoria (Expandido)
*   Compliance (Expandido)
*   Configurações (Expandido)
*   Dashboards (Expandido)
*   Faturamento
*   IA - Análise (Expandido)
*   Integrações (Expandido)
*   Loja
*   Notas Fiscais (Expandido)
*   Relatórios (Expandido)

### Fase 5: Desenvolvimento de Módulos de Usuário (3-5 dias)

*   Borracharia
*   Motorista
*   Recapadora
*   Revenda

### Fase 6: Testes e Refinamento (3-5 dias)

*   Testes de integração
*   Testes de funcionalidade
*   Correção de bugs
*   Otimização de performance
*   Ajustes de UI/UX

### Fase 7: Documentação e Entrega (1-2 dias)

*   Documentação do código
*   Guia de uso para usuários
*   Preparação para deploy

**Total Estimado: 23-34 dias de desenvolvimento**

## 5. Considerações Finais

Este plano de desenvolvimento é ambicioso e abrangente, visando conectar todas as funcionalidades do backend ao frontend do sistema XBPneus. A execução deste plano resultará em um sistema completo, profissional e pronto para uso em produção.

É importante ressaltar que:

*   **Flexibilidade:** O cronograma é uma estimativa e pode ser ajustado conforme necessário.
*   **Priorização:** A ordem de desenvolvimento dos módulos pode ser alterada com base nas necessidades do negócio.
*   **Qualidade:** A qualidade do código e da experiência do usuário deve ser sempre priorizada.
*   **Testes:** Testes contínuos são essenciais para garantir a estabilidade do sistema.
*   **Comunicação:** Comunicação clara e frequente com a equipe é fundamental para o sucesso do projeto.

Com este plano em mãos, estamos prontos para iniciar o desenvolvimento e transformar o sistema XBPneus em uma solução completa e robusta para gestão de frotas de pneus.

