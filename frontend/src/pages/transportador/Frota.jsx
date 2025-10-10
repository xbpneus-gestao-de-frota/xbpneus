import ActionGrid from "../../components/ActionGrid";
export default function Frota() {
  const actions = [
    { label: "Veículos", to: "veiculos", desc: "Listagem e detalhes dos veículos." },
    { label: "Posições", to: "posicoes", desc: "Mapa de posições por eixo/lado." }
  ];
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>Frota</h1>
      <ActionGrid actions={actions} />
    </section>
  );
}
