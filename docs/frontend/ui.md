# Frontend overview

The frontend is a React-based single-page application that lets users explore
machine data for a selected day.

## Tech stack

- React + TypeScript (Vite)
- HTTP client: fetch / axios (depending on what you actually use)
- Deployed as static assets (served separately from the FastAPI backend)

## Main responsibilities

- Let the user pick a **date**.
- Call the backend API endpoints:
  - `/api/daily_temp_avg`
  - `/api/daily_spindle_avg`
  - `/api/hourly_temp_avg`
  - `/api/hourly_spindle_avg`
  - `/api/hourly_combined`
  - `/api/critical_alerts`
- Render:
  - daily KPIs (cards)
  - hourly graphs (temperature, spindle load, later energy)
  - list of alerts for the selected day

