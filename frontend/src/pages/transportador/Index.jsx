import React, { useState, useEffect } from 'react';
import api from "../../api/http";

function Card({ title, value }) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
      <div className="text-sm opacity-70">{title}</div>
      <div className="text-2xl font-extrabold">{value}</div>
    </div>
  );
}

export default function IndexTransportador(){
  const [m, setM] = useState(null);
  const [err, setErr] = useState(null);
  useEffect(()=>{
    let mounted = true;
    api.get("/api/transportador/dashboard/") // Corrigido para a rota correta
      .then(r => { if (mounted) setM(r.data); })
      .catch(e => { if (mounted) setErr(e); });
    return () => { mounted = false; }
  }, []);
  return (
    <section>
      <h1 className="text-3xl font-extrabold mb-4 bg-clip-text text-transparent"
          style={{ backgroundImage: "var(--xbp-grad)" }}>Painel do Transportador</h1>
      {err && <div className="text-sm text-red-400">Falha ao carregar métricas.</div>}
      {!m && !err && <div className="opacity-70 text-sm">Carregando métricas…</div>}
      {m && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card title="Veículos" value={m.vehicles} />
          <Card title="Posições" value={m.positions} />
          <Card title="Pneus" value={m.tires} />
          <Card title="Aplicações" value={m.applications} />
          <Card title="Mov. Estoque" value={m.stock_moves} />
          <Card title="OS" value={m.work_orders} />
          <Card title="Testes" value={m.tests} />
        </div>
      )}
    </section>
  );
}
