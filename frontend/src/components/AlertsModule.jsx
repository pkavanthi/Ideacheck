import React, { useState } from 'react';
import {
  Bell,
  Plus,
  Search,
  Filter,
  Radio,
  CheckCircle2,
  Clock,
  AlertTriangle,
  X,
  Edit2,
  Trash2,
  Share2,
  ShieldCheck,
  Send,
  Link as LinkIcon
} from 'lucide-react';

export function AlertsModule({
  alerts = [],
  risks = [],
  onCreateAlert,
  onUpdateAlert,
  onDeleteAlert,
  loading
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedHazard, setSelectedHazard] = useState('all');
  const [activeFilter, setActiveFilter] = useState('all'); // 'all', 'active', 'resolved'

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingAlert, setEditingAlert] = useState(null);
  const [deleteConfirmId, setDeleteConfirmId] = useState(null);

  // Form State
  const [formData, setFormData] = useState({
    event_id: '',
    hazard_type: 'flood',
    severity: 'critical',
    region: '',
    message: '',
    issued_by: '',
    active: 1,
    expires_at: '',
  });

  const [formError, setFormError] = useState('');

  const openCreateModal = (linkedRisk = null) => {
    setEditingAlert(null);
    const defaultExpiry = new Date(Date.now() + 24 * 3600000).toISOString().slice(0, 16);

    setFormData({
      event_id: linkedRisk ? String(linkedRisk.id) : '',
      hazard_type: linkedRisk ? linkedRisk.hazard_type : 'flood',
      severity: linkedRisk ? linkedRisk.severity : 'critical',
      region: linkedRisk ? linkedRisk.location : '',
      message: linkedRisk
        ? `EMERGENCY ALERT: Elevated ${linkedRisk.hazard_type} warning active for ${linkedRisk.location}. Immediate precautionary safety protocols in effect.`
        : '',
      issued_by: 'National Emergency Operations Centre (NEOC)',
      active: 1,
      expires_at: defaultExpiry,
    });
    setFormError('');
    setIsModalOpen(true);
  };

  const openEditModal = (alert) => {
    setEditingAlert(alert);
    setFormData({
      event_id: alert.event_id ? String(alert.event_id) : '',
      hazard_type: alert.hazard_type || 'flood',
      severity: alert.severity || 'critical',
      region: alert.region || '',
      message: alert.message || '',
      issued_by: alert.issued_by || '',
      active: alert.active !== undefined ? alert.active : 1,
      expires_at: alert.expires_at ? new Date(alert.expires_at).toISOString().slice(0, 16) : '',
    });
    setFormError('');
    setIsModalOpen(true);
  };

  const handleToggleActive = async (alert) => {
    const newStatus = alert.active === 1 ? 0 : 1;
    try {
      await onUpdateAlert(alert.id, { active: newStatus });
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError('');

    if (!formData.region.trim()) {
      setFormError('Target region is required.');
      return;
    }
    if (!formData.message.trim() || formData.message.trim().length < 5) {
      setFormError('Alert broadcast message must be at least 5 characters long.');
      return;
    }

    const payload = {
      event_id: formData.event_id ? parseInt(formData.event_id, 10) : null,
      hazard_type: formData.hazard_type,
      severity: formData.severity,
      region: formData.region.trim(),
      message: formData.message.trim(),
      issued_by: formData.issued_by.trim() || null,
      active: Number(formData.active),
      expires_at: formData.expires_at ? new Date(formData.expires_at).toISOString() : null,
    };

    try {
      if (editingAlert) {
        await onUpdateAlert(editingAlert.id, payload);
      } else {
        await onCreateAlert(payload);
      }
      setIsModalOpen(false);
    } catch (err) {
      setFormError(err.message || 'Failed to dispatch alert.');
    }
  };

  // Filter Logic
  const filteredAlerts = alerts.filter((alert) => {
    const matchesSearch =
      alert.region.toLowerCase().includes(searchTerm.toLowerCase()) ||
      alert.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (alert.issued_by && alert.issued_by.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesHazard = selectedHazard === 'all' || alert.hazard_type === selectedHazard;

    let matchesActive = true;
    if (activeFilter === 'active') matchesActive = alert.active === 1;
    if (activeFilter === 'resolved') matchesActive = alert.active === 0;

    return matchesSearch && matchesHazard && matchesActive;
  });

  const getSeverityBadge = (severity) => {
    switch (severity) {
      case 'critical':
        return <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase bg-rose-950 text-rose-300 border border-rose-800">Critical Red</span>;
      case 'high':
        return <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase bg-orange-950 text-orange-300 border border-orange-800">Orange Alert</span>;
      case 'medium':
        return <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase bg-amber-950 text-amber-300 border border-amber-800">Yellow Advisory</span>;
      default:
        return <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase bg-emerald-950 text-emerald-300 border border-emerald-800">Low</span>;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <Bell className="w-5 h-5 text-rose-400" />
            <span>Emergency Risk Alerts Operations</span>
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Active sirens, early warning bulletins and emergency SOP resolutions
          </p>
        </div>

        <button
          onClick={() => openCreateModal()}
          className="flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-rose-900/30 transition-all active:scale-95"
        >
          <Send className="w-4 h-4" />
          <span>Broadcast New Alert</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-md space-y-3">
        <div className="flex flex-col md:flex-row items-center gap-3">
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search by target region, broadcast message, or agency..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-rose-500 transition-colors"
            />
          </div>

          <div className="flex items-center gap-2 w-full md:w-auto">
            <select
              value={selectedHazard}
              onChange={(e) => setSelectedHazard(e.target.value)}
              className="w-full md:w-auto px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-rose-500 capitalize"
            >
              <option value="all">All Hazard Types</option>
              <option value="flood">Flood</option>
              <option value="cyclone">Cyclone</option>
              <option value="earthquake">Earthquake</option>
              <option value="heatwave">Heatwave</option>
            </select>

            <select
              value={activeFilter}
              onChange={(e) => setActiveFilter(e.target.value)}
              className="w-full md:w-auto px-3 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-rose-500"
            >
              <option value="all">All Statuses</option>
              <option value="active">Active Only (Broadcasting)</option>
              <option value="resolved">Resolved / Stand-down</option>
            </select>
          </div>
        </div>

        <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
          <span>
            Displaying <strong className="text-slate-200">{filteredAlerts.length}</strong> of{' '}
            <strong className="text-slate-200">{alerts.length}</strong> alerts
          </span>
          {(searchTerm || selectedHazard !== 'all' || activeFilter !== 'all') && (
            <button
              onClick={() => {
                setSearchTerm('');
                setSelectedHazard('all');
                setActiveFilter('all');
              }}
              className="text-cyan-400 hover:underline"
            >
              Reset Filters
            </button>
          )}
        </div>
      </div>

      {/* Alert Feed List */}
      <div className="space-y-4">
        {filteredAlerts.map((alert) => {
          const isActive = alert.active === 1;

          return (
            <div
              key={alert.id}
              className={`p-5 rounded-2xl border transition-all shadow-lg ${
                isActive
                  ? 'bg-gradient-to-r from-slate-900 via-slate-900/95 to-rose-950/20 border-rose-900/70 hover:border-rose-700'
                  : 'bg-slate-900/70 border-slate-800/80 opacity-80'
              }`}
            >
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                <div className="space-y-2.5 flex-1">
                  {/* Status, Hazard & Severity Bar */}
                  <div className="flex items-center gap-2 flex-wrap">
                    {isActive ? (
                      <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-bold bg-rose-600 text-white animate-pulse">
                        <Radio className="w-3 h-3" />
                        <span>ACTIVE SIREN</span>
                      </span>
                    ) : (
                      <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-medium bg-emerald-950 text-emerald-300 border border-emerald-800">
                        <ShieldCheck className="w-3 h-3" />
                        <span>RESOLVED / STAND-DOWN</span>
                      </span>
                    )}

                    <span className="px-2 py-0.5 rounded text-[11px] font-bold uppercase bg-slate-800 text-cyan-300 border border-slate-700">
                      {alert.hazard_type}
                    </span>

                    {getSeverityBadge(alert.severity)}

                    {alert.event_id && (
                      <span className="flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-950 text-indigo-300 border border-indigo-800">
                        <LinkIcon className="w-3 h-3" />
                        <span>Linked Risk #{alert.event_id}</span>
                      </span>
                    )}
                  </div>

                  {/* Target Region */}
                  <div className="text-sm font-bold text-slate-100 flex items-center gap-2">
                    <span>Target Region:</span>
                    <span className="text-cyan-300">{alert.region}</span>
                  </div>

                  {/* Message Content */}
                  <div className="p-3 rounded-xl bg-slate-950 border border-slate-800/80 text-xs text-slate-200 font-mono leading-relaxed">
                    {alert.message}
                  </div>

                  {/* Metadata */}
                  <div className="flex items-center gap-4 text-[11px] text-slate-400 flex-wrap">
                    <span>
                      Issued by: <strong className="text-slate-300">{alert.issued_by || 'Authority'}</strong>
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3 h-3 text-slate-400" />
                      <span>Issued: {new Date(alert.issued_at).toLocaleString()}</span>
                    </span>
                    {alert.expires_at && (
                      <>
                        <span>•</span>
                        <span className="text-amber-400">
                          Expires: {new Date(alert.expires_at).toLocaleString()}
                        </span>
                      </>
                    )}
                  </div>
                </div>

                {/* Quick Action Controls */}
                <div className="flex md:flex-col items-center gap-2 shrink-0 self-end md:self-start">
                  <button
                    onClick={() => handleToggleActive(alert)}
                    className={`w-full py-2 px-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-1.5 ${
                      isActive
                        ? 'bg-emerald-950/80 hover:bg-emerald-900 border border-emerald-700 text-emerald-200'
                        : 'bg-rose-950/80 hover:bg-rose-900 border border-rose-700 text-rose-200'
                    }`}
                  >
                    {isActive ? (
                      <>
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Mark Resolved</span>
                      </>
                    ) : (
                      <>
                        <Radio className="w-3.5 h-3.5" />
                        <span>Reactivate Siren</span>
                      </>
                    )}
                  </button>

                  <div className="flex items-center gap-1 w-full justify-end">
                    <button
                      onClick={() => openEditModal(alert)}
                      className="p-2 text-slate-400 hover:text-cyan-300 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-lg transition-colors flex-1 flex items-center justify-center"
                      title="Edit alert"
                    >
                      <Edit2 className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => setDeleteConfirmId(alert.id)}
                      className="p-2 text-slate-400 hover:text-rose-400 bg-slate-950 hover:bg-slate-800 border border-slate-800 rounded-lg transition-colors flex-1 flex items-center justify-center"
                      title="Delete alert"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Empty State */}
      {filteredAlerts.length === 0 && (
        <div className="p-12 text-center rounded-2xl bg-slate-900/60 border border-slate-800 space-y-3">
          <Bell className="w-10 h-10 text-slate-500 mx-auto" />
          <h4 className="text-base font-semibold text-slate-200">No Emergency Alerts Found</h4>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            All regional sectors are currently reporting normal baseline status or filters are restricting results.
          </p>
          <button
            onClick={() => openCreateModal()}
            className="px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-xl text-xs font-semibold inline-flex items-center gap-2 mt-2"
          >
            <Send className="w-4 h-4" />
            <span>Broadcast Emergency Bulletin</span>
          </button>
        </div>
      )}

      {/* Broadcast Alert Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                <Bell className="w-5 h-5 text-rose-400" />
                <span>{editingAlert ? 'Edit Emergency Alert' : 'Broadcast Emergency Risk Alert'}</span>
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
              {/* Linked Climate Risk Event Selector */}
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Link to Recorded Risk Event (Optional)
                </label>
                <select
                  value={formData.event_id}
                  onChange={(e) => {
                    const eventId = e.target.value;
                    const linked = risks.find((r) => String(r.id) === eventId);
                    setFormData((prev) => ({
                      ...prev,
                      event_id: eventId,
                      hazard_type: linked ? linked.hazard_type : prev.hazard_type,
                      severity: linked ? linked.severity : prev.severity,
                      region: linked ? linked.location : prev.region,
                    }));
                  }}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-rose-500"
                >
                  <option value="">-- Standalone Alert (No specific event link) --</option>
                  {risks.map((r) => (
                    <option key={r.id} value={r.id}>
                      #{r.id} [{r.hazard_type.toUpperCase()}] {r.title} ({r.location})
                    </option>
                  ))}
                </select>
              </div>

              {/* Hazard Classification & Severity */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Hazard Classification *
                  </label>
                  <select
                    value={formData.hazard_type}
                    onChange={(e) => setFormData({ ...formData, hazard_type: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-rose-500 capitalize"
                  >
                    <option value="flood">Flood</option>
                    <option value="cyclone">Cyclone</option>
                    <option value="earthquake">Earthquake</option>
                    <option value="heatwave">Heatwave</option>
                  </select>
                </div>

                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Alert Level / Severity *
                  </label>
                  <select
                    value={formData.severity}
                    onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-rose-500 capitalize"
                  >
                    <option value="critical">Critical (Red Siren / Mandatory Action)</option>
                    <option value="high">High (Orange Alert / Preparedness)</option>
                    <option value="medium">Medium (Yellow Advisory)</option>
                    <option value="low">Low (General Information)</option>
                  </select>
                </div>
              </div>

              {/* Region */}
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Target Region / Sector *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Odisha Coast (Balasore, Bhadrak & Kendrapara)"
                  value={formData.region}
                  onChange={(e) => setFormData({ ...formData, region: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500"
                />
              </div>

              {/* Message */}
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Broadcast Directive Message *
                </label>
                <textarea
                  rows={4}
                  required
                  placeholder="Provide precise emergency instructions (e.g., evacuation routes, shelter locations, hotline contacts)..."
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500 font-mono text-xs"
                />
              </div>

              {/* Issued By & Expiry */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Issuing Authority
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. National Disaster Management Authority"
                    value={formData.issued_by}
                    onChange={(e) => setFormData({ ...formData, issued_by: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-rose-500"
                  />
                </div>

                <div>
                  <label className="block font-semibold text-slate-300 mb-1">
                    Expiration Timestamp
                  </label>
                  <input
                    type="datetime-local"
                    value={formData.expires_at}
                    onChange={(e) => setFormData({ ...formData, expires_at: e.target.value })}
                    className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-100 focus:outline-none focus:border-rose-500"
                  />
                </div>
              </div>

              {/* Status Selector */}
              <div>
                <label className="block font-semibold text-slate-300 mb-1">
                  Operational Broadcast Status
                </label>
                <div className="flex gap-4">
                  <label className="flex items-center gap-2 text-slate-200 cursor-pointer">
                    <input
                      type="radio"
                      name="active"
                      value="1"
                      checked={Number(formData.active) === 1}
                      onChange={() => setFormData({ ...formData, active: 1 })}
                      className="accent-rose-500"
                    />
                    <span>Active Broadcast (Live siren)</span>
                  </label>
                  <label className="flex items-center gap-2 text-slate-200 cursor-pointer">
                    <input
                      type="radio"
                      name="active"
                      value="0"
                      checked={Number(formData.active) === 0}
                      onChange={() => setFormData({ ...formData, active: 0 })}
                      className="accent-emerald-500"
                    />
                    <span>Resolved / Archived</span>
                  </label>
                </div>
              </div>

              {/* Modal Buttons */}
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
                  className="px-5 py-2 bg-gradient-to-r from-rose-600 to-red-600 hover:from-rose-500 hover:to-red-500 text-white rounded-xl font-bold shadow-lg shadow-rose-900/30 transition-all"
                >
                  {editingAlert ? 'Update Alert' : 'Dispatch Live Broadcast'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Delete Confirmation */}
      {deleteConfirmId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-rose-950/80 border border-rose-800 flex items-center justify-center mx-auto text-rose-400">
              <Trash2 className="w-6 h-6" />
            </div>

            <div className="text-center space-y-1">
              <h3 className="text-base font-bold text-slate-100">Delete Emergency Alert</h3>
              <p className="text-xs text-slate-400">
                Are you sure you want to permanently delete this alert broadcast record?
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
                  await onDeleteAlert(deleteConfirmId);
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
