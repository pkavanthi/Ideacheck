import React, { useState, useEffect, useCallback } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './components/Dashboard';
import { RisksModule } from './components/RisksModule';
import { AlertsModule } from './components/AlertsModule';
import { ImpactAnalytics } from './components/ImpactAnalytics';
import { ToastContainer } from './components/Toast';
import { api } from './services/api';

export function App() {
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [risks, setRisks] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isBackendLive, setIsBackendLive] = useState(false);
  const [toasts, setToasts] = useState([]);

  // Toast Helper
  const addToast = useCallback((title, message, type = 'info') => {
    const id = Date.now() + Math.random();
    setToasts((prev) => [...prev, { id, title, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4500);
  }, []);

  const dismissToast = (id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  // Load all telemetry data
  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const health = await api.checkHealth();
      setIsBackendLive(health.live);

      const [risksData, alertsData] = await Promise.all([
        api.getRisks(),
        api.getAlerts({ active_only: undefined }),
      ]);

      setRisks(risksData || []);
      setAlerts(alertsData || []);
    } catch (err) {
      console.error('Data loading error:', err);
      addToast('Sync Issue', 'Could not fetch latest updates. Using cached data.', 'warning');
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  useEffect(() => {
    loadData();
    // Periodic refresh every 30 seconds
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, [loadData]);

  // Risk Handlers
  const handleCreateRisk = async (payload) => {
    const created = await api.createRisk(payload);
    setRisks((prev) => [created, ...prev]);
    addToast('Risk Recorded', `"${created.title}" successfully added to registry.`, 'success');
    return created;
  };

  const handleUpdateRisk = async (id, payload) => {
    const updated = await api.updateRisk(id, payload);
    setRisks((prev) => prev.map((r) => (r.id === id ? updated : r)));
    addToast('Risk Updated', `Event #${id} records have been updated.`, 'success');
    return updated;
  };

  const handleDeleteRisk = async (id) => {
    await api.deleteRisk(id);
    setRisks((prev) => prev.filter((r) => r.id !== id));
    addToast('Risk Removed', `Event #${id} removed from the registry.`, 'info');
  };

  // Alert Handlers
  const handleCreateAlert = async (payload) => {
    const created = await api.createAlert(payload);
    setAlerts((prev) => [created, ...prev]);
    addToast('Alert Broadcasted', `Emergency siren dispatched for ${created.region}.`, 'warning');
    return created;
  };

  const handleUpdateAlert = async (id, payload) => {
    const updated = await api.updateAlert(id, payload);
    setAlerts((prev) => prev.map((a) => (a.id === id ? updated : a)));
    if (payload.active === 0) {
      addToast('Alert Resolved', `Emergency directive #${id} marked as stand-down.`, 'success');
    } else {
      addToast('Alert Updated', `Emergency directive #${id} modified.`, 'info');
    }
    return updated;
  };

  const handleDeleteAlert = async (id) => {
    await api.deleteAlert(id);
    setAlerts((prev) => prev.filter((a) => a.id !== id));
    addToast('Alert Deleted', `Alert directive #${id} deleted.`, 'info');
  };

  // Reset demo datasets
  const handleResetDemo = () => {
    api.resetDemoData();
    loadData();
    addToast('Demo Data Restored', 'National hazard scenarios reset to factory baseline.', 'info');
  };

  const activeAlertsCount = alerts.filter((a) => a.active === 1).length;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-cyan-500/30">
      {/* Top Navigation */}
      <Navbar
        isBackendLive={isBackendLive}
        onRefresh={loadData}
        loading={loading}
        activeAlertsCount={activeAlertsCount}
        onOpenCreateRisk={() => setCurrentTab('risks')}
        onOpenCreateAlert={() => setCurrentTab('alerts')}
      />

      {/* Main Body */}
      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        <Sidebar
          currentTab={currentTab}
          setTab={setCurrentTab}
          onResetDemo={handleResetDemo}
          isBackendLive={isBackendLive}
        />

        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
          {currentTab === 'dashboard' && (
            <Dashboard
              risks={risks}
              alerts={alerts}
              onNavigateTab={setCurrentTab}
              onOpenCreateRisk={() => setCurrentTab('risks')}
              onOpenCreateAlert={() => setCurrentTab('alerts')}
              onSelectRisk={(risk) => setCurrentTab('risks')}
            />
          )}

          {currentTab === 'risks' && (
            <RisksModule
              risks={risks}
              onCreateRisk={handleCreateRisk}
              onUpdateRisk={handleUpdateRisk}
              onDeleteRisk={handleDeleteRisk}
              onBroadcastAlert={(risk) => setCurrentTab('alerts')}
              loading={loading}
            />
          )}

          {currentTab === 'alerts' && (
            <AlertsModule
              alerts={alerts}
              risks={risks}
              onCreateAlert={handleCreateAlert}
              onUpdateAlert={handleUpdateAlert}
              onDeleteAlert={handleDeleteAlert}
              loading={loading}
            />
          )}

          {currentTab === 'impact' && (
            <ImpactAnalytics
              risks={risks}
              alerts={alerts}
            />
          )}
        </main>
      </div>

      {/* Global Toast System */}
      <ToastContainer toasts={toasts} onDismiss={dismissToast} />
    </div>
  );
}

export default App;
