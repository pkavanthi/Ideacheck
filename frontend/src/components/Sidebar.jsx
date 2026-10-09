import React from 'react';
import {
  LayoutDashboard,
  MapPin,
  Bell,
  Activity,
  FileSpreadsheet,
  Settings,
  HelpCircle,
  Database,
  RotateCcw
} from 'lucide-react';

export function Sidebar({ currentTab, setTab, onResetDemo, isBackendLive }) {
  const navItems = [
    {
      id: 'dashboard',
      label: 'Command Center',
      sub: 'Overview & Geospatial Map',
      icon: LayoutDashboard,
    },
    {
      id: 'risks',
      label: 'Climate Risk Events',
      sub: 'Registry & Hazard Records',
      icon: Activity,
    },
    {
      id: 'alerts',
      label: 'Emergency Alerts',
      sub: 'Broadcast & SOP Action',
      icon: Bell,
    },
    {
      id: 'impact',
      label: 'Impact & EOC SOPs',
      sub: 'Vulnerability & Insurance',
      icon: FileSpreadsheet,
    },
  ];

  return (
    <aside className="w-64 shrink-0 bg-slate-900/80 border-r border-slate-800 p-4 flex flex-col justify-between hidden md:flex min-h-[calc(100vh-4rem)]">
      <div className="space-y-6">
        {/* Navigation Group */}
        <div>
          <div className="px-3 mb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Operations & Telemetry
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setTab(item.id)}
                  className={`w-full flex items-start gap-3 px-3.5 py-3 rounded-xl text-left transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-cyan-950/80 to-blue-950/50 border border-cyan-800/80 text-white shadow-md'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
                  }`}
                >
                  <Icon
                    className={`w-5 h-5 shrink-0 mt-0.5 ${
                      isActive ? 'text-cyan-400' : 'text-slate-400'
                    }`}
                  />
                  <div>
                    <div className={`text-sm font-semibold ${isActive ? 'text-slate-100' : 'text-slate-300'}`}>
                      {item.label}
                    </div>
                    <div className="text-[11px] text-slate-400 font-normal">
                      {item.sub}
                    </div>
                  </div>
                </button>
              );
            })}
          </nav>
        </div>

        {/* Hazard Legend Card */}
        <div className="p-3.5 bg-slate-950/60 rounded-xl border border-slate-800/80 text-xs space-y-2">
          <div className="text-[11px] font-semibold text-slate-300 flex items-center justify-between">
            <span>Hazard Color Key</span>
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping-slow"></span>
          </div>
          <div className="grid grid-cols-2 gap-2 text-[11px] text-slate-400">
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-sky-500"></span>
              <span>Flood</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-teal-500"></span>
              <span>Cyclone</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-orange-500"></span>
              <span>Earthquake</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
              <span>Heatwave</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer System Info & Reset Option */}
      <div className="pt-4 border-t border-slate-800 space-y-3">
        <div className="flex items-center justify-between px-2 text-[11px] text-slate-400">
          <span>Engine Status</span>
          <span className="font-mono text-cyan-400">v1.0.0 FastBrain</span>
        </div>

        <button
          onClick={onResetDemo}
          className="w-full flex items-center justify-center gap-2 px-3 py-2 text-xs font-medium text-slate-400 hover:text-slate-200 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-lg transition-colors"
          title="Restore baseline emergency scenarios & alerts"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Restore Demo Datasets</span>
        </button>
      </div>
    </aside>
  );
}
