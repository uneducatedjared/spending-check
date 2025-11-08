import { Link, useLocation } from '@modern-js/runtime/router';

interface NavProps {
  user: { email: string; role: string } | null;
  onLogout: () => void;
}

export default function Nav({ user, onLogout }: NavProps) {
  const location = useLocation();

  const getLinkClass = (path: string) => {
    // This function checks if the current path matches the link's path
    // and returns the appropriate classes for active/inactive states.
    return location.pathname === path ? 'nav-link nav-link-active' : 'nav-link';
  };

  return (
    <header className="app-header">
      <div className="nav-container">
        <Link to="/tickets" className="logo">
          Contoso
        </Link>
        <nav className="nav-links">
          {user && (
            <Link to="/tickets" className={getLinkClass('/tickets')}>
              Tickets
            </Link>
          )}
          {user?.role === 'employer' && (
            <Link to="/employees" className={getLinkClass('/employees')}>
              Employees
            </Link>
          )}
        </nav>
        <div className="user-info">
          {user ? (
            <>
              <span>
                {user.email} (<strong>{user.role}</strong>)
              </span>
              <button onClick={onLogout} className="logout-btn">
                Logout
              </button>
            </>
          ) : (
            <Link to="/" className="nav-link">
              Login
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}