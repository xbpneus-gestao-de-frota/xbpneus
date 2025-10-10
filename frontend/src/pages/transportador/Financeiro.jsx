import ActionGrid from "../../components/ActionGrid";
export default function Financeiro() {
  const actions = [{ label: "Painel (em breve)", to: "#", desc: "Despesas, CPK, lançamentos.", disabled: true }];
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>Financeiro</h1>
      <ActionGrid actions={actions} />
    </section>
  );
}
