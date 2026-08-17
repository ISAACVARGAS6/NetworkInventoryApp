import { useEffect, useState } from "react";
import StatCard from "../components/StatCard";
import { getInventory, getInventoryStats } from "../services/api";

function Dashboard() {
    const [data, setData] = useState(null);
    const [error, setError] = useState("");

    useEffect(() => {
        async function loadDashboard() {
            try {
                const [inventory, stats] = await Promise.all([getInventory(), getInventoryStats()]);
                setData({ inventory, stats });
            } catch (requestError) {
                setError(requestError.message);
            }
        }
        loadDashboard();
    }, []);

    if (error) return <div className="error-message">Unable to load dashboard: {error}</div>;
    if (!data) return <div className="loading">Loading inventory data…</div>;

    const { inventory, stats } = data;
    const { types } = stats;
    return (
        <div className="page">
            <header className="page-header"><div><h1>Dashboard</h1><p>Network overview and inventory status.</p></div></header>
            <div className="stats-grid">
                <StatCard title="Devices" value={inventory.total_devices} description="Discovered devices" />
                <StatCard title="Scans" value={inventory.total_scans} description="Completed scans" />
                <StatCard title="Windows" value={types.windows} description="Windows devices" />
                <StatCard title="Network" value={types.network} description="Network devices" />
            </div>
            <section className="dashboard-section">
                <div className="section-header"><h2>Inventory Overview</h2><p>Current network device distribution.</p></div>
                <div className="inventory-summary">
                    <SummaryCard label="Linux" value={types.linux} />
                    <SummaryCard label="Servers" value={types.servers} />
                    <SummaryCard label="Printers" value={types.printers} />
                    <SummaryCard label="Unknown" value={types.unknown} />
                </div>
            </section>
        </div>
    );
}

function SummaryCard({ label, value }) {
    return <div className="inventory-card"><div className="inventory-card-info"><span>{label}</span><strong>{value}</strong></div></div>;
}

export default Dashboard;
