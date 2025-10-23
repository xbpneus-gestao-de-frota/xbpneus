# Raio-X Completo do Sistema XBPneus

Este documento apresenta um "Raio-X" completo do sistema XBPneus, abordando sua arquitetura, tecnologias utilizadas, funcionalidades de backend e frontend, e um resumo do status dos serviços. O objetivo é fornecer uma visão abrangente do sistema para fins de análise, manutenção e desenvolvimento.

## 1. Arquitetura e Tecnologias Utilizadas

O sistema XBPneus adota uma arquitetura de microsserviços com um backend robusto baseado em Django e um frontend interativo construído com React. A comunicação entre as camadas é realizada via APIs RESTful.

### 1.1. Tecnologias de Backend

O backend é desenvolvido em Python, utilizando o framework Django e o Django REST Framework para a construção das APIs. As principais dependências e tecnologias incluem:

*   **Framework Web:** Django (versão 4.2.11)
*   **API REST:** Django REST Framework (versão 3.14.0)
*   **Autenticação:** djangorestframework-simplejwt (para tokens JWT), django-axes (para proteção contra ataques de força bruta)
*   **Banco de Dados:** Suporte a PostgreSQL (psycopg2-binary) e dj-database-url para configuração.
*   **Cache e Filas:** django-redis e redis (para cache e gerenciamento de tarefas em segundo plano com RQ).
*   **Documentação API:** drf-spectacular (para geração de documentação OpenAPI/Swagger UI).
*   **Monitoramento e Logs:** sentry-sdk (para monitoramento de erros), python-json-logger.
*   **Servidor Web:** Gunicorn (para produção), Whitenoise (para servir arquivos estáticos).
*   **Utilitários:** Pillow (processamento de imagens), openpyxl e xlsxwriter (para manipulação de arquivos Excel), validators.

### 1.2. Tecnologias de Frontend

O frontend é uma aplicação de página única (SPA) desenvolvida com React, utilizando Vite como ferramenta de build. As principais dependências e tecnologias incluem:

*   **Framework UI:** React (versão 18.2.0)
*   **Gerenciador de Estado:** Zustand (versão 4.4.0)
*   **Roteamento:** react-router-dom (versão 6.21.0)
*   **Requisições HTTP:** Axios (versão 1.6.0)
*   **Estilização:** Tailwind CSS (com PostCSS e Autoprefixer)
*   **Componentes UI/Ícones:** lucide-react
*   **Gráficos:** Recharts (versão 2.10.0)
*   **Utilitários:** date-fns (para manipulação de datas), jwt-decode (para decodificação de tokens JWT).
*   **Ferramenta de Build:** Vite (versão 7.1.10)

## 2. Funcionalidades de Backend

O backend do sistema XBPneus oferece uma vasta gama de funcionalidades, organizadas em módulos e expostas através de uma API RESTful. As principais categorias de endpoints incluem:

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

*   **Gestão de Frota:** `/api/transportador/frota/`, `/api/transportador/motorista/`, `/api/transportador/implemento/`, `/api/transportador/rastreamento/`.
*   **Gestão de Pneus:** `/api/transportador/pneus/`, `/api/transportador/analise_pneus/`, `/api/transportador/garantias/`.
*   **Manutenção:** `/api/transportador/manutencao/`.
*   **Estoque:** `/api/transportador/estoque/`, `/api/transportador/almoxarifado/`, `/api/transportador/pecas/`.
*   **Financeiro:** `/api/transportador/financeiro/`, `/api/transportador/custos/`, `/api/transportador/faturamento/`, `/api/transportador/pagamentos/`, `/api/transportador/notas_fiscais/`.
*   **Operacional:** `/api/transportador/combustivel/`, `/api/transportador/multas/`, `/api/transportador/documentos/`, `/api/transportador/viagens/`, `/api/transportador/clientes/`, `/api/transportador/fornecedores/`, `/api/transportador/seguros/`, `/api/transportador/contratos/`, `/api/transportador/telemetria/`, `/api/transportador/rotas/`, `/api/transportador/entregas/`, `/api/transportador/cargas/`.
*   **Gestão e Compliance:** `/api/transportador/empresas/`, `/api/transportador/configuracoes/`, `/api/transportador/compliance/`, `/api/transportador/auditoria/`, `/api/transportador/treinamentos/`, `/api/transportador/epis/`.
*   **Inteligência Artificial:** `/api/transportador/ia/`.
*   **Relatórios e Dashboards:** `/api/transportador/dashboards/`, `/api/transportador/relatorios/`, `/api/transportador/relatorios_transportador/`, `/api/reports/`.
*   **Outros:** `/api/transportador/loja/`, `/api/transportador/ferramentas/`, `/api/transportador/alertas/`, `/api/transportador/integracoes/`, `/api/transportador/tr/`, `/api/jobs/`.

## 3. Funcionalidades de Frontend

O frontend do sistema XBPneus é uma aplicação de página única (SPA) construída com React, oferecendo uma interface de usuário rica e interativa. Ele é projetado para suportar diferentes perfis de usuários, cada um com acesso a módulos e dashboards específicos. As principais funcionalidades e rotas incluem:

### Rotas de Acesso Público

*   `/login`: Página de autenticação.
*   `/cadastro`: Registro de novos usuários.
*   `/pos-cadastro`: Página de confirmação pós-cadastro.
*   `/cadastro/tipo`: Seleção do tipo de cliente durante o registro.

### Módulos e Dashboards por Perfil de Usuário

*   **Transportador:** Acessa um dashboard principal (`/dashboard`) que serve como ponto de entrada para módulos como Frota, Pneus, Estoque, Manutenção, IA, Financeiro, Compras, Eventos, Relatórios e Configurações.
    *   **Frota:** Gerenciamento de veículos, motoristas, implementos, documentos e rastreamento.
    *   **Pneus:** Listagem, cadastro, edição, aplicações, manutenção, análise de desgaste, garantias e eventos de pneus.
    *   **Estoque:** Movimentações, itens, entradas/saídas e relatórios de estoque.
    *   **Manutenção:** Ordens de serviço (criação, edição, detalhes), testes pós-manutenção, histórico e planejamento preventivo.
    *   **IA:** Dashboards, análises, gamificação e garantias baseadas em IA.
    *   **Relatórios:** Relatórios específicos para frota, pneus, estoque, manutenção e finanças.
*   **Motorista:** Dashboard específico (`/motorista/dashboard`).
*   **Revenda:** Dashboard específico (`/revenda/dashboard`).
*   **Borracharia:** Dashboard específico (`/borracharia/dashboard`).
*   **Recapagem:** Dashboard específico (`/recapagem/dashboard`).

## 4. Resumo do Status dos Serviços

Atualmente, todos os serviços principais do sistema XBPneus estão operacionais e em execução, conforme verificado pelo script de monitoramento. Os PIDs dos processos ativos são:

*   **Redis:** Rodando.
*   **Backend (Django):** Rodando (PID: 3584).
*   **Frontend (React + Vite):** Rodando (PID: 3603).

Este status indica que o ambiente está saudável e pronto para operação.

## 5. Scripts de Verificação Gerados

Para auxiliar na manutenção e verificação contínua do sistema, foram gerados os seguintes scripts:

*   **`check_backend_functionality.py`:** Verifica a acessibilidade dos endpoints do backend.
*   **`check_frontend_functionality.py`:** Navega por rotas do frontend para verificar o carregamento das páginas e a presença de elementos básicos.
*   **`check_service_status.sh`:** Monitora o status de execução dos serviços Redis, Backend e Frontend.

Estes scripts podem ser utilizados para realizar verificações rápidas e automatizadas da saúde e funcionalidade do sistema XBPneus.
