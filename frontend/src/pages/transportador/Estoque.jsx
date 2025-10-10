import ActionGrid from "../../components/ActionGrid";
export default function Estoque() {
  const actions = [{ label: "Movimentações", to: "movimentacoes", desc: "Entradas/Saídas/Transferências." }];
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>Estoque</h1>
      <ActionGrid actions={actions} />
    </section>
  );
}
