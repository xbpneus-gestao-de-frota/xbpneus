import { NavLink } from "react-router-dom";
const items = [
  { to: "/dashboard", label: "Início" },
  { to: "/dashboard/frota", label: "Frota" },
  { to: "/dashboard/pneus", label: "Pneus" },
  { to: "/dashboard/estoque", label: "Estoque" },
  { to: "/dashboard/manutencao", label: "Manutenção" },
  { to: "/dashboard/ia", label: "🤖 IA - Análise", highlight: true },
  { to: "/dashboard/financeiro", label: "Financeiro" },
  { to: "/dashboard/compras", label: "Compras" },
  { to: "/dashboard/eventos", label: "Eventos" },
  { to: "/dashboard/relatorios", label: "Relatórios" },
  { to: "/dashboard/configuracoes", label: "Configurações" },
];
export default function Sidebar(){
  return (
    <aside className="w-60 shrink-0 border-r border-white/10 bg-white/[0.04]">
      <div className="p-4 font-extrabold bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>XBPNEUS</div>
      <nav className="p-2 space-y-1">
        {items.map(it => (
          <NavLink 
            key={it.to} 
            to={it.to} 
            className={({isActive}) => 
              "block px-3 py-2 rounded-lg hover:bg-white/10 " + 
              (isActive ? "bg-white/10 " : "") +
              (it.highlight ? "font-bold bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-blue-400/30" : "")
            }
          >
            {it.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
