import {
    useEffect,
    useState,
} from "react";

import StatCard from "../components/StatCard";

import {
    getInventory,
    getInventoryStats,
} from "../services/api";


function Dashboard() {

    const [inventory, setInventory] =
        useState(null);

    const [stats, setStats] =
        useState(null);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState(null);


    useEffect(() => {

        async function loadDashboard() {

            try {

                const [
                    inventoryData,
                    statsData,
                ] = await Promise.all([
                    getInventory(),
                    getInventoryStats(),
                ]);

                setInventory(
                    inventoryData
                );

                setStats(
                    statsData
                );

            } catch (error) {

                setError(
                    "Unable to connect to the API."
                );

            } finally {

                setLoading(false);

            }
        }


        loadDashboard();

    }, []);


    if (loading) {
        return (
            <div className="page">
                <div className="loading">
                    Loading dashboard...
                </div>
            </div>
        );
    }


    if (error) {
        return (
            <div className="page">
                <div className="error-message">
                    {error}
                </div>
            </div>
        );
    }


    return (
        <div className="page">

            <header className="page-header">

                <div>

                    <h1>
                        Dashboard
                    </h1>

                    <p>
                        Network overview and inventory status.
                    </p>

                </div>

            </header>


            <section className="stats-grid">

                <StatCard
                    title="Devices"
                    value={
                        inventory?.total_devices ?? 0
                    }
                    description="Discovered devices"
                />

                <StatCard
                    title="Scans"
                    value={
                        inventory?.total_scans ?? 0
                    }
                    description="Completed scans"
                />

                <StatCard
                    title="Windows"
                    value={
                        stats?.types?.windows ?? 0
                    }
                    description="Windows devices"
                />

                <StatCard
                    title="Network"
                    value={
                        stats?.types?.network ?? 0
                    }
                    description="Network devices"
                />

            </section>


            <section className="dashboard-section">

                <div className="section-header">

                    <div>

                        <h2>
                            Inventory overview
                        </h2>

                        <p>
                            Current network device distribution.
                        </p>

                    </div>

                </div>


                <div className="inventory-summary">

                    <div>
                        <span>Linux</span>
                        <strong>
                            {stats?.types?.linux ?? 0}
                        </strong>
                    </div>

                    <div>
                        <span>Servers</span>
                        <strong>
                            {stats?.types?.servers ?? 0}
                        </strong>
                    </div>

                    <div>
                        <span>Printers</span>
                        <strong>
                            {stats?.types?.printers ?? 0}
                        </strong>
                    </div>

                    <div>
                        <span>Unknown</span>
                        <strong>
                            {stats?.types?.unknown ?? 0}
                        </strong>
                    </div>

                </div>

            </section>

        </div>
    );
}


export default Dashboard;