import { INITIAL_RISKS, INITIAL_ALERTS } from './mockData';

const BASE_URL = import.meta.env.VITE_API_URL || '';

// Local storage keys for seamless offline / standalone fallback
const LS_RISKS = 'climate_risk_brain_risks_v1';
const LS_ALERTS = 'climate_risk_brain_alerts_v1';

function getStoredRisks() {
  const data = localStorage.getItem(LS_RISKS);
  if (!data) {
    localStorage.setItem(LS_RISKS, JSON.stringify(INITIAL_RISKS));
    return [...INITIAL_RISKS];
  }
  try {
    return JSON.parse(data);
  } catch {
    return [...INITIAL_RISKS];
  }
}

function setStoredRisks(risks) {
  localStorage.setItem(LS_RISKS, JSON.stringify(risks));
}

function getStoredAlerts() {
  const data = localStorage.getItem(LS_ALERTS);
  if (!data) {
    localStorage.setItem(LS_ALERTS, JSON.stringify(INITIAL_ALERTS));
    return [...INITIAL_ALERTS];
  }
  try {
    return JSON.parse(data);
  } catch {
    return [...INITIAL_ALERTS];
  }
}

function setStoredAlerts(alerts) {
  localStorage.setItem(LS_ALERTS, JSON.stringify(alerts));
}

export const api = {
  isMockMode: false,

  async checkHealth() {
    try {
      const res = await fetch(`${BASE_URL}/health`, { signal: AbortSignal.timeout(2500) });
      if (res.ok) {
        const data = await res.json();
        this.isMockMode = false;
        return { live: true, data };
      }
    } catch {
      // Backend not running
    }
    this.isMockMode = true;
    return { live: false, data: { status: 'mock', app: 'Unified Climate Risk Brain (Standalone Demo)' } };
  },

  // -------------------------------------------------------------------------
  // RISKS API
  // -------------------------------------------------------------------------
  async getRisks(filters = {}) {
    const params = new URLSearchParams();
    if (filters.hazard_type && filters.hazard_type !== 'all') params.append('hazard_type', filters.hazard_type);
    if (filters.severity && filters.severity !== 'all') params.append('severity', filters.severity);
    if (filters.skip !== undefined) params.append('skip', filters.skip);
    if (filters.limit !== undefined) params.append('limit', filters.limit);

    try {
      const res = await fetch(`${BASE_URL}/api/v1/risks/?${params.toString()}`, {
        headers: { 'Content-Type': 'application/json' },
        signal: AbortSignal.timeout(3000),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      this.isMockMode = false;
      return data;
    } catch {
      this.isMockMode = true;
      let risks = getStoredRisks();
      if (filters.hazard_type && filters.hazard_type !== 'all') {
        risks = risks.filter(r => r.hazard_type === filters.hazard_type);
      }
      if (filters.severity && filters.severity !== 'all') {
        risks = risks.filter(r => r.severity === filters.severity);
      }
      return risks;
    }
  },

  async createRisk(payload) {
    try {
      const res = await fetch(`${BASE_URL}/api/v1/risks/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(3500),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail ? JSON.stringify(err.detail) : `HTTP ${res.status}`);
      }
      const data = await res.json();
      return data;
    } catch (error) {
      if (!this.isMockMode && !error.message.includes('Failed to fetch') && !error.name.includes('Abort')) {
        throw error;
      }
      // Mock Fallback
      const risks = getStoredRisks();
      const newRisk = {
        id: risks.length > 0 ? Math.max(...risks.map(r => r.id)) + 1 : 1,
        ...payload,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      risks.unshift(newRisk);
      setStoredRisks(risks);
      return newRisk;
    }
  },

  async updateRisk(id, payload) {
    try {
      const res = await fetch(`${BASE_URL}/api/v1/risks/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(3500),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail ? JSON.stringify(err.detail) : `HTTP ${res.status}`);
      }
      return await res.json();
    } catch (error) {
      if (!this.isMockMode && !error.message.includes('Failed to fetch') && !error.name.includes('Abort')) {
        throw error;
      }
      const risks = getStoredRisks();
      const index = risks.findIndex(r => r.id === Number(id));
      if (index === -1) throw new Error('Risk event not found');
      risks[index] = {
        ...risks[index],
        ...payload,
        updated_at: new Date().toISOString(),
      };
      setStoredRisks(risks);
      return risks[index];
    }
  },

  async deleteRisk(id) {
    try {
      const res = await fetch(`${BASE_URL}/api/v1/risks/${id}`, {
        method: 'DELETE',
        signal: AbortSignal.timeout(3500),
      });
      if (!res.ok && res.status !== 404) throw new Error(`HTTP ${res.status}`);
      return true;
    } catch (error) {
      if (!this.isMockMode && !error.message.includes('Failed to fetch') && !error.name.includes('Abort')) {
        throw error;
      }
      const risks = getStoredRisks().filter(r => r.id !== Number(id));
      setStoredRisks(risks);
      return true;
    }
  },

  // -------------------------------------------------------------------------
  // ALERTS API
  // -------------------------------------------------------------------------
  async getAlerts(filters = {}) {
    const params = new URLSearchParams();
    if (filters.hazard_type && filters.hazard_type !== 'all') params.append('hazard_type', filters.hazard_type);
    if (filters.active_only !== undefined) params.append('active_only', filters.active_only ? 'true' : 'false');
    if (filters.skip !== undefined) params.append('skip', filters.skip);
    if (filters.limit !== undefined) params.append('limit', filters.limit);

    try {
      const res = await fetch(`${BASE_URL}/api/v1/alerts/?${params.toString()}`, {
        headers: { 'Content-Type': 'application/json' },
        signal: AbortSignal.timeout(3000),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch {
      this.isMockMode = true;
      let alerts = getStoredAlerts();
      if (filters.hazard_type && filters.hazard_type !== 'all') {
        alerts = alerts.filter(a => a.hazard_type === filters.hazard_type);
      }
      if (filters.active_only !== undefined && filters.active_only !== 'all') {
        const activeNum = filters.active_only ? 1 : 0;
        alerts = alerts.filter(a => a.active === activeNum);
      }
      return alerts;
    }
  },

  async createAlert(payload) {
    try {
      const res = await fetch(`${BASE_URL}/api/v1/alerts/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(3500),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail ? JSON.stringify(err.detail) : `HTTP ${res.status}`);
      }
      return await res.json();
    } catch (error) {
      if (!this.isMockMode && !error.message.includes('Failed to fetch') && !error.name.includes('Abort')) {
        throw error;
      }
      const alerts = getStoredAlerts();
      const newAlert = {
        id: alerts.length > 0 ? Math.max(...alerts.map(a => a.id)) + 1 : 1,
        ...payload,
        active: payload.active !== undefined ? payload.active : 1,
        issued_at: new Date().toISOString(),
      };
      alerts.unshift(newAlert);
      setStoredAlerts(alerts);
      return newAlert;
    }
  },

  async updateAlert(id, payload) {
    try {
      const res = await fetch(`${BASE_URL}/api/v1/alerts/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(3500),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail ? JSON.stringify(err.detail) : `HTTP ${res.status}`);
      }
      return await res.json();
    } catch (error) {
      if (!this.isMockMode && !error.message.includes('Failed to fetch') && !error.name.includes('Abort')) {
        throw error;
      }
      const alerts = getStoredAlerts();
      const index = alerts.findIndex(a => a.id === Number(id));
      if (index === -1) throw new Error('Alert not found');
      alerts[index] = {
        ...alerts[index],
        ...payload,
      };
      setStoredAlerts(alerts);
      return alerts[index];
    }
  },

  async deleteAlert(id) {
    try {
      const res = await fetch(`${BASE_URL}/api/v1/alerts/${id}`, {
        method: 'DELETE',
        signal: AbortSignal.timeout(3500),
      });
      if (!res.ok && res.status !== 404) throw new Error(`HTTP ${res.status}`);
      return true;
    } catch (error) {
      if (!this.isMockMode && !error.message.includes('Failed to fetch') && !error.name.includes('Abort')) {
        throw error;
      }
      const alerts = getStoredAlerts().filter(a => a.id !== Number(id));
      setStoredAlerts(alerts);
      return true;
    }
  },

  // Reset demo data helper
  resetDemoData() {
    localStorage.setItem(LS_RISKS, JSON.stringify(INITIAL_RISKS));
    localStorage.setItem(LS_ALERTS, JSON.stringify(INITIAL_ALERTS));
  }
};
