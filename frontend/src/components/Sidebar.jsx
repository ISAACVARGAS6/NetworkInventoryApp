import { NavLink } from "react-router-dom";
import ThemeToggle from "./ThemeToggle";

// SVG Icons ligeros en línea
const LayoutDashboardIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect width="7" height="9" x="3" y="3" rx="1"/>
        <rect width="7" height="5" x="14" y="3" rx="1"/>
        <rect width="7" height="9" x="14" y="12" rx="1"/>
        <rect width="7" height="5" x="3" y="16" rx="1"/>
    </svg>
);

const RadioIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9"/>
        <path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5"/>
        <circle cx="12" cy="12" r="2"/>
        <path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5"/>
        <path d="M19.1 4.9c3.9 3.9 3.9 10.3 0 14.2"/>
    </svg>
);

const ServerIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect width="20" height="8" x="2" y="2" rx="2" ry="2"/>
        <rect width="20" height="8" x="2" y="14" rx="2" ry="2"/>
        <line x1="6" x2="6.01" y1="6" y2="6"/>
        <line x1="6" x2="6.01" y1="18" y2="18"/>
    </svg>
);

const BoxesIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>
        <path d="m3.3 7 8.7 5 8.7-5"/>
        <path d="M12 22V12"/>
    </svg>
);

function Sidebar() {
    return (
        <aside className="sidebar">
            <div className="brand">
                <div className="brand-mark">NI</div>
                <div className="brand-info">
                    <span className="brand-name">Network Inventory</span>
                    <span className="brand-version">v1.0.0</span>
                </div>
            </div>

            <nav className="navigation">
                <NavLink
                    to="/"
                    end
                    className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
                >
                    <LayoutDashboardIcon />
                    <span>Dashboard</span>
                </NavLink>

                <NavLink
                    to="/scans"
                    className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
                >
                    <RadioIcon />
                    <span>Scans</span>
                </NavLink>

                <NavLink
                    to="/devices"
                    className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
                >
                    <ServerIcon />
                    <span>Devices</span>
                </NavLink>

                <NavLink
                    to="/inventory"
                    className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`}
                >
                    <BoxesIcon />
                    <span>Inventory</span>
                </NavLink>
            </nav>

            <div className="sidebar-footer">
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span className="status-dot" />
                    <span>API Connected</span>
                </div>
                
                {/* Selector de Tema */}
                <div style={{ marginTop: '16px' }}>
                    <ThemeToggle />
                </div>
            </div>
        </aside>
    );
}

export default Sidebar;