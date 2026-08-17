# Network Inventory
<img width="1172" height="894" alt="image" src="https://github.com/user-attachments/assets/f002798e-b8ef-4508-b0c2-c28462295dab" />
<img width="1160" height="886" alt="image" src="https://github.com/user-attachments/assets/d7bdaa61-a94b-46c5-9bb7-24283c986699" />
<img width="1153" height="888" alt="image" src="https://github.com/user-attachments/assets/5ee7666a-cbf8-4625-9665-57cd5d63487d" />
<img width="1157" height="895" alt="image" src="https://github.com/user-attachments/assets/ac6b0d45-98a9-4a55-8454-6544cac5e6d2" />




Network inventory and discovery application built with React and FastAPI.

The application scans an authorized IPv4 network, discovers active hosts, identifies basic device information, detects common TCP services, classifies devices, and stores scan results in a SQLite database.

## Features

- IPv4 network discovery
- ICMP host detection
- Hostname resolution
- MAC address detection through ARP
- MAC manufacturer identification using OUI data
- TCP port scanning
- Basic device classification
- Scan history
- Persistent inventory using SQLite
- REST API with FastAPI
- React dashboard
- Network inventory statistics
- Modular backend architecture
- Environment-based configuration

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Concurrent network scanning with ThreadPoolExecutor

### Frontend

- React
- Vite
- React Router
- JavaScript
- CSS

## Project Structure

```text
network-inventory/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   │
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   │
│   ├── .env.example
│   └── package.json
│
├── .gitignore
├── LICENSE

Requirements
Python 3.11+
Node.js 20.19+ or Node.js 22+
npm

The scanner must be executed against networks for which you have authorization to perform network discovery and port scanning.

Backend Setup

Navigate to the backend directory:

cd backend

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the dependencies:

pip install -r requirements.txt

Create a .env file based on .env.example.

Example:

NETWORK=192.168.1.0/24
DISCOVERY_TIMEOUT=500
PORT_TIMEOUT=0.25
DISCOVERY_WORKERS=50
PORT_WORKERS=30

Start the API:

uvicorn app.main:app --reload

The API will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs
Frontend Setup

Open another terminal and navigate to the frontend:

cd frontend

Install dependencies:

npm install

Create a .env file based on .env.example.

Example:

VITE_API_URL=http://127.0.0.1:8000/api

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5173
API Endpoints
Inventory
GET /api/inventory
GET /api/inventory/stats
Devices
GET /api/devices
GET /api/devices/{device_id}
Scans
GET /api/scans
GET /api/scans/{scan_id}
POST /api/scans
Example Scan Request

A scan can use the network configured in the backend environment:

{}

Or a specific authorized network can be supplied:

{
    "network": "192.168.1.0/24"
}
Architecture

The application is divided into three main layers:

React Frontend
       │
       │ REST API
       ▼
FastAPI Backend
       │
       ├── Scanner Services
       │
       ├── Device Classification
       │
       └── SQLAlchemy
              │
              ▼
           SQLite

The frontend is responsible for presentation and user interaction.

The FastAPI backend exposes the REST API and coordinates scanning and persistence.

The scanner logic is isolated from the API layer so it can be reused independently.

Development Status

Current functionality includes:

Network host discovery
Device information collection
TCP service detection
Device classification
SQLite persistence
REST API
React dashboard

Planned improvements:

Scan progress reporting
Device detail view
Scan history interface
Inventory filtering and search
Device status tracking
Comparison between scans
Export to CSV
Improved device classification
Authentication
Background scan execution
License

This project is licensed under the MIT License.
