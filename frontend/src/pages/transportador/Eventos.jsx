import ActionGrid from "../../components/ActionGrid";
export default function Eventos() {
  const actions = [{ label: "Registro de eventos (em breve)", to: "#", disabled: true }];
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>Eventos</h1>
      <ActionGrid actions={actions} />
    </section>
  );
}
