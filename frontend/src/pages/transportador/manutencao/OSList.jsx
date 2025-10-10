import { useState, useEffect } from "react";
import useTryFetch from "../../../hooks/useTryFetch";
import DataTable from "../../../components/DataTable";
import ColumnPicker from "../../../components/ColumnPicker";
import ServerExportButtons from "../../../components/ServerExportButtons";
import ExportButton from "../../../components/ExportButton";
import Loader from "../../../components/Loader";
import ErrorState from "../../../components/ErrorState";
import EmptyState from "../../../components/EmptyState";

const CANDIDATES = ["/api/transportador/manutencao/os/", "/api/manutencao/os/"];
const MOCK = ()=>[{ id:401, tipo:'Corretiva', status:'Aguardando Peça', veiculo:'ABC1D23', agendamento:'2025-10-06' }];

export default function ListPage(){
  const [q, setQ] = useState("");
  const [ordering, setOrdering] = useState("agendamento");

  const [tipo, setTipo] = useState("");
  const [status, setStatus] = useState("");
  const [veiculo, setVeiculo] = useState("");
  const params = {};
  if (q) params.search = q;
  if (ordering) params.ordering = ordering;
  if (tipo) params.tipo = tipo;
  if (status) params.status = status;
  if (veiculo) params.veiculo = veiculo;
  const { data, error, loading, simulated, usedEndpoint, meta, page, setPage } = useTryFetch(CANDIDATES, { mock: MOCK, params, paginated: true, initialPage: 1, pageSize: 20 });

  const cols = [{"key": "id", "label": "ID"}, {"key": "tipo", "label": "Tipo"}, {"key": "status", "label": "Status"}, {"key": "veiculo", "label": "Veículo"}, {"key": "agendamento", "label": "Agendamento"}];
  const [selectedCols, setSelectedCols] = useState(cols.map(c=>c.label));
  useEffect(()=>{ try{ const saved = localStorage.getItem('cols:'+window.location.pathname); if(saved){ setSelectedCols(JSON.parse(saved)); } }catch{} }, []);
  const visibleCols = cols.filter(c => selectedCols.includes(c.label));


  return (
    <section>
      <div className="flex items-baseline justify-between mb-3">
        <h2 className="text-xl font-bold">Ordens de Serviço</h2>
        <div className="text-xs opacity-60">{ usedEndpoint ? `Endpoint: { usedEndpoint }` : simulated ? "Modo simulado" : "" }</div>
      </div>

      <div className="flex flex-wrap items-center gap-2 mb-3">
        <input value={ q } onChange={ e=>setQ(e.target.value) } placeholder="Buscar tipo/status/veículo" className="px-3 py-2 rounded-lg bg-white/10 border border-white/10" />
        <select value={ ordering } onChange={ e=>setOrdering(e.target.value) } className="px-3 py-2 rounded-lg bg-white/10 border border-white/10">
          <option value="agendamento">Ordem: Agendamento ↑</option>
          <option value="-agendamento">Ordem: Agendamento ↓</option>
          <option value="status">Ordem: Status ↑</option>
          <option value="-status">Ordem: Status ↓</option>
          <option value="id">Ordem: ID ↑</option>
          <option value="-id">Ordem: ID ↓</option>
        </select>
        <select onChange={e=>setPageSize(parseInt(e.target.value,10))} className="px-3 py-2 rounded-lg bg-white/10 border border-white/10">
          <option value="20">20/página</option>
          <option value="50">50/página</option>
          <option value="100">100/página</option>
        </select>
        <ExportButton columns={cols.filter(c=>!c.linkTo)} rows={data || []} filename="lista.csv" />

        <select value={tipo} onChange={e=>setTipo(e.target.value)} className="px-3 py-2 rounded-lg bg-white/10 border border-white/10">
          <option value="">Tipo</option>
          <option value="Corretiva">Corretiva</option>
          <option value="Preventiva">Preventiva</option>
        </select>
        <input value={status} onChange={e=>setStatus(e.target.value)} placeholder="Status" className="px-3 py-2 rounded-lg bg-white/10 border border-white/10" />
        <input value={veiculo} onChange={e=>setVeiculo(e.target.value)} placeholder="Veículo (placa)" className="px-3 py-2 rounded-lg bg-white/10 border border-white/10" />
      </div>

      { loading && <Loader /> }
      { error && <ErrorState message="Falha ao carregar." /> }
      { !loading && !error && (!data || data.length === 0) && <EmptyState /> }
      { !loading && !error && data && data.length > 0 && <DataTable columns={ visibleCols } rows={ data } /> }

      <div className="flex items-center gap-2 mt-3">
        <button onClick={ ()=>setPage(p=> Math.max(1, p-1)) } disabled={ !meta.previous } className="px-3 py-2 rounded-lg border border-white/10 bg-white/10 disabled:opacity-40">Anterior</button>
        <div className="text-sm opacity-80">Página { meta.page }{ meta.count !== null ? ` · Total { meta.count }` : "" }</div>
        <button onClick={ ()=>setPage(p=> meta.next ? p+1 : p) } disabled={ !meta.next } className="px-3 py-2 rounded-lg border border-white/10 bg-white/10 disabled:opacity-40">Próxima</button>
      </div>
    </section>
  );
}
