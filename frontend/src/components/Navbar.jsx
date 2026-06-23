import { BarChart3, BookOpen, LayoutDashboard, Library, LogOut, Quote, Settings } from "lucide-react";
import { NavLink } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <NavLink to="/dashboard" className="brand" title="Book Tracker dashboard">
          <BookOpen size={24} />
          <span>Book Tracker</span>
        </NavLink>

        <nav className="nav-links" aria-label="Primary navigation">
          <NavLink to="/dashboard">
            <LayoutDashboard size={18} />
            <span>Dashboard</span>
          </NavLink>
          <NavLink to="/books">
            <Library size={18} />
            <span>Books</span>
          </NavLink>
          <NavLink to="/quotes">
            <Quote size={18} />
            <span>Quotes</span>
          </NavLink>
          <NavLink to="/analytics">
            <BarChart3 size={18} />
            <span>Analytics</span>
          </NavLink>
          <NavLink to="/settings">
            <Settings size={18} />
            <span>Settings</span>
          </NavLink>
        </nav>

        <div className="nav-user">
          <span>{user?.name}</span>
          <button className="icon-button" type="button" onClick={logout} title="Log out">
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </header>
  );
}
