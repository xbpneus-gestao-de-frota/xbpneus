import { Navigate, useLocation } from "react-router-dom";
export default function RequireAuth({ children }){
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  const loc = useLocation();
  if (!token) return <Navigate to="/login" state={{ from: loc }} replace />;
  return children;
}
