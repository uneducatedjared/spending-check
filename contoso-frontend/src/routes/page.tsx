import { useState, useEffect } from 'react';
import client from '../api/client';
import { useNavigate } from '@modern-js/runtime/router';
import './index.css';
import { getDecodedToken } from '../services/auth';

// Hash password using Web Crypto API (SHA-256), return hex string
async function hashPasswordHex(password: string) {
  const enc = new TextEncoder();
  const data = enc.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

export default function AuthPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [role, setRole] = useState('employee');
  const [isAwaitingNewUserDetails, setIsAwaitingNewUserDetails] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const decodedToken = getDecodedToken();
    if (decodedToken && decodedToken.role) {
      navigate('/tickets');
    }
  }, [navigate]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      if (!isAwaitingNewUserDetails) {
        const payload = { email, password };
        try {
          const response = await client.auth.registerOrLogin(payload);
          const token = response?.data?.access_token;
          if (token) {
            localStorage.setItem('access_token', token);
            navigate('/tickets');
            return;
          }
          setError(response?.detail || 'Login failed. No token returned.');
        } catch (err: any) {
          const msg = err?.message || String(err);
          // If backend signals that user not found, reveal additional fields
          if (/not found|no user|user does not exist/i.test(msg)) {
            setIsAwaitingNewUserDetails(true);
            setError(null);
            return;
          }
          setError(msg);
        }
      } else {
        // New user flow: hash password, then create user and login
        const hashed = await hashPasswordHex(password);
        const payload = { email, password: hashed, username, role };
        const response = await client.auth.registerOrLogin(payload);
        const token = response?.data?.access_token;
        if (token) {
          localStorage.setItem('access_token', token);
          navigate('/tickets');
          return;
        }
        setError(response?.detail || 'Registration failed. No token returned.');
      }
    } catch (err: any) {
      setError(err?.message || String(err));
    }
  }

  return (
    <div className="container-box">
      <main className="auth-container">
        <h2>Login / Register</h2>
        <form onSubmit={submit} className="auth-form">
          <label>
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
          </label>
          <label>
            Password
            <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
          </label>

          {isAwaitingNewUserDetails && (
            <>
              <p>Please provide username and role to create a new account for <strong>{email}</strong>.</p>
              <label>
                Username
                <input value={username} onChange={(e) => setUsername(e.target.value)} required />
              </label>
              <label>
                Role
                <select value={role} onChange={(e) => setRole(e.target.value)}>
                  <option value="employee">Employee</option>
                  <option value="employer">Employer</option>
                </select>
              </label>
            </>
          )}

          <div>
            <button type="submit">Login / Register</button>
          </div>
          {error && <div className="error">{error}</div>}
        </form>
      </main>
    </div>
  );
}