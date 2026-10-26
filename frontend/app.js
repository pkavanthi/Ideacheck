/**
 * DisasterOps Tactical Command — Dynamic Frontend Application
 * Handles Real-time Incidents, Resource Tracking, Interactive Leaflet Map,
 * Tactical Analytics Charts, and Full CRUD Integration.
 */

(function () {
  'use strict';

  // --- API Configuration ---
  const API_BASE = '/api/v1';

  // --- Application State ---
  const state = {
    incidents: [],
    resources: [],
    activeTab: 'overviewTab',
    autoRefreshTimer: null,
    autoRefreshInterval: 10000, // 10s
    map: null,
    mapMarkers: [],
    charts: {
      severity: null,
      status: null,
      resourceStatus: null,
      resourceType: null,
    },
    deleteTarget: null, // { type: 'incident'|'resource', id, name }
  };

  // --- Realistic Demo Seed Data ---
  const DEMO_INCIDENTS = [
    {
      title: "Mahanadi River Surge & Embankment Breach",
      description: "Water levels exceeded danger mark by 1.8m. Low-lying wards 4, 7, and 12 inundated. Evacuation boats requested.",
      location: "Cuttack Sadar, Ward 12, Odisha",
      latitude: 20.4625,
      longitude: 85.8830,
      severity: "critical",
      status: "active",
      affected_population: 14500,
      reported_by: "District Collectorate Control Room"
    },
    {
      title: "Severe Coastal Cyclone Warning - Landfall Zone",
      description: "Severe Cyclonic Storm tracking towards coast with wind speeds 110-120 kmph. High tide storm surge imminent.",
      location: "Puri Coastal Belt, Odisha",
      latitude: 19.8135,
      longitude: 85.8312,
      severity: "high",
      status: "active",
      affected_population: 32000,
      reported_by: "IMD Early Warning Center"
    },
    {
      title: "Meppadi Hillside Landslide & Debris Flow",
      description: "Heavy continuous monsoon triggered soil erosion and multiple road blockages. Search and rescue underway.",
      location: "Meppadi, Wayanad District, Kerala",
      latitude: 11.5540,
      longitude: 76.1280,
      severity: "critical",
      status: "active",
      affected_population: 4800,
      reported_by: "State Disaster Response Force (SDRF)"
    },
    {
      title: "Chemical Storage Warehouse Fire",
      description: "Industrial warehouse fire with toxic smoke plume. 500m perimeter evacuated.",
      location: "Bhiwandi Logistics Hub, Maharashtra",
      latitude: 19.2967,
      longitude: 73.0631,
      severity: "high",
      status: "contained",
      affected_population: 1200,
      reported_by: "Chief Fire Officer Bhiwandi"
    },
    {
      title: "Rural Water Supply Contamination Outbreak",
      description: "Flash flood runoff affected local borewells. Clean drinking water packets and chlorine tablets required.",
      location: "Tehsil Barabanki, Uttar Pradesh",
      latitude: 26.9268,
      longitude: 81.1834,
      severity: "medium",
      status: "reported",
      affected_population: 3500,
      reported_by: "Primary Health Center Officer"
    },
    {
      title: "Bridge Approach Road Subsidence",
      description: "Culvert foundation weakened after heavy rainfall. Traffic diverted to alternate highway.",
      location: "NH-31 Highway Crossing, Bihar",
      latitude: 25.5941,
      longitude: 85.1376,
      severity: "low",
      status: "resolved",
      affected_population: 400,
      reported_by: "NHAI Highway Patrol"
    }
  ];

  const DEMO_RESOURCES = [
    {
      name: "NDRF 04 Battalion Quick Response Team",
      type: "rescue_team",
      quantity: 45,
      unit: "personnel",
      location: "Bhubaneswar Regional Base Hub",
      status: "deployed",
      contact_info: "Cmdt. Rajesh Verma (VHF Ch 16 / +91-9876543210)",
      notes: "Equipped with 6 inflatable motorized boats, underwater cameras, and satellite radios."
    },
    {
      name: "Mobile Trauma & Emergency ICU Unit",
      type: "medical_unit",
      quantity: 4,
      unit: "ambulances",
      location: "District HQ Hospital, Cuttack",
      status: "deployed",
      contact_info: "Dr. Ananya Sen (+91-9811223344)",
      notes: "Equipped with portable ventilators, oxygen concentrators, and emergency surgical kits."
    },
    {
      name: "Amphibious All-Terrain Rescue Vehicles (ARV)",
      type: "vehicle",
      quantity: 6,
      unit: "vehicles",
      location: "Coastal Staging Area Beta",
      status: "available",
      contact_info: "Logistics Officer S. Patil (+91-9445566778)",
      notes: "Capable of navigating 1.5m floodwaters and mud flats."
    },
    {
      name: "Emergency Cyclone Relief Shelter Camp 01",
      type: "shelter",
      quantity: 2500,
      unit: "capacity",
      location: "Puri Multi-Purpose Cyclone Shelter",
      status: "available",
      contact_info: "Block Development Officer (+91-9822334455)",
      notes: "Generator backup, RO water filtration, separate medical ward."
    },
    {
      name: "Heavy Hydraulic Excavator & Crane Squad",
      type: "heavy_equipment",
      quantity: 8,
      unit: "heavy machinery",
      location: "Wayanad Disaster Staging Yard",
      status: "deployed",
      contact_info: "Eng. Suresh Nair (+91-9733445566)",
      notes: "Tracked excavators and rock breakers for debris removal."
    },
    {
      name: "Emergency Potable Water & Rations Packets",
      type: "food_water",
      quantity: 12000,
      unit: "ration kits",
      location: "Central Warehouse, Lucknow",
      status: "available",
      contact_info: "Supply Officer M. Khan (+91-9899001122)",
      notes: "Ready-to-eat meals and 1L sealed drinking water pouches."
    },
    {
      name: "Tactical Satellite Comms & HAM Terminal",
      type: "communication",
      quantity: 5,
      unit: "satellite terminals",
      location: "SDMA Central Command Room",
      status: "available",
      contact_info: "Signals Officer (+91-9988776655)",
      notes: "Inmarsat and Starlink backup links for remote zones."
    }
  ];

  // --- Toast Manager ---
  function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'danger') icon = '⚠️';

    toast.innerHTML = `<span>${icon}</span><span>${escapeHtml(message)}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(30px)';
      setTimeout(() => toast.remove(), 250);
    }, 3500);
  }

  // --- Helper Utilities ---
  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function formatTime(isoStr) {
    if (!isoStr) return 'N/A';
    try {
      const date = new Date(isoStr);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
      return isoStr;
    }
  }

  function formatNumber(num) {
    if (num === null || num === undefined) return '0';
    return Number(num).toLocaleString();
  }

  // --- API Client ---
  async function apiFetch(endpoint, options = {}) {
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: {
          ...defaultHeaders,
          ...options.headers,
        },
      });

      if (!response.ok) {
        let errorDetail = `HTTP ${response.status}: ${response.statusText}`;
        try {
          const errJson = await response.json();
          if (errJson && errJson.detail) {
            errorDetail = typeof errJson.detail === 'string' ? errJson.detail : JSON.stringify(errJson.detail);
          }
        } catch (_) {}
        throw new Error(errorDetail);
      }

      if (response.status === 204) {
        return null;
      }

      return await response.json();
    } catch (err) {
      console.error(`API Error on [${options.method || 'GET'} ${endpoint}]:`, err);
      throw err;
    }
  }

  // --- Tactical Map Management ---
  function initMap() {
    const mapElement = document.getElementById('tacticalMap');
    if (!mapElement) return;

    // Center on India by default (20.5937° N, 78.9629° E)
    state.map = L.map('tacticalMap', {
      zoomControl: true,
      attributionControl: false,
    }).setView([20.5937, 78.9629], 5);

    // Dark tile layer (CartoDB Dark Matter) with OSM fallback
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      subdomains: 'abcd',
    }).addTo(state.map);

    // Click anywhere on map to pre-fill coordinates in incident modal
    state.map.on('click', function (e) {
      const lat = parseFloat(e.latlng.lat.toFixed(6));
      const lng = parseFloat(e.latlng.lng.toFixed(6));
      openIncidentModal(null, lat, lng);
      showToast(`Selected coordinates: ${lat}, ${lng}`, 'info');
    });

    // Reset view button
    document.getElementById('btnResetMapView')?.addEventListener('click', () => {
      if (state.incidents.some(i => i.latitude && i.longitude)) {
        fitMapToMarkers();
      } else {
        state.map.setView([20.5937, 78.9629], 5);
      }
    });
  }

  function renderMapMarkers() {
    if (!state.map) return;

    // Clear existing markers
    state.mapMarkers.forEach(m => state.map.removeLayer(m));
    state.mapMarkers = [];

    const geoIncidents = state.incidents.filter(i => i.latitude !== null && i.longitude !== null && !isNaN(i.latitude) && !isNaN(i.longitude));
    const markerCountEl = document.getElementById('mapMarkerCount');
    if (markerCountEl) {
      markerCountEl.textContent = `${geoIncidents.length} geo-located incident${geoIncidents.length === 1 ? '' : 's'}`;
    }

    geoIncidents.forEach(incident => {
      const severity = (incident.severity || 'medium').toLowerCase();
      
      const customIcon = L.divIcon({
        className: 'custom-tactical-marker',
        html: `<div class="marker-pin ${severity}" title="${escapeHtml(incident.title)}">🚨</div>`,
        iconSize: [26, 26],
        iconAnchor: [13, 13],
        popupAnchor: [0, -14],
      });

      const marker = L.marker([incident.latitude, incident.longitude], { icon: customIcon });

      const popupHtml = `
        <div class="map-popup-card">
          <div class="map-popup-title">${escapeHtml(incident.title)}</div>
          <div class="map-popup-info">
            <div><strong>Location:</strong> ${escapeHtml(incident.location)}</div>
            <div><strong>Severity:</strong> <span class="badge badge-${severity}">${severity.toUpperCase()}</span></div>
            <div><strong>Status:</strong> <span class="badge badge-${(incident.status||'reported').toLowerCase()}">${(incident.status||'').toUpperCase()}</span></div>
            <div><strong>Affected Pop:</strong> ${formatNumber(incident.affected_population)}</div>
            <div><strong>Reported:</strong> ${formatTime(incident.created_at)}</div>
          </div>
          <div class="map-popup-actions">
            <button class="btn btn-xs btn-primary" onclick="window.DisasterOpsApp.openIncidentModal(${incident.id})">Edit</button>
            <button class="btn btn-xs btn-secondary" onclick="window.DisasterOpsApp.quickAdvanceIncidentStatus(${incident.id})">Advance Status</button>
          </div>
        </div>
      `;

      marker.bindPopup(popupHtml);
      marker.addTo(state.map);
      state.mapMarkers.push(marker);
    });
  }

  function fitMapToMarkers() {
    if (!state.map || state.mapMarkers.length === 0) return;
    const group = L.featureGroup(state.mapMarkers);
    state.map.fitBounds(group.getBounds().pad(0.15));
  }

  // --- Tactical Analytics Charts ---
  function initCharts() {
    if (typeof Chart === 'undefined') return;

    // Dark chart default theme
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.borderColor = '#222f46';
    Chart.defaults.font.family = "'Inter', sans-serif";

    // Chart 1: Severity
    const ctxSeverity = document.getElementById('chartSeverity')?.getContext('2d');
    if (ctxSeverity) {
      state.charts.severity = new Chart(ctxSeverity, {
        type: 'doughnut',
        data: {
          labels: ['Critical', 'High', 'Medium', 'Low'],
          datasets: [{
            data: [0, 0, 0, 0],
            backgroundColor: ['#ef4444', '#f59e0b', '#eab308', '#10b981'],
            borderWidth: 2,
            borderColor: '#141d2d',
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' }
          }
        }
      });
    }

    // Chart 2: Status
    const ctxStatus = document.getElementById('chartStatus')?.getContext('2d');
    if (ctxStatus) {
      state.charts.status = new Chart(ctxStatus, {
        type: 'bar',
        data: {
          labels: ['Reported', 'Active', 'Contained', 'Resolved'],
          datasets: [{
            label: 'Incidents Count',
            data: [0, 0, 0, 0],
            backgroundColor: ['#38bdf8', '#f59e0b', '#06b6d4', '#10b981'],
            borderRadius: 4,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { beginAtZero: true, ticks: { stepSize: 1 } }
          }
        }
      });
    }

    // Chart 3: Resource Status
    const ctxResStatus = document.getElementById('chartResourceStatus')?.getContext('2d');
    if (ctxResStatus) {
      state.charts.resourceStatus = new Chart(ctxResStatus, {
        type: 'doughnut',
        data: {
          labels: ['Available', 'Deployed', 'Unavailable'],
          datasets: [{
            data: [0, 0, 0],
            backgroundColor: ['#10b981', '#38bdf8', '#64748b'],
            borderWidth: 2,
            borderColor: '#141d2d',
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { position: 'bottom' }
          }
        }
      });
    }

    // Chart 4: Resource Type
    const ctxResType = document.getElementById('chartResourceType')?.getContext('2d');
    if (ctxResType) {
      state.charts.resourceType = new Chart(ctxResType, {
        type: 'bar',
        data: {
          labels: [],
          datasets: [{
            label: 'Total Units',
            data: [],
            backgroundColor: '#3b82f6',
            borderRadius: 4,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { beginAtZero: true, ticks: { stepSize: 1 } }
          }
        }
      });
    }
  }

  function updateCharts() {
    if (!state.charts.severity) return;

    // Severity counts
    const sevMap = { critical: 0, high: 0, medium: 0, low: 0 };
    state.incidents.forEach(i => {
      const s = (i.severity || '').toLowerCase();
      if (sevMap[s] !== undefined) sevMap[s]++;
    });
    state.charts.severity.data.datasets[0].data = [sevMap.critical, sevMap.high, sevMap.medium, sevMap.low];
    state.charts.severity.update();

    // Status counts
    const stMap = { reported: 0, active: 0, contained: 0, resolved: 0 };
    state.incidents.forEach(i => {
      const s = (i.status || '').toLowerCase();
      if (stMap[s] !== undefined) stMap[s]++;
    });
    state.charts.status.data.datasets[0].data = [stMap.reported, stMap.active, stMap.contained, stMap.resolved];
    state.charts.status.update();

    // Resource Status
    const resStMap = { available: 0, deployed: 0, unavailable: 0 };
    state.resources.forEach(r => {
      const s = (r.status || '').toLowerCase();
      if (resStMap[s] !== undefined) resStMap[s]++;
    });
    state.charts.resourceStatus.data.datasets[0].data = [resStMap.available, resStMap.deployed, resStMap.unavailable];
    state.charts.resourceStatus.update();

    // Resource Type
    const typeCountMap = {};
    state.resources.forEach(r => {
      const t = r.type || 'other';
      const label = t.replace(/_/g, ' ').toUpperCase();
      typeCountMap[label] = (typeCountMap[label] || 0) + (r.quantity || 1);
    });
    const typeLabels = Object.keys(typeCountMap);
    const typeValues = Object.values(typeCountMap);
    state.charts.resourceType.data.labels = typeLabels;
    state.charts.resourceType.data.datasets[0].data = typeValues;
    state.charts.resourceType.update();
  }

  // --- Data Loading & UI Rendering ---
  async function loadAllData() {
    try {
      const [incidents, resources] = await Promise.all([
        apiFetch('/incidents/'),
        apiFetch('/resources/'),
      ]);

      state.incidents = incidents || [];
      state.resources = resources || [];

      renderKPIs();
      renderLiveAlertsFeed();
      renderIncidentsTable();
      renderResourcesTable();
      renderMapMarkers();
      updateCharts();

      const incidentTabCount = document.getElementById('tabIncidentCount');
      if (incidentTabCount) incidentTabCount.textContent = state.incidents.length;

      const resourceTabCount = document.getElementById('tabResourceCount');
      if (resourceTabCount) resourceTabCount.textContent = state.resources.length;

    } catch (err) {
      console.error('Error fetching system data:', err);
      showToast(`Error fetching live data: ${err.message}`, 'danger');
    }
  }

  function renderKPIs() {
    const totalIncidents = state.incidents.length;
    const criticalIncidents = state.incidents.filter(i => i.severity === 'critical').length;
    const highIncidents = state.incidents.filter(i => i.severity === 'high').length;
    const activeIncidents = state.incidents.filter(i => i.status === 'active').length;
    const containedIncidents = state.incidents.filter(i => i.status === 'contained').length;
    const resolvedIncidents = state.incidents.filter(i => i.status === 'resolved').length;
    
    const affectedPop = state.incidents.reduce((sum, i) => sum + (i.affected_population || 0), 0);

    const totalResources = state.resources.length;
    const deployedResources = state.resources.filter(r => r.status === 'deployed').length;
    const availableResources = state.resources.filter(r => r.status === 'available').length;

    // Update Elements
    const elTotal = document.getElementById('kpiTotalIncidents');
    if (elTotal) elTotal.textContent = totalIncidents;

    const elCritCount = document.getElementById('kpiCriticalCount');
    if (elCritCount) elCritCount.textContent = `${criticalIncidents} Critical / ${highIncidents} High`;

    const elCritBar = document.getElementById('kpiCriticalBar');
    if (elCritBar) {
      const critPct = totalIncidents > 0 ? ((criticalIncidents + highIncidents) / totalIncidents) * 100 : 0;
      elCritBar.style.width = `${critPct}%`;
    }

    const elActive = document.getElementById('kpiActiveIncidents');
    if (elActive) elActive.textContent = activeIncidents;

    const elContained = document.getElementById('kpiContainedCount');
    if (elContained) elContained.textContent = `${containedIncidents} Contained / ${resolvedIncidents} Resolved`;

    const elActiveBar = document.getElementById('kpiActiveBar');
    if (elActiveBar) {
      const actPct = totalIncidents > 0 ? (activeIncidents / totalIncidents) * 100 : 0;
      elActiveBar.style.width = `${actPct}%`;
    }

    const elPop = document.getElementById('kpiAffectedPopulation');
    if (elPop) elPop.textContent = formatNumber(affectedPop);

    const elRes = document.getElementById('kpiTotalResources');
    if (elRes) elRes.textContent = totalResources;

    const elResRate = document.getElementById('kpiResourceDeploymentRate');
    if (elResRate) elResRate.textContent = `${deployedResources} Deployed / ${availableResources} Available`;

    const elResBar = document.getElementById('kpiResourceBar');
    if (elResBar) {
      const depPct = totalResources > 0 ? (deployedResources / totalResources) * 100 : 0;
      elResBar.style.width = `${depPct}%`;
    }
  }

  function renderLiveAlertsFeed() {
    const container = document.getElementById('liveAlertsList');
    if (!container) return;

    if (state.incidents.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <span class="empty-icon">🛰️</span>
          <p>No active incidents registered.</p>
          <button class="btn btn-sm btn-outline mt-2" onclick="window.DisasterOpsApp.seedSampleData()">Seed Mock Incidents</button>
        </div>
      `;
      return;
    }

    // Sort by severity (critical first) then newest
    const sorted = [...state.incidents].sort((a, b) => {
      const rank = { critical: 4, high: 3, medium: 2, low: 1 };
      const rankA = rank[(a.severity || '').toLowerCase()] || 0;
      const rankB = rank[(b.severity || '').toLowerCase()] || 0;
      if (rankB !== rankA) return rankB - rankA;
      return new Date(b.created_at || 0) - new Date(a.created_at || 0);
    });

    let html = '';
    sorted.slice(0, 8).forEach(incident => {
      const severity = (incident.severity || 'medium').toLowerCase();
      const status = (incident.status || 'reported').toLowerCase();
      html += `
        <div class="alert-feed-item ${severity}" onclick="window.DisasterOpsApp.focusIncidentOnMap(${incident.id})">
          <div class="alert-feed-header">
            <span class="alert-feed-title">${escapeHtml(incident.title)}</span>
            <span class="badge badge-${severity}">${severity}</span>
          </div>
          <div class="cell-subtext">${escapeHtml(incident.location)}</div>
          <div class="alert-feed-meta">
            <span class="badge badge-${status}">${status}</span>
            <span>👥 ${formatNumber(incident.affected_population)} affected</span>
            <span>🕒 ${formatTime(incident.created_at)}</span>
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }

  function renderIncidentsTable() {
    const tbody = document.getElementById('incidentsTableBody');
    if (!tbody) return;

    const filterSev = document.getElementById('filterIncidentSeverity')?.value.toLowerCase() || '';
    const filterStat = document.getElementById('filterIncidentStatus')?.value.toLowerCase() || '';
    const searchQuery = (document.getElementById('searchIncidentsInput')?.value || document.getElementById('globalSearchInput')?.value || '').toLowerCase().trim();

    let filtered = state.incidents.filter(inc => {
      if (filterSev && (inc.severity || '').toLowerCase() !== filterSev) return false;
      if (filterStat && (inc.status || '').toLowerCase() !== filterStat) return false;
      if (searchQuery) {
        const title = (inc.title || '').toLowerCase();
        const loc = (inc.location || '').toLowerCase();
        const desc = (inc.description || '').toLowerCase();
        const rep = (inc.reported_by || '').toLowerCase();
        if (!title.includes(searchQuery) && !loc.includes(searchQuery) && !desc.includes(searchQuery) && !rep.includes(searchQuery)) {
          return false;
        }
      }
      return true;
    });

    if (filtered.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" class="text-center" style="padding: 2.5rem; color: var(--text-muted);">
            No matching incidents found.
          </td>
        </tr>
      `;
      return;
    }

    let rowsHtml = '';
    filtered.forEach(inc => {
      const severity = (inc.severity || 'medium').toLowerCase();
      const status = (inc.status || 'reported').toLowerCase();
      const geoCoords = (inc.latitude !== null && inc.longitude !== null && inc.latitude !== undefined) 
        ? `<div class="cell-geo">📍 ${inc.latitude.toFixed(4)}, ${inc.longitude.toFixed(4)}</div>` 
        : '<div class="cell-subtext text-muted">No geo coords</div>';

      rowsHtml += `
        <tr>
          <td><span class="badge badge-subtle">#${inc.id}</span></td>
          <td>
            <span class="cell-title">${escapeHtml(inc.title)}</span>
            <span class="cell-subtext">${escapeHtml(inc.description || 'No description provided')}</span>
          </td>
          <td>
            <div>${escapeHtml(inc.location)}</div>
            ${geoCoords}
          </td>
          <td>
            <span class="badge badge-${severity}">${severity}</span>
          </td>
          <td>
            <span class="badge badge-${status}">${status}</span>
          </td>
          <td>
            <strong>${formatNumber(inc.affected_population)}</strong>
          </td>
          <td>
            <div>${escapeHtml(inc.reported_by || 'Anonymous')}</div>
            <div class="cell-subtext">${formatTime(inc.created_at)}</div>
          </td>
          <td style="text-align: right;">
            <div style="display: inline-flex; gap: 4px;">
              <button class="btn-icon" title="Advance Operational Status" onclick="window.DisasterOpsApp.quickAdvanceIncidentStatus(${inc.id})">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
              </button>
              <button class="btn-icon" title="Edit Incident" onclick="window.DisasterOpsApp.openIncidentModal(${inc.id})">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
              </button>
              <button class="btn-icon danger" title="Delete Incident" onclick="window.DisasterOpsApp.promptDeleteIncident(${inc.id}, '${escapeHtml(inc.title)}')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
              </button>
            </div>
          </td>
        </tr>
      `;
    });

    tbody.innerHTML = rowsHtml;
  }

  function renderResourcesTable() {
    const tbody = document.getElementById('resourcesTableBody');
    if (!tbody) return;

    const filterType = document.getElementById('filterResourceType')?.value || '';
    const filterStat = document.getElementById('filterResourceStatus')?.value.toLowerCase() || '';
    const searchQuery = (document.getElementById('searchResourcesInput')?.value || document.getElementById('globalSearchInput')?.value || '').toLowerCase().trim();

    let filtered = state.resources.filter(res => {
      if (filterType && res.type !== filterType) return false;
      if (filterStat && (res.status || '').toLowerCase() !== filterStat) return false;
      if (searchQuery) {
        const name = (res.name || '').toLowerCase();
        const loc = (res.location || '').toLowerCase();
        const contact = (res.contact_info || '').toLowerCase();
        const notes = (res.notes || '').toLowerCase();
        if (!name.includes(searchQuery) && !loc.includes(searchQuery) && !contact.includes(searchQuery) && !notes.includes(searchQuery)) {
          return false;
        }
      }
      return true;
    });

    if (filtered.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="8" class="text-center" style="padding: 2.5rem; color: var(--text-muted);">
            No matching resources found.
          </td>
        </tr>
      `;
      return;
    }

    let rowsHtml = '';
    filtered.forEach(res => {
      const status = (res.status || 'available').toLowerCase();
      const typeDisplay = (res.type || 'other').replace(/_/g, ' ').toUpperCase();
      const toggleActionTitle = status === 'available' ? 'Deploy Resource' : 'Return to Available';

      rowsHtml += `
        <tr>
          <td><span class="badge badge-subtle">#${res.id}</span></td>
          <td>
            <span class="cell-title">${escapeHtml(res.name)}</span>
          </td>
          <td>
            <span class="badge badge-type">${typeDisplay}</span>
          </td>
          <td>
            <strong>${res.quantity}</strong> <span class="cell-subtext">${escapeHtml(res.unit || 'units')}</span>
          </td>
          <td>
            <div>${escapeHtml(res.location || 'Unassigned Hub')}</div>
          </td>
          <td>
            <span class="badge badge-${status}">${status}</span>
          </td>
          <td>
            <div>${escapeHtml(res.contact_info || 'No contact specified')}</div>
            <div class="cell-subtext">${escapeHtml(res.notes || '')}</div>
          </td>
          <td style="text-align: right;">
            <div style="display: inline-flex; gap: 4px;">
              <button class="btn btn-xs ${status === 'available' ? 'btn-outline' : 'btn-secondary'}" title="${toggleActionTitle}" onclick="window.DisasterOpsApp.toggleResourceDeployment(${res.id})">
                ${status === 'available' ? 'Deploy' : 'Recall'}
              </button>
              <button class="btn-icon" title="Edit Resource" onclick="window.DisasterOpsApp.openResourceModal(${res.id})">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
              </button>
              <button class="btn-icon danger" title="Delete Resource" onclick="window.DisasterOpsApp.promptDeleteResource(${res.id}, '${escapeHtml(res.name)}')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
              </button>
            </div>
          </td>
        </tr>
      `;
    });

    tbody.innerHTML = rowsHtml;
  }

  // --- Quick Status Progression ---
  async function quickAdvanceIncidentStatus(id) {
    const inc = state.incidents.find(i => i.id === id);
    if (!inc) return;

    const cycle = {
      reported: 'active',
      active: 'contained',
      contained: 'resolved',
      resolved: 'reported'
    };
    const nextStatus = cycle[(inc.status || 'reported').toLowerCase()] || 'active';

    try {
      await apiFetch(`/incidents/${id}`, {
        method: 'PATCH',
        body: JSON.stringify({ status: nextStatus })
      });
      showToast(`Incident #${id} advanced to ${nextStatus.toUpperCase()}`, 'success');
      await loadAllData();
    } catch (err) {
      showToast(`Failed to update status: ${err.message}`, 'danger');
    }
  }

  async function toggleResourceDeployment(id) {
    const res = state.resources.find(r => r.id === id);
    if (!res) return;

    const nextStatus = (res.status === 'available') ? 'deployed' : 'available';
    try {
      await apiFetch(`/resources/${id}`, {
        method: 'PATCH',
        body: JSON.stringify({ status: nextStatus })
      });
      showToast(`Resource #${id} status changed to ${nextStatus.toUpperCase()}`, 'success');
      await loadAllData();
    } catch (err) {
      showToast(`Failed to update resource: ${err.message}`, 'danger');
    }
  }

  function focusIncidentOnMap(id) {
    const inc = state.incidents.find(i => i.id === id);
    if (!inc || !state.map) return;

    // Switch to Map tab
    switchTab('overviewTab');

    if (inc.latitude && inc.longitude) {
      state.map.flyTo([inc.latitude, inc.longitude], 12, { duration: 1.2 });
      const marker = state.mapMarkers.find(m => {
        const pos = m.getLatLng();
        return Math.abs(pos.lat - inc.latitude) < 0.0001 && Math.abs(pos.lng - inc.longitude) < 0.0001;
      });
      if (marker) {
        setTimeout(() => marker.openPopup(), 1300);
      }
    } else {
      showToast(`Incident #${id} does not have geo coordinates assigned`, 'info');
    }
  }

  // --- Modals Management ---
  function openIncidentModal(id = null, defaultLat = null, defaultLng = null) {
    const modal = document.getElementById('incidentModal');
    const titleEl = document.getElementById('incidentModalTitle');
    const form = document.getElementById('incidentForm');
    form.reset();

    if (id) {
      const inc = state.incidents.find(i => i.id === id);
      if (!inc) return;
      titleEl.textContent = `Edit Incident #${inc.id}`;
      document.getElementById('incidentFormId').value = inc.id;
      document.getElementById('incidentTitle').value = inc.title || '';
      document.getElementById('incidentSeverity').value = (inc.severity || 'medium').toLowerCase();
      document.getElementById('incidentStatus').value = (inc.status || 'reported').toLowerCase();
      document.getElementById('incidentLocation').value = inc.location || '';
      document.getElementById('incidentLatitude').value = inc.latitude !== null && inc.latitude !== undefined ? inc.latitude : '';
      document.getElementById('incidentLongitude').value = inc.longitude !== null && inc.longitude !== undefined ? inc.longitude : '';
      document.getElementById('incidentPopulation').value = inc.affected_population || 0;
      document.getElementById('incidentReportedBy').value = inc.reported_by || '';
      document.getElementById('incidentDescription').value = inc.description || '';
    } else {
      titleEl.textContent = 'Report New Incident';
      document.getElementById('incidentFormId').value = '';
      if (defaultLat !== null && defaultLng !== null) {
        document.getElementById('incidentLatitude').value = defaultLat;
        document.getElementById('incidentLongitude').value = defaultLng;
        document.getElementById('incidentLocation').value = `Geo (${defaultLat}, ${defaultLng})`;
      }
    }

    modal.classList.add('show');
    document.getElementById('incidentTitle').focus();
  }

  function closeIncidentModal() {
    document.getElementById('incidentModal')?.classList.remove('show');
  }

  function openResourceModal(id = null) {
    const modal = document.getElementById('resourceModal');
    const titleEl = document.getElementById('resourceModalTitle');
    const form = document.getElementById('resourceForm');
    form.reset();

    if (id) {
      const res = state.resources.find(r => r.id === id);
      if (!res) return;
      titleEl.textContent = `Edit Resource #${res.id}`;
      document.getElementById('resourceFormId').value = res.id;
      document.getElementById('resourceName').value = res.name || '';
      document.getElementById('resourceType').value = res.type || 'rescue_team';
      document.getElementById('resourceStatus').value = (res.status || 'available').toLowerCase();
      document.getElementById('resourceQuantity').value = res.quantity || 1;
      document.getElementById('resourceUnit').value = res.unit || '';
      document.getElementById('resourceLocation').value = res.location || '';
      document.getElementById('resourceContact').value = res.contact_info || '';
      document.getElementById('resourceNotes').value = res.notes || '';
    } else {
      titleEl.textContent = 'Register Emergency Resource';
      document.getElementById('resourceFormId').value = '';
    }

    modal.classList.add('show');
    document.getElementById('resourceName').focus();
  }

  function closeResourceModal() {
    document.getElementById('resourceModal')?.classList.remove('show');
  }

  // --- Deletion Flow ---
  function promptDeleteIncident(id, name) {
    state.deleteTarget = { type: 'incident', id, name };
    const msg = document.getElementById('deleteModalMessage');
    if (msg) msg.textContent = `Are you sure you want to permanently delete incident "${name}" (ID: #${id})?`;
    document.getElementById('confirmDeleteModal')?.classList.add('show');
  }

  function promptDeleteResource(id, name) {
    state.deleteTarget = { type: 'resource', id, name };
    const msg = document.getElementById('deleteModalMessage');
    if (msg) msg.textContent = `Are you sure you want to permanently delete resource "${name}" (ID: #${id})?`;
    document.getElementById('confirmDeleteModal')?.classList.add('show');
  }

  function closeDeleteModal() {
    state.deleteTarget = null;
    document.getElementById('confirmDeleteModal')?.classList.remove('show');
  }

  async function executeDelete() {
    if (!state.deleteTarget) return;
    const { type, id, name } = state.deleteTarget;
    try {
      if (type === 'incident') {
        await apiFetch(`/incidents/${id}`, { method: 'DELETE' });
        showToast(`Incident "${name}" deleted successfully`, 'success');
      } else if (type === 'resource') {
        await apiFetch(`/resources/${id}`, { method: 'DELETE' });
        showToast(`Resource "${name}" deleted successfully`, 'success');
      }
      closeDeleteModal();
      await loadAllData();
    } catch (err) {
      showToast(`Delete failed: ${err.message}`, 'danger');
    }
  }

  // --- Form Handlers ---
  async function handleIncidentSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('incidentFormId').value;
    const title = document.getElementById('incidentTitle').value.trim();
    const location = document.getElementById('incidentLocation').value.trim();
    const severity = document.getElementById('incidentSeverity').value;
    const status = document.getElementById('incidentStatus').value;
    const latStr = document.getElementById('incidentLatitude').value.trim();
    const lngStr = document.getElementById('incidentLongitude').value.trim();
    const popStr = document.getElementById('incidentPopulation').value.trim();
    const reportedBy = document.getElementById('incidentReportedBy').value.trim();
    const description = document.getElementById('incidentDescription').value.trim();

    if (!title || !location) {
      showToast('Title and Location are required fields.', 'danger');
      return;
    }

    const payload = {
      title,
      location,
      severity,
      description: description || null,
      reported_by: reportedBy || null,
      affected_population: popStr ? parseInt(popStr, 10) : 0,
      latitude: latStr ? parseFloat(latStr) : null,
      longitude: lngStr ? parseFloat(lngStr) : null,
    };

    if (id) {
      payload.status = status;
    }

    try {
      if (id) {
        await apiFetch(`/incidents/${id}`, {
          method: 'PATCH',
          body: JSON.stringify(payload),
        });
        showToast('Incident updated successfully!', 'success');
      } else {
        await apiFetch('/incidents/', {
          method: 'POST',
          body: JSON.stringify(payload),
        });
        showToast('New Incident reported successfully!', 'success');
      }
      closeIncidentModal();
      await loadAllData();
    } catch (err) {
      showToast(`Failed to save incident: ${err.message}`, 'danger');
    }
  }

  async function handleResourceSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('resourceFormId').value;
    const name = document.getElementById('resourceName').value.trim();
    const type = document.getElementById('resourceType').value;
    const status = document.getElementById('resourceStatus').value;
    const qtyStr = document.getElementById('resourceQuantity').value.trim();
    const unit = document.getElementById('resourceUnit').value.trim();
    const location = document.getElementById('resourceLocation').value.trim();
    const contactInfo = document.getElementById('resourceContact').value.trim();
    const notes = document.getElementById('resourceNotes').value.trim();

    if (!name || !type) {
      showToast('Name and Type are required fields.', 'danger');
      return;
    }

    const payload = {
      name,
      type,
      status,
      quantity: qtyStr ? parseInt(qtyStr, 10) : 1,
      unit: unit || null,
      location: location || null,
      contact_info: contactInfo || null,
      notes: notes || null,
    };

    try {
      if (id) {
        await apiFetch(`/resources/${id}`, {
          method: 'PATCH',
          body: JSON.stringify(payload),
        });
        showToast('Resource updated successfully!', 'success');
      } else {
        await apiFetch('/resources/', {
          method: 'POST',
          body: JSON.stringify(payload),
        });
        showToast('New Resource registered successfully!', 'success');
      }
      closeResourceModal();
      await loadAllData();
    } catch (err) {
      showToast(`Failed to save resource: ${err.message}`, 'danger');
    }
  }

  // --- Demo Seeding Action ---
  async function seedSampleData() {
    try {
      showToast('Seeding realistic incident and resource mock data...', 'info');

      // Create incidents in parallel
      const incidentPromises = DEMO_INCIDENTS.map(inc => 
        apiFetch('/incidents/', { method: 'POST', body: JSON.stringify(inc) })
      );

      // Create resources in parallel
      const resourcePromises = DEMO_RESOURCES.map(res => 
        apiFetch('/resources/', { method: 'POST', body: JSON.stringify(res) })
      );

      await Promise.all([...incidentPromises, ...resourcePromises]);

      showToast('Demo data seeded successfully! 6 incidents and 7 resources added.', 'success');
      await loadAllData();
      fitMapToMarkers();
    } catch (err) {
      showToast(`Seeding encountered error: ${err.message}`, 'danger');
    }
  }

  // --- Tab Navigation ---
  function switchTab(tabId) {
    state.activeTab = tabId;
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
    });
    document.querySelectorAll('.tab-content').forEach(pane => {
      pane.classList.toggle('active', pane.id === tabId);
    });

    if (tabId === 'overviewTab' && state.map) {
      setTimeout(() => state.map.invalidateSize(), 200);
    }
    if (tabId === 'analyticsTab') {
      setTimeout(updateCharts, 100);
    }
  }

  // --- Clock & Auto-Refresh ---
  function startClock() {
    const clockEl = document.getElementById('liveClock');
    function update() {
      const now = new Date();
      if (clockEl) {
        clockEl.textContent = now.toUTCString().replace('GMT', 'UTC');
      }
    }
    update();
    setInterval(update, 1000);
  }

  function setupAutoRefresh() {
    const toggle = document.getElementById('autoRefreshToggle');
    if (!toggle) return;

    function restartTimer() {
      if (state.autoRefreshTimer) clearInterval(state.autoRefreshTimer);
      if (toggle.checked) {
        state.autoRefreshTimer = setInterval(() => {
          loadAllData();
        }, state.autoRefreshInterval);
      }
    }

    toggle.addEventListener('change', restartTimer);
    restartTimer();
  }

  // --- Setup Event Listeners ---
  function attachEventListeners() {
    // Tab switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => switchTab(btn.getAttribute('data-tab')));
    });

    // Top action buttons
    document.getElementById('btnRefreshData')?.addEventListener('click', () => {
      showToast('Refreshing data from server...', 'info');
      loadAllData();
    });
    document.getElementById('btnSeedData')?.addEventListener('click', seedSampleData);
    document.getElementById('btnOpenNewIncident')?.addEventListener('click', () => openIncidentModal());
    document.getElementById('btnOpenNewResource')?.addEventListener('click', () => openResourceModal());

    // Incident Modal Close buttons
    document.getElementById('btnCloseIncidentModal')?.addEventListener('click', closeIncidentModal);
    document.getElementById('btnCancelIncidentModal')?.addEventListener('click', closeIncidentModal);
    document.getElementById('incidentForm')?.addEventListener('submit', handleIncidentSubmit);

    // Resource Modal Close buttons
    document.getElementById('btnCloseResourceModal')?.addEventListener('click', closeResourceModal);
    document.getElementById('btnCancelResourceModal')?.addEventListener('click', closeResourceModal);
    document.getElementById('resourceForm')?.addEventListener('submit', handleResourceSubmit);

    // Delete Modal Actions
    document.getElementById('btnCloseDeleteModal')?.addEventListener('click', closeDeleteModal);
    document.getElementById('btnCancelDelete')?.addEventListener('click', closeDeleteModal);
    document.getElementById('btnConfirmDelete')?.addEventListener('click', executeDelete);

    // Filter changes
    document.getElementById('filterIncidentSeverity')?.addEventListener('change', renderIncidentsTable);
    document.getElementById('filterIncidentStatus')?.addEventListener('change', renderIncidentsTable);
    document.getElementById('searchIncidentsInput')?.addEventListener('input', renderIncidentsTable);

    document.getElementById('filterResourceType')?.addEventListener('change', renderResourcesTable);
    document.getElementById('filterResourceStatus')?.addEventListener('change', renderResourcesTable);
    document.getElementById('searchResourcesInput')?.addEventListener('input', renderResourcesTable);

    // Global Search Bar
    document.getElementById('globalSearchInput')?.addEventListener('input', () => {
      renderIncidentsTable();
      renderResourcesTable();
    });

    // Modal Backdrop Clicks & Escape Key
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeIncidentModal();
        closeResourceModal();
        closeDeleteModal();
      }
    });

    document.querySelectorAll('.modal-backdrop').forEach(modal => {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          closeIncidentModal();
          closeResourceModal();
          closeDeleteModal();
        }
      });
    });
  }

  // --- Initial Boot ---
  async function boot() {
    startClock();
    initMap();
    initCharts();
    attachEventListeners();
    setupAutoRefresh();

    await loadAllData();

    // Auto seed initial data if database has no incidents yet
    if (state.incidents.length === 0 && state.resources.length === 0) {
      await seedSampleData();
    }
  }

  // Expose global controller
  window.DisasterOpsApp = {
    openIncidentModal,
    openResourceModal,
    promptDeleteIncident,
    promptDeleteResource,
    quickAdvanceIncidentStatus,
    toggleResourceDeployment,
    focusIncidentOnMap,
    seedSampleData,
    switchTab,
    loadAllData,
  };

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
