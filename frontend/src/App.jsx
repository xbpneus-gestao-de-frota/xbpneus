import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Cadastro from "./pages/Cadastro";
import CadastroTipoCliente from "./pages/CadastroTipoCliente";
import PosCadastro from "./pages/PosCadastro";

import RequireAuth from "@/components/RequireAuth";
import ProtectedRoute from "@/components/ProtectedRoute";
import LayoutTransportador from "@/components/LayoutTransportador";

// Dashboards por tipo de usuário
import DashboardMotorista from "./pages/motorista/DashboardMotorista";
import DashboardRevenda from "./pages/revenda/DashboardRevenda";
import DashboardBorracharia from "./pages/borracharia/DashboardBorracharia";
import DashboardRecapagem from "./pages/recapagem/DashboardRecapagem";

import IndexTransportador from "./pages/transportador/Index";
import Frota from "./pages/transportador/Frota";
import Pneus from "./pages/transportador/Pneus";
import Estoque from "./pages/transportador/Estoque";
import Manutencao from "./pages/transportador/Manutencao";
import Financeiro from "./pages/transportador/Financeiro";
import Compras from "./pages/transportador/Compras";
import Eventos from "./pages/transportador/Eventos";
import Relatorios from "./pages/transportador/Relatorios";
import Configuracoes from "./pages/transportador/Configuracoes";
import MinhaEmpresa from "./pages/transportador/MinhaEmpresa";

import VeiculosList from "./pages/transportador/frota/VeiculosList";
import VeiculoCreate from "./pages/transportador/frota/VeiculoCreate";
import VeiculoEdit from "./pages/transportador/frota/VeiculoEdit";
import VehicleDetail from "./pages/transportador/frota/VehicleDetail";
import PosicoesList from "./pages/transportador/frota/PosicoesList";

import PneusList from "./pages/transportador/pneus/PneusList";
import PneuCreate from "./pages/transportador/pneus/PneuCreate";
import PneuEdit from "./pages/transportador/pneus/PneuEdit";
import AplicacoesList from "./pages/transportador/pneus/AplicacoesList";

import MovimentacoesList from "./pages/transportador/estoque/MovimentacoesList";

import OSList from "./pages/transportador/manutencao/OSList";
import OSCreate from "./pages/transportador/manutencao/OSCreate";
import OSEdit from "./pages/transportador/manutencao/OSEdit";
import OSDetail from "./pages/transportador/manutencao/OSDetail";
import TestesList from "./pages/transportador/manutencao/TestesList";

// IA - Análise de Pneus
import IADashboard from "./pages/transportador/ia/Dashboard";
import IAAnalise from "./pages/transportador/ia/Analise";
import IAGamificacao from "./pages/transportador/ia/Gamificacao";
import IAGarantias from "./pages/transportador/ia/Garantias";

import EmpresasList from "./pages/transportador/empresas/EmpresasList";
import EmpresaForm from "./pages/transportador/empresas/EmpresaForm";
import FiliaisList from "./pages/transportador/filiais/FiliaisList";
import FilialForm from "./pages/transportador/filiais/FilialForm";

// Dashboard de Empresas
import LayoutEmpresasDashboard from "@/components/LayoutEmpresasDashboard";
import EmpresasDashboard from "./pages/transportador/empresas-dashboard/EmpresasDashboard";
import EmpresasListNew from "./pages/transportador/empresas-dashboard/EmpresasList";
import FiliaisListNew from "./pages/transportador/empresas-dashboard/FiliaisList";
import AgregadosList from "./pages/transportador/empresas-dashboard/AgregadosList";

// Dashboard de Frota
import LayoutFrotaDashboard from "@/components/LayoutFrotaDashboard";
import FrotaDashboard from "./pages/transportador/frota-dashboard/FrotaDashboard";
import VeiculosListNew from "./pages/transportador/frota-dashboard/VeiculosList";
import MotoristasList from "./pages/transportador/frota-dashboard/MotoristasList";
import LayoutMotoristasDashboard from "@/components/LayoutMotoristasDashboard";

// Sub-Dashboards do Pilar de Frota
import LayoutVeiculosDashboard from "@/components/LayoutVeiculosDashboard";
import VeiculosDashboard from "./pages/transportador/frota-dashboard/veiculos/VeiculosDashboard";
import LayoutPosicoesDashboard from "@/components/LayoutPosicoesDashboard";
import PosicoesDashboard from "./pages/transportador/frota-dashboard/posicoes/PosicoesDashboard";
import PosicoesListNew from "./pages/transportador/frota-dashboard/posicoes/PosicoesList";
import LayoutRastreamentoDashboard from "@/components/LayoutRastreamentoDashboard";
import RastreamentoDashboard from "./pages/transportador/frota-dashboard/rastreamento/RastreamentoDashboard";

// Dashboard de Pneus
import LayoutPneusDashboard from "@/components/LayoutPneusDashboard";
import PneusDashboard from "./pages/transportador/pneus-dashboard/PneusDashboard";
import PneusListNew from "./pages/transportador/pneus-dashboard/PneusList";

// Dashboard de Estoque
import LayoutEstoqueDashboard from "@/components/LayoutEstoqueDashboard";
import EstoqueDashboard from "./pages/transportador/estoque-dashboard/EstoqueDashboard";
import MovimentacoesListNew from "./pages/transportador/estoque-dashboard/MovimentacoesList";

// Dashboard de Manutenção
import LayoutManutencaoDashboard from "@/components/LayoutManutencaoDashboard";
import ManutencaoDashboard from "./pages/transportador/manutencao-dashboard/ManutencaoDashboard";
import OSListNew from "./pages/transportador/manutencao-dashboard/OSList";

export default function App(){
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/cadastro" element={<Cadastro />} />
      <Route path="/pos-cadastro" element={<PosCadastro />} />
      <Route path="/cadastro/tipo" element={<CadastroTipoCliente />} />

      {/* Rotas para Transportador */}
      <Route path="/dashboard" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutTransportador /></RequireAuth></ProtectedRoute>}>
        <Route index element={<IndexTransportador />} />
        <Route path="frota" element={<Frota />} />
        <Route path="frota/veiculos" element={<VeiculosList />} />
        <Route path="frota/veiculos/create" element={<VeiculoCreate />} />
        <Route path="frota/veiculos/:id/edit" element={<VeiculoEdit />} />
        <Route path="frota/veiculos/:id" element={<VehicleDetail />} />
        <Route path="frota/posicoes" element={<PosicoesList />} />

        <Route path="pneus" element={<Pneus />} />
        <Route path="pneus/lista" element={<PneusList />} />
        <Route path="pneus/create" element={<PneuCreate />} />
        <Route path="pneus/:id/edit" element={<PneuEdit />} />
        <Route path="pneus/aplicacoes" element={<AplicacoesList />} />

        <Route path="estoque" element={<Estoque />} />
        <Route path="estoque/movimentacoes" element={<MovimentacoesList />} />

        <Route path="manutencao" element={<Manutencao />} />
        <Route path="manutencao/ordens-servico" element={<OSList />} />
        <Route path="manutencao/ordens-servico/create" element={<OSCreate />} />
        <Route path="manutencao/ordens-servico/:id/edit" element={<OSEdit />} />
        <Route path="manutencao/ordens-servico/:id" element={<OSDetail />} />
        <Route path="manutencao/testes" element={<TestesList />} />

        {/* IA - Análise de Pneus */}
        <Route path="ia" element={<IADashboard />} />
        <Route path="ia/analise" element={<IAAnalise />} />
        <Route path="ia/gamificacao" element={<IAGamificacao />} />
        <Route path="ia/garantias" element={<IAGarantias />} />

        {/* Empresas e Filiais (antigas rotas - manter compatibilidade) */}
        <Route path="empresas" element={<EmpresasList />} />
        <Route path="empresas/create" element={<EmpresaForm />} />
        <Route path="empresas/:id/edit" element={<EmpresaForm />} />
        <Route path="filiais" element={<FiliaisList />} />
        <Route path="filiais/create" element={<FilialForm />} />
        <Route path="filiais/:id/edit" element={<FilialForm />} />
      </Route>

      {/* Dashboard de Empresas */}
      <Route path="/dashboard/empresas-dashboard" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutEmpresasDashboard /></RequireAuth></ProtectedRoute>}>
        <Route index element={<EmpresasDashboard />} />
        <Route path="empresas" element={<EmpresasListNew />} />
        <Route path="filiais" element={<FiliaisListNew />} />
        <Route path="agregados" element={<AgregadosList />} />
        <Route path="documentos" element={<div className="text-white">Documentos - Em breve</div>} />
        <Route path="relatorios" element={<div className="text-white">Relatórios - Em breve</div>} />
        <Route path="configuracoes" element={<div className="text-white">Configurações - Em breve</div>} />
      </Route>

      {/* Dashboard de Frota */}
      <Route path="/dashboard/frota-dashboard" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutFrotaDashboard /></RequireAuth></ProtectedRoute>}>
        <Route index element={<FrotaDashboard />} />
        {/* Rotas para o Dashboard de Veículos */}
        <Route path="veiculos" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutVeiculosDashboard /></RequireAuth></ProtectedRoute>}>
          <Route index element={<VeiculosDashboard />} />
          <Route path="lista" element={<VeiculosListNew />} />
          <Route path="inserir" element={<div className="text-white">Inserir Veículo - Em breve</div>} />
          <Route path="implemento" element={<div className="text-white">Adicionar Implemento - Em breve</div>} />
          <Route path="documentos" element={<div className="text-white">Documentos Veículos - Em breve</div>} />
          <Route path="configuracoes" element={<div className="text-white">Configurações Veículos - Em breve</div>} />
        </Route>

        {/* Rotas para o Dashboard de Motoristas */}
        <Route path="motoristas" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutMotoristasDashboard /></RequireAuth></ProtectedRoute>}>
          <Route index element={<MotoristasList />} /> {/* MotoristasList já é o dashboard e lista */}
          <Route path="lista" element={<MotoristasList />} />
          <Route path="cadastrar" element={<div className="text-white">Cadastrar Motorista - Em breve</div>} />
          <Route path="conexao" element={<div className="text-white">Conexão Externa - Em breve</div>} />
          <Route path="habilitacoes" element={<div className="text-white">Habilitações - Em breve</div>} />
          <Route path="documentos" element={<div className="text-white">Documentos Motoristas - Em breve</div>} />
          <Route path="configuracoes" element={<div className="text-white">Configurações Motoristas - Em breve</div>} />
        </Route>

        {/* Rotas para o Dashboard de Posições */}
        <Route path="posicoes" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutPosicoesDashboard /></RequireAuth></ProtectedRoute>}>
          <Route index element={<PosicoesDashboard />} />
          <Route path="lista" element={<PosicoesListNew />} />
          <Route path="gerenciar" element={<div className="text-white">Gerenciar Posições - Em breve</div>} />
          <Route path="configuracoes" element={<div className="text-white">Configurações Posições - Em breve</div>} />
        </Route>

        {/* Rotas para o Dashboard de Rastreamento */}
        <Route path="rastreamento" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutRastreamentoDashboard /></RequireAuth></ProtectedRoute>}>
          <Route index element={<RastreamentoDashboard />} />
          <Route path="monitoramento" element={<div className="text-white">Monitoramento Ao Vivo - Em breve</div>} />
          <Route path="historico" element={<div className="text-white">Histórico de Rotas - Em breve</div>} />
          <Route path="veiculos" element={<div className="text-white">Veículos Rastreáveis - Em breve</div>} />
          <Route path="configuracoes" element={<div className="text-white">Configurações Rastreamento - Em breve</div>} />
        </Route>

        <Route path="financeiro" element={<Financeiro />} />

        {/* Dashboard de Pneus */}
        <Route path="pneus-dashboard" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutPneusDashboard /></RequireAuth></ProtectedRoute>}>
          <Route index element={<PneusDashboard />} />
          <Route path="lista" element={<PneusListNew />} />
          <Route path="cadastrar" element={<div className="text-white">Cadastrar Pneu - Em breve</div>} />
          <Route path="aplicacoes" element={<div className="text-white">Aplicações - Em breve</div>} />
          <Route path="manutencao" element={<div className="text-white">Manutenção Pneus - Em breve</div>} />
          <Route path="analise" element={<div className="text-white">Análise de Desempenho - Em breve</div>} />
          <Route path="garantias" element={<div className="text-white">Garantias - Em breve</div>} />
          <Route path="configuracoes" element={<div className="text-white">Configurações Pneus - Em breve</div>} />
        </Route>
        <Route path="compras" element={<Compras />} />

        {/* Dashboard de Estoque */}
        <Route path="estoque-dashboard" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutEstoqueDashboard /></RequireAuth></ProtectedRoute>}>
          <Route index element={<EstoqueDashboard />} />
          <Route path="movimentacoes" element={<MovimentacoesListNew />} />
          <Route path="itens" element={<div className="text-white">Itens em Estoque - Em breve</div>} />
          <Route path="entradas" element={<div className="text-white">Entradas - Em breve</div>} />
          <Route path="saidas" element={<div className="text-white">Saídas - Em breve</div>} />
          <Route path="relatorios" element={<div className="text-white">Relatórios de Estoque - Em breve</div>} />
          <Route path="configuracoes" element={<div className="text-white">Configurações de Estoque - Em breve</div>} />
        </Route>
        <Route path="eventos" element={<Eventos />} />

        {/* Dashboard de Manutenção */}
        <Route path="manutencao-dashboard" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutManutencaoDashboard /></RequireAuth></ProtectedRoute>}>
          <Route index element={<ManutencaoDashboard />} />
          <Route path="ordens-servico" element={<OSListNew />} />
          <Route path="testes" element={<div className="text-white">Testes Pós-Manutenção - Em breve</div>} />
          <Route path="relatorios" element={<div className="text-white">Relatórios de Manutenção - Em breve</div>} />
          <Route path="configuracoes" element={<div className="text-white">Configurações de Manutenção - Em breve</div>} />
        </Route>
        <Route path="relatorios" element={<Relatorios />} />
        <Route path="configuracoes" element={<Configuracoes />} />
        <Route path="minha-empresa" element={<MinhaEmpresa />} />
      </Route>

      {/* Rota para Motorista */}
      <Route path="/motorista/dashboard" element={
        <ProtectedRoute allowedRoles={['motorista']}>
          <RequireAuth><DashboardMotorista /></RequireAuth>
        </ProtectedRoute>
      } />

      {/* Rota para Revenda */}
      <Route path="/revenda/dashboard" element={
        <ProtectedRoute allowedRoles={['revenda']}>
          <RequireAuth><DashboardRevenda /></RequireAuth>
        </ProtectedRoute>
      } />

      {/* Rota para Borracharia */}
      <Route path="/borracharia/dashboard" element={
        <ProtectedRoute allowedRoles={['borracharia']}>
          <RequireAuth><DashboardBorracharia /></RequireAuth>
        </ProtectedRoute>
      } />

      {/* Rota para Recapagem */}
      <Route path="/recapagem/dashboard" element={
        <ProtectedRoute allowedRoles={['recapagem']}>
          <RequireAuth><DashboardRecapagem /></RequireAuth>
        </ProtectedRoute>
      } />

      {/* Manter compatibilidade com rota antiga */}
      <Route path="/app/transportador" element={
        <ProtectedRoute allowedRoles={['transportador']}>
          <RequireAuth><LayoutTransportador /></RequireAuth>
        </ProtectedRoute>
      }>
        <Route index element={<IndexTransportador />} />
      </Route>

      <Route path="*" element={<Login />} />
    </Routes>
  );
}
