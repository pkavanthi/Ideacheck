import React, { useState, useEffect } from 'react';
import IncidentForm from './components/IncidentForm';
import IncidentList from './components/IncidentList';
import ResourcePanel from './components/ResourcePanel';
import {
  fetchIncidents,
  createIncident,
  updateIncident,
  deleteIncident,
  fetchResources,
  createResource,
  deleteResource,
} from './api';

export default function App() {
  const [incidents, setIncidents] = useState([]);
  const [resources, setResources] = useState([]);
  const [activeTab, setActiveTab] = useState('incidents');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [incidentsData, resourcesData] = await Promise.all([
        fetchIncidents(),
        fetchResources(),
      ]);
      setIncidents(incidentsData);
      setResources(resourcesData);
      setError(null);
    } catch (err) {
      setError('Failed to sync live operational picture. Please ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateIncident = async (payload) => {
    try {
      const created = await createIncident(payload);
      setIncidents((prev) => [created, ...prev]);
    } catch (err) {
      alert('Error creating incident');
    }
  };

  const handleUpdateStatus = async (id, status) => {
    try {
      const updated = await updateIncident(id, { status });
      setIncidents((prev) =>
        prev.map((inc) => (inc.id === id ? updated : inc))
      );
    } catch (err) {
      alert('Error updating status');
    }
  };

  const handleDeleteIncident = async (id) => {
    if (!window.confirm('Confirm deletion of incident?')) return;
    try {
      await deleteIncident(id);
      setIncidents((prev) => prev.filter((inc) => inc.id !== id));
    } catch (err) {
      alert('Error deleting incident');
    }
  };

  const handleAddResource = async (payload) => {
    try {
      const created = await createResource(payload);
      setResources((prev) => [...prev, created]);
    } catch (err) {
      alert('Error adding resource');
    }
  };

  const handleDeleteResource = async (id) => {
    if (!window.confirm('Confirm deletion of resource?')) return;
    try {
      await deleteResource(id);
      setResources((prev) => prev.filter((res) => res.id !== id));
    } catch (err) {
      alert('Error deleting resource');
    }
  };

  const totalAffected = incidents.reduce((sum, item) => sum + (item.affected_population || 0), 0);
  const criticalCount = incidents.filter((i) => i.threat_level === 'CRITICAL' && i.status !== 'RESOLVED').length;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Top Navigation */}
      <header className="bg-slate-900 border-b border-slate-800 px-6 py-4 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="bg-red-600 text-white font-black px-2.5 py-1 rounded text-lg tracking-wider">
            GUARDIAN
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight">Monsoon Threat Operations Center</h1>
            <p className="text-xs text-slate-400">24–48 Hour Imminent Disaster Intelligence Feed</p>
          </div>
        </div>

        <div className="flex items-center gap-6 text-sm">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 bg-red-500 rounded-full animate-ping"></span>
            <span className="text-xs text-slate-300">
              Critical Alerts: <strong className="text-red-400">{criticalCount}</strong>
            </span>
          </div>
          <div className="text-xs text-slate-300">
            Total Est. Impacted: <strong className="text-amber-400">{totalAffected.toLocaleString()}</strong>
          </div>
          <button
            onClick={loadData}
            className="text-xs bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded border border-slate-700 transition"
          >
            Refresh Feed
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 space-y-6">
        {error && (
          <div className="bg-red-950/80 border border-red-800 text-red-200 px-4 py-3 rounded text-sm flex justify-between items-center">
            <span>{error}</span>
            <button onClick={loadData} className="underline text-xs">Retry</button>
          </div>
        )}

        {/* View Toggle */}
        <div className="flex border-b border-slate-800 gap-4">
          <button
            onClick={() => setActiveTab('incidents')}
            className={`pb-2 text-sm font-semibold border-b-2 transition ${
              activeTab === 'incidents'
                ? 'border-blue-500 text-blue-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Active Incidents & Response
          </button>
          <button
            onClick={() => setActiveTab('resources')}
            className={`pb-2 text-sm font-semibold border-b-2 transition ${
              activeTab === 'resources'
                ? 'border-blue-500 text-blue-400'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            Relief Resources & Staging
          </button>
        </div>

        {loading ? (
          <div className="text-center py-12 text-slate-400 text-sm">Loading unified operational telemetry...</div>
        ) : (
          <div>
            {activeTab === 'incidents' ? (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-1">
                  <IncidentForm onSubmit={handleCreateIncident} />
                </div>
                <div className="lg:col-span-2">
                  <IncidentList
                    incidents={incidents}
                    onUpdateStatus={handleUpdateStatus}
                    onDelete={handleDeleteIncident}
                  />
                </div>
              </div>
            ) : (
              <ResourcePanel
                resources={resources}
                onAddResource={handleAddResource}
                onDeleteResource={handleDeleteResource}
              />
            )}
          </div>
        )}
      </main>

      <footer className="bg-slate-900 border-t border-slate-800 px-6 py-3 text-center text-xs text-slate-500">
        GUARDIAN State Disaster Management Operational Platform &copy; 2025
      </footer>
    </div>
  );
}
