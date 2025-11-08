const BASE_URL = process.env.MODERN_API_BASE_URL || 'http://localhost:8000';

function getToken() {
  return localStorage.getItem('access_token');
}

async function apiRequest(path: string, options: RequestInit = {}) {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  const token = getToken();
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(BASE_URL + path, { ...options, headers });
  const text = await res.text();
  let data: any = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }
  if (!res.ok) {
    const err = data?.detail || data || res.statusText;
    throw new Error(err);
  }
  return data;
}

export const auth = {
  async registerOrLogin(payload: { email: string; password: string; username?: string; role?: string }) {
    // This function should return the whole unified response object, not just the data part.
    const data = await apiRequest('/auth/registerorlogin', { method: 'POST', body: JSON.stringify(payload) });
    return data;
  },
};

export const tickets = {
  async list() {
    return await apiRequest('/tickets', { method: 'GET' });
  },
  async create(payload: any) {
    return await apiRequest('/tickets/create', { method: 'POST', body: JSON.stringify(payload) });
  },
  async updateStatus(ticketId: number, status: string) {
    return await apiRequest(`/tickets/${ticketId}`, { method: 'PUT', body: JSON.stringify({ status }) });
  }
};

export const employees = {
  async list() {
    return await apiRequest('/employees/');
  },
  async updateStatus(employeeId: number, is_suspended: boolean) {
    return await apiRequest(`/employees/${employeeId}/status`, { method: 'PATCH', body: JSON.stringify({ is_suspended }) });
  }
};

export default { auth, tickets, employees };
