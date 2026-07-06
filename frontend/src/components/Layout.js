import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const Layout = () => {
  const { user, signOut } = useAuth();
  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <h1>Leave Management</h1>
          <p>Track leave balances, request approvals, and manage type-specific policies.</p>
        </div>
        <nav>
          <Link to="/">Dashboard</Link>
          <Link to="/request">Request Leave</Link>
          {user?.role === "admin" && <Link to="/leave-types">Leave Types</Link>}
          {(user?.role === "manager" || user?.role === "admin") && (
            <Link to="/pending">Pending Approvals</Link>
          )}
        </nav>
        {user ? (
          <div className="profile">
            <span>{user.email}</span>
            <button type="button" onClick={signOut}>
              Sign out
            </button>
          </div>
        ) : null}
      </header>
      <main className="app-content">
        <Outlet />
      </main>
      <footer className="app-footer">Leave management system · Built with React + FastAPI</footer>
    </div>
  );
};

export default Layout;
