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
    </div>
  );
}

