import { useEffect, useState } from "react";
import api from "../api/http";

export default function TransportadorDashboard() {
  const [veiculos, setVeiculos] = useState([]);
  const [erro, setErro] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const empresa_id = localStorage.getItem('empresa_id');
        const { data } = await api.get(`/api/transportador/frota/veiculos/?empresa_id=${empresa_id}`);
        setVeiculos(data);
      } catch (e) {
        setErro("Erro ao carregar veículos. Faça login.");
      }
    })();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Header com degradê */}
      <div className="mb-8">
        <h1 
          className="text-4xl font-black mb-2"
          style={{
            background: 'linear-gradient(135deg, #60a5fa, #6366f1, #7c3aed)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}
        >
          Dashboard Transportador
        </h1>
        <p className="text-gray-600">Gestão de Veículos da Frota</p>
      </div>

      {/* Mensagem de erro */}
      {erro && (
        <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-lg">
          <p className="font-medium">⚠️ {erro}</p>
        </div>
      )}

      {/* Lista de veículos em cards */}
      {veiculos.length === 0 && !erro ? (
        <div className="text-center py-12 bg-white rounded-xl shadow-md">
          <p className="text-gray-500 text-lg">Nenhum veículo cadastrado</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {veiculos.map(v => (
            <div 
              key={v.id} 
              className="bg-white rounded-xl shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden border border-gray-200"
            >
              {/* Header do card com degradê */}
              <div 
                className="p-4 text-white"
                style={{
                  background: 'linear-gradient(to right, #60a5fa, #6366f1, #7c3aed)'
                }}
              >
                <h3 className="text-2xl font-bold">{v.placa}</h3>
              </div>
              
              {/* Conteúdo do card */}
              <div className="p-4 space-y-2">
                <div className="flex items-center text-gray-700">
                  <span className="font-medium mr-2">Marca:</span>
                  <span>{v.marca || "N/A"}</span>
                </div>
                <div className="flex items-center text-gray-700">
                  <span className="font-medium mr-2">Modelo:</span>
                  <span>{v.modelo || "N/A"}</span>
                </div>
                <div className="flex items-center text-gray-700">
                  <span className="font-medium mr-2">Eixos:</span>
                  <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded font-semibold">
                    {v.eixos_total}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
