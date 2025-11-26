# Backend Overview

## What this module does
- Provides database access to recent runs and zone status.
- Computes daily averages for temperature and spindle load.
- Used by the FastAPI routes in `main.py`.

## How to run the backend
```bash
cd backend
source .venv/bin/activate
python -m uvicorn main:app --reload
```

## Code Reference

::: backend.services
    options:
      show_root_heading: false
      show_root_toc_entry: false
      heading_level: 3
      show_source: false
      members_order: source
