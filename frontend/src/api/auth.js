import api from "./http";

// Função para detectar o tipo de usuário pelo e-mail
function detectUserType(email) {
  // Verifica padrões no e-mail para determinar o tipo
  const lowerEmail = email.toLowerCase();
  
  if (lowerEmail.includes('transportador') || lowerEmail.includes('admin')) {
    return 'transportador';
  } else if (lowerEmail.includes('motorista')) {
    return 'motorista';
  } else if (lowerEmail.includes('borracharia')) {
    return 'borracharia';
  } else if (lowerEmail.includes('revenda')) {
    return 'revenda';
  } else if (lowerEmail.includes('recapagem')) {
    return 'recapagem';
  }
  
  // Se não conseguir detectar, tenta todos os endpoints
  return null;
}

export async function login(username, password){
  const userType = detectUserType(username);
  
  // Se conseguiu detectar o tipo, usa o endpoint específico
  if (userType) {
    const url = `/api/${userType}/login/`;
    try {
      const { data } = await api.post(url, { email: username, password });
      // A resposta vem com tokens.access e tokens.refresh
      const accessToken = data.tokens?.access || data.access;
      const refreshToken = data.tokens?.refresh || data.refresh;
      
      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("refresh_token", refreshToken);
      localStorage.setItem("user_role", userType);
      localStorage.setItem("user_data", JSON.stringify(data.user || {}));
      localStorage.setItem("redirect_url", data.redirect || `/${userType}/dashboard/`);
      return data;
    } catch (error) {
      console.error(`Erro no login (${userType}):`, error);
      throw error;
    }
  }
  
  // Se não conseguiu detectar, tenta todos os endpoints
  const types = ['transportador', 'motorista', 'borracharia', 'revenda', 'recapagem'];
  
  for (const type of types) {
    try {
      const url = `/api/${type}/login/`;
      const { data } = await api.post(url, { email: username, password });
      // A resposta vem com tokens.access e tokens.refresh
      const accessToken = data.tokens?.access || data.access;
      const refreshToken = data.tokens?.refresh || data.refresh;
      
      localStorage.setItem("access_token", accessToken);
      localStorage.setItem("refresh_token", refreshToken);
      localStorage.setItem("user_role", type);
      localStorage.setItem("user_data", JSON.stringify(data.user || {}));
      localStorage.setItem("redirect_url", data.redirect || `/${type}/dashboard/`);
      return data;
    } catch (error) {
      // Continua tentando outros tipos
      continue;
    }
  }
  
  // Se nenhum funcionou, lança erro
  throw new Error("Credenciais inválidas");
}

export function logout(){
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user_role");
  localStorage.removeItem("user_data");
}

export function getUserRole() {
  return localStorage.getItem("user_role");
}

export function getUserData() {
  const data = localStorage.getItem("user_data");
  return data ? JSON.parse(data) : null;
}

