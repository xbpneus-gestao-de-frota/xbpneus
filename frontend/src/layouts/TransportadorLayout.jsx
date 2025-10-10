import Sidebar from "../components/Sidebar";
import { Outlet } from "react-router-dom";

export default function TransportadorLayout() {
  return (
    <div className="min-h-screen bg-[#0b1220] text-[#e5e7eb]">
      <div className="grid grid-cols-1 md:grid-cols-[18rem_1fr]">
        <Sidebar />
        <main className="min-h-screen p-6">
          <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-sm p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
