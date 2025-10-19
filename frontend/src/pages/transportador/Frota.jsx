import ActionGrid from "../../components/ActionGrid";
import PageHeader from "../../components/PageHeader";

export default function Frota() {
  const actions = [
    { label: "Veículos", to: "veiculos", desc: "Listagem e detalhes dos veículos." },
    { label: "Posições", to: "posicoes", desc: "Mapa de posições por eixo/lado." },
    { label: "Motoristas", to: "motoristas", desc: "Gerencie a equipe de motoristas e suas informações." },
    { label: "Implementos", to: "implementos", desc: "Controle seus implementos e equipamentos adicionais." },
    { label: "Documentos", to: "documentos", desc: "Organize e acesse os documentos da sua frota." },
    { label: "Rastreamento", to: "rastreamento", desc: "Monitore seus veículos em tempo real no mapa." },
  ];

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader
        title="Gestão de Frota"
        subtitle="Gerencie seus veículos, motoristas e operações em tempo real"
      />
      <div className="mt-8">
        <ActionGrid actions={actions} />
      </div>
    </div>
  );
}

