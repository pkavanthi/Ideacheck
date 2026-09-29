const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const fetchIncidents = async () => {
  const res = await fetch(`${API_BASE}/incidents/`);
  if (!res.ok) throw new Error('Failed to fetch incidents');
  return res.json();
};

export const createIncident = async (data) => {
  const res = await fetch(`${API_BASE}/incidents/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create incident');
  return res.json();
};

export const updateIncident = async (id, data) => {
  const res = await fetch(`${API_BASE}/incidents/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to update incident');
  return res.json();
};

export const deleteIncident = async (id) => {
  const res = await fetch(`${API_BASE}/incidents/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete incident');
  return true;
};

export const fetchResources = async () => {
  const res = await fetch(`${API_BASE}/resources/`);
  if (!res.ok) throw new Error('Failed to fetch resources');
  return res.json();
};

export const createResource = async (data) => {
  const res = await fetch(`${API_BASE}/resources/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create resource');
  return res.json();
};

export const deleteResource = async (id) => {
  const res = await fetch(`${API_BASE}/resources/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete resource');
  return true;
};
