import React, { useState } from 'react';

export default function IncidentForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    title: '',
    district: 'Wayanad',
    location_name: '',
    latitude: 11.5534,
    longitude: 76.0407,
    threat_level: 'CRITICAL',
    status: 'ACTIVE',
    affected_population: 100,
    description: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'latitude' || name === 'longitude' || name === 'affected_population' 
        ? Number(value) 
        : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({
      title: '',
      district: 'Wayanad',
      location_name: '',
      latitude: 11.5534,
      longitude: 76.0407,
      threat_level: 'CRITICAL',
      status: 'ACTIVE',
      affected_population: 100,
      description: '',
    });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-slate-800 p-5 rounded-lg border border-slate-700 space-y-4">
      <h3 className="text-lg font-bold text-white flex items-center gap-2">
        <span className="w-2.5 h-2.5 bg-red-500 rounded-full animate-pulse"></span>
        Report New Incident (24-48h Imminent Threat)
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Incident Title</label>
          <input
            required
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="e.g., Aluva Periyar River Spillage"
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">District</label>
          <select
            name="district"
            value={formData.district}
            onChange={handleChange}
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
          >
            <option value="Wayanad">Wayanad</option>
            <option value="Idukki">Idukki</option>
            <option value="Ernakulam">Ernakulam</option>
            <option value="Alappuzha">Alappuzha</option>
            <option value="Pathanamthitta">Pathanamthitta</option>
            <option value="Thrissur">Thrissur</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Specific Location</label>
          <input
            required
            name="location_name"
            value={formData.location_name}
            onChange={handleChange}
            placeholder="e.g., Mananthavady Bridge"
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Threat Level</label>
          <select
            name="threat_level"
            value={formData.threat_level}
            onChange={handleChange}
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
          >
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MODERATE">MODERATE</option>
            <option value="LOW">LOW</option>
          </select>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Est. Affected Population</label>
          <input
            type="number"
            name="affected_population"
            value={formData.affected_population}
            onChange={handleChange}
            className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
          />
        </div>

        <div className="grid grid-cols-2 gap-2">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Latitude</label>
            <input
              type="number"
              step="0.0001"
              name="latitude"
              value={formData.latitude}
              onChange={handleChange}
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Longitude</label>
            <input
              type="number"
              step="0.0001"
              name="longitude"
              value={formData.longitude}
              onChange={handleChange}
              className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>
      </div>

      <div>
        <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Emergency Description</label>
        <textarea
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows="2"
          placeholder="Details on rising water levels, dam discharge, evacuated families..."
          className="w-full bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
        />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 px-4 rounded transition-colors duration-150"
      >
        Submit Emergency Incident
      </button>
    </form>
  );
}
