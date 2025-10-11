import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useTryFetch from "../../../hooks/useTryFetch";
import DataTable from "../../../components/DataTable";
import ExportButton from "../../../components/ExportButton";
import Loader from "../../../components/Loader";
import ErrorState from "../../../components/ErrorState";
import EmptyState from "../../../components/EmptyState";
import PageHeader from "../../../components/PageHeader";
import api from "../../../api/http";

const CANDIDATES = ["/api/transportador/pneus/pneus/", "/api/transportador/pneus/", "/api/pneus/"];
const MOCK = ()=>[{ id:11, codigo:'XBRI-29580225', medida:'295/80R22.5', dot:'2424', status:'Em uso', posicao_atual:'Dianteiro Esq' }];

export default function ListPage(){
  const navigate = useNavigate();
  const [q, setQ] = useState("");
  const [ordering, setOrdering] = useState("codigo");
  const [deleting, setDeleting] = useState(null);

  const [medida, setMedida] = useState("");
  const [status, setStatus] = useState("");
  const params = {};
  if (q) params.search = q;
  if (ordering) params.ordering = ordering;
  if (medida) params.medida = medida;
  if (status) params.status = status;
  const { data, error, loading, simulated, usedEndpoint, meta, page, setPage } = useTryFetch(CANDIDATES, { mock: MOCK, params, paginated: true, initialPage: 1, pageSize: 20 });

  const handleDelete = async (id, codigo) => {
    if (!confirm(`Tem certeza que deseja excluir o pneu ${codigo}?`)) return;
    setDeleting(id);
    try {
      await api.delete(`/api/transportador/pneus/pneus/${id}/`);
      window.location.reload();
    } catch (ex) {
      alert("Erro ao excluir pneu.");
    } finally {
      setDeleting(null);
    }
  };

  const cols = [
    {"key": "id", "label": "ID"}, 
    {"key": "codigo", "label": "Código"}, 
    {"key": "medida", "label": "Medida"}, 
    {"key": "marca", "label": "Marca"},
    {"key": "tipo", "label": "Tipo"},
    {"key": "status", "label": "Status"}, 
    {"key": "posicao_atual", "label": "Posição"},
    {
      "key": "acoes",
      "label": "Ações",
      "render": (row) => (
        <div className="flex items-center gap-2">
          <button onClick={() => navigate(`/dashboard/pneus/${row.id}/edit`)} className="px-3 py-1 text-sm rounded bg-green-500 text-white hover:bg-green-600">Editar</button>
          <button onClick={() => handleDelete(row.id, row.codigo)} disabled={deleting === row.id} className="px-3 py-1 text-sm rounded bg-red-500 text-white hover:bg-red-600 disabled:opacity-50">{deleting === row.id ? "..." : "Excluir"}</button>
        </div>
      )
    }
  ];
  const [selectedCols, setSelectedCols] = useState(cols.map(c=>c.label));
  useEffect(()=>{ try{ const saved = localStorage.getItem('cols:'+window.location.pathname); if(saved){ setSelectedCols(JSON.parse(saved)); } }catch{} }, []);
  const visibleCols = cols.filter(c => selectedCols.includes(c.label));

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="flex items-center justify-between mb-6">
        <PageHeader title="Pneus" subtitle="Gestão de pneus">
          {usedEndpoint && <span className="text-xs text-gray-500">Endpoint: {usedEndpoint}</span>}
          {simulated && <span className="text-xs text-orange-500 font-medium">⚠️ Modo simulado</span>}
        </PageHeader>
        <button onClick={() => navigate("/dashboard/pneus/create")} className="px-6 py-3 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium hover:opacity-90 transition-opacity flex items-center gap-2">
          <span className="text-xl">+</span>Novo Pneu
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-md p-4 mb-6">
        <div className="flex flex-wrap items-center gap-3">
          <input value={q} onChange={e=>setQ(e.target.value)} placeholder="🔍 Buscar código/medida/status" className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 min-w-[200px]" />
          <select value={ordering} onChange={e=>setOrdering(e.target.value)} className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="codigo">Ordem: Código ↑</option>
            <option value="-codigo">Ordem: Código ↓</option>
            <option value="medida">Ordem: Medida ↑</option>
            <option value="-medida">Ordem: Medida ↓</option>
          </select>
          <ExportButton columns={cols.filter(c=>!c.render)} rows={data || []} filename="pneus.csv" />
        </div>
        <div className="flex flex-wrap items-center gap-3 mt-3">
          <input value={medida} onChange={e=>setMedida(e.target.value)} placeholder="Filtrar por medida" className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500" />
          <select value={status} onChange={e=>setStatus(e.target.value)} className="px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">Todos os status</option>
            <option value="ESTOQUE">Estoque</option>
            <option value="MONTADO">Montado</option>
            <option value="MANUTENCAO">Manutenção</option>
          </select>
        </div>
      </div>

      {loading && <Loader />}
      {error && <ErrorState message="Falha ao carregar pneus." />}
      {!loading && !error && (!data || data.length === 0) && <EmptyState />}
      {!loading && !error && data && data.length > 0 && (
        <div className="mb-6">
          <DataTable columns={visibleCols} rows={data} />
        </div>
      )}

      {!loading && !error && data && data.length > 0 && (
        <div className="flex items-center justify-between bg-white rounded-xl shadow-md p-4">
          <button onClick={()=>setPage(p=> Math.max(1, p-1))} disabled={!meta.previous} className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium disabled:opacity-40 disabled:cursor-not-allowed hover:opacity-90 transition-opacity">← Anterior</button>
          <div className="text-sm text-gray-700 font-medium">Página {meta.page}{meta.count !== null && ` · Total: ${meta.count} registros`}</div>
          <button onClick={()=>setPage(p=> meta.next ? p+1 : p)} disabled={!meta.next} className="px-4 py-2 rounded-lg bg-gradient-to-r from-blue-400 via-indigo-500 to-purple-600 text-white font-medium disabled:opacity-40 disabled:cursor-not-allowed hover:opacity-90 transition-opacity">Próxima →</button>
        </div>
      )}
    </div>
  );
}

