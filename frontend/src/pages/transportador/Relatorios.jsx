import ActionGrid from "../../components/ActionGrid";
export default function Relatorios() {
  const actions = [{ label: "Dashboards", to: "#", desc: "Em breve", disabled: true }];
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>Relatórios</h1>
      <ActionGrid actions={actions} />
    </section>
  );
}
