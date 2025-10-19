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

// Frota
import VeiculosList from "./pages/transportador/frota/VeiculosList";
import VeiculoCreate from "./pages/transportador/frota/VeiculoCreate";
import VeiculoEdit from "./pages/transportador/frota/VeiculoEdit";
import VehicleDetail from "./pages/transportador/frota/VehicleDetail";
import PosicoesList from "./pages/transportador/frota/PosicoesList";
import Motoristas from "./pages/transportador/Motoristas";
import Implementos from "./pages/transportador/Implementos";
import Documentos from "./pages/transportador/Documentos";
import Rastreamento from "./pages/transportador/Rastreamento";

// Pneus
import PneusList from "./pages/transportador/pneus/PneusList";
import PneuCreate from "./pages/transportador/pneus/PneuCreate";
import PneuEdit from "./pages/transportador/pneus/PneuEdit";
import AplicacoesList from "./pages/transportador/pneus/AplicacoesList";
import ManutencaoPneus from "./pages/transportador/ManutencaoPneus";
import AnaliseDesgaste from "./pages/transportador/AnaliseDesgaste";
import Garantias from "./pages/transportador/Garantias";
import EventosPneus from "./pages/transportador/EventosPneus";

// Estoque
import MovimentacoesList from "./pages/transportador/estoque/MovimentacoesList";
import ItensEstoque from "./pages/transportador/ItensEstoque";
import EntradasSaidas from "./pages/transportador/EntradasSaidas";
import RelatoriosEstoque from "./pages/transportador/RelatoriosEstoque";

// Manutenção
import OSList from "./pages/transportador/manutencao/OSList";
import OSCreate from "./pages/transportador/manutencao/OSCreate";
import OSEdit from "./pages/transportador/manutencao/OSEdit";
import OSDetail from "./pages/transportador/manutencao/OSDetail";
import TestesList from "./pages/transportador/manutencao/TestesList";
import HistoricoManutencao from "./pages/transportador/HistoricoManutencao";
import PlanejamentoPreventivo from "./pages/transportador/PlanejamentoPreventivo";

// IA - Análise de Pneus
import IADashboard from "./pages/transportador/ia/Dashboard";
import IAAnalise from "./pages/transportador/ia/Analise";
import IAGamificacao from "./pages/transportador/ia/Gamificacao";
import IAGarantias from "./pages/transportador/ia/Garantias";

// Relatórios
import RelatoriosFrota from "./pages/transportador/RelatoriosFrota";
import RelatoriosPneus from "./pages/transportador/RelatoriosPneus";
import RelatoriosManutencao from "./pages/transportador/RelatoriosManutencao";
import RelatoriosFinanceiros from "./pages/transportador/RelatoriosFinanceiros";

import EmBreve from "./pages/EmBreve";

export default function App(){
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/cadastro" element={<Cadastro />} />
      <Route path="/pos-cadastro" element={<PosCadastro />} />
      <Route path="/cadastro/tipo" element={<CadastroTipoCliente />} />

      {/* Rotas para Transportador */}
      <Route path="/dashboard" element={<ProtectedRoute allowedRoles={["transportador"]}><RequireAuth><LayoutTransportador /></RequireAuth></ProtectedRoute>}>
        <Route index element={<RequireAuth><IndexTransportador /></RequireAuth>} />
        
        <Route path="frota" element={<RequireAuth><Frota /></RequireAuth>} />
        <Route path="frota/veiculos" element={<RequireAuth><VeiculosList /></RequireAuth>} />
        <Route path="frota/veiculos/create" element={<RequireAuth><VeiculoCreate /></RequireAuth>} />
        <Route path="frota/veiculos/:id/edit" element={<RequireAuth><VeiculoEdit /></RequireAuth>} />
        <Route path="frota/veiculos/:id" element={<RequireAuth><VehicleDetail /></RequireAuth>} />
        <Route path="frota/posicoes" element={<RequireAuth><PosicoesList /></RequireAuth>} />
        <Route path="frota/motoristas" element={<RequireAuth><Motoristas /></RequireAuth>} />
        <Route path="frota/implementos" element={<RequireAuth><Implementos /></RequireAuth>} />
        <Route path="frota/documentos" element={<RequireAuth><Documentos /></RequireAuth>} />
        <Route path="frota/rastreamento" element={<RequireAuth><Rastreamento /></RequireAuth>} />

        <Route path="pneus" element={<RequireAuth><Pneus /></RequireAuth>} />
        <Route path="pneus/lista" element={<RequireAuth><PneusList /></RequireAuth>} />
        <Route path="pneus/create" element={<RequireAuth><PneuCreate /></RequireAuth>} />
        <Route path="pneus/:id/edit" element={<RequireAuth><PneuEdit /></RequireAuth>} />
        <Route path="pneus/aplicacoes" element={<RequireAuth><AplicacoesList /></RequireAuth>} />
        <Route path="pneus/manutencao-pneus" element={<RequireAuth><ManutencaoPneus /></RequireAuth>} />
        <Route path="pneus/analise-desgaste" element={<RequireAuth><AnaliseDesgaste /></RequireAuth>} />
        <Route path="pneus/garantias" element={<RequireAuth><Garantias /></RequireAuth>} />
        <Route path="pneus/eventos-pneus" element={<RequireAuth><EventosPneus /></RequireAuth>} />

        <Route path="estoque" element={<RequireAuth><Estoque /></RequireAuth>} />
        <Route path="estoque/movimentacoes" element={<RequireAuth><MovimentacoesList /></RequireAuth>} />
        <Route path="estoque/itens" element={<RequireAuth><ItensEstoque /></RequireAuth>} />
        <Route path="estoque/entradas-saidas" element={<RequireAuth><EntradasSaidas /></RequireAuth>} />
        <Route path="estoque/relatorios-estoque" element={<RequireAuth><RelatoriosEstoque /></RequireAuth>} />

        <Route path="manutencao" element={<RequireAuth><Manutencao /></RequireAuth>} />
        <Route path="manutencao/ordens-servico" element={<RequireAuth><OSList /></RequireAuth>} />
        <Route path="manutencao/ordens-servico/create" element={<RequireAuth><OSCreate /></RequireAuth>} />
        <Route path="manutencao/ordens-servico/:id/edit" element={<RequireAuth><OSEdit /></RequireAuth>} />
        <Route path="manutencao/ordens-servico/:id" element={<RequireAuth><OSDetail /></RequireAuth>} />
        <Route path="manutencao/testes-pos-manutencao" element={<RequireAuth><TestesList /></RequireAuth>} />
        <Route path="manutencao/historico" element={<RequireAuth><HistoricoManutencao /></RequireAuth>} />
        <Route path="manutencao/planejamento-preventivo" element={<RequireAuth><PlanejamentoPreventivo /></RequireAuth>} />

        <Route path="ia" element={<RequireAuth><IADashboard /></RequireAuth>} />
        <Route path="ia/analise" element={<RequireAuth><IAAnalise /></RequireAuth>} />
        <Route path="ia/gamificacao" element={<RequireAuth><IAGamificacao /></RequireAuth>} />
        <Route path="ia/garantias" element={<RequireAuth><IAGarantias /></RequireAuth>} />

        <Route path="financeiro" element={<RequireAuth><Financeiro /></RequireAuth>} />
        <Route path="compras" element={<RequireAuth><Compras /></RequireAuth>} />
        <Route path="eventos" element={<RequireAuth><Eventos /></RequireAuth>} />
        
        <Route path="relatorios" element={<RequireAuth><Relatorios /></RequireAuth>} />
        <Route path="relatorios/frota" element={<RequireAuth><RelatoriosFrota /></RequireAuth>} />
        <Route path="relatorios/pneus" element={<RequireAuth><RelatoriosPneus /></RequireAuth>} />
        <Route path="relatorios/estoque" element={<RequireAuth><RelatoriosEstoque /></RequireAuth>} />
        <Route path="relatorios/manutencao" element={<RequireAuth><RelatoriosManutencao /></RequireAuth>} />
        <Route path="relatorios/financeiro" element={<RequireAuth><RelatoriosFinanceiros /></RequireAuth>} />

        <Route path="configuracoes" element={<RequireAuth><Configuracoes /></RequireAuth>} />
        <Route path="minha-empresa" element={<RequireAuth><MinhaEmpresa /></RequireAuth>} />
        <Route path="empresas" element={<RequireAuth><EmBreve /></RequireAuth>} />
        <Route path="filiais" element={<RequireAuth><EmBreve /></RequireAuth>} />

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

      {/* Rota padrão */}
      <Route path="/" element={<Login />} />
    </Routes>
  );
}

