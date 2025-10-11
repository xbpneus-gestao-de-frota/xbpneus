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
          <Card title="Total Veículos" value={m.frota.total_veiculos} />
          <Card title="Veículos Ativos" value={m.frota.veiculos_ativos} />
          <Card title="Total Posições" value={m.pneus.total_posicoes} />
          <Card title="Posições Ocupadas" value={m.pneus.posicoes_ocupadas} />
          <Card title="OS Abertas" value={m.manutencao.os_abertas} />
          <Card title="OS Em Andamento" value={m.manutencao.os_em_andamento} />
          <Card title="Entradas (30d)" value={m.estoque.entradas_30d} />
          <Card title="Saídas (30d)" value={m.estoque.saidas_30d} />
        </div>
      )}
    </section>
  );
}
