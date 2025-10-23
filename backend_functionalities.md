# Funcionalidades de Backend - Sistema XBPneus

Este documento detalha as funcionalidades de backend do sistema XBPneus, identificadas a partir dos endpoints da API expostos via Swagger UI.

## Endpoints da API

Abaixo está uma lista dos principais endpoints da API, categorizados por suas funcionalidades:

### Autenticação e Autorização

*   `/api/token/`: Geração de tokens de autenticação.
*   `/api/token/refresh/`: Renovação de tokens de autenticação.
*   `/api/token/verify/`: Verificação de tokens de autenticação.
*   `/api/auth/logout/`: Logout de usuários.
*   `/api/auth/me/`: Obtenção de informações do usuário autenticado.
*   `/api/users/register_full/`: Registro completo de novos usuários.
*   `/api/approve/`: Aprovação de usuários (provavelmente por administradores).

### Módulos Principais

*   `/api/transportador/`: Módulo geral para funcionalidades relacionadas a transportadoras.
*   `/api/motorista/`: Módulo para gestão de motoristas.
*   `/api/borracharia/`: Módulo para funcionalidades de borracharias.
*   `/api/revenda/`: Módulo para funcionalidades de revendas.
*   `/api/recapagem/`: Módulo para funcionalidades de recapagem.

### Funcionalidades Detalhadas para Transportadoras

*   `/api/transportador/motorista/`: Gestão de motoristas de transportadoras.
*   `/api/transportador/frota/`: Gestão da frota de veículos.
*   `/api/transportador/pneus/`: Gestão de pneus da frota.
*   `/api/transportador/manutencao/`: Gestão de manutenção de veículos e pneus.
*   `/api/transportador/estoque/`: Gestão de estoque (peças, pneus, etc.).
*   `/api/transportador/loja/`: Funcionalidades de loja/compras.
*   `/api/transportador/custos/`: Controle de custos.
*   `/api/transportador/combustivel/`: Gestão de combustível.
*   `/api/transportador/multas/`: Gestão de multas.
*   `/api/transportador/documentos/`: Gestão de documentos.
*   `/api/transportador/viagens/`: Gestão de viagens.
*   `/api/transportador/clientes/`: Gestão de clientes.
*   `/api/transportador/fornecedores/`: Gestão de fornecedores.
*   `/api/transportador/seguros/`: Gestão de seguros.
*   `/api/transportador/contratos/`: Gestão de contratos.
*   `/api/transportador/faturamento/`: Gestão de faturamento.
*   `/api/transportador/pagamentos/`: Gestão de pagamentos.
*   `/api/transportador/telemetria/`: Dados de telemetria.
*   `/api/transportador/rastreamento/`: Rastreamento de veículos/cargas.
*   `/api/transportador/rotas/`: Gestão de rotas.
*   `/api/transportador/entregas/`: Gestão de entregas.
*   `/api/transportador/dashboards/`: Dashboards específicos para transportadoras.
*   `/api/transportador/notificacoes/`: Sistema de notificações.
*   `/api/transportador/almoxarifado/`: Gestão de almoxarifado.
*   `/api/transportador/relatorios/`: Geração de relatórios gerais.
*   `/api/transportador/cargas/`: Gestão de cargas.
*   `/api/transportador/pecas/`: Gestão de peças.
*   `/api/transportador/ferramentas/`: Gestão de ferramentas.
*   `/api/transportador/epis/`: Gestão de EPIs.
*   `/api/transportador/treinamentos/`: Gestão de treinamentos.
*   `/api/transportador/compliance/`: Funcionalidades de compliance.
*   `/api/transportador/alertas/`: Sistema de alertas.
*   `/api/transportador/integracoes/`: Gestão de integrações com outros sistemas.
*   `/api/transportador/configuracoes/`: Configurações do sistema para transportadoras.
*   `/api/transportador/empresas/`: Gestão de empresas (filiais, etc.).
*   `/api/transportador/financeiro/`: Módulo financeiro.
*   `/api/transportador/relatorios_transportador/`: Relatórios específicos para transportadoras.
*   `/api/transportador/tr/`: (Função não especificada, possivelmente relacionada a transporte ou rastreamento).
*   `/api/transportador/implemento/`: Gestão de implementos.
*   `/api/transportador/analise_pneus/`: Análise aprofundada de pneus.
*   `/api/transportador/garantias/`: Gestão de garantias.
*   `/api/transportador/auditoria/`: Funcionalidades de auditoria.
*   `/api/transportador/notas_fiscais/`: Gestão de notas fiscais.
*   `/api/transportador/ia/`: Funcionalidades de Inteligência Artificial.

### Outras Funcionalidades

*   `/api/reports/`: Geração de relatórios gerais.
*   `/api/jobs/`: Gestão de tarefas/jobs em segundo plano.

### Documentação da API

*   `/api/schema/swagger/`: Interface Swagger UI para documentação interativa da API.
*   `/api/docs/`: Documentação da API.

Esta listagem oferece uma visão abrangente das capacidades do backend do sistema XBPneus, cobrindo desde a autenticação de usuários até módulos complexos de gestão de frotas e integração com IA.
