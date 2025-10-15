import { Outlet } from 'react-router-dom';
import Header from './Header';
import EmpresasSidebar from './EmpresasSidebar';

export default function LayoutEmpresasDashboard() {
  return (
    <div className="flex h-screen bg-[#0b1220]">
      <EmpresasSidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

