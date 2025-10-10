import { useEffect, useState } from "react";
import api from "../api/http";

export default function TransportadorDashboard() {
  const [veiculos, setVeiculos] = useState([]);
  const [erro, setErro] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const empresa_id = getEmpresaId();
        const { data } = await api.get(`/api/transportador/frota/veiculos/?empresa_id=${empresa_id}`);
        setVeiculos(data);
      } catch (e) {
        setErro("Erro ao carregar veículos. Faça login.");
      }
    })();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Transportador — Veículos</h1>
      {erro && <div className="text-red-600 text-sm">{erro}</div>}
      <ul className="space-y-2">
        {veiculos.map(v => (
          <li key={v.id} className="border p-3 rounded">
            <div className="font-semibold">{v.placa}</div>
            <div className="text-sm text-gray-600">{v.marca || ""} {v.modelo || ""} — eixos: {v.eixos_total}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
