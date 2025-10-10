import ActionGrid from "../../components/ActionGrid";
export default function Manutencao() {
  const actions = [
    { label: "Ordens de Serviço", to: "os", desc: "Corretivas/Preventivas." },
    { label: "Testes Pós-Manutenção", to: "testes", desc: "Torque, pressão e rodagem." }
  ];
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent" style={{ backgroundImage: "var(--xbp-grad)" }}>Manutenção</h1>
      <ActionGrid actions={actions} />
    </section>
  );
}
