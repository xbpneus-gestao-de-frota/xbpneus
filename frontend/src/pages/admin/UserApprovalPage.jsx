import React, { useState, useEffect } from 'react';
import { Check, X, Search, Filter } from 'lucide-react';
import { xbpneusClasses, xbpneusColors } from '../../styles/colors';

const UserApprovalPage = () => {
  const [users, setUsers] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Simular carregamento de usuários pendentes de aprovação
  useEffect(() => {
    const fetchPendingUsers = async () => {
      try {
        setLoading(true);
        // Substituir pela chamada real à API
        // const response = await fetch('/api/users/pending-approval/');
        // const data = await response.json();
        
        // Dados de exemplo
        const mockData = [
          {
            id: 1,
            name: 'João Silva',
            email: 'joao@example.com',
            userType: 'transportador',
            registeredAt: '2025-10-20',
          },
          {
            id: 2,
            name: 'Maria Santos',
            email: 'maria@example.com',
            userType: 'motorista',
            registeredAt: '2025-10-21',
          },
          {
            id: 3,
            name: 'Carlos Oliveira',
            email: 'carlos@example.com',
            userType: 'borracharia',
            registeredAt: '2025-10-22',
          },
        ];
        
        setUsers(mockData);
        setFilteredUsers(mockData);
        setLoading(false);
      } catch (err) {
        setError('Erro ao carregar usuários pendentes de aprovação');
        setLoading(false);
      }
    };

    fetchPendingUsers();
  }, []);

  // Filtrar usuários
  useEffect(() => {
    let filtered = users;

    if (searchTerm) {
      filtered = filtered.filter(
        (user) =>
          user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          user.email.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (filterType !== 'all') {
      filtered = filtered.filter((user) => user.userType === filterType);
    }

    setFilteredUsers(filtered);
  }, [searchTerm, filterType, users]);

  const handleApprove = async (userId) => {
    try {
      // Substituir pela chamada real à API
      // await fetch(`/api/users/${userId}/approve/`, { method: 'POST' });
      
      setUsers(users.filter((user) => user.id !== userId));
      alert('Usuário aprovado com sucesso!');
    } catch (err) {
      alert('Erro ao aprovar usuário');
    }
  };

  const handleReject = async (userId) => {
    try {
      // Substituir pela chamada real à API
      // await fetch(`/api/users/${userId}/reject/`, { method: 'POST' });
      
      setUsers(users.filter((user) => user.id !== userId));
      alert('Usuário rejeitado com sucesso!');
    } catch (err) {
      alert('Erro ao rejeitar usuário');
    }
  };

  const userTypeLabels = {
    transportador: 'Transportador',
    motorista: 'Motorista',
    borracharia: 'Borracharia',
    revenda: 'Revenda',
    recapagem: 'Recapagem',
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className={`${xbpneusClasses.card} p-6`}>
        {/* Cabeçalho */}
        <div className="mb-6">
          <h1 className={`${xbpneusClasses.cardTitle} text-2xl mb-2`}>
            Aprovação de Usuários
          </h1>
          <p className="text-gray-600">
            Gerenciar usuários recém-cadastrados que aguardam aprovação
          </p>
        </div>

        {/* Filtros e Busca */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="md:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-3 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Buscar por nome ou email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className={`${xbpneusClasses.input} pl-10 w-full`}
              />
            </div>
          </div>
          <div>
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className={`${xbpneusClasses.input} w-full`}
            >
              <option value="all">Todos os Tipos</option>
              <option value="transportador">Transportador</option>
              <option value="motorista">Motorista</option>
              <option value="borracharia">Borracharia</option>
              <option value="revenda">Revenda</option>
              <option value="recapagem">Recapagem</option>
            </select>
          </div>
        </div>

        {/* Conteúdo */}
        {loading ? (
          <div className="text-center py-8">
            <p className="text-gray-600">Carregando usuários...</p>
          </div>
        ) : error ? (
          <div className="text-center py-8">
            <p className="text-red-600">{error}</p>
          </div>
        ) : filteredUsers.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-600">Nenhum usuário pendente de aprovação</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className={xbpneusClasses.tableHeader}>
                  <th className="px-6 py-3 text-left">Nome</th>
                  <th className="px-6 py-3 text-left">Email</th>
                  <th className="px-6 py-3 text-left">Tipo de Cliente</th>
                  <th className="px-6 py-3 text-left">Data de Cadastro</th>
                  <th className="px-6 py-3 text-center">Ações</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((user, index) => (
                  <tr
                    key={user.id}
                    className={index % 2 === 0 ? xbpneusClasses.tableRow : xbpneusClasses.tableRowAlt}
                  >
                    <td className="px-6 py-4">{user.name}</td>
                    <td className="px-6 py-4">{user.email}</td>
                    <td className="px-6 py-4">
                      <span className={xbpneusClasses.badgeInfo}>
                        {userTypeLabels[user.userType]}
                      </span>
                    </td>
                    <td className="px-6 py-4">{user.registeredAt}</td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center gap-2">
                        <button
                          onClick={() => handleApprove(user.id)}
                          className={`${xbpneusClasses.buttonPrimary} px-4 py-2 rounded-lg flex items-center gap-2 text-sm`}
                          style={{
                            background: `linear-gradient(to right, ${xbpneusColors.status.success}, ${xbpneusColors.status.success})`,
                          }}
                        >
                          <Check size={16} />
                          Aprovar
                        </button>
                        <button
                          onClick={() => handleReject(user.id)}
                          className={`${xbpneusClasses.buttonSecondary} px-4 py-2 rounded-lg flex items-center gap-2 text-sm`}
                          style={{
                            borderColor: xbpneusColors.status.error,
                            color: xbpneusColors.status.error,
                          }}
                        >
                          <X size={16} />
                          Rejeitar
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserApprovalPage;

