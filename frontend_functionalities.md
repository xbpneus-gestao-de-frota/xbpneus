# Funcionalidades de Frontend - Sistema XBPneus

Este documento detalha as funcionalidades de frontend do sistema XBPneus, identificadas a partir das rotas e componentes definidos no arquivo `App.jsx`.

## Estrutura de Rotas e Módulos

O frontend do sistema é construído com React e utiliza `react-router-dom` para gerenciar as rotas. A aplicação suporta múltiplos tipos de usuários, cada um com seu próprio dashboard e funcionalidades específicas.

### Rotas de Acesso Público

*   `/login`: Página de autenticação de usuários.
*   `/cadastro`: Página para registro de novos usuários.
*   `/pos-cadastro`: Página exibida após o processo de cadastro.
*   `/cadastro/tipo`: Página para seleção do tipo de cliente durante o cadastro.

### Módulos Principais para Transportadoras (Rotas Protegidas)

As seguintes rotas são acessíveis através do `/dashboard` para usuários com o perfil de `transportador`:

*   `/dashboard`: Página inicial do dashboard para transportadoras.
*   `frota`: Gerenciamento da frota de veículos.
    *   `frota/veiculos`: Listagem de veículos.
    *   `frota/veiculos/create`: Criação de novos veículos.
    *   `frota/veiculos/:id/edit`: Edição de veículos existentes.
    *   `frota/veiculos/:id`: Detalhes de um veículo específico.
    *   `frota/posicoes`: Posições dos veículos.
    *   `frota/motoristas`: Gerenciamento de motoristas.
    *   `frota/implementos`: Gerenciamento de implementos.
    *   `frota/documentos`: Gerenciamento de documentos da frota.
    *   `frota/rastreamento`: Rastreamento de veículos.
*   `pneus`: Gerenciamento de pneus.
    *   `pneus/lista`: Listagem de pneus.
    *   `pneus/create`: Cadastro de novos pneus.
    *   `pneus/:id/edit`: Edição de pneus existentes.
    *   `pneus/aplicacoes`: Aplicações de pneus.
    *   `pneus/manutencao-pneus`: Manutenção de pneus.
    *   `pneus/analise-desgaste`: Análise de desgaste de pneus.
    *   `pneus/garantias`: Gerenciamento de garantias de pneus.
    *   `pneus/eventos-pneus`: Eventos relacionados a pneus.
*   `estoque`: Gerenciamento de estoque.
    *   `estoque/movimentacoes`: Movimentações de estoque.
    *   `estoque/itens`: Itens em estoque.
    *   `estoque/entradas-saidas`: Entradas e saídas do estoque.
    *   `estoque/relatorios-estoque`: Relatórios de estoque.
*   `manutencao`: Gerenciamento de manutenção.
    *   `manutencao/ordens-servico`: Listagem de ordens de serviço.
    *   `manutencao/ordens-servico/create`: Criação de novas ordens de serviço.
    *   `manutencao/ordens-servico/:id/edit`: Edição de ordens de serviço.
    *   `manutencao/ordens-servico/:id`: Detalhes de uma ordem de serviço.
    *   `manutencao/testes-pos-manutencao`: Testes pós-manutenção.
    *   `manutencao/historico`: Histórico de manutenção.
    *   `manutencao/planejamento-preventivo`: Planejamento de manutenção preventiva.
*   `ia`: Funcionalidades de Inteligência Artificial.
    *   `ia/analise`: Análise via IA.
    *   `ia/gamificacao`: Gamificação.
    *   `ia/garantias`: Garantias via IA.
*   `financeiro`: Módulo financeiro.
*   `compras`: Módulo de compras.
*   `eventos`: Gerenciamento de eventos.
*   `relatorios`: Geração de relatórios gerais.
    *   `relatorios/frota`: Relatórios da frota.
    *   `relatorios/pneus`: Relatórios de pneus.
    *   `relatorios/estoque`: Relatórios de estoque.
    *   `relatorios/manutencao`: Relatórios de manutenção.
    *   `relatorios/financeiro`: Relatórios financeiros.
*   `configuracoes`: Configurações do sistema.
*   `minha-empresa`: Informações da empresa do usuário.
*   `empresas`: (Em Breve) Gerenciamento de empresas.
*   `filiais`: (Em Breve) Gerenciamento de filiais.

### Dashboards Específicos por Tipo de Usuário (Rotas Protegidas)

*   `/motorista/dashboard`: Dashboard para usuários com perfil de `motorista`.
*   `/revenda/dashboard`: Dashboard para usuários com perfil de `revenda`.
*   `/borracharia/dashboard`: Dashboard para usuários com perfil de `borracharia`.
*   `/recapagem/dashboard`: Dashboard para usuários com perfil de `recapagem`.

Esta estrutura de rotas demonstra um sistema frontend robusto e modular, projetado para atender às necessidades específicas de diferentes perfis de usuários dentro do ecossistema XBPneus.
