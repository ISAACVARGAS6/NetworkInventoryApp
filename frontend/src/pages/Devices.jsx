import { useEffect, useState } from "react";
import { getDevices } from "../services/api";

function Devices() {
    const [devices, setDevices] = useState([]);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function loadDevices() {
            try { setDevices(await getDevices()); } catch (requestError) { setError(requestError.message); } finally { setLoading(false); }
        }
        loadDevices();
    }, []);

    return <div className="page">
        <header className="page-header"><div><h1>Devices</h1><p>Discovered network devices.</p></div></header>
        {loading && <div className="loading">Loading devices…</div>}
        {error && <div className="error-message">Unable to load devices: {error}</div>}
        {!loading && !error && devices.length === 0 && <div className="empty-state">No devices have been discovered yet.</div>}
        {!loading && !error && devices.length > 0 && <div className="table-card"><div className="table-scroll"><table>
            <thead><tr><th>IP</th><th>Hostname</th><th>Type</th><th>Manufacturer</th><th>MAC</th><th>Services</th></tr></thead>
            <tbody>{devices.map((device) => <tr key={device.id}>
                <td>{device.ip}</td><td>{device.hostname}</td><td><span className="type-badge">{device.device_type}</span></td><td>{device.manufacturer}</td><td className="mono">{device.mac}</td>
                <td>{device.ports.length ? device.ports.map((port) => `${port.port} (${port.service})`).join(", ") : "—"}</td>
            </tr>)}</tbody>
        </table></div></div>}
    </div>;
}

export default Devices;
