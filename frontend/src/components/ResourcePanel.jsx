import React, { useState } from 'react';

export default function ResourcePanel({ resources, onAddResource, onDeleteResource }) {
  const [formData, setFormData] = useState({
    name: '',
    resource_type: 'RESCUE_BOAT',
    district: 'Wayanad',
    quantity: 10,
    available_quantity: 10,
    location_hub: '',
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.name || !formData.location_hub) return;
    onAddResource(formData);
    setFormData({
      name: '',
      resource_type: 'RESCUE_BOAT',
      district: 'Wayanad',
      quantity: 10,
      available_quantity: 10,
      location_hub: '',
    });
  };

  return (
    <div className="bg-slate-800 p-5 rounded-lg border border-slate-700 space-y-4">
      <h3 className="text-lg font-bold text-white">Relief Resources & Staging Hubs</h3>

      <form onSubmit={handleSubmit} className="bg-slate-900 p-3 rounded border border-slate-700 space-y-2">
        <h4 className="text-xs font-semibold text-slate-300 uppercase">Deploy / Register New Resource</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
          <input
            required
            placeholder="Resource Name (e.g. Life Jackets)"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            className="bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-xs text-white"
          />
          <select
            value={formData.resource_type}
            onChange={(e) => setFormData({ ...formData, resource_type: e.target.value })}
            className="bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-xs text-white"
          >
            <option value="RESCUE_BOAT">Rescue Boats</option>
            <option value="MEDICAL_KIT">Medical Kits</option>
            <option value="FOOD_RATION">Food Rations</option>
            <option value="SHELTER_KIT">Shelter Kits</option>
            <option value="WATER_PUMP">High Capacity Pumps</option>
            <option value="PERSONNEL">Personnel / NDRF Unit</option>
          </select>
          <input
            required
            placeholder="Hub Location (e.g. Base Depot 1)"
            value={formData.location_hub}
            onChange={(e) => setFormData({ ...formData, location_hub: e.target.value })}
            className="bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-xs text-white"
          />
        </div>
        <div className="flex gap-2">
          <input
            type="number"
            placeholder="Total Qty"
            value={formData.quantity}
            onChange={(e) => setFormData({ ...formData, quantity: Number(e.target.value), available_quantity: Number(e.target.value) })}
            className="w-1/3 bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-xs text-white"
          />
          <select
            value={formData.district}
            onChange={(e) => setFormData({ ...formData, district: e.target.value })}
            className="w-1/3 bg-slate-800 border border-slate-700 rounded px-2 py-1.5 text-xs text-white"
          >
            <option value="Wayanad">Wayanad</option>
            <option value="Idukki">Idukki</option>
            <option value="Ernakulam">Ernakulam</option>
            <option value="Alappuzha">Alappuzha</option>
          </select>
          <button
            type="submit"
            className="w-1/3 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded px-2 py-1.5"
          >
            Add Resource
          </button>
        </div>
      </form>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-900 text-slate-400 uppercase font-semibold">
            <tr>
              <th className="p-2">Name</th>
              <th className="p-2">Type</th>
              <th className="p-2">District / Hub</th>
              <th className="p-2">Available / Total</th>
              <th className="p-2">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700">
            {resources.map((res) => (
              <tr key={res.id} className="hover:bg-slate-700/50">
                <td className="p-2 font-medium text-white">{res.name}</td>
                <td className="p-2">{res.resource_type}</td>
                <td className="p-2">{res.district} ({res.location_hub})</td>
                <td className="p-2 font-mono">{res.available_quantity} / {res.quantity}</td>
                <td className="p-2">
                  <button
                    onClick={() => onDeleteResource(res.id)}
                    className="text-red-400 hover:text-red-300"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
