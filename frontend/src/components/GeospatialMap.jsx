import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import L from 'leaflet';
import { Waves, Wind, Activity, Flame, ExternalLink, Bell, AlertOctagon } from 'lucide-react';

// Fix Leaflet's default marker icon issue in Vite bundling
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom SVG Icons for each Hazard Type
const getHazardIcon = (type, severity) => {
  let color = '#0284c7'; // flood
  if (type === 'cyclone') color = '#0d9488';
  if (type === 'earthquake') color = '#ea580c';
  if (type === 'heatwave') color = '#e11d48';

  const isCritical = severity === 'critical';
  const pulseClass = isCritical ? 'animation: pulse 1.2s infinite;' : '';

  const svgHtml = `
    <div style="
      position: relative;
      width: 36px;
      height: 36px;
      background: ${color};
      border: 2px solid #ffffff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 15px ${color};
      ${pulseClass}
    ">
      <span style="color: white; font-size: 14px; font-weight: bold;">
        ${type === 'flood' ? '🌊' : type === 'cyclone' ? '🌀' : type === 'earthquake' ? '🌋' : '🔥'}
      </span>
    </div>
  `;

  return L.divIcon({
    html: svgHtml,
    className: 'custom-hazard-marker',
    iconSize: [36, 36],
    iconAnchor: [18, 18],
    popupAnchor: [0, -20],
  });
};

function ChangeMapView({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center && center[0] && center[1]) {
      map.setView(center, zoom || map.getZoom());
    }
  }, [center, zoom, map]);
  return null;
}

export function GeospatialMap({
  risks = [],
  alerts = [],
  onSelectRisk,
  onBroadcastAlert,
  center = [22.5937, 78.9629], // Center of India / subcontinent
  zoom = 5
}) {
  const [selectedHazardFilter, setSelectedHazardFilter] = useState('all');

  const filteredRisks = risks.filter((r) => {
    if (!r.latitude || !r.longitude) return false;
    if (selectedHazardFilter === 'all') return true;
    return r.hazard_type === selectedHazardFilter;
  });

  const getCircleColor = (severity) => {
    switch (severity) {
      case 'critical': return '#ef4444';
      case 'high': return '#f97316';
      case 'medium': return '#f59e0b';
      default: return '#10b981';
    }
  };

  return (
    <div className="relative w-full h-[520px] rounded-2xl overflow-hidden border border-slate-800 bg-slate-900 shadow-xl">
      {/* Map Control Bar Overlay */}
      <div className="absolute top-3 left-3 z-[1000] bg-slate-900/90 backdrop-blur-md p-2 rounded-xl border border-slate-700 shadow-xl flex items-center gap-2 text-xs">
        <span className="font-semibold text-slate-300 px-2">Hazard Filter:</span>
        {['all', 'flood', 'cyclone', 'earthquake', 'heatwave'].map((type) => (
          <button
            key={type}
            onClick={() => setSelectedHazardFilter(type)}
            className={`px-2.5 py-1 rounded-lg capitalize font-medium transition-all ${
              selectedHazardFilter === type
                ? 'bg-cyan-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
            }`}
          >
            {type}
          </button>
        ))}
      </div>

      {/* Map Legend Overlay */}
      <div className="absolute bottom-3 right-3 z-[1000] bg-slate-900/90 backdrop-blur-md p-3 rounded-xl border border-slate-700 shadow-xl text-xs space-y-1.5 hidden sm:block">
        <div className="font-semibold text-slate-300 text-[11px] mb-1">Geospatial Alert Severity</div>
        <div className="flex items-center gap-2 text-slate-300">
          <span className="w-3 h-3 rounded-full bg-red-500 inline-block"></span>
          <span>Critical Risk Zone (Evacuation Mandatory)</span>
        </div>
        <div className="flex items-center gap-2 text-slate-300">
          <span className="w-3 h-3 rounded-full bg-orange-500 inline-block"></span>
          <span>High Risk (SDRF / Pre-alert)</span>
        </div>
        <div className="flex items-center gap-2 text-slate-300">
          <span className="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>
          <span>Medium Risk (Advisory)</span>
        </div>
      </div>

      <MapContainer
        center={center}
        zoom={zoom}
        scrollWheelZoom={true}
        className="w-full h-full"
      >
        <ChangeMapView center={center} zoom={zoom} />
        {/* CartoDB Dark Matter tiles for operational dark theme */}
        <TileLayer
          attribution='&copy; <a href="https://carto.com/">CARTO</a> | &copy; OpenStreetMap contributors'
          url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        />

        {filteredRisks.map((risk) => {
          const lat = parseFloat(risk.latitude);
          const lng = parseFloat(risk.longitude);
          if (isNaN(lat) || isNaN(lng)) return null;

          const radius = risk.severity === 'critical' ? 75000 : risk.severity === 'high' ? 50000 : 30000;
          const circleColor = getCircleColor(risk.severity);

          // Find if there are active alerts linked to this event
          const activeAlerts = alerts.filter((a) => a.event_id === risk.id && a.active === 1);

          return (
            <React.Fragment key={`risk-${risk.id}`}>
              {/* Radius Circle */}
              <Circle
                center={[lat, lng]}
                radius={radius}
                pathOptions={{
                  color: circleColor,
                  fillColor: circleColor,
                  fillOpacity: risk.severity === 'critical' ? 0.25 : 0.15,
                  weight: 2,
                  dashArray: risk.severity === 'critical' ? '4, 4' : undefined,
                }}
              />

              {/* Marker with Custom Icon */}
              <Marker
                position={[lat, lng]}
                icon={getHazardIcon(risk.hazard_type, risk.severity)}
              >
                <Popup>
                  <div className="space-y-2 max-w-xs">
                    <div className="flex items-center justify-between gap-2">
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-cyan-300 border border-slate-700">
                        {risk.hazard_type}
                      </span>
                      <span
                        className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                          risk.severity === 'critical'
                            ? 'bg-rose-950 text-rose-300 border border-rose-800'
                            : risk.severity === 'high'
                            ? 'bg-orange-950 text-orange-300 border border-orange-800'
                            : 'bg-amber-950 text-amber-300 border border-amber-800'
                        }`}
                      >
                        {risk.severity}
                      </span>
                    </div>

                    <h4 className="font-bold text-slate-100 text-sm leading-tight">
                      {risk.title}
                    </h4>

                    <p className="text-xs text-slate-300 leading-snug">
                      {risk.description || risk.location}
                    </p>

                    <div className="pt-1 border-t border-slate-700/60 grid grid-cols-2 gap-2 text-[11px] text-slate-400">
                      <div>
                        <span className="block text-slate-400">Location:</span>
                        <span className="font-medium text-slate-200">{risk.location}</span>
                      </div>
                      <div>
                        <span className="block text-slate-400">Affected Pop:</span>
                        <span className="font-semibold text-slate-200">
                          {risk.affected_population ? Number(risk.affected_population).toLocaleString() : 'N/A'}
                        </span>
                      </div>
                    </div>

                    {activeAlerts.length > 0 && (
                      <div className="p-2 bg-rose-950/70 border border-rose-800/80 rounded-lg text-rose-200 text-xs">
                        <div className="flex items-center gap-1 font-semibold text-rose-300">
                          <AlertOctagon className="w-3.5 h-3.5" />
                          <span>Active Warning In Effect</span>
                        </div>
                        <p className="text-[11px] mt-0.5 line-clamp-2">{activeAlerts[0].message}</p>
                      </div>
                    )}

                    <div className="pt-2 flex items-center gap-2">
                      {onSelectRisk && (
                        <button
                          onClick={() => onSelectRisk(risk)}
                          className="flex-1 py-1.5 px-2 bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white rounded text-xs font-medium text-center transition-colors"
                        >
                          View Details
                        </button>
                      )}
                      {onBroadcastAlert && (
                        <button
                          onClick={() => onBroadcastAlert(risk)}
                          className="flex-1 py-1.5 px-2 bg-rose-600 hover:bg-rose-500 text-white rounded text-xs font-semibold text-center transition-colors flex items-center justify-center gap-1"
                        >
                          <Bell className="w-3 h-3" />
                          Alert
                        </button>
                      )}
                    </div>
                  </div>
                </Popup>
              </Marker>
            </React.Fragment>
          );
        })}
      </MapContainer>
    </div>
  );
}
