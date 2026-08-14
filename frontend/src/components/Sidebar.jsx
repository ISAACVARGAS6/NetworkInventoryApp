import {
    NavLink,
} from "react-router-dom";


function Sidebar() {

    return (
        <aside className="sidebar">

            <div className="brand">

                <div className="brand-mark">
                    NI
                </div>

                <div>
                    <div className="brand-name">
                        Network Inventory
                    </div>

                    <div className="brand-version">
                        v1.0
                    </div>
                </div>

            </div>


            <nav className="navigation">

                <NavLink
                    to="/"
                    end
                    className="nav-link"
                >
                    Dashboard
                </NavLink>


                <NavLink
                    to="/scans"
                    className="nav-link"
                >
                    Scans
                </NavLink>


                <NavLink
                    to="/devices"
                    className="nav-link"
                >
                    Devices
                </NavLink>


                <NavLink
                    to="/inventory"
                    className="nav-link"
                >
                    Inventory
                </NavLink>

            </nav>


            <div className="sidebar-footer">

                <span className="status-dot" />

                API Connected

            </div>

        </aside>
    );
}


export default Sidebar;