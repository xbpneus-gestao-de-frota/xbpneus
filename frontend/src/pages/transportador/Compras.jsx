import ActionGrid from "../../components/ActionGrid";
export default function Compras() {
  const actions = [{ label: "Loja interna (em breve)", to: "#", desc: "Catálogo de pneus", disabled: true }];
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>Compras</h1>
      <ActionGrid actions={actions} />
    </section>
  );
}
