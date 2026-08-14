const API_URL =
    import.meta.env.VITE_API_URL ||
    "http://127.0.0.1:8000/api";


async function request(endpoint, options = {}) {
    const response = await fetch(
        `${API_URL}${endpoint}`,
        {
            headers: {
                "Content-Type": "application/json",
                ...options.headers,
            },
            ...options,
        }
    );


    if (!response.ok) {

        let message =
            `API request failed: ${response.status}`;

        try {

            const data =
                await response.json();

            if (data.detail) {
                message = data.detail;
            }

        } catch {
            // Response was not JSON.
        }

        throw new Error(message);
    }


    return response.json();
}


/* ============================================================
   INVENTORY
   ============================================================ */

export async function getInventory() {
    return request("/inventory");
}


export async function getInventoryStats() {
    return request("/inventory/stats");
}


/* ============================================================
   DEVICES
   ============================================================ */

export async function getDevices() {
    return request("/devices");
}


/* ============================================================
   SCANS
   ============================================================ */

export async function getScans() {
    return request("/scans");
}


export async function getScan(scanId) {
    return request(`/scans/${scanId}`);
}


export async function startScan(network = null) {

    return request(
        "/scans",
        {
            method: "POST",

            body: JSON.stringify(
                network
                    ? { network }
                    : {}
            ),
        }
    );
}