import { useState, useEffect } from "react";
import useTryFetch from "../../../hooks/useTryFetch";
import DataTable from "../../../components/DataTable";
import ColumnPicker from "../../../components/ColumnPicker";
import ServerExportButtons from "../../../components/ServerExportButtons";
import ExportButton from "../../../components/ExportButton";
import Loader from "../../../components/Loader";
import ErrorState from "../../../components/ErrorState";
import EmptyState from "../../../components/EmptyState";
import PageHeader from "../../../components/PageHeader";

const CANDIDATES = ["/api/transportador/frota/veiculos/", "/api/frota/veiculos/", "/api/veiculos/"];
const MOCK = ()=>[{ id:1, placa:'ABC1D23', modelo:'Cavalo Mecânico', km:458200, motorista:'João Silva' }];

export default function ListPage(){
  const [q, setQ] = useState("");
  const [ordering, setOrdering] = useState("placa");

  const [placa, setPlaca] = useState("");
  const [modelo, setModelo] = useState("");
  const [motorista, setMotorista] = useState("");
  const params = {};
  if (q) params.search = q;
  if (ordering) params.ordering = ordering;
  if (placa) params.placa = placa;
  if (modelo) params.modelo = modelo;
  if (motorista) params.motorista = motorista;
  const { data, error, loading, simulated, usedEndpoint, meta, page, setPage } = useTryFetch(CANDIDATES, { mock: MOCK, params, paginated: true, initialPage: 1, pageSize: 20 });

  const cols = [{"key": "id", "label": "ID"}, {"key": "placa", "label": "Placa"}, {"key": "modelo", "label": "Modelo"}, {"key": "km", "label": "Km"}, {"key": "motorista", "label": "Motorista"}, {"key":"acao","label":"Ação","linkTo":"/app/transportador/frota/veiculos/:id"}];
  const [selectedCols, setSelectedCols] = useState(cols.map(c=>c.label));
  useEffect(()=>{ try{ const saved = localStorage.getItem('cols:'+window.location.pathname); if(saved){ setSelectedCols(JSON.parse(saved)); } }catch{} }, []);
  const visibleCols = cols.filter(c => selectedCols.includes(c.label));


  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <PageHeader 
        title="Veículos" 
        subtitle="Gestão da frota de veículos"
      >
        {usedEndpoint && (
          <span className="text-xs text-gray-500">
            Endpoint: {usedEndpoint}
          </span>
        )}
        {simulated && (
          <span className="text-xs text-orange-500 font-medium">
            ⚠️ Modo simulado
          </span>
        )}
      </PageHeader>

      {/* Filtros e controles */}
      <div className="bg-white rounded-xl shadow-md p-4 mb-6">
        <div className="flex flex-wrap items-center gap-3">
          {/* Busca geral */}
          <input 
            value={q} 
            onChange={e=>setQ(e.target.value)} 
            placeholder="🔍 Buscar placa/modelo/motorista" 
            className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 min-w-[200px]"
          />
          
          {/* Ordenação */}
          <select 
            value={ordering} 
            onChange={e=>setOrdering(e.target.value)} 
            className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="placa">Ordem: Placa ↑</option>
            <option value="-placa">Ordem: Placa ↓</option>
            <option value="km">Ordem: KM ↑</option>
            <option value="-km">Ordem: KM ↓</option>
            <option value="id">Ordem: ID ↑</option>
            <option value="-id">Ordem: ID ↓</option>
          </select>
          
          {/* Itens por página */}
          <select 
            onChange={e=>setPageSize(parseInt(e.target.value,10))} 
            className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="20">20/página</option>
            <option value="50">50/página</option>
            <option value="100">100/página</option>
          </select>
          
          {/* Botão de exportação */}
          <ExportButton 
            columns={cols.filter(c=>!c.linkTo)} 
            rows={data || []} 
            filename="veiculos.csv" 
          />
        </div>
        
        {/* Filtros específicos */}
        <div className="flex flex-wrap items-center gap-3 mt-3">
          <input 
            value={placa} 
            onChange={e=>setPlaca(e.target.value)} 
            placeholder="Filtrar por placa" 
            className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input 
            value={modelo} 
            onChange={e=>setModelo(e.target.value)} 
            placeholder="Filtrar por modelo" 
            className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input 
            value={motorista} 
            onChange={e=>setMotorista(e.target.value)} 
            placeholder="Filtrar por motorista" 
            className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* Estados de carregamento/erro */}
      {loading && <Loader />}
      {error && <ErrorState message="Falha ao carregar veículos." />}
      {!loading && !error && (!data || data.length === 0) && <EmptyState />}
      
      {/* Tabela de dados */}
      {!loading && !error && data && data.length > 0 && (
        <div className="mb-6">
          <DataTable columns={visibleCols} rows={data} />
        </div>
      )}

      {/* Paginação */}
      {!loading && !error && data && data.length > 0 && (
        <div className="flex items-center justify-between bg-white rounded-xl shadow-md p-4">
          <button 
            onClick={()=>setPage(p=> Math.max(1, p-1))} 
            disabled={!meta.previous} 
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium disabled:opacity-40 disabled:cursor-not-allowed hover:opacity-90 transition-opacity"
          >
            ← Anterior
          </button>
          
          <div className="text-sm text-gray-700 font-medium">
            Página {meta.page}
            {meta.count !== null && ` · Total: ${meta.count} registros`}
          </div>
          
          <button 
            onClick={()=>setPage(p=> meta.next ? p+1 : p)} 
            disabled={!meta.next} 
            className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium disabled:opacity-40 disabled:cursor-not-allowed hover:opacity-90 transition-opacity"
          >
            Próxima →
          </button>
        </div>
      )}
    </div>
  );
}
