import React from 'react';
import {
  ShieldAlert,
  Radio,
  RefreshCw,
  Bell,
  Activity,
  PlusCircle,
  Server
} from 'lucide-react';

export function Navbar({
  isBackendLive,
  onRefresh,
  loading,
  activeAlertsCount,
  onOpenCreateAlert,
  onOpenCreateRisk
}) {
  return (
    <header className="sticky top-0 z-40 bg-slate-900/90 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & National Title */}
          <div className="flex items-center gap-3">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 shadow-lg shadow-cyan-500/20">
              <ShieldAlert className="w-6 h-6 text-white" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-rose-500 rounded-full border-2 border-slate-900 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-cyan-400 via-sky-200 to-indigo-300 bg-clip-text text-transparent">
                  Unified Climate Risk Brain
                </span>
                <span className="hidden md:inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold tracking-wide uppercase bg-cyan-950 text-cyan-300 border border-cyan-800">
                  National EOC
                </span>
              </div>
              <p className="text-[11px] text-slate-400 hidden sm:block">
                Multi-Hazard Intelligence • Flood • Cyclone • Earthquake • Heatwave
              </p>
            </div>
          </div>

          {/* Right Actions & Status */}
          <div className="flex items-center gap-3">
            {/* Backend Connectivity Status Badge */}
            <div
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium transition-colors ${
                isBackendLive
                  ? 'bg-emerald-950/60 border-emerald-800/80 text-emerald-300'
                  : 'bg-amber-950/60 border-amber-800/80 text-amber-300'
              }`}
              title={
                isBackendLive
                  ? 'Connected to FastAPI backend (http://127.0.0.1:8000)'
                  : 'FastAPI backend offline — Running in high-performance browser demo mode with local persistence'
              }
            >
              <div
                className={`w-2 h-2 rounded-full ${
                  isBackendLive ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'
                }`}
              />
              <Server className="w-3.5 h-3.5 opacity-80" />
              <span className="hidden sm:inline">
                {isBackendLive ? 'Backend API Live' : 'Demo Mode (Offline Sync)'}
              </span>
            </div>

            {/* Refresh Data Button */}
            <button
              onClick={onRefresh}
              disabled={loading}
              className="p-2 text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-lg transition-all active:scale-95 disabled:opacity-50"
              title="Refresh Telemetry & Hazard Data"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-cyan-400' : ''}`} />
            </button>

            {/* Active Alert Counter Badge */}
            <div className="flex items-center gap-1.5 px-3 py-1.5 bg-rose-950/40 border border-rose-900/60 rounded-lg text-rose-300 text-xs font-semibold">
              <Radio className="w-3.5 h-3.5 text-rose-400 animate-pulse" />
              <span>{activeAlertsCount} Active {activeAlertsCount === 1 ? 'Alert' : 'Alerts'}</span>
            </div>

            {/* Quick Action: Record Event */}
            <button
              onClick={onOpenCreateRisk}
              className="hidden lg:flex items-center gap-1.5 px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 hover:text-white rounded-lg text-xs font-medium transition-all"
            >
              <PlusCircle className="w-3.5 h-3.5 text-sky-400" />
              <span>Record Event</span>
            </button>

            {/* Quick Action: Broadcast Alert */}
            <button
              onClick={onOpenCreateAlert}
              className="flex items-center gap-1.5 px-3.5 py-1.5 bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white rounded-lg text-xs font-semibold shadow-lg shadow-rose-900/30 transition-all active:scale-95"
            >
              <Bell className="w-3.5 h-3.5" />
              <span>Broadcast Alert</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
