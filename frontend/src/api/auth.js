import api from "./http";
import { jwtDecode } from "jwt-decode";

function persistSession(accessToken, refreshToken, userRoleFallback = "transportador") {
  if (!accessToken || !refreshToken) {
    throw new Error("Tokens de autenticação não recebidos.");
  }

  localStorage.setItem("access_token", accessToken);
  localStorage.setItem("refresh_token", refreshToken);

  let decodedToken = null;
  try {
    decodedToken = jwtDecode(accessToken);
  } catch (decodeError) {
    console.error("Falha ao decodificar token JWT:", decodeError);
    throw new Error("Token de acesso inválido recebido do servidor.");
  }

  const userRole = decodedToken.user_role || userRoleFallback;
  const userId = decodedToken.user_id;

  if (!userId) {
    throw new Error("Token de acesso não contém o identificador do usuário.");
  }

  localStorage.setItem("user_role", userRole);
  localStorage.setItem("user_id", userId);

  let redirectUrl = "/dashboard";
  if (userRole && userRole !== "transportador") {
    redirectUrl = `/${userRole}/dashboard`;
  }

  localStorage.setItem("redirect_url", redirectUrl);

  return { userRole, redirectUrl };
}

function wrapAndThrow(error) {
  if (error.response) {
    const message = error.response.data?.error || error.response.data?.detail;
    if (message) {
      const wrappedError = new Error(message);
      wrappedError.response = error.response;
      throw wrappedError;
    }
  }
  throw error;
}

export async function login(email, password) {
  const timestamp = Date.now();

  try {
    const { data } = await api.post(`/api/token/?t=${timestamp}`, { email, password });
    return persistSession(data.access, data.refresh);
  } catch (primaryError) {
    const status = primaryError.response?.status;

    if (status === 400 || status === 401 || status === 404) {
      try {
        const { data } = await api.post(`/api/motorista/login/?t=${timestamp}`, { email, password });
        const tokens = data.tokens || {};
        const session = persistSession(tokens.access, tokens.refresh, "motorista");

        // Se o backend informar uma URL específica de redirecionamento, priorize-a
        const redirectUrl = data.redirect || session.redirectUrl;
        localStorage.setItem("redirect_url", redirectUrl);

        return { userRole: session.userRole, redirectUrl };
      } catch (motoristaError) {
        console.error("Erro no login do motorista:", motoristaError);
        wrapAndThrow(motoristaError);
      }
    }

    console.error("Erro no login principal:", primaryError);
    wrapAndThrow(primaryError);
  }
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user_role");
  localStorage.removeItem("user_id");
  localStorage.removeItem("user_data");
  localStorage.removeItem("redirect_url");
}

export function getAccessToken() {
  return localStorage.getItem("access_token");
}

export function getRefreshToken() {
  return localStorage.getItem("refresh_token");
}

export function getUserRole() {
  return localStorage.getItem("user_role");
}

export function getUserId() {
  return localStorage.getItem("user_id");
}

export function getUserData() {
  const data = localStorage.getItem("user_data");
  return data ? JSON.parse(data) : null;
}

/**
 * Valida se o token JWT é válido e não expirou
 */
export function isTokenValid() {
  const token = localStorage.getItem("access_token");
  if (!token) return false;
  
  try {
    const decoded = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    const isValid = decoded.exp > currentTime;
    
    if (!isValid) {
      console.warn("Token expirado ou inválido");
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user_role");
      localStorage.removeItem("user_id");
    }
    
    return isValid;
  } catch (e) {
    console.error("Erro ao validar token:", e);
    return false;
  }
}

/**
 * Configura um intervalo para renovar o token automaticamente antes de expirar
 */
export function setupTokenRefreshInterval() {
  const interval = setInterval(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const decoded = jwtDecode(token);
        const currentTime = Date.now() / 1000;
        const timeUntilExpiry = (decoded.exp - currentTime) * 1000;
        
        // Se faltam menos de 5 minutos para expirar, renovar
        if (timeUntilExpiry > 0 && timeUntilExpiry < 5 * 60 * 1000) {
          console.log("Renovando token automaticamente...");
          refreshToken();
        }
      } catch (e) {
        console.error("Erro ao verificar expiração do token:", e);
      }
    }
  }, 60000); // Verificar a cada minuto
  
  return interval;
}

/**
 * Renova o token de acesso usando o refresh token
 */
export async function refreshToken() {
  try {
    const refresh = localStorage.getItem("refresh_token");
    if (!refresh) {
      throw new Error("Refresh token não disponível");
    }
    
    const { data } = await api.post("/api/token/refresh/", { refresh });
    if (data.access) {
      localStorage.setItem("access_token", data.access);
      console.log("Token renovado com sucesso");
      return true;
    }
  } catch (e) {
    console.error("Erro ao renovar token:", e);
    logout();
    return false;
  }
}

