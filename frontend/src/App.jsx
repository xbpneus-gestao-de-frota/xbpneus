import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Cadastro from "./pages/Cadastro";
import CadastroTipoCliente from "./pages/CadastroTipoCliente";
import PosCadastro from "./pages/PosCadastro";

import RequireAuth from "./components/RequireAuth";
import ProtectedRoute from "./components/ProtectedRoute";
import LayoutTransportador from "./components/LayoutTransportador";

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

// Empresas e Filiais
import EmpresasList from "./pages/transportador/empresas/EmpresasList";
import EmpresaForm from "./pages/transportador/empresas/EmpresaForm";
import FiliaisList from "./pages/transportador/empresas/FiliaisList";
import FilialForm from "./pages/transportador/empresas/FilialForm";

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

        {/* Empresas e Filiais */}
        <Route path="empresas" element={<EmpresasList />} />
        <Route path="empresas/new" element={<EmpresaForm />} />
        <Route path="empresas/:id/edit" element={<EmpresaForm />} />
        <Route path="filiais" element={<FiliaisList />} />
        <Route path="filiais/new" element={<FilialForm />} />
        <Route path="filiais/:id/edit" element={<FilialForm />} />

        <Route path="financeiro" element={<Financeiro />} />
        <Route path="compras" element={<Compras />} />
        <Route path="eventos" element={<Eventos />} />
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
