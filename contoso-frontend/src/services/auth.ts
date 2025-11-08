import { jwtDecode } from 'jwt-decode';

type DecodedToken = {
  sub: string;
  role?: 'employee' | 'employer' | string;
  exp?: number;
};

export function getToken(): string | null {
  return localStorage.getItem('access_token');
}

export function getDecodedToken(): DecodedToken | null {
  const token = getToken();
  if (!token) return null;

  try {
    const decoded: DecodedToken = jwtDecode(token);

    if (!decoded || typeof decoded !== 'object') {
      localStorage.removeItem('access_token');
      return null;
    }

    if (decoded.exp && typeof decoded.exp === 'number' && decoded.exp * 1000 < Date.now()) {
      localStorage.removeItem('access_token');
      return null;
    }

    return decoded;
  } catch (error) {
    console.error('Failed to decode token:', error);
    localStorage.removeItem('access_token');
    return null;
  }
}

export function logout() {
  localStorage.removeItem('access_token');
  window.location.href = '/';
}