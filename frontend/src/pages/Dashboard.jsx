import StatCard from "../components/StatCard";

// Iconos vectoriales
const IconDevices = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>
    </svg>
);

const IconScans = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
    </svg>
);

const IconWindows = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <path d="M3 12h18M12 3v18M4 4l16 16"/>
    </svg>
);

const IconNetwork = () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
        <rect x="2" y="2" width="6" height="6" rx="1"/><rect x="16" y="2" width="6" height="6" rx="1"/><rect x="9" y="16" width="6" height="6" rx="1"/><path d="M5 8v4h14V8M12 12v4"/>
    </svg>
);

function Dashboard() {
    return (
        <div className="page">
            <header className="page-header">
                <div>
                    <h1>Dashboard</h1>
                    <p>Network overview and inventory status.</p>
                </div>
            </header>

            {/* Grid Horizontal de 4 Columnas */}
            <div className="stats-grid">
                <StatCard 
                    title="Devices" 
                    value="20" 
                    description="Discovered devices" 
                    icon={<IconDevices />} 
                />
                <StatCard 
                    title="Scans" 
                    value="4" 
                    description="Completed scans" 
                    icon={<IconScans />} 
                />
                <StatCard 
                    title="Windows" 
                    value="5" 
                    description="Windows devices" 
                    icon={<IconWindows />} 
                />
                <StatCard 
                    title="Network" 
                    value="0" 
                    description="Network devices" 
                    icon={<IconNetwork />} 
                />
            </div>

            {/* Sección de Resumen de Inventario */}
            <section className="dashboard-section">
                <div className="section-header">
                    <h2>Inventory Overview</h2>
                    <p>Current network device distribution.</p>
                </div>

                <div className="inventory-summary">
                    <div className="inventory-card">
                        <div className="inventory-card-info">
                            <span>Linux</span>
                            <strong>0</strong>
                        </div>
                    </div>
                    <div className="inventory-card">
                        <div className="inventory-card-info">
                            <span>Servers</span>
                            <strong>0</strong>
                        </div>
                    </div>
                    <div className="inventory-card">
                        <div className="inventory-card-info">
                            <span>Printers</span>
                            <strong>3</strong>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Dashboard;