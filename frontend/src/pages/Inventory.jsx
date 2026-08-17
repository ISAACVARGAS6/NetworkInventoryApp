import { useEffect, useState } from "react";
import StatCard from "../components/StatCard";
import { getInventory, getInventoryStats } from "../services/api";

const typeLabels = { windows: "Windows", linux: "Linux", servers: "Servers", printers: "Printers", network: "Network infrastructure", unknown: "Unknown" };

function Inventory() {
    const [data, setData] = useState(null);
    const [error, setError] = useState("");
    useEffect(() => {
        async function loadInventory() {
            try { const [inventory, stats] = await Promise.all([getInventory(), getInventoryStats()]); setData({ inventory, stats }); } catch (requestError) { setError(requestError.message); }
        }
        loadInventory();
    }, []);
    if (error) return <div className="error-message">Unable to load inventory: {error}</div>;
    if (!data) return <div className="loading">Loading inventory…</div>;
    return <div className="page">
        <header className="page-header"><div><h1>Inventory</h1><p>Network inventory and statistics.</p></div></header>
        <div className="stats-grid inventory-top-stats"><StatCard title="Total devices" value={data.inventory.total_devices} /><StatCard title="Total scans" value={data.inventory.total_scans} /></div>
        <section className="dashboard-section"><div className="section-header"><h2>Device types</h2><p>Classification from saved scan results.</p></div>
            <div className="inventory-summary">{Object.entries(data.stats.types).map(([type, count]) => <div className="inventory-card" key={type}><div className="inventory-card-info"><span>{typeLabels[type]}</span><strong>{count}</strong></div></div>)}</div>
        </section>
    </div>;
}

export default Inventory;
