import React, { useState } from 'react';
import {
  FileSpreadsheet,
  Download,
  Calculator,
  Shield,
  LifeBuoy,
  Building2,
  CheckSquare,
  Square,
  AlertCircle,
  FileText
} from 'lucide-react';

export function ImpactAnalytics({ risks = [], alerts = [] }) {
  // Interactive Calculator State
  const [calcHazard, setCalcHazard] = useState('flood');
  const [calcPop, setCalcPop] = useState(250000);
  const [calcSeverity, setCalcSeverity] = useState('critical');
  const [calcInfraDensity, setCalcInfraDensity] = useState('urban'); // urban, peri-urban, rural

  // SOP Checklists State
  const [completedSOPs, setCompletedSOPs] = useState({});

  const toggleSOP = (id) => {
    setCompletedSOPs((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  // Compute Risk Impact Score & Insurance Loss Exposure Index
  const severityMultiplier =
    calcSeverity === 'critical' ? 1.0 : calcSeverity === 'high' ? 0.7 : calcSeverity === 'medium' ? 0.4 : 0.2;
  const hazardFactor =
    calcHazard === 'cyclone' ? 1.2 : calcHazard === 'flood' ? 1.0 : calcHazard === 'earthquake' ? 1.5 : 0.8;
  const infraFactor = calcInfraDensity === 'urban' ? 1.8 : calcInfraDensity === 'peri-urban' ? 1.2 : 0.6;

  const compositeRiskScore = Math.min(
    100,
    Math.round(((calcPop / 50000) * severityMultiplier * hazardFactor * infraFactor * 10))
  );

  const estimatedEconomicLossCrores = (
    (calcPop * 0.045 * severityMultiplier * hazardFactor * infraFactor)
  ).toFixed(1);

  const estimatedInsuredPortionCrores = (
    estimatedEconomicLossCrores * (calcInfraDensity === 'urban' ? 0.35 : 0.15)
  ).toFixed(1);

  // SOP Protocols
  const sopProtocols = [
    {
      audience: 'National & State Disaster Management Authorities (NDMA / SDMA)',
      icon: Shield,
      color: 'text-cyan-400',
      items: [
        { id: 'ndma-1', text: 'Activate State Emergency Operations Centre (SEOC) 24/7 Level-3 protocol.' },
        { id: 'ndma-2', text: 'Issue statutory Red Alert directive to District Collectors in affected polygons.' },
        { id: 'ndma-3', text: 'Pre-position emergency wireless satellite phones and emergency backup generators.' },
        { id: 'ndma-4', text: 'Mobilise inter-departmental relief supply buffers (rations, water purifiers, medicines).' },
      ],
    },
    {
      audience: 'Search & Rescue Battalions (NDRF / SDRF)',
      icon: LifeBuoy,
      color: 'text-rose-400',
      items: [
        { id: 'ndrf-1', text: 'Deploy motorised inflatable rescue boats (IRBs) and deep-diving tactical squads.' },
        { id: 'ndrf-2', text: 'Establish temporary casualty clearing stations (TCCS) above peak inundation levels.' },
        { id: 'ndrf-3', text: 'Clear key road transport lifelines using tree-cutters and heavy earthmoving gear.' },
      ],
    },
    {
      audience: 'Underwriters, Reinsurers & Loss Assessors',
      icon: Building2,
      color: 'text-amber-400',
      items: [
        { id: 'ins-1', text: 'Run catastrophic portfolio exposure models against real-time hazard coordinates.' },
        { id: 'ins-2', text: 'Notify rapid loss-assessment survey teams and trigger parametric payout triggers.' },
        { id: 'ins-3', text: 'Establish dedicated emergency toll-free claims triage helpline for affected policyholders.' },
      ],
    },
  ];

  // Export Data to CSV
  const handleExportCSV = () => {
    const headers = ['ID', 'Title', 'Hazard Type', 'Severity', 'Location', 'Latitude', 'Longitude', 'Affected Pop', 'Reported By', 'Created At'];
    const rows = risks.map((r) => [
      r.id,
      `"${r.title.replace(/"/g, '""')}"`,
      r.hazard_type,
      r.severity,
      `"${r.location.replace(/"/g, '""')}"`,
      r.latitude || '',
      r.longitude || '',
      r.affected_population || 0,
      `"${(r.reported_by || '').replace(/"/g, '""')}"`,
      r.created_at,
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `climate_risk_events_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Export Data to JSON
  const handleExportJSON = () => {
    const exportObject = {
      exported_at: new Date().toISOString(),
      system: 'Unified Climate Risk Brain',
      risk_events: risks,
      alerts: alerts,
    };

    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(exportObject, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `unified_climate_risk_report_${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <FileSpreadsheet className="w-5 h-5 text-cyan-400" />
            <span>Impact Analytics & EOC SOP Directives</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Parametric insurance modeling, composite vulnerability calculator, and disaster protocol checklists
          </p>
        </div>

        {/* Export Hub Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleExportCSV}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 hover:text-white rounded-xl text-xs font-medium transition-all"
          >
            <Download className="w-3.5 h-3.5 text-cyan-400" />
            <span>Export CSV</span>
          </button>
          <button
            onClick={handleExportJSON}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-bold transition-all shadow-md shadow-cyan-900/30"
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Export Full JSON Report</span>
          </button>
        </div>
      </div>

      {/* Two-Column Grid: Impact Calculator & Insurance Exposure */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Parametric Vulnerability & Loss Calculator */}
        <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4 shadow-xl">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
              <Calculator className="w-4 h-4 text-cyan-400" />
              <span>Parametric Impact & Insurance Loss Estimator</span>
            </h3>
            <span className="text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
              Simulation Engine
            </span>
          </div>

          <div className="space-y-3 text-xs">
            {/* Hazard Selector */}
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Simulated Hazard Scenario</label>
              <div className="grid grid-cols-4 gap-2">
                {[
                  { id: 'flood', label: '🌊 Flood' },
                  { id: 'cyclone', label: '🌀 Cyclone' },
                  { id: 'earthquake', label: '🌋 Quake' },
                  { id: 'heatwave', label: '🔥 Heatwave' },
                ].map((item) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => setCalcHazard(item.id)}
                    className={`py-2 px-1 rounded-xl font-medium text-center transition-all ${
                      calcHazard === item.id
                        ? 'bg-cyan-600 text-white shadow-md'
                        : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Severity & Density */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-300 font-semibold mb-1">Severity Category</label>
                <select
                  value={calcSeverity}
                  onChange={(e) => setCalcSeverity(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 focus:outline-none focus:border-cyan-500 capitalize text-xs"
                >
                  <option value="low">Low Warning</option>
                  <option value="medium">Medium Warning</option>
                  <option value="high">High Warning</option>
                  <option value="critical">Critical Disaster</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-300 font-semibold mb-1">Asset Density</label>
                <select
                  value={calcInfraDensity}
                  onChange={(e) => setCalcInfraDensity(e.target.value)}
                  className="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 focus:outline-none focus:border-cyan-500 capitalize text-xs"
                >
                  <option value="urban">Urban Dense (Metro/Hub)</option>
                  <option value="peri-urban">Semi-Urban Suburb</option>
                  <option value="rural">Rural Agricultural</option>
                </select>
              </div>
            </div>

            {/* Population Slider */}
            <div>
              <div className="flex items-center justify-between text-slate-300 font-semibold mb-1">
                <span>Estimated Population Exposed:</span>
                <span className="text-cyan-400 font-mono">{calcPop.toLocaleString()} people</span>
              </div>
              <input
                type="range"
                min="10000"
                max="5000000"
                step="25000"
                value={calcPop}
                onChange={(e) => setCalcPop(Number(e.target.value))}
                className="w-full accent-cyan-500 bg-slate-950 rounded-lg cursor-pointer"
              />
            </div>
          </div>

          {/* Calculator Output KPI Card */}
          <div className="p-4 rounded-xl bg-gradient-to-br from-slate-950 to-cyan-950/40 border border-cyan-800/60 space-y-3">
            <div className="grid grid-cols-3 gap-3 text-center">
              <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold">Vulnerability Index</div>
                <div className="text-xl font-extrabold text-cyan-300 mt-1">{compositeRiskScore} / 100</div>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold">Est. Economic Loss</div>
                <div className="text-xl font-extrabold text-amber-300 mt-1">₹{estimatedEconomicLossCrores} Cr</div>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800">
                <div className="text-[10px] text-slate-400 uppercase font-semibold">Insured Exposure</div>
                <div className="text-xl font-extrabold text-rose-300 mt-1">₹{estimatedInsuredPortionCrores} Cr</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right: National SOP Execution Checklists */}
        <div className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 space-y-4 shadow-xl flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <Shield className="w-4 h-4 text-emerald-400" />
                <span>Inter-Agency Standard Operating Procedures (SOPs)</span>
              </h3>
              <span className="text-xs text-slate-400 font-mono">
                {Object.values(completedSOPs).filter(Boolean).length} / 10 Checked
              </span>
            </div>

            <div className="space-y-4 mt-3 max-h-[380px] overflow-y-auto pr-1">
              {sopProtocols.map((protocol, pIdx) => {
                const Icon = protocol.icon;
                return (
                  <div key={pIdx} className="space-y-2">
                    <div className="flex items-center gap-2 text-xs font-bold text-slate-200">
                      <Icon className={`w-4 h-4 ${protocol.color}`} />
                      <span>{protocol.audience}</span>
                    </div>

                    <div className="space-y-1.5 pl-6">
                      {protocol.items.map((item) => {
                        const isDone = !!completedSOPs[item.id];
                        return (
                          <div
                            key={item.id}
                            onClick={() => toggleSOP(item.id)}
                            className={`p-2 rounded-xl text-xs flex items-start gap-2.5 cursor-pointer transition-all border ${
                              isDone
                                ? 'bg-emerald-950/30 border-emerald-800/60 text-slate-300'
                                : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700'
                            }`}
                          >
                            <button className="mt-0.5 shrink-0 text-emerald-400">
                              {isDone ? (
                                <CheckSquare className="w-4 h-4 text-emerald-400" />
                              ) : (
                                <Square className="w-4 h-4 text-slate-500" />
                              )}
                            </button>
                            <span className={isDone ? 'line-through text-slate-400' : ''}>
                              {item.text}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
