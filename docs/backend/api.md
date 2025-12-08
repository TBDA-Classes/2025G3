# Backend API

## How to run the backend
From the project root:

```bash
cd backend
source .venv/bin/activate
uvicorn backend.main:app --reload
```

## FastAPI endpoints

::: backend.main
    options:
      members:
        - get_daily_temp_avg
        - get_daily_alerts_number
        - get_critical_alerts_data
        - get_daily_spindle_avg
        - get_hourly_spindle_avg
        - get_hourly_temp_avg
        - get_hourly_combined
      show_root_heading: false
      show_source: false
