# Instruções de Integração das Novas Funcionalidades

Este documento fornece instruções para integrar os novos componentes e rotas criados no sistema XBPneus.

## 1. Novos Componentes Criados

Os seguintes componentes foram criados e precisam ser integrados no `App.jsx`:

### 1.1. UserApprovalPage
- **Localização:** `frontend/src/pages/admin/UserApprovalPage.jsx`
- **Rota:** `/admin/usuarios/aprovacao`
- **Descrição:** Tela para aprovação de usuários recém-cadastrados
- **Acesso:** Apenas administradores

### 1.2. IntegrationsManagementPage
- **Localização:** `frontend/src/pages/admin/IntegrationsManagementPage.jsx`
- **Rota:** `/dashboard/configuracoes/integracoes`
- **Descrição:** Tela para gerenciar integrações com outros sistemas
- **Acesso:** Usuários autenticados com perfil de transportador

### 1.3. ProfileManagementPage
- **Localização:** `frontend/src/pages/ProfileManagementPage.jsx`
- **Rota:** `/dashboard/perfil`
- **Descrição:** Tela para gerenciar perfil do usuário e alterar senha
- **Acesso:** Usuários autenticados

### 1.4. ExportButtons (Componente Reutilizável)
- **Localização:** `frontend/src/components/ExportButtons.jsx`
- **Descrição:** Componente para exportar e imprimir relatórios
- **Uso:** Adicionar em telas de relatórios

## 2. Passos de Integração

### 2.1. Importar os Componentes no App.jsx

```javascript
import UserApprovalPage from './pages/admin/UserApprovalPage';
import IntegrationsManagementPage from './pages/admin/IntegrationsManagementPage';
import ProfileManagementPage from './pages/ProfileManagementPage';
```

### 2.2. Adicionar as Rotas no App.jsx

Adicionar as seguintes rotas dentro da estrutura de rotas existentes:

```javascript
// Rota de Aprovação de Usuários (Admin)
<Route path="/admin/usuarios/aprovacao" element={<ProtectedRoute><UserApprovalPage /></ProtectedRoute>} />

// Rota de Gerenciamento de Integrações
<Route path="/dashboard/configuracoes/integracoes" element={<ProtectedRoute><IntegrationsManagementPage /></ProtectedRoute>} />

// Rota de Gerenciamento de Perfil
<Route path="/dashboard/perfil" element={<ProtectedRoute><ProfileManagementPage /></ProtectedRoute>} />
```

### 2.3. Usar o Componente ExportButtons em Telas de Relatórios

```javascript
import ExportButtons from '../components/ExportButtons';

// Dentro do componente de relatório:
<ExportButtons 
  onExport={(format) => handleExport(format)} 
  onPrint={() => handlePrint()}
  reportName="Relatório de Frota"
/>
```

## 3. Conectar com Backend

Os componentes incluem chamadas de API comentadas que precisam ser descomentas e configuradas:

### 3.1. UserApprovalPage
- **GET** `/api/users/pending-approval/` - Listar usuários pendentes
- **POST** `/api/users/{userId}/approve/` - Aprovar usuário
- **POST** `/api/users/{userId}/reject/` - Rejeitar usuário

### 3.2. IntegrationsManagementPage
- **GET** `/api/transportador/integracoes/` - Listar integrações
- **POST** `/api/transportador/integracoes/{integrationId}/toggle/` - Ativar/Desativar integração

### 3.3. ProfileManagementPage
- **GET** `/api/auth/me/` - Obter informações do usuário
- **PUT** `/api/auth/me/` - Atualizar informações do usuário
- **POST** `/api/auth/change-password/` - Alterar senha

## 4. Testes Recomendados

1. Verificar se as rotas são acessíveis
2. Testar os filtros e buscas em UserApprovalPage
3. Verificar o funcionamento dos botões de aprovação/rejeição
4. Testar a ativação/desativação de integrações
5. Validar a edição de perfil e alteração de senha
6. Testar a responsividade em diferentes tamanhos de tela

## 5. Próximas Etapas

1. Descomentar e configurar as chamadas de API
2. Adicionar validações de formulário
3. Implementar tratamento de erros mais robusto
4. Adicionar confirmações de ação (modals de confirmação)
5. Implementar notificações de sucesso/erro
6. Realizar testes de integração com o backend

