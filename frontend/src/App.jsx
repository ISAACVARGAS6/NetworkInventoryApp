import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import Scans from "./pages/Scans";
import Devices from "./pages/Devices";
import Inventory from "./pages/Inventory";

import "./App.css";


function App() {
    return (
        <BrowserRouter>

            <div className="app">

                <Sidebar />

                <main className="main-content">

                    <Routes>

                        <Route
                            path="/"
                            element={<Dashboard />}
                        />

                        <Route
                            path="/scans"
                            element={<Scans />}
                        />

                        <Route
                            path="/devices"
                            element={<Devices />}
                        />

                        <Route
                            path="/inventory"
                            element={<Inventory />}
                        />

                    </Routes>

                </main>

            </div>

        </BrowserRouter>
    );
}


export default App;