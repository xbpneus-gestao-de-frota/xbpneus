# Plano de Implementação para Botões e Telas Ausentes no Frontend do Sistema XBPneus

Este documento detalha um plano de implementação para os botões e telas identificados como ausentes na análise anterior (`frontend_missing_elements_analysis.md`). O plano considera os padrões de formato e cores existentes no sistema XBPneus, conforme definido em `xbpneus/frontend/src/styles/colors.js` e a estrutura de rotas em `xbpneus/frontend/src/App.jsx`.

## 1. Padrões de Estilo e Cores a Serem Seguidos

O sistema XBPneus utiliza uma paleta de cores e classes Tailwind CSS bem definidas, garantindo consistência visual. As principais referências são:

*   **Cores Primárias:** `xbpneusColors.primary.DEFAULT` (`#6366f1` - indigo-500), `xbpneusColors.primary.light` (`#60a5fa` - blue-400), `xbpneusColors.primary.dark` (`#7c3aed` - purple-600).
*   **Azul Marinho Escuro (Navy):** `xbpneusColors.navy.DEFAULT` (`#1A237E`) para elementos como sidebar e texto primário.
*   **Cores de Input:** Bordas coloridas como `xbpneusColors.input.blue` (`#5B7FE8`). A cor da fonte dos campos de entrada, incluindo os campos de senha, nas páginas de login e cadastro deve ser azul escuro (`xbpneusColors.text.primary`) após a digitação.
*   **Cores de Status:** `xbpneusColors.status.success` (`#4CAF50`), `xbpneusColors.status.error` (`#E91E63`).
*   **Botões Primários:** `xbpneusClasses.buttonPrimary` (`bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white hover:opacity-90 disabled:opacity-50 shadow-lg`).
*   **Botões Secundários:** `xbpneusClasses.buttonSecondary` (`border-2 border-blue-500 text-blue-500 hover:bg-blue-50`).
*   **Cards:** `xbpneusClasses.card` (`bg-white rounded-xl shadow-md`).
*   **Headers:** `xbpneusClasses.headerBg` (`bg-white shadow-md`).

As páginas de login, cadastro e pós-cadastro devem seguir a aparência fornecida no arquivo `f.zip` (mencionado no conhecimento de domínio), mantendo o mesmo tamanho, posições e cores dos elementos (logo, mascotes, etc.). As telas devem ser responsivas e redimensionar automaticamente.

## 2. Plano de Implementação Detalhado

### 2.1. Tela de Aprovação de Usuários (Nova Tela)

**Necessidade:** Gerenciar usuários recém-cadastrados que aguardam aprovação, conforme o fluxo de aprovação de cadastro de usuários.

*   **Rota:** `/admin/usuarios/aprovacao` (ou similar, dentro de um contexto de administração).
*   **Componente:** `UserApprovalPage.jsx`.
*   **UI/UX:**
    *   **Layout:** Utilizar o `LayoutTransportador` como base, adaptando-o para um layout de administração. Sidebar com navegação para outras funcionalidades administrativas.
    *   **Tabela:** Exibir uma tabela responsiva com os seguintes campos para cada usuário pendente:
        *   Nome Completo
        *   Email
        *   Tipo de Cliente (Transportador, Motorista, Borracharia, Revenda, Recapagem)
        *   Data de Cadastro
        *   Ações (Botões de Aprovar/Rejeitar).
    *   **Botões de Ação na Tabela:**
        *   **"Aprovar"**: Utilizar `xbpneusClasses.buttonPrimary` com um tom de verde (`xbpneusColors.status.success`). Ícone de check (lucide-react: `Check`).
        *   **"Rejeitar"**: Utilizar `xbpneusClasses.buttonSecondary` com um tom de vermelho (`xbpneusColors.status.error`). Ícone de cruz (lucide-react: `X`).
    *   **Filtros e Busca:** Campos de input (`xbpneusClasses.input`) para filtrar por nome, email ou tipo de cliente. Botão de busca (`xbpneusClasses.buttonPrimary`).
    *   **Estilo:** Utilizar `xbpneusClasses.card` para encapsular a tabela e os filtros. Títulos de cards com `xbpneusClasses.cardTitle`.

### 2.2. Botões de Ação Comuns (Atualizações em Telas Existentes)

**Necessidade:** Adicionar botões de "Exportar" e "Imprimir" em telas de relatórios, e botões de "Editar Perfil" e "Alterar Senha" em telas de configuração/perfil.

*   **Telas Alvo:**
    *   **Relatórios:** `/dashboard/relatorios/frota`, `/dashboard/relatorios/pneus`, `/dashboard/relatorios/estoque`, etc.
    *   **Configurações/Perfil:** `/dashboard/configuracoes`, `/dashboard/minha-empresa`.
*   **UI/UX:**
    *   **Botões "Exportar" e "Imprimir" (Relatórios):**
        *   Localização: Geralmente no canto superior direito da área de conteúdo do relatório.
        *   Estilo: `xbpneusClasses.buttonSecondary`. Ícones de download (lucide-react: `Download`) e impressora (lucide-react: `Printer`).
        *   Dropdown para seleção de formato (PDF, CSV, Excel) ao clicar em "Exportar".
    *   **Botões "Editar Perfil" e "Alterar Senha" (Configurações):**
        *   Localização: Próximo às informações do perfil do usuário.
        *   Estilo: `xbpneusClasses.buttonPrimary` ou `xbpneusClasses.buttonSecondary`. Ícones de edição (lucide-react: `Edit`) e chave (lucide-react: `Key`).

### 2.3. Telas de Gerenciamento de Integrações (Nova Tela)

**Necessidade:** Permitir que o usuário configure e gerencie integrações com outros sistemas, utilizando o endpoint de backend `/api/transportador/integracoes/`.

*   **Rota:** `/dashboard/configuracoes/integracoes`.
*   **Componente:** `IntegrationsManagementPage.jsx`.
*   **UI/UX:**
    *   **Layout:** Seguir o padrão das telas de configuração existentes.
    *   **Listagem de Integrações:** Exibir cards (`xbpneusClasses.card`) para cada integração disponível ou configurada, mostrando o status (ativa/inativa).
    *   **Botões de Ação por Integração:**
        *   **"Configurar"**: `xbpneusClasses.buttonPrimary`. Ícone de engrenagem (lucide-react: `Settings`). Abre um modal ou navega para uma tela de configuração específica para aquela integração.
        *   **"Ativar/Desativar"**: Um toggle switch ou botões (`xbpneusClasses.buttonSecondary`) para mudar o status da integração.
    *   **Botão "Adicionar Nova Integração"**: `xbpneusClasses.buttonPrimary` no topo da página. Ícone de mais (lucide-react: `Plus`). Abre um modal ou tela para selecionar e configurar novas integrações.

### 2.4. Profundidade dos Módulos para Outros Perfis (Motorista, Revenda, Borracharia, Recapagem)

**Necessidade:** Desenvolver telas de detalhe, criação e edição para módulos específicos de cada perfil, além dos dashboards já existentes.

*   **Rotas Exemplo (para Motorista):**
    *   `/motorista/dashboard/rotas-atribuidas`
    *   `/motorista/dashboard/registrar-entrega`
    *   `/motorista/dashboard/historico-viagens`
*   **UI/UX (Generalizado):**
    *   **Consistência:** As novas telas devem seguir rigorosamente os padrões de layout, cores (`xbpneusColors`) e componentes (`xbpneusClasses`) já estabelecidos para o perfil de transportador, adaptando apenas o conteúdo e as funcionalidades específicas de cada perfil.
    *   **Botões:** Utilizar `xbpneusClasses.buttonPrimary` para ações principais (ex: "Registrar Entrega", "Adicionar Pneu") e `xbpneusClasses.buttonSecondary` para ações secundárias ou de navegação (ex: "Ver Detalhes", "Voltar").
    *   **Formulários:** Campos de input (`xbpneusClasses.input`) com labels (`xbpneusClasses.inputLabel`). Cores de validação (`xbpneusColors.status.error`, `xbpneusColors.status.success`).
    *   **Tabelas:** Utilizar `xbpneusClasses.tableHeader` e `xbpneusClasses.tableRow` para listagens de dados.

## 3. Próximos Passos

1.  **Criação de Componentes:** Desenvolver os novos componentes React (`UserApprovalPage.jsx`, `IntegrationsManagementPage.jsx`, e outros específicos por perfil).
2.  **Implementação de Rotas:** Adicionar as novas rotas no `App.jsx` e garantir a proteção por `ProtectedRoute` e `RequireAuth` conforme o perfil de usuário.
3.  **Integração com Backend:** Conectar os novos componentes e botões aos endpoints de API correspondentes.
4.  **Testes:** Realizar testes de UI/UX, funcionalidade e responsividade para todas as novas telas e botões.

Este plano serve como um guia para o desenvolvimento das funcionalidades ausentes, garantindo que a expansão do sistema XBPneus mantenha a consistência e a qualidade da experiência do usuário.
