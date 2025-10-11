import api from "./http";
import { jwtDecode } from "jwt-decode";

export async function login(email, password) {
  try {
    // Adicionar timestamp para evitar cache
    const timestamp = Date.now();
    const { data } = await api.post(`/api/token/?t=${timestamp}`, { email, password });
    const accessToken = data.access;
    const refreshToken = data.refresh;

    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);

    // Decodificar o token para obter o user_id e user_role
    const decodedToken = jwtDecode(accessToken);
    const userRole = decodedToken.user_role; // Assumindo que o papel do usuário está no token
    const userId = decodedToken.user_id;

    localStorage.setItem("user_role", userRole);
    localStorage.setItem("user_id", userId);

    // Redirecionar para o dashboard apropriado com base no papel
    let redirectUrl = "/dashboard"; // Default
    if (userRole) {
      redirectUrl = `/${userRole}/dashboard`;
    }
    localStorage.setItem("redirect_url", redirectUrl);

    // Opcional: buscar dados completos do usuário se necessário
    // const userData = await api.get(`/api/users/${userId}/`);
    // localStorage.setItem("user_data", JSON.stringify(userData.data));

    return { userRole, redirectUrl };
  } catch (error) {
    console.error("Erro no login:", error);
    throw error;
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

