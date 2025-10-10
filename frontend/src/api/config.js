/**
 * Configuração centralizada de APIs
 * Sistema XBPneus
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  // Autenticação
  users: {
    registerFull: `${API_BASE_URL}/api/users/register_full/`,
  },
  auth: {
    login: `${API_BASE_URL}/api/auth/login/`,
    logout: `${API_BASE_URL}/api/auth/logout/`,
    me: `${API_BASE_URL}/api/auth/me/`,
  },
  
  // Transportador
  transportador: {
    // Frota
    veiculos: `${API_BASE_URL}/api/transportador/frota/veiculos/`,
    posicoes: `${API_BASE_URL}/api/transportador/frota/posicoes/`,
    
    // Pneus
    pneus: `${API_BASE_URL}/api/transportador/pneus/pneus/`,
    aplicacoes: `${API_BASE_URL}/api/transportador/pneus/aplicacoes/`,
    eventos: `${API_BASE_URL}/api/transportador/pneus/eventos/`,
    
    // Estoque
    estoque: `${API_BASE_URL}/api/transportador/estoque/produtos/`,
    movimentacoes: `${API_BASE_URL}/api/transportador/estoque/movimentacoes/`,
    categorias: `${API_BASE_URL}/api/transportador/estoque/categorias/`,
    
    // Manutenção
    ordensServico: `${API_BASE_URL}/api/transportador/manutencao/ordens-servico/`,
    itensOS: `${API_BASE_URL}/api/transportador/manutencao/itens-os/`,
    checklists: `${API_BASE_URL}/api/transportador/manutencao/checklists/`,
    planosPreventiva: `${API_BASE_URL}/api/transportador/manutencao/planos-preventiva/`,
    historicoManutencao: `${API_BASE_URL}/api/transportador/manutencao/historico/`,
    
    // Almoxarifado
    almoxarifados: `${API_BASE_URL}/api/transportador/almoxarifado/almoxarifados/`,
    locaisEstoque: `${API_BASE_URL}/api/transportador/almoxarifado/locais/`,
    
    // Cargas
    cargas: `${API_BASE_URL}/api/transportador/cargas/cargas/`,
    
    // Peças
    pecas: `${API_BASE_URL}/api/transportador/pecas/pecas/`,
    
    // Ferramentas
    ferramentas: `${API_BASE_URL}/api/transportador/ferramentas/ferramentas/`,
    
    // EPIs
    epis: `${API_BASE_URL}/api/transportador/epis/epis/`,
    
    // Treinamentos
    treinamentos: `${API_BASE_URL}/api/transportador/treinamentos/treinamentos/`,
    
    // Compliance
    compliance: `${API_BASE_URL}/api/transportador/compliance/documentos/`,
    
    // Alertas
    alertas: `${API_BASE_URL}/api/transportador/alertas/alertas/`,
    
    // Integrações
    integracoes: `${API_BASE_URL}/api/transportador/integracoes/integracoes/`,
    
    // Configurações
    configuracoes: `${API_BASE_URL}/api/transportador/configuracoes/configuracoes/`,
    
    // Relatórios
    relatorios: `${API_BASE_URL}/api/transportador/relatorios/relatorios/`,
    
    // Notas Fiscais
    notasFiscais: `${API_BASE_URL}/api/transportador/notas_fiscais/notas/`,
    
    // Auditoria
    auditoria: `${API_BASE_URL}/api/transportador/auditoria/logs/`,
  },
};

export default API_ENDPOINTS;
