# User Guide – CNC Analytics Dashboard

This document explains how to run and use the CNC Analytics Dashboard locally.
It is intended for technical users and evaluators of the project.

The system consists of:
- A FastAPI backend that exposes CNC data through a REST API
- A React frontend that visualizes the data in a dashboard

Both components must be running locally for the dashboard to function.
---

## 1. System Overview

The dashboard allows users to:
- Select a date
- View daily average KPIs:
  - Temperature (°C)
  - Spindle load (%)
  - Power usage (kW)
  - Number of alerts
- Inspect hourly trends for temperature, spindle load, and power
- View critical alert for the selected day

    Only dates with available historical data (typically before 2022) will return results.
    - **An example of a week with data is one starting on 2021-11-22**

---

## 2. Dashboard Usage

### Selecting a Date
1. Use the date picker at the top of the dashboard
2. Select a date with available data
3. Click **Apply**

All KPIs, charts, and alerts update automatically.

### KPI Cards
The top cards show:
- **Average Daily Temperature** (°C)
- **Average Daily Spindle Load** (%)
- **Daily Alerts** (count)
- **Average Daily Power** (kW)

### Hourly Performance Chart
The chart displays hourly averages for:
- Temperature (°C)
- Spindle load (%)
- Power usage (kW)

Each metric has its own axis and color.

### Critical Alerts Panel
The right-hand panel lists critical alerts:
- Timestamp
- Alert description (e.g. *EMERGENCIA EXTERNA*)

---

## 3. Repository Structure (relevant parts)

From the project root:

```2025G3/
  backend/            # FastAPI backend
  frontend/TBDA/      # React frontend
  docs/               # Project documentation
  ```

## 4. Prerequisites

To run the system locally, you need:

- Python 3.11 or newer
- Node.js and npm
- Access to the course PostgreSQL database
- A .env file with database credentials

## 5. 5. Running the Backend (FastAPI)

Activate the virtual environment
From the project root:
    
```cd backend
source .venv/bin/activate
cd ..
uvicorn backend.main:app --reload
```

If successful, you should see output similar to:
```Uvicorn running on http://127.0.0.1:8000```

The backend API will now be available at:
[http://localhost:8000](http://localhost:8000)




