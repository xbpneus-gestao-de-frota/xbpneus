## Relatório de Análise de Conexões e Inconsistências do Sistema XBPneus

### 1. Análise das Relações dos Modelos Django

O sistema XBPneus utiliza o framework Django para o backend, com uma estrutura modular que organiza os modelos em diferentes aplicativos. A análise dos arquivos `models.py` revelou as seguintes relações chave:

#### 1.1. Modelos de Empresa e Filial (`backend/transportador/empresas/models.py`)

*   **`Empresa`**: Representa a entidade principal (matriz) e pode ter múltiplos tipos (transportador, revenda, borracharia, recapagem). Contém campos para informações cadastrais, endereço e contato.
*   **`Filial`**: Vinculada a uma `Empresa` através de uma `ForeignKey` (`empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='filiais')`). Isso estabelece uma relação de um-para-muitos, onde uma empresa pode ter várias filiais. Cada filial possui seu próprio código, nome, CNPJ e informações de contato/endereço.

#### 1.2. Modelos de Frota (`backend/transportador/frota/models.py`)

*   **`Vehicle`**: Representa um veículo na frota. Possui `ForeignKey` para `Empresa` e `Filial` (`empresa = models.ForeignKey('transportador_empresas.Empresa', ...)` e `filial = models.ForeignKey('transportador_empresas.Filial', ...)`, ambos com `on_delete=models.PROTECT`). Isso garante que um veículo esteja sempre associado a uma empresa e, opcionalmente, a uma filial específica. O modelo `Vehicle` também inclui campos para placa, modelo, ano, tipo, status, quilometragem e um campo temporário para `motorista` (string), que será substituído por um vínculo mais robusto.
*   **`Position`**: Representa uma posição de pneu em um `Vehicle`. Possui `ForeignKey` para `Vehicle` (`veiculo = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='posicoes_pneu')`) e também para `Empresa` e `Filial`, replicando a estrutura de multi-tenancy.
*   **`HistoricoKm`**: Registra o histórico de quilometragem de um `Vehicle`, com `ForeignKey` para `Vehicle`.

#### 1.3. Modelos de Motorista (`backend/transportador/motorista_interno/models.py` e `backend/motorista/models.py`)

*   **`UsuarioTransportador` (`backend/transportador/models.py`)**: É o modelo de usuário principal para transportadores, com uma `ForeignKey` opcional para `Empresa` (`empresa = models.ForeignKey('transportador_empresas.Empresa', on_delete=models.SET_NULL, ...) `). Isso indica que um usuário transportador pode estar associado a uma empresa.
*   **`MotoristaInterno` (`backend/transportador/motorista_interno/models.py`)**: Representa um motorista vinculado a uma empresa transportadora. Possui `ForeignKey` para `Empresa` e `Filial` (`empresa = models.ForeignKey(Empresa, ...)` e `filial = models.ForeignKey('transportador_empresas.Filial', ...)`). Contém dados pessoais, profissionais e status.
*   **`VinculoMotoristaVeiculo`**: Estabelece a relação entre `MotoristaInterno` e `Vehicle` (`motorista = models.ForeignKey(MotoristaInterno, ...)` e `veiculo = models.ForeignKey(Vehicle, ...)`). Também possui `ForeignKey` para `Empresa` e `Filial`.
*   **`RegistroJornada`**: Registra a jornada de trabalho de um `MotoristaInterno`, com `ForeignKey` para `MotoristaInterno` e `Vehicle`.
*   **`MensagemMotorista`**: Gerencia mensagens entre transportador e `MotoristaInterno`.
*   **`AlertaMotorista`**: Gerencia alertas relacionados a `MotoristaInterno`.
*   **`UsuarioMotorista` (`backend/motorista/models.py`)**: Um modelo de usuário separado para motoristas, com campos para email, nome, CPF, CNH, etc. Este modelo parece ser para motoristas que acessam o sistema diretamente (talvez via app externo), enquanto `MotoristaInterno` é para motoristas gerenciados por uma transportadora.

**Conexões Confirmadas:**

*   **Empresas e Filiais:** A relação entre `Empresa` e `Filial` está bem definida, com `Filial` referenciando `Empresa` via `ForeignKey`.
*   **Frota e Empresas/Filiais:** `Vehicle` e `Position` estão corretamente vinculados a `Empresa` e `Filial`.
*   **Motoristas e Frota/Empresas/Filiais:** `MotoristaInterno` e `VinculoMotoristaVeiculo` estão conectados a `Empresa`, `Filial` e `Vehicle`, estabelecendo as relações esperadas.

### 2. Análise das URLs e Mapeamento de Endpoints Django

O arquivo `config/urls.py` atua como o roteador principal, incluindo URLs de diversos aplicativos Django. A estrutura utiliza `rest_framework.routers.DefaultRouter` para ViewSets, o que simplifica a criação de endpoints RESTful.

#### 2.1. Endpoints Principais (`config/urls.py`)

*   **Autenticação**: Endpoints para login (`api/token/`, `api/token/refresh/`, `api/token/verify/`), logout (`api/auth/logout/`) e informações do usuário logado (`api/auth/me/`).
*   **Registro**: `api/users/register_full/` para registro completo de usuários.
*   **Admin**: `admin/` para o painel administrativo do Django.
*   **Documentação API**: `api/schema/` e `api/docs/` para OpenAPI/Swagger.

#### 2.2. Módulos do Transportador (Exemplos)

*   **Empresas**: `api/transportador/empresas/` (inclui `empresas/` e `filiais/` via `DefaultRouter`).
*   **Frota**: `api/transportador/frota/` (inclui `veiculos/` e `posicoes/` via `DefaultRouter`).
*   **Motorista Interno**: `api/transportador/motorista-interno/` (inclui `motoristas/`, `vinculos/`, `jornadas/`, `mensagens/`, `alertas/` via `DefaultRouter`).

Os endpoints estão bem organizados por módulo e tipo de usuário, utilizando prefixos como `api/transportador/` para as funcionalidades específicas do transportador.

### 3. Análise do Código Frontend para Chamadas de API e Tratamento de Dados

O frontend, desenvolvido em React, utiliza `axios` (via `api/http.js`) para interagir com o backend. A configuração dos endpoints é centralizada em `frontend/src/api/config.js`.

#### 3.1. Configuração da API (`frontend/src/api/config.js`)

O arquivo `config.js` define `API_BASE_URL` e um objeto `API_ENDPOINTS` que mapeia as URLs para diferentes recursos do backend. Isso facilita a manutenção e a consistência das chamadas de API.

Exemplos de endpoints configurados:

*   `API_ENDPOINTS.auth.login`: `http://localhost:8000/api/transportador/login/`
*   `API_ENDPOINTS.transportador.veiculos`: `http://localhost:8000/api/transportador/frota/veiculos/`
*   `API_ENDPOINTS.transportador.posicoes`: `http://localhost:8000/api/transportador/frota/posicoes/`

#### 3.2. Interação Frontend-Backend (Exemplos)

*   **`EmpresasList.jsx`**: Utiliza `api.get('/api/empresas/')` para buscar a lista de empresas e `api.delete('/api/transportador/empresas/empresas/${id}/')` para exclusão. Também há chamadas para ativar/desativar empresas.
*   **`FiliaisList.jsx`**: Utiliza `api.get('/api/empresas/')` para buscar as empresas (para o filtro) e `api.get('/api/filiais/')` ou `/api/filiais/?empresa_id=${selectedEmpresa}` para buscar as filiais. A exclusão é feita via `api.delete('/api/filiais/${id}/')`.

### 4. Erros e Inconsistências Identificados

Durante a análise e os testes, foram observados os seguintes pontos:

#### 4.1. Erro ao Carregar Filiais

*   **Descrição**: Ao navegar para a seção "Filiais" no painel do transportador, o sistema exibe a mensagem "Erro ao carregar filiais".
*   **Análise**: O componente `FiliaisList.jsx` tenta buscar filiais através do endpoint `/api/filiais/` ou `/api/filiais/?empresa_id=${selectedEmpresa}`. O erro indica que a chamada a este endpoint falhou. Isso pode ser devido a:
    *   **Backend**: O endpoint `/api/filiais/` (que é mapeado via `backend.transportador.empresas.urls`) pode não estar retornando dados corretamente, ou pode haver um erro no `FilialViewSet` que impede a listagem.
    *   **Dados**: Pode não haver filiais cadastradas para a empresa do usuário logado, e o frontend não está tratando essa condição de forma graciosa (embora o código mostre um `EmptyState` para `filiais.length === 0`, o `setError` é acionado antes).
    *   **Permissões**: O usuário transportador pode não ter permissão para listar filiais através deste endpoint específico, ou a empresa/filial associada ao usuário não está configurada corretamente para permitir a consulta.

#### 4.2. Funcionalidades "Em Breve"

*   **Descrição**: Várias seções do painel do transportador, como "Financeiro", "Compras", "Eventos", "Relatórios" e "Configurações" (sub-item "Usuários e permissões"), exibem o status "em breve".
*   **Análise**: Isso indica que essas funcionalidades ainda não foram implementadas no frontend e/ou no backend. Embora não seja um "erro" no sentido de quebrar o sistema, representa uma inconsistência em relação a um sistema completo e funcional.

#### 4.3. Expiração de Sessão/Redirecionamento para Login

*   **Descrição**: Em alguns momentos durante a navegação, especialmente após um curto período de inatividade ou ao tentar acessar sub-rotas, o sistema redireciona o usuário de volta para a página de login.
*   **Análise**: Isso sugere que o tempo de expiração do token JWT (ou da sessão) pode ser muito curto, ou há um problema na renovação automática do token. O frontend pode não estar tratando adequadamente a expiração do token, resultando em redirecionamentos inesperados. Isso afeta a usabilidade e a fluidez da experiência do usuário.

### 5. Conclusão

O sistema XBPneus apresenta uma arquitetura Django-React bem definida, com modelos e URLs organizados. As relações entre `Empresa`, `Filial`, `Vehicle` e `MotoristaInterno` estão logicamente estabelecidas no backend. No entanto, existem inconsistências e erros que precisam ser abordados:

*   O erro ao carregar filiais é crítico e impede a visualização dessa seção. Requer depuração no backend (`FilialViewSet`) e/ou verificação de dados e permissões.
*   A grande quantidade de funcionalidades "em breve" indica que o sistema ainda está em desenvolvimento e muitas partes prometidas não estão acessíveis.
*   A gestão de sessão/autenticação no frontend precisa ser revisada para evitar redirecionamentos frequentes para a página de login, melhorando a experiência do usuário.

Recomenda-se priorizar a correção do erro de carregamento de filiais e a melhoria da gestão de sessão para garantir a estabilidade das funcionalidades existentes, antes de avançar na implementação das funcionalidades "em breve".
