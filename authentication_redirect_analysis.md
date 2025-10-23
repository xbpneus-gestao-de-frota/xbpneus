# Análise de Problemas de Redirecionamento para Tela de Login

## Resumo Executivo

Após análise aprofundada do código do frontend e backend do sistema XBPneus, foram identificados **problemas potenciais** no fluxo de autenticação e redirecionamento que podem causar redirecionamentos inesperados para a tela de login ao clicar em botões. Este documento detalha os problemas encontrados, suas causas raiz e recomendações de correção.

---

## 1. Problemas Identificados

### 1.1. Problema: Token JWT Inválido ou Expirado

**Localização:** `frontend/src/api/http.js` (linhas 31-65)

**Descrição:** O interceptor de resposta do Axios está configurado para redirecionar para `/login` quando recebe um erro 401 (Unauthorized). Isso ocorre quando:

*   O token de acesso expirou
*   O token é inválido
*   O servidor retorna 401 por qualquer motivo

**Causa Raiz:** Se o backend não está renovando corretamente os tokens ou se o token expirou, qualquer clique em um botão que dispare uma requisição HTTP resultará em um erro 401, causando o redirecionamento para login.

**Código Problemático:**
```javascript
if (error.response && error.response.status === 401) {
  // ... tenta renovar o token
  if (!refresh) {
    localStorage.removeItem("access_token");
    window.location.href = "/login";  // Redirecionamento para login
    return Promise.reject(error);
  }
}
```

**Impacto:** Usuários são redirecionados para login mesmo que tenham acabado de fazer login.

---

### 1.2. Problema: Role do Usuário Não Configurado Corretamente

**Localização:** `frontend/src/api/auth.js` (linhas 20-32)

**Descrição:** A função `persistSession` tenta extrair o `user_role` do token JWT decodificado. Se o token não contiver este campo, usa um valor padrão ("transportador").

**Causa Raiz:** Se o backend não está incluindo o campo `user_role` no token JWT, o frontend não consegue determinar corretamente o tipo de usuário, causando redirecionamentos incorretos.

**Código Problemático:**
```javascript
const userRole = decodedToken.user_role || userRoleFallback;
```

**Impacto:** Usuários podem ser redirecionados para o dashboard errado ou para login se o role não for identificado.

---

### 1.3. Problema: ProtectedRoute Não Valida Corretamente o Token

**Localização:** `frontend/src/components/ProtectedRoute.jsx` (linhas 10-23)

**Descrição:** O componente `ProtectedRoute` verifica apenas se o token existe no localStorage e se o role está definido. Não valida se o token é válido ou se ainda não expirou.

**Causa Raiz:** Um token expirado pode estar presente no localStorage, causando que o componente permita a navegação, mas as requisições HTTP subsequentes falhem com 401.

**Código Problemático:**
```javascript
const token = localStorage.getItem("access_token");
const userRole = getUserRole();

if (!token) {
  return <Navigate to="/login" replace />;
}
```

**Impacto:** Usuários conseguem navegar para páginas protegidas, mas são redirecionados para login ao clicar em botões que disparam requisições.

---

### 1.4. Problema: Falta de Validação de Token na Função `getUserRole`

**Localização:** `frontend/src/api/auth.js` (linhas 100-102)

**Descrição:** A função `getUserRole` apenas retorna o valor armazenado no localStorage sem validar se o token é válido.

**Causa Raiz:** Não há verificação se o token ainda é válido antes de retornar o role.

**Código Problemático:**
```javascript
export function getUserRole() {
  return localStorage.getItem("user_role");
}
```

**Impacto:** O frontend pode pensar que o usuário está autenticado quando na verdade o token expirou.

---

### 1.5. Problema: RequireAuth Não Valida Token

**Localização:** `frontend/src/components/RequireAuth.jsx` (linhas 2-7)

**Descrição:** O componente `RequireAuth` apenas verifica se o token existe, sem validar sua validade.

**Causa Raiz:** Similar ao problema 1.3, não há validação do token.

**Código Problemático:**
```javascript
const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
if (!token) return <Navigate to="/login" state={{ from: loc }} replace />;
```

**Impacto:** Permite navegação com tokens expirados.

---

### 1.6. Problema: Falta de Tratamento de Erro 403 (Forbidden)

**Localização:** `frontend/src/api/http.js` (linhas 24-68)

**Descrição:** O interceptor de resposta só trata erro 401 (Unauthorized). Se o backend retorna 403 (Forbidden) por falta de permissão, o erro não é tratado adequadamente.

**Causa Raiz:** Não há tratamento específico para 403.

**Impacto:** Usuários podem ver mensagens de erro genéricas ou comportamento inesperado quando não têm permissão para acessar um recurso.

---

## 2. Fluxo de Autenticação Esperado vs. Atual

### Fluxo Esperado:
1. Usuário faz login com email e senha
2. Backend valida credenciais e retorna tokens (access e refresh)
3. Frontend armazena tokens no localStorage
4. Usuário é redirecionado para o dashboard apropriado
5. Ao clicar em botões, requisições são feitas com o token no header
6. Se o token expirar, o frontend tenta renovar automaticamente
7. Se a renovação falhar, o usuário é redirecionado para login

### Fluxo Atual (Problemático):
1. Usuário faz login ✓
2. Backend retorna tokens ✓
3. Frontend armazena tokens ✓
4. Usuário é redirecionado para dashboard ✓
5. Ao clicar em botões, requisições são feitas ✓
6. **Se o token expirou ou é inválido, erro 401 é retornado**
7. **Frontend redireciona para login mesmo que o token deveria ser renovado**

---

## 3. Recomendações de Correção

### 3.1. Validar Token Antes de Usar

**Arquivo:** `frontend/src/api/auth.js`

**Ação:** Adicionar função para validar se o token é válido e não expirou.

```javascript
export function isTokenValid() {
  const token = localStorage.getItem("access_token");
  if (!token) return false;
  
  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    return decoded.exp > currentTime;
  } catch (e) {
    return false;
  }
}
```

### 3.2. Melhorar ProtectedRoute

**Arquivo:** `frontend/src/components/ProtectedRoute.jsx`

**Ação:** Validar se o token é válido antes de permitir acesso.

```javascript
import { isTokenValid } from "../api/auth";

export default function ProtectedRoute({ children, allowedRoles = [] }) {
  const token = localStorage.getItem("access_token");
  const userRole = getUserRole();

  if (!token || !isTokenValid()) {
    return <Navigate to="/login" replace />;
  }

  if (!userRole) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
    const dashboard = getDefaultDashboard(userRole);
    return <Navigate to={dashboard} replace />;
  }

  return children;
}
```

### 3.3. Melhorar Interceptor de Resposta

**Arquivo:** `frontend/src/api/http.js`

**Ação:** Adicionar logging melhorado e tratamento de 403.

```javascript
api.interceptors.response.use(
  (resp) => resp,
  async (error) => {
    const original = error.config;
    
    // Tratamento de 403 (Forbidden)
    if (error.response && error.response.status === 403) {
      console.error("Acesso negado:", error.response.data);
      return Promise.reject(error);
    }
    
    // Tratamento de 401 (Unauthorized)
    if (error.response && error.response.status === 401) {
      // ... resto do código
    }
    
    return Promise.reject(error);
  }
);
```

### 3.4. Adicionar Refresh Token Automático

**Arquivo:** `frontend/src/api/auth.js`

**Ação:** Implementar refresh automático de token antes de expirar.

```javascript
export function setupTokenRefreshInterval() {
  setInterval(() => {
    const token = localStorage.getItem("access_token");
    if (token && isTokenValid()) {
      const decoded = jwtDecode(token);
      const timeUntilExpiry = (decoded.exp * 1000) - Date.now();
      
      // Se faltam menos de 5 minutos para expirar, renovar
      if (timeUntilExpiry < 5 * 60 * 1000) {
        refreshToken();
      }
    }
  }, 60000); // Verificar a cada minuto
}
```

### 3.5. Verificar Resposta do Backend

**Verificação Necessária:**

*   Confirmar que o backend está incluindo `user_role` no token JWT
*   Confirmar que o backend está retornando tokens válidos e com tempo de expiração apropriado
*   Verificar se o endpoint `/api/token/refresh/` está funcionando corretamente
*   Verificar se o backend está retornando 401 quando o token é inválido

---

## 4. Checklist de Testes

Após implementar as correções, realizar os seguintes testes:

- [ ] Fazer login e verificar se o token é armazenado corretamente
- [ ] Verificar se o token contém o campo `user_role`
- [ ] Clicar em botões de navegação e verificar se as requisições são bem-sucedidas
- [ ] Aguardar a expiração do token e verificar se o frontend redireciona para login
- [ ] Testar o refresh automático de token
- [ ] Testar logout e verificar se o token é removido
- [ ] Testar acesso a rotas não permitidas para o tipo de usuário
- [ ] Testar em diferentes navegadores e dispositivos

---

## 5. Conclusão

O sistema XBPneus possui uma estrutura de autenticação bem definida, mas há problemas na validação e renovação de tokens que causam redirecionamentos inesperados para a tela de login. As recomendações acima devem ser implementadas para melhorar a experiência do usuário e a confiabilidade do sistema.

A prioridade deve ser:
1. **Imediata:** Validar se o backend está incluindo `user_role` no token
2. **Alta:** Implementar validação de token no frontend
3. **Alta:** Melhorar o interceptor de resposta com logging
4. **Média:** Implementar refresh automático de token
5. **Média:** Adicionar tratamento de 403

---

## Referências

*   Arquivo de Autenticação: `frontend/src/api/auth.js`
*   Arquivo de HTTP: `frontend/src/api/http.js`
*   Componente ProtectedRoute: `frontend/src/components/ProtectedRoute.jsx`
*   Componente RequireAuth: `frontend/src/components/RequireAuth.jsx`
*   Configuração de Permissões: `frontend/src/config/permissions.js`

