# NetworkInventoryApp

<img width="1172" height="894" alt="image" src="https://github.com/user-attachments/assets/f002798e-b8ef-4508-b0c2-c28462295dab" />
<img width="1160" height="886" alt="image" src="https://github.com/user-attachments/assets/d7bdaa61-a94b-46c5-9bb7-24283c986699" />
<img width="1153" height="888" alt="image" src="https://github.com/user-attachments/assets/5ee7666a-cbf8-4625-9665-57cd5d63487d" />
<img width="1157" height="895" alt="image" src="https://github.com/user-attachments/assets/ac6b0d45-98a9-4a55-8454-6544cac5e6d2" />

Full-stack network inventory and discovery application built with **React and FastAPI**.

The application scans authorized IPv4 networks, discovers active devices, identifies manufacturers and services, classifies devices, and stores the collected information in a centralized inventory.

The project was built to combine **network discovery, backend API development, database management, and a modern web interface** into a single application.

## Features

* Network discovery using ICMP and ARP
* MAC address detection
* Device manufacturer identification using OUI data
* TCP port and service detection
* Automatic device classification
* Network scan history
* Persistent device inventory
* REST API built with FastAPI
* React dashboard for visualization
* Concurrent network scanning
* SQLite database
* CORS configuration for frontend/backend communication
* Environment-based configuration


## Architecture

```text
┌──────────────────────────┐
│        React + Vite      │
│      Frontend / UI       │
└────────────┬─────────────┘
             │ HTTP / REST
             ▼
┌──────────────────────────┐
│       FastAPI Backend    │
│                          │
│  ┌────────────────────┐  │
│  │ Network Scanner    │  │
│  └─────────┬──────────┘  │
│            │             │
│  ┌─────────▼──────────┐  │
│  │ Device Detection   │  │
│  │ & Classification   │  │
│  └─────────┬──────────┘  │
└────────────┼─────────────┘
             │
             ▼
┌──────────────────────────┐
│      SQLite Database     │
│                          │
│  Devices / Scans / Data  │
└──────────────────────────┘
```

## Technology Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite

### Frontend

* React
* Vite
* JavaScript
* React Router

### Network

* ICMP discovery
* ARP
* TCP port scanning
* OUI manufacturer lookup

## Project Structure

```text
NetworkInventoryApp/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── .env
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

## How It Works

The application follows this general workflow:

```text
1. User starts a network scan
              ↓
2. Backend receives the network range
              ↓
3. Scanner discovers active hosts
              ↓
4. MAC addresses are identified
              ↓
5. OUI data is used to identify manufacturers
              ↓
6. TCP services are detected
              ↓
7. Devices are classified
              ↓
8. Results are stored in SQLite
              ↓
9. React dashboard displays the inventory
```

## API

The backend exposes REST endpoints for managing scans and devices.

### Start a network scan

```http
POST /scan
```

Example request:

```json
{
  "network": "192.168.1.0/24"
}
```

### Get devices

```http
GET /devices
```

### Get scan history

```http
GET /scans
```

The exact available endpoints can be explored through the FastAPI interactive documentation.

## Installation

### Requirements

* Python 3.10+
* Node.js 20+
* npm
* Access to an authorized IPv4 network

### Clone the repository

```bash
git clone https://github.com/ISAACVARGAS6/NetworkInventoryApp.git

cd NetworkInventoryApp
```

## Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Open another terminal and navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will be available at the URL provided by Vite.

## Configuration

Network configuration and environment-specific values should be stored in environment variables rather than hard-coded into the application.

Example:

```env
NETWORK=192.168.1.0/24
```

The OUI database used for manufacturer identification is kept outside version control.

## Security and Scope

This project is intended for **authorized network environments** such as local labs, development environments, and networks where the user has permission to perform discovery and inventory operations.

The application does not attempt to exploit discovered services or gain unauthorized access to devices.

## Current Status

The core functionality of the application is implemented, including:

* Network discovery
* Device detection
* MAC address identification
* Manufacturer lookup
* Device classification
* Port/service detection
* Scan persistence
* Device inventory
* REST API
* React frontend

The project is still being improved as a personal portfolio project.

## Future Improvements

Possible future improvements include:

* User authentication and authorization
* Scheduled network scans
* Background scanning
* CSV/Excel inventory export
* Scan comparison
* Device change detection
* Improved device classification
* More detailed network statistics
* Improved dashboard visualization

## What I Learned

This project allowed me to work across multiple areas of full-stack development, including:

* Designing and consuming REST APIs
* Building a backend with FastAPI
* Working with relational databases
* Developing reusable React components
* Managing frontend/backend communication
* Implementing concurrent network discovery
* Processing network information
* Working with MAC addresses and OUI databases
* Structuring a full-stack application
* Managing configuration and sensitive files with environment variables and `.gitignore`

## Author

**Isaac Vargas**

Full Stack Developer | React, Next.js, Python, FastAPI & Laravel

GitHub:
https://github.com/ISAACVARGAS6




