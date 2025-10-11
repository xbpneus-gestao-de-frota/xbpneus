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

export default function Sidebar() {
  return (
    <aside className="w-60 shrink-0 bg-[#1A237E] text-white shadow-lg">
      {/* Logo com degradê */}
      <div 
        className="p-4 font-black text-2xl text-center border-b border-white/20"
        style={{
          background: 'linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          letterSpacing: '0.05em',
        }}
      >
        XBPNEUS
      </div>
      
      {/* Menu de navegação */}
      <nav className="p-2 space-y-1">
        {items.map(it => (
          <NavLink 
            key={it.to} 
            to={it.to} 
            className={({isActive}) => 
              "block px-4 py-3 rounded-lg transition-all duration-200 " + 
              (isActive 
                ? "bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-semibold shadow-md" 
                : "hover:bg-[#3949AB] text-white/90"
              ) +
              (it.highlight ? " font-bold border-2 border-blue-400/50" : "")
            }
          >
            {it.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
