import { Outlet, useLocation, useNavigate } from '@modern-js/runtime/router';
import Nav from '../components/Nav';
import { useEffect, useState } from 'react';
import { getDecodedToken, logout } from '../services/auth';
import './index.css';

export default function Layout() {
  const [user, setUser] = useState<{ email: string; role: string } | null>(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const decodedToken = getDecodedToken();
    if (decodedToken && decodedToken.role) {
      setUser({ email: decodedToken.sub, role: decodedToken.role });
    } else if (location.pathname !== '/') {
      navigate('/');
    }
  }, [location.pathname, navigate]);

  if (location.pathname === '/') {
    return <Outlet />;
  }

  return (
    <div>
      <Nav user={user} onLogout={logout} />
      <main className="page-container">
        <Outlet />
      </main>
    </div>
  );
}