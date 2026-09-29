import React from 'react';

export default function IncidentList({ incidents, onUpdateStatus, onDelete }) {
  const getThreatBadge = (level) => {
    switch (level) {
      case 'CRITICAL':
        return 'bg-red-500/20 text-red-400 border border-red-500/50';
      case 'HIGH':
        return 'bg-amber-500/20 text-amber-400 border border-amber-500/50';
      case 'MODERATE':
        return 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/50';
      default:
        return 'bg-blue-500/20 text-blue-400 border border-blue-500/50';
    }
  };

  return (
    <div className="bg-slate-800 p-5 rounded-lg border border-slate-700">
      <h3 className="text-lg font-bold text-white mb-4">Active Incidents Operational Queue</h3>
      {incidents.length === 0 ? (
        <p className="text-slate-400 text-sm italic">No incidents recorded in the current active emergency window.</p>
      ) : (
        <div className="space-y-3">
          {incidents.map((incident) => (
            <div
              key={incident.id}
              className="p-4 rounded-md bg-slate-900 border border-slate-700/70 hover:border-slate-600 transition"
            >
              <div className="flex flex-wrap items-center justify-between gap-2 mb-2">
                <div className="flex items-center gap-2">
                  <h4 className="font-semibold text-white">{incident.title}</h4>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getThreatBadge(incident.threat_level)}`}>
                    {incident.threat_level}
                  </span>
                </div>
                <span className="text-xs text-slate-400 font-mono">
                  {new Date(incident.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>

              <p className="text-sm text-slate-300 mb-2">{incident.description || 'No detailed remarks'}</p>

              <div className="flex flex-wrap items-center justify-between text-xs text-slate-400 gap-2 border-t border-slate-800 pt-2">
                <div>
                  <span className="font-medium text-slate-200">District:</span> {incident.district} |{' '}
                  <span className="font-medium text-slate-200">Location:</span> {incident.location_name} |{' '}
                  <span className="font-medium text-slate-200">Affected:</span> {incident.affected_population.toLocaleString()}
                </div>

                <div className="flex items-center gap-2">
                  <select
                    value={incident.status}
                    onChange={(e) => onUpdateStatus(incident.id, e.target.value)}
                    className="bg-slate-800 border border-slate-700 text-slate-200 rounded px-2 py-1 text-xs"
                  >
                    <option value="REPORTED">REPORTED</option>
                    <option value="ACTIVE">ACTIVE</option>
                    <option value="CONTAINED">CONTAINED</option>
                    <option value="RESOLVED">RESOLVED</option>
                  </select>

                  <button
                    onClick={() => onDelete(incident.id)}
                    className="text-red-400 hover:text-red-300 text-xs px-2 py-1 rounded bg-red-950/40 hover:bg-red-950 border border-red-800"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
