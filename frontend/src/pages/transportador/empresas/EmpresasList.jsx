<<<<<<< HEAD
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Plus, Building2, Edit, Trash2 } from 'lucide-react';
import api from '../../../api/http';

export default function EmpresasList() {
  const [empresas, setEmpresas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEmpresas();
  }, []);

  const fetchEmpresas = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/empresas/');
      setEmpresas(response.data);
      setError(null);
    } catch (err) {
      setError('Erro ao carregar empresas');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Tem certeza que deseja excluir esta empresa?')) {
      return;
    }

    try {
      await api.delete(`/api/empresas/${id}/`);
      fetchEmpresas();
    } catch (err) {
      alert('Erro ao excluir empresa');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Empresas (Matriz)</h1>
          <p className="text-gray-600 mt-1">Gerencie as empresas do sistema</p>
        </div>
        <Link
          to="/dashboard/empresas/create"
          className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus className="w-5 h-5 mr-2" />
          Nova Empresa
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Empresa
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                CNPJ
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Cidade/UF
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Contato
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ações
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {empresas.length === 0 ? (
              <tr>
                <td colSpan="6" className="px-6 py-12 text-center text-gray-500">
                  <Building2 className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                  <p>Nenhuma empresa cadastrada</p>
                </td>
              </tr>
            ) : (
              empresas.map((empresa) => (
                <tr key={empresa.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <div className="flex items-center">
                      <Building2 className="w-5 h-5 text-gray-400 mr-3" />
                      <div>
                        <div className="text-sm font-medium text-gray-900">
                          {empresa.nome_fantasia || empresa.razao_social}
                        </div>
                        {empresa.nome_fantasia && (
                          <div className="text-sm text-gray-500">{empresa.razao_social}</div>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">{empresa.cnpj}</td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    {empresa.cidade}/{empresa.uf}
                  </td>
                  <td className="px-6 py-4">
                    <div className="text-sm text-gray-900">{empresa.telefone_principal}</div>
                    <div className="text-sm text-gray-500">{empresa.email_principal}</div>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                        empresa.ativo
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {empresa.ativo ? 'Ativo' : 'Inativo'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right text-sm font-medium space-x-2">
                    <Link
                      to={`/dashboard/empresas/${empresa.id}/edit`}
                      className="inline-flex items-center text-blue-600 hover:text-blue-900"
                    >
                      <Edit className="w-4 h-4" />
                    </Link>
                    <button
                      onClick={() => handleDelete(empresa.id)}
                      className="inline-flex items-center text-red-600 hover:text-red-900"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
=======
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useTryFetch from "../../../hooks/useTryFetch";
import DataTable from "../../../components/DataTable";
import ColumnPicker from "../../../components/ColumnPicker";
import Loader from "../../../components/Loader";
import ErrorState from "../../../components/ErrorState";
import EmptyState from "../../../components/EmptyState";
import PageHeader from "../../../components/PageHeader";
import api from "../../../api/http";

const CANDIDATES = ["/api/transportador/empresas/empresas/", "/api/empresas/"];

export default function EmpresasList() {
  const navigate = useNavigate();
  const [q, setQ] = useState("");
  const [ordering, setOrdering] = useState("nome");
  const [deleting, setDeleting] = useState(null);
  const [tipo, setTipo] = useState("");
  const [ativa, setAtiva] = useState("");

  const params = {};
  if (q) params.search = q;
  if (ordering) params.ordering = ordering;
  if (tipo) params.tipo = tipo;
  if (ativa !== "") params.ativa = ativa;

  const { data, error, loading, usedEndpoint, meta, page, setPage } = useTryFetch(
    CANDIDATES,
    { params, paginated: true, initialPage: 1, pageSize: 20 }
  );

  const handleDelete = async (id, nome) => {
    if (!confirm(`Tem certeza que deseja excluir a empresa ${nome}?`)) return;

    setDeleting(id);
    try {
      await api.delete(`/api/transportador/empresas/empresas/${id}/`);
      window.location.reload();
    } catch (ex) {
      alert("Erro ao excluir empresa.");
      console.error(ex);
    } finally {
      setDeleting(null);
    }
  };

  const handleToggleAtiva = async (id, ativaAtual) => {
    try {
      const action = ativaAtual ? "desativar" : "ativar";
      await api.post(`/api/transportador/empresas/empresas/${id}/${action}/`);
      window.location.reload();
    } catch (ex) {
      alert("Erro ao alterar status da empresa.");
      console.error(ex);
    }
  };

  const cols = [
    { key: "id", label: "ID" },
    { key: "nome", label: "Nome" },
    { key: "tipo", label: "Tipo" },
    { key: "cnpj", label: "CNPJ" },
    { key: "cidade", label: "Cidade" },
    { key: "estado", label: "Estado" },
    { key: "total_filiais", label: "Filiais" },
    {
      key: "ativa",
      label: "Status",
      render: (row) => (
        <span
          className={`px-2 py-1 text-xs rounded ${
            row.ativa ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
          }`}
        >
          {row.ativa ? "Ativa" : "Inativa"}
        </span>
      ),
    },
    {
      key: "acoes",
      label: "Ações",
      render: (row) => (
        <div className="flex items-center gap-2">
          <button
            onClick={() => navigate(`/dashboard/empresas/${row.id}`)}
            className="px-3 py-1 text-sm rounded bg-blue-500 text-white hover:bg-blue-600"
          >
            Ver
          </button>
          <button
            onClick={() => navigate(`/dashboard/empresas/${row.id}/edit`)}
            className="px-3 py-1 text-sm rounded bg-green-500 text-white hover:bg-green-600"
          >
            Editar
          </button>
          <button
            onClick={() => handleToggleAtiva(row.id, row.ativa)}
            className={`px-3 py-1 text-sm rounded text-white ${
              row.ativa ? "bg-orange-500 hover:bg-orange-600" : "bg-teal-500 hover:bg-teal-600"
            }`}
          >
            {row.ativa ? "Desativar" : "Ativar"}
          </button>
          <button
            onClick={() => handleDelete(row.id, row.nome)}
            disabled={deleting === row.id}
            className="px-3 py-1 text-sm rounded bg-red-500 text-white hover:bg-red-600 disabled:opacity-50"
          >
            {deleting === row.id ? "..." : "Excluir"}
          </button>
        </div>
      ),
    },
  ];

  const [selectedCols, setSelectedCols] = useState(cols.map((c) => c.label));
  useEffect(() => {
    try {
      const saved = localStorage.getItem("cols:" + window.location.pathname);
      if (saved) {
        setSelectedCols(JSON.parse(saved));
      }
    } catch {}
  }, []);

  const visibleCols = cols.filter((c) => selectedCols.includes(c.label));

  if (loading) return <Loader />;
  if (error) return <ErrorState error={error} />;

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="flex items-center justify-between mb-6">
        <PageHeader title="Empresas" subtitle="Gestão de empresas do sistema">
          {usedEndpoint && (
            <span className="text-xs text-gray-500">Endpoint: {usedEndpoint}</span>
          )}
        </PageHeader>
        <button
          onClick={() => navigate("/dashboard/empresas/new")}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          + Nova Empresa
        </button>
      </div>

      {/* Filtros */}
      <div className="bg-white p-4 rounded shadow mb-4 grid grid-cols-1 md:grid-cols-4 gap-4">
        <input
          type="text"
          placeholder="Buscar..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="border px-3 py-2 rounded"
        />
        <select
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
          className="border px-3 py-2 rounded"
        >
          <option value="">Todos os tipos</option>
          <option value="transportador">Transportador</option>
          <option value="revenda">Revenda</option>
          <option value="borracharia">Borracharia</option>
          <option value="recapagem">Recapagem</option>
        </select>
        <select
          value={ativa}
          onChange={(e) => setAtiva(e.target.value)}
          className="border px-3 py-2 rounded"
        >
          <option value="">Todos os status</option>
          <option value="true">Ativas</option>
          <option value="false">Inativas</option>
        </select>
        <ColumnPicker
          allCols={cols.map((c) => c.label)}
          selected={selectedCols}
          onChange={setSelectedCols}
        />
      </div>

      {/* Tabela */}
      {data && data.length === 0 ? (
        <EmptyState
          message="Nenhuma empresa encontrada"
          action={() => navigate("/dashboard/empresas/new")}
          actionLabel="Criar primeira empresa"
        />
      ) : (
        <DataTable
          data={data || []}
          columns={visibleCols}
          meta={meta}
          page={page}
          onPageChange={setPage}
        />
      )}
>>>>>>> remotes/origin/feature/arquitetura-matriz-filiais
    </div>
  );
}

