import ActionGrid from "../../components/ActionGrid";
export default function Pneus() {
  const actions = [
    { label: "Lista de Pneus", to: "lista", desc: "Todos os pneus cadastrados." },
    { label: "Aplicações", to: "aplicacoes", desc: "Aplicações por medida/operação." }
  ];
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>Pneus</h1>
      <ActionGrid actions={actions} />
    </section>
  );
}
