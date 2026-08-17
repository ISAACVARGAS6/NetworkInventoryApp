import { useEffect, useState } from "react";
import { getScan, getScans, startScan } from "../services/api";

function formatDate(value) { return value ? new Date(value).toLocaleString() : "—"; }

function Scans() {
    const [scans, setScans] = useState([]);
    const [network, setNetwork] = useState("");
    const [selectedScan, setSelectedScan] = useState(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);
    const [running, setRunning] = useState(false);

    async function loadScans() {
        try { setError(""); setScans(await getScans()); } catch (requestError) { setError(requestError.message); } finally { setLoading(false); }
    }
    useEffect(() => {
        let active = true;

        getScans()
            .then((scanList) => {
                if (active) setScans(scanList);
            })
            .catch((requestError) => {
                if (active) setError(requestError.message);
            })
            .finally(() => {
                if (active) setLoading(false);
            });

        return () => { active = false; };
    }, []);

    async function handleStartScan(event) {
        event.preventDefault(); setRunning(true); setError("");
        try { await startScan(network.trim() || null); setNetwork(""); await loadScans(); } catch (requestError) { setError(requestError.message); } finally { setRunning(false); }
    }
    async function showDetails(scanId) {
        try { setError(""); setSelectedScan(await getScan(scanId)); } catch (requestError) { setError(requestError.message); }
    }

    return <div className="page">
        <header className="page-header"><div><h1>Scans</h1><p>Network scan history and execution.</p></div></header>
        <form className="scan-form" onSubmit={handleStartScan}><label htmlFor="network">Network (CIDR, optional)<input id="network" value={network} onChange={(event) => setNetwork(event.target.value)} placeholder="192.168.1.0/24" disabled={running} /></label><button type="submit" disabled={running}>{running ? "Scanning…" : "Start scan"}</button></form>
        {error && <div className="error-message">{error}</div>}
        {loading && <div className="loading">Loading scans…</div>}
        {!loading && !error && scans.length === 0 && <div className="empty-state">No scans have been completed yet.</div>}
        {!loading && scans.length > 0 && <div className="table-card"><div className="table-scroll"><table><thead><tr><th>ID</th><th>Network</th><th>Started</th><th>Hosts</th><th></th></tr></thead><tbody>{scans.map((scan) => <tr key={scan.id}><td>{scan.id}</td><td>{scan.network}</td><td>{formatDate(scan.started_at)}</td><td>{scan.hosts_found}</td><td><button className="secondary-button" onClick={() => showDetails(scan.id)}>Details</button></td></tr>)}</tbody></table></div></div>}
        {selectedScan && <section className="scan-details"><div className="section-header"><h2>Scan #{selectedScan.id}</h2><p>{selectedScan.devices.length} saved devices</p></div><ul>{selectedScan.devices.map((device) => <li key={device.id}><strong>{device.ip}</strong> — {device.hostname} ({device.device_type})</li>)}</ul></section>}
    </div>;
}

export default Scans;
