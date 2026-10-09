import React from 'react';
import {
  ShieldAlert,
  AlertTriangle,
  Users,
  Activity,
  Waves,
  Wind,
  Flame,
  Radio,
  ArrowRight,
  TrendingUp,
  MapPin,
  Clock
} from 'lucide-react';
import { GeospatialMap } from './GeospatialMap';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

export function Dashboard({
  risks = [],
  alerts = [],
  onNavigateTab,
  onOpenCreateRisk,
  onOpenCreateAlert,
  onSelectRisk
}) {
  const activeAlerts = alerts.filter((a) => a.active === 1);
  const criticalEvents = risks.filter((r) => r.severity === 'critical');
  const totalAffectedPop = risks.reduce(
    (acc, curr) => acc + (curr.affected_population ? Number(curr.affected_population) : 0),
    0
  );

  // Counts by hazard type
  const hazardCounts = {
    flood: risks.filter((r) => r.hazard_type === 'flood').length,
    cyclone: risks.filter((r) => r.hazard_type === 'cyclone').length,
    earthquake: risks.filter((r) => r.hazard_type === 'earthquake').length,
    heatwave: risks.filter((r) => r.hazard_type === 'heatwave').length,
  };

  // Severity Distribution Chart Data
  const severityChartData = {
    labels: ['Critical', 'High', 'Medium', 'Low'],
    datasets: [
      {
        data: [
          risks.filter((r) => r.severity === 'critical').length,
          risks.filter((r) => r.severity === 'high').length,
          risks.filter((r) => r.severity === 'medium').length,
          risks.filter((r) => r.severity === 'low').length,
        ],
        backgroundColor: ['#ef4444', '#f97316', '#f59e0b', '#10b981'],
        borderWidth: 0,
      },
    ],
  };

  // Hazard Breakdown Chart Data
  const hazardChartData = {
    labels: ['Flood', 'Cyclone', 'Earthquake', 'Heatwave'],
    datasets: [
      {
        label: 'Recorded Events',
        data: [
          hazardCounts.flood,
          hazardCounts.cyclone,
          hazardCounts.earthquake,
          hazardCounts.heatwave,
        ],
        backgroundColor: ['#0284c7', '#0d9488', '#ea580c', '#e11d48'],
        borderRadius: 6,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#94a3b8',
          font: { size: 11 },
        },
      },
    },
    scales: {
      x: {
        ticks: { color: '#94a3b8' },
        grid: { color: '#1e293b' },
      },
      y: {
        ticks: { color: '#94a3b8', stepSize: 1 },
        grid: { color: '#1e293b' },
      },
    },
  };

  return (
    <div className="space-y-6">
      {/* Top Banner Ticker if Active Alerts exist */}
      {activeAlerts.length > 0 && (
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-rose-950 via-slate-900 to-amber-950 p-4 border border-rose-800/80 shadow-2xl">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-rose-600/30 border border-rose-500/50 flex items-center justify-center shrink-0">
                <Radio className="w-5 h-5 text-rose-400 animate-pulse" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-bold text-rose-200 text-sm tracking-wide uppercase">
                    National Emergency Alert Stream
                  </span>
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded-full bg-rose-600 text-white animate-pulse">
                    LIVE
                  </span>
                </div>
                <p className="text-xs text-rose-100 font-medium mt-0.5 max-w-3xl">
                  {activeAlerts[0]?.message}
                </p>
              </div>
            </div>

            <button
              onClick={() => onNavigateTab('alerts')}
              className="flex items-center gap-1.5 px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-xs font-bold transition-all shadow-md shrink-0"
            >
              <span>View All {activeAlerts.length} Alerts</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Metric Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Metric 1: Active Alerts */}
        <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition-all shadow-lg relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-rose-500/5 rounded-full blur-2xl group-hover:bg-rose-500/10 transition-all" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Active Warnings
            </span>
            <div className="p-2 rounded-xl bg-rose-950/60 border border-rose-800 text-rose-400">
              <Radio className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{activeAlerts.length}</span>
            <span className="text-xs text-rose-400 font-medium">Broadcasts</span>
          </div>
          <div className="mt-2 text-xs text-slate-400 flex items-center justify-between">
            <span>Critical Severity: {activeAlerts.filter(a => a.severity === 'critical').length}</span>
            <button
              onClick={() => onNavigateTab('alerts')}
              className="text-cyan-400 hover:underline text-[11px]"
            >
              Manage &rarr;
            </button>
          </div>
        </div>

        {/* Metric 2: Critical Risk Events */}
        <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition-all shadow-lg relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-orange-500/5 rounded-full blur-2xl group-hover:bg-orange-500/10 transition-all" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Critical Hazards
            </span>
            <div className="p-2 rounded-xl bg-orange-950/60 border border-orange-800 text-orange-400">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">{criticalEvents.length}</span>
            <span className="text-xs text-slate-400">of {risks.length} total events</span>
          </div>
          <div className="mt-2 text-xs text-slate-400 flex items-center justify-between">
            <span>High: {risks.filter(r => r.severity === 'high').length}</span>
            <button
              onClick={() => onNavigateTab('risks')}
              className="text-cyan-400 hover:underline text-[11px]"
            >
              View registry &rarr;
            </button>
          </div>
        </div>

        {/* Metric 3: Total Affected Population */}
        <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition-all shadow-lg relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-cyan-500/5 rounded-full blur-2xl group-hover:bg-cyan-500/10 transition-all" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Pop. At Risk
            </span>
            <div className="p-2 rounded-xl bg-cyan-950/60 border border-cyan-800 text-cyan-400">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-cyan-200">
              {(totalAffectedPop / 1000000).toFixed(2)}M
            </span>
            <span className="text-xs text-slate-400">Citizens</span>
          </div>
          <div className="mt-2 text-xs text-slate-400">
            Across {risks.length} distinct impact zones
          </div>
        </div>

        {/* Metric 4: Monitored Hazard Vectors */}
        <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition-all shadow-lg relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-500/5 rounded-full blur-2xl group-hover:bg-indigo-500/10 transition-all" />
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Monitored Vectors
            </span>
            <div className="p-2 rounded-xl bg-indigo-950/60 border border-indigo-800 text-indigo-400">
              <Activity className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-4 flex items-center gap-2">
            <span className="text-3xl font-extrabold text-white">4</span>
            <div className="flex gap-1.5 ml-2">
              <span className="p-1 rounded bg-sky-950 text-sky-400 border border-sky-800" title="Flood">🌊</span>
              <span className="p-1 rounded bg-teal-950 text-teal-400 border border-teal-800" title="Cyclone">🌀</span>
              <span className="p-1 rounded bg-orange-950 text-orange-400 border border-orange-800" title="Earthquake">🌋</span>
              <span className="p-1 rounded bg-rose-950 text-rose-400 border border-rose-800" title="Heatwave">🔥</span>
            </div>
          </div>
          <div className="mt-2 text-xs text-slate-400">
            Real-time multi-hazard telemetry
          </div>
        </div>
      </div>

      {/* Geospatial Map Centerpiece */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <MapPin className="w-4 h-4 text-cyan-400" />
              <span>Interactive Geospatial Climate Risk Map</span>
            </h3>
            <p className="text-xs text-slate-400">
              Real-time multi-hazard coordinates, impact radii, and active warning zones
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={onOpenCreateRisk}
              className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 rounded-lg text-xs font-medium transition-colors"
            >
              + Add Hazard Coordinate
            </button>
          </div>
        </div>

        <GeospatialMap
          risks={risks}
          alerts={alerts}
          onSelectRisk={onSelectRisk}
          onBroadcastAlert={onOpenCreateAlert}
        />
      </div>

      {/* Two Column Section: Analytics & Recent Events Feed */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Hazard Analytics Visualisation */}
        <div className="lg:col-span-1 p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-slate-200">Hazard Vector Distribution</h4>
            <span className="text-[11px] text-slate-400 font-mono">Live Sync</span>
          </div>

          <div className="h-56 relative flex items-center justify-center">
            {risks.length > 0 ? (
              <Doughnut
                data={severityChartData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'bottom',
                      labels: { color: '#94a3b8', font: { size: 10 } },
                    },
                  },
                  cutout: '70%',
                }}
              />
            ) : (
              <span className="text-xs text-slate-400">No events logged yet</span>
            )}
          </div>

          <div className="pt-3 border-t border-slate-800/80 space-y-2">
            <div className="text-xs font-semibold text-slate-300">Hazard Counts</div>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <span className="text-sky-400 flex items-center gap-1.5">🌊 Flood</span>
                <span className="font-bold text-slate-200">{hazardCounts.flood}</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <span className="text-teal-400 flex items-center gap-1.5">🌀 Cyclone</span>
                <span className="font-bold text-slate-200">{hazardCounts.cyclone}</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <span className="text-orange-400 flex items-center gap-1.5">🌋 Earthquake</span>
                <span className="font-bold text-slate-200">{hazardCounts.earthquake}</span>
              </div>
              <div className="p-2.5 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
                <span className="text-rose-400 flex items-center gap-1.5">🔥 Heatwave</span>
                <span className="font-bold text-slate-200">{hazardCounts.heatwave}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Live Hazard Feed & Emergency SOP Summary */}
        <div className="lg:col-span-2 p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-bold text-slate-200">Priority Climate Hazard Events</h4>
              <p className="text-xs text-slate-400">Latest situation reports from regional EOCs</p>
            </div>
            <button
              onClick={() => onNavigateTab('risks')}
              className="text-xs text-cyan-400 hover:text-cyan-300 font-medium"
            >
              View Full Table &rarr;
            </button>
          </div>

          <div className="space-y-3">
            {risks.slice(0, 4).map((risk) => {
              const severityBadge =
                risk.severity === 'critical'
                  ? 'bg-rose-950 text-rose-300 border-rose-800'
                  : risk.severity === 'high'
                  ? 'bg-orange-950 text-orange-300 border-orange-800'
                  : risk.severity === 'medium'
                  ? 'bg-amber-950 text-amber-300 border-amber-800'
                  : 'bg-emerald-950 text-emerald-300 border-emerald-800';

              return (
                <div
                  key={risk.id}
                  onClick={() => onSelectRisk && onSelectRisk(risk)}
                  className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 hover:border-slate-700 transition-all cursor-pointer flex items-start justify-between gap-3 group"
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-xs font-bold uppercase tracking-wider text-cyan-400 font-mono">
                        {risk.hazard_type}
                      </span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${severityBadge}`}>
                        {risk.severity}
                      </span>
                      <span className="text-xs text-slate-400 flex items-center gap-1">
                        <MapPin className="w-3 h-3 text-slate-400" />
                        {risk.location}
                      </span>
                    </div>
                    <h5 className="text-sm font-semibold text-slate-100 group-hover:text-cyan-300 transition-colors">
                      {risk.title}
                    </h5>
                    <p className="text-xs text-slate-400 line-clamp-1">
                      {risk.description || 'No detailed briefing provided.'}
                    </p>
                  </div>

                  <div className="text-right shrink-0">
                    <div className="text-xs font-semibold text-slate-200">
                      {risk.affected_population ? Number(risk.affected_population).toLocaleString() : 'N/A'}
                    </div>
                    <div className="text-[10px] text-slate-400">Affected Pop</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
