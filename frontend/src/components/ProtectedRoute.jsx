import { Navigate } from "react-router-dom";
import { getUserRole } from "../api/auth";
import { hasPermission, getDefaultDashboard } from "../config/permissions";

/**
 * Componente para proteger rotas baseado no role do usuário
 * Redireciona para o dashboard correto se o usuário não tiver permissão
 */
export default function ProtectedRoute({ children, allowedRoles = [] }) {
  const token = localStorage.getItem("access_token");
  const userRole = getUserRole();

  console.log("ProtectedRoute: Token", token ? "Present" : "Absent");
  console.log("ProtectedRoute: User Role", userRole);

  // Se não estiver autenticado, redireciona para login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Se não tiver role definido, redireciona para login
  if (!userRole) {
    return <Navigate to="/login" replace />;
  }

  // Se a rota tem restrição de roles e o usuário não está na lista
  if (allowedRoles.length > 0 && !allowedRoles.includes(userRole)) {
    // Redireciona para o dashboard correto do usuário
    const dashboard = getDefaultDashboard(userRole);
    return <Navigate to={dashboard} replace />;
  }

  return children;
}

