import React, { useState, useEffect } from 'react';
import { Settings, Plus, ToggleLeft, ToggleRight } from 'lucide-react';
import { xbpneusClasses, xbpneusColors } from '../../styles/colors';

const IntegrationsManagementPage = () => {
  const [integrations, setIntegrations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Simular carregamento de integrações
  useEffect(() => {
    const fetchIntegrations = async () => {
      try {
        setLoading(true);
        // Substituir pela chamada real à API
        // const response = await fetch('/api/transportador/integracoes/');
        // const data = await response.json();
        
        // Dados de exemplo
        const mockData = [
          {
            id: 1,
            name: 'Telemetria GPS',
            description: 'Integração com sistema de rastreamento de veículos',
            active: true,
            icon: '📍',
          },
          {
            id: 2,
            name: 'ERP Integrado',
            description: 'Sincronização com sistema ERP da empresa',
            active: false,
            icon: '📊',
          },
          {
            id: 3,
            name: 'Notificações SMS',
            description: 'Envio de notificações via SMS para motoristas',
            active: true,
            icon: '📱',
          },
          {
            id: 4,
            name: 'Pagamento Online',
            description: 'Integração com gateway de pagamento',
            active: false,
            icon: '💳',
          },
        ];
        
        setIntegrations(mockData);
        setLoading(false);
      } catch (err) {
        setError('Erro ao carregar integrações');
        setLoading(false);
      }
    };

    fetchIntegrations();
  }, []);

  const handleToggleIntegration = async (integrationId) => {
    try {
      // Substituir pela chamada real à API
      // await fetch(`/api/transportador/integracoes/${integrationId}/toggle/`, { method: 'POST' });
      
      setIntegrations(
        integrations.map((integration) =>
          integration.id === integrationId
            ? { ...integration, active: !integration.active }
            : integration
        )
      );
    } catch (err) {
      alert('Erro ao atualizar integração');
    }
  };

  const handleConfigureIntegration = (integrationId) => {
    // Navegar para página de configuração específica
    alert(`Configurar integração ${integrationId}`);
  };

  const handleAddIntegration = () => {
    // Abrir modal ou navegar para página de adição de integração
    alert('Adicionar nova integração');
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Cabeçalho */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className={`${xbpneusClasses.cardTitle} text-3xl mb-2`}>
                Gerenciamento de Integrações
              </h1>
              <p className="text-gray-600">
                Configure e gerencie integrações com outros sistemas
              </p>
            </div>
            <button
              onClick={handleAddIntegration}
              className={`${xbpneusClasses.buttonPrimary} px-6 py-3 rounded-lg flex items-center gap-2`}
            >
              <Plus size={20} />
              Adicionar Integração
            </button>
          </div>
        </div>

        {/* Conteúdo */}
        {loading ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Carregando integrações...</p>
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-600">{error}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {integrations.map((integration) => (
              <div key={integration.id} className={xbpneusClasses.card + ' p-6'}>
                {/* Ícone e Título */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="text-3xl">{integration.icon}</div>
                    <div>
                      <h3 className={`${xbpneusClasses.cardTitle} text-lg`}>
                        {integration.name}
                      </h3>
                      <p className="text-sm text-gray-600">{integration.description}</p>
                    </div>
                  </div>
                </div>

                {/* Status */}
                <div className="mb-4">
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600">Status:</span>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        integration.active
                          ? xbpneusClasses.badgeSuccess
                          : xbpneusClasses.badgeWarning
                      }`}
                    >
                      {integration.active ? 'Ativa' : 'Inativa'}
                    </span>
                  </div>
                </div>

                {/* Botões de Ação */}
                <div className="flex gap-2">
                  <button
                    onClick={() => handleConfigureIntegration(integration.id)}
                    className={`${xbpneusClasses.buttonPrimary} flex-1 px-4 py-2 rounded-lg flex items-center justify-center gap-2 text-sm`}
                  >
                    <Settings size={16} />
                    Configurar
                  </button>
                  <button
                    onClick={() => handleToggleIntegration(integration.id)}
                    className={`flex-1 px-4 py-2 rounded-lg flex items-center justify-center gap-2 text-sm ${
                      integration.active
                        ? 'bg-red-100 text-red-700 hover:bg-red-200'
                        : 'bg-green-100 text-green-700 hover:bg-green-200'
                    }`}
                  >
                    {integration.active ? (
                      <>
                        <ToggleRight size={16} />
                        Desativar
                      </>
                    ) : (
                      <>
                        <ToggleLeft size={16} />
                        Ativar
                      </>
                    )}
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default IntegrationsManagementPage;

