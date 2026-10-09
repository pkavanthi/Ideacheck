import React, { useState } from 'react';
import {
  Activity,
  Plus,
  Search,
  Filter,
  MapPin,
  Users,
  Calendar,
  Edit2,
  Trash2,
  Bell,
  AlertTriangle,
  X,
  ExternalLink,
  ChevronRight,
  Sparkles
} from 'lucide-react';
import { REGION_COORDINATE_PRESETS } from '../services/mockData';

export function RisksModule({
  risks = [],
  onCreateRisk,
  onUpdateRisk,
  onDeleteRisk,
  onBroadcastAlert,
  loading
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedHazard, setSelectedHazard] = useState('all');
  const [selectedSeverity, setSelectedSeverity] = useState('all');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'table'

  // Modal states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingRisk, setEditingRisk] = useState(null);
  const [deleteConfirmId, setDeleteConfirmId] = useState(null);

  // Form State
  const [formData, setFormData] = useState({
    title: '',
    hazard_type: 'flood',
    severity: 'medium',
    location: '',
    latitude: '',
    longitude: '',
    description: '',
    affected_population: '',
    reported_by: '',
  });

  const [formError, setFormError] = useState('');

  const openCreateModal = () => {
    setEditingRisk(null);
    setFormData({
      title: '',
      hazard_type: 'flood',
      severity: 'medium',
      location: '',
      latitude: '',
      longitude: '',
      description: '',
      affected_population: '',
      reported_by: 'State Disaster Management Authority (SDMA)',
    });
    setFormError('');
    setIsModalOpen(true);
  };

  const openEditModal = (risk) => {
    setEditingRisk(risk);
    setFormData({
      title: risk.title || '',
      hazard_type: risk.hazard_type || 'flood',
      severity: risk.severity || 'medium',
      location: risk.location || '',
      latitude: risk.latitude !== null && risk.latitude !== undefined ? String(risk.latitude) : '',
      longitude: risk.longitude !== null && risk.longitude !== undefined ? String(risk.longitude) : '',
      description: risk.description || '',
      affected_population: risk.affected_population !== null && risk.affected_population !== undefined ? String(risk.affected_population) : '',
      reported_by: risk.reported_by || '',
    });
    setFormError('');
    setIsModalOpen(true);
  };

  const handlePresetSelect = (preset) => {
    setFormData((prev) => ({
      ...prev,
      location: prev.location || preset.name,
      latitude: String(preset.lat),
      longitude: String(preset.lng),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');

    if (!formData.title.trim()) {
      setFormError('Hazard event title is required.');
      return;
    }
    if (!formData.location.trim()) {
      setFormError('Location details are required.');
      return;
    }

    const payload = {
      title: formData.title.trim(),
      hazard_type: formData.hazard_type,
      severity: formData.severity,
      location: formData.location.trim(),
      latitude: formData.latitude ? parseFloat(formData.latitude) : null,
      longitude: formData.longitude ? parseFloat(formData.longitude) : null,
      description: formData.description.trim() || null,
      affected_population: formData.affected_population ? parseInt(formData.affected_population, 10) : null,
      reported_by: formData.reported_by.trim() || null,
    };

    try {
      if (editingRisk) {
        await onUpdateRisk(editingRisk.id, payload);
      } else {
        await onCreateRisk(payload);
      }
      setIsModalOpen(false);
    } catch (err) {
      setFormError(err.message || 'Failed to save climate risk event.');
    }
  };

  // Filter & Search Logic
  const filteredRisks = risks.filter((risk) => {
    const matchesSearch =
      risk.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      risk.location.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (risk.reported_by && risk.reported_by.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesHazard = selectedHazard === 'all' || risk.hazard_type === selectedHazard;
    const matchesSeverity = selectedSeverity === 'all' || risk.severity === selectedSeverity;

    return matchesSearch && matchesHazard && matchesSeverity;
  });

  const getHazardBadge = (type) => {
    switch (type) {
      case 'flood':
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold uppercase bg-sky-950 text-sky-300 border border-sky-800">🌊 Flood</span>;
      case 'cyclone':
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold uppercase bg-teal-950 text-teal-300 border border-teal-800">🌀 Cyclone</span>;
      case 'earthquake':
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold uppercase bg-orange-950 text-orange-300 border border-orange-800">🌋 Earthquake</span>;
      case 'heatwave':
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold uppercase bg-rose-950 text-rose-300 border border-rose-800">🔥 Heatwave</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[11px] font-bold uppercase bg-slate-800 text-slate-300">{type}</span>;
    }
  };

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'critical':
        return <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wide bg-rose-950 text-rose-300 border border-rose-800">Critical</span>;
      case 'high':
        return <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wide bg-orange-950 text-orange-300 border border-orange-800">High</span>;
      case 'medium':
        return <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wide bg-amber-950 text-amber-300 border border-amber-800">Medium</span>;
      default:
        return <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wide bg-emerald-950 text-emerald-300 border border-emerald-800">Low</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Module Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            <span>Climate Risk Events Registry</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Full lifecycle tracking of floods, cyclones, earthquakes and heatwaves
          </p>
        </div>

        <button
          onClick={openCreateModal}
          className="flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-cyan-900/30 transition-all active:scale-95"
        >
          <Plus className="w-4 h-4" />
          <span>Record New Event</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-md space-y-3">
        <div className="flex flex-col md:flex-row items-center gap-3">
          {/* Search Input */}
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search by title, location, or reporting authority..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition-colors"
            />
          </div>

          {/* Hazard Filter */}
          <div className="flex items-center gap-2 w-full md:w-auto">
            <select
              value={selectedHazard}
              onChange={(e) => setSelectedHazard(e.target.value)}
              className="w-full md:w-auto px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-cyan-500 capitalize"
            >
              <option value="all">All Hazard Types</option>
              <option value="flood">Flood</option>
              <option value="cyclone">Cyclone</option>
              <option value="earthquake">Earthquake</option>
              <option value="heatwave">Heatwave</option>
            </select>

            {/* Severity Filter */}
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="w-full md:w-auto px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-cyan-500 capitalize"
            >
              <option value="all">All Severities</option>
              <option value="critical">Critical</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>

            {/* View Mode Toggle */}
            <div className="hidden sm:flex border border-slate-800 bg-slate-950 rounded-xl p-0.5 shrink-0">
              <button
                onClick={() => setViewMode('grid')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  viewMode === 'grid' ? 'bg-slate-800 text-cyan-300' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Cards
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  viewMode === 'table' ? 'bg-slate-800 text-cyan-300' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                Table
              </button>
            </div>
          </div>
        </div>

        {/* Filter Summary */}
        <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
          <span>
            Showing <strong className="text-slate-200">{filteredRisks.length}</strong> of{' '}
            <strong className="text-slate-200">{risks.length}</strong> registered risk events
          </span>
          {(searchTerm || selectedHazard !== 'all' || selectedSeverity !== 'all') && (
            <button
              onClick={() => {
                setSearchTerm('');
                setSelectedHazard('all');
                setSelectedSeverity('all');
              }}
              className="text-cyan-400 hover:underline"
            >
              Clear Filters
            </button>
          )}
        </div>
      </div>

      {/* Grid View */}
      {viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredRisks.map((risk) => (
            <div
              key={risk.id}
              className="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition-all shadow-lg flex flex-col justify-between space-y-4 group"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  {getHazardBadge(risk.hazard_type)}
                  {getSeverityBadge(risk.severity)}
                </div>

                <h3 className="font-bold text-slate-100 text-sm group-hover:text-cyan-300 transition-colors line-clamp-2">
                  {risk.title}
                </h3>

                <p className="text-xs text-slate-400 mt-2 line-clamp-3 leading-relaxed">
                  {risk.description || 'No detailed situational synopsis recorded.'}
                </p>

                <div className="mt-4 pt-3 border-t border-slate-800/80 space-y-2 text-xs">
                  <div className="flex items-center gap-2 text-slate-300">
                    <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                    <span className="truncate">{risk.location}</span>
                  </div>

                  {risk.latitude && risk.longitude && (
                    <div className="flex items-center gap-2 font-mono text-[11px] text-slate-400">
                      <span className="text-slate-400">Coords:</span>
                      <span>{risk.latitude.toFixed(4)}°N, {risk.longitude.toFixed(4)}°E</span>
                    </div>
                  )}

                  <div className="flex items-center justify-between text-slate-400 text-[11px] pt-1">
                    <span className="flex items-center gap-1.5">
                      <Users className="w-3.5 h-3.5 text-cyan-400" />
                      <span>{risk.affected_population ? Number(risk.affected_population).toLocaleString() : 'N/A'} pop.</span>
                    </span>
                    <span className="truncate max-w-[120px]" title={risk.reported_by}>
                      {risk.reported_by || 'EOC Telemetry'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-3 border-t border-slate-800 flex items-center justify-between gap-2">
                <button
                  onClick={() => onBroadcastAlert(risk)}
                  className="flex-1 py-1.5 px-2 bg-rose-950/60 hover:bg-rose-900/70 border border-rose-800/80 text-rose-200 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
                  title="Broadcast alert linked to this risk event"
                >
                  <Bell className="w-3.5 h-3.5" />
                  <span>Alert</span>
                </button>

                <button
                  onClick={() => openEditModal(risk)}
                  className="p-2 text-slate-400 hover:text-cyan-300 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-lg transition-colors"
                  title="Edit event"
                >
                  <Edit2 className="w-3.5 h-3.5" />
                </button>

                <button
                  onClick={() => setDeleteConfirmId(risk.id)}
                  className="p-2 text-slate-400 hover:text-rose-400 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-lg transition-colors"
                  title="Delete event"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        /* Table View */
        <div className="rounded-2xl bg-slate-900/90 border border-slate-800 overflow-hidden shadow-lg">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/80 border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
                <tr>
                  <th className="py-3 px-4">Event Title</th>
                  <th className="py-3 px-4">Hazard Type</th>
                  <th className="py-3 px-4">Severity</th>
                  <th className="py-3 px-4">Location</th>
                  <th className="py-3 px-4">Affected Pop</th>
                  <th className="py-3 px-4">Reported By</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {filteredRisks.map((risk) => (
                  <tr key={risk.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3.5 px-4 font-semibold text-slate-100 max-w-xs">
                      {risk.title}
                    </td>
                    <td className="py-3.5 px-4">{getHazardBadge(risk.hazard_type)}</td>
                    <td className="py-3.5 px-4">{getSeverityBadge(risk.severity)}</td>
                    <td className="py-3.5 px-4 text-slate-300">{risk.location}</td>
                    <td className="py-3.5 px-4 font-mono font-medium">
                      {risk.affected_population ? Number(risk.affected_population).toLocaleString() : 'N/A'}
                    </td>
                    <td className="py-3.5 px-4 text-slate-400">{risk.reported_by || 'Telemetry'}</td>
                    <td className="py-3.5 px-4 text-right space-x-1 whitespace-nowrap">
                      <button
                        onClick={() => onBroadcastAlert(risk)}
                        className="p-1.5 text-rose-400 hover:bg-rose-950/50 rounded-md transition-colors"
                        title="Broadcast alert"
                      >
                        <Bell className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => openEditModal(risk)}
                        className="p-1.5 text-slate-400 hover:text-cyan-300 hover:bg-slate-800 rounded-md transition-colors"
                        title="Edit event"
                      >
                        <Edit2 className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => setDeleteConfirmId(risk.id)}
                        className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-md transition-colors"
                        title="Delete event"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Empty State */}
      {filteredRisks.length === 0 && (
        <div className="p-12 text-center rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
          <Activity className="w-10 h-10 text-slate-500 mx-auto" />
          <h4 className="text-base font-semibold text-slate-200">No Climate Risk Events Found</h4>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Try adjusting your search criteria or register a new hazard event using the button above.
          </p>
          <button
            onClick={openCreateModal}
            className="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-semibold inline-flex items-center gap-2 mt-2"
          >
            <Plus className="w-4 h-4" />
            <span>Record First Hazard Event</span>
          </button>
        </div>
      )}

      {/* Create / Edit Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <Activity className="w-5 h-5 text-cyan-400" />
                <span>{editingRisk ? 'Update Climate Risk Event' : 'Record New Climate Risk Event'}</span>
              </h3>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-200 p-1 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {formError && (
              <div className="p-3 bg-rose-950/80 border border-rose-800 rounded-xl text-rose-200 text-xs flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400" />
                <span>{formError}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              {/* Preset Coordinate Quick-Selector */}
              <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-[11px] text-slate-400 font-semibold">
                  <span className="flex items-center gap-1.5 text-cyan-400">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Quick Autofill Regional Coordinates:</span>
                  </span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {REGION_COORDINATE_PRESETS.map((preset) => (
                    <button
                      type="button"
                      key={preset.name}
                      onClick={() => handlePresetSelect(preset)}
                      className="px-2.5 py-1 bg-slate-900 hover:bg-slate-800 border border-slate-700/80 rounded-lg text-[11px] text-slate-300 transition-colors"
                    >
                      {preset.name}
                    </button>
                  ))}
                </div>
              </div>

              {/* Title */}
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Event Title *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Brahmaputra Basin Flash Flood Surge"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                />
              </div>

              {/* Hazard Type & Severity */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Hazard Classification *
                  </label>
                  <select
                    value={formData.hazard_type}
                    onChange={(e) => setFormData({ ...formData, hazard_type: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-cyan-500 capitalize"
                  >
                    <option value="flood">Flood (Hydrological)</option>
                    <option value="cyclone">Cyclone (Meteorological)</option>
                    <option value="earthquake">Earthquake (Geophysical)</option>
                    <option value="heatwave">Heatwave (Climatological)</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Severity Level *
                  </label>
                  <select
                    value={formData.severity}
                    onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-cyan-500 capitalize"
                  >
                    <option value="low">Low (Precautionary)</option>
                    <option value="medium">Medium (Advisory)</option>
                    <option value="high">High (Evacuation/Response)</option>
                    <option value="critical">Critical (Disaster/Emergency)</option>
                  </select>
                </div>
              </div>

              {/* Location */}
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Geographic Location / Region *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Assam, Barpeta & Dhubri Districts"
                  value={formData.location}
                  onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                />
              </div>

              {/* Latitude, Longitude, Affected Population */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Latitude (-90 to 90)
                  </label>
                  <input
                    type="number"
                    step="any"
                    min="-90"
                    max="90"
                    placeholder="26.2006"
                    value={formData.latitude}
                    onChange={(e) => setFormData({ ...formData, latitude: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Longitude (-180 to 180)
                  </label>
                  <input
                    type="number"
                    step="any"
                    min="-180"
                    max="180"
                    placeholder="92.9376"
                    value={formData.longitude}
                    onChange={(e) => setFormData({ ...formData, longitude: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Affected Population
                  </label>
                  <input
                    type="number"
                    min="0"
                    placeholder="e.g. 450000"
                    value={formData.affected_population}
                    onChange={(e) => setFormData({ ...formData, affected_population: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                  />
                </div>
              </div>

              {/* Description */}
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Situation Synopsis & Field Telemetry
                </label>
                <textarea
                  rows={3}
                  placeholder="Provide operational context, river gauge readings, wind metrics, or structural damage..."
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                />
              </div>

              {/* Reported By */}
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Reporting Authority / Agency
                </label>
                <input
                  type="text"
                  placeholder="e.g. Central Water Commission / IMD / State EOC"
                  value={formData.reported_by}
                  onChange={(e) => setFormData({ ...formData, reported_by: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
                />
              </div>

              {/* Modal Actions */}
              <div className="pt-3 border-t border-slate-800 flex items-center justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl transition-colors font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl font-bold shadow-lg shadow-cyan-900/30 transition-all"
                >
                  {editingRisk ? 'Save Changes' : 'Record Risk Event'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deleteConfirmId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-rose-950/80 border border-rose-800 flex items-center justify-center mx-auto text-rose-400">
              <Trash2 className="w-6 h-6" />
            </div>

            <div className="text-center space-y-1">
              <h3 className="text-base font-bold text-slate-100">Delete Climate Risk Event</h3>
              <p className="text-xs text-slate-400">
                Are you sure you want to permanently remove this event from the national registry? This action cannot be undone.
              </p>
            </div>

            <div className="flex items-center justify-center gap-3 pt-2">
              <button
                onClick={() => setDeleteConfirmId(null)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={async () => {
                  await onDeleteRisk(deleteConfirmId);
                  setDeleteConfirmId(null);
                }}
                className="px-5 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-xs font-bold transition-colors shadow-lg shadow-rose-900/30"
              >
                Confirm Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
