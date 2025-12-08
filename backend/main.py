from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database import get_connection
import backend.services as services

# Run with:
# uvicorn backend.main:app --reload

#CORS 
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"]

db_conn = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_conn
    db_conn = get_connection()
    print("Database connection established")
    try: 
        yield
    finally:
        if db_conn:
            db_conn.close()
            print("Database connection closed")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/daily_temp_avg")
def get_daily_temp_avg(date: str = Query(...)):
    """Return the average daily temperature for a given date.

    Args:
        date: ISO date string YYYY-MM-DD.

    Returns:
        A dict with the date and average temperature value.
    """
    try:
        return services.get_daily_average_temp(db_conn, date)
    except Exception as e:
        db_conn.rollback()

        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/number_daily_alerts")
def get_daily_alerts_number(date: str = Query(...)):
    """Return the number of alert snapshots recorded on the given date.

    Args:
        date: ISO date string YYYY-MM-DD.

    Returns:
        Dict with key 'num_alarms'.
    """
    try:
        return services.get_number_daily_alerts(db_conn, date)
    except Exception as e:
        db_conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/critical_alerts")
def get_critical_alerts_data(date: str = Query(...)):
    """Return all critical alert events for the given date.

    Args:
        date: ISO date string YYYY-MM-DD.

    Returns:
        List of dicts with timestamp and alert description.
    """
    try:
        return services.get_critical_alerts(db_conn, date)
    except Exception as e:
        db_conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/daily_spindle_avg")
def get_daily_spindle_avg(date: str = Query(...)):
    """Return the average daily spindle load for the given date.

    Args:
        date: ISO date string YYYY-MM-DD.

    Returns:
        Dict with average spindle load.
    """
    try:
        return services.get_daily_average_spindle_load(db_conn, date)
    except Exception as e:
        db_conn.rollback()

        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/api/hourly_spindle_avg")
def get_hourly_spindle_avg(date: str = Query(...)):
    """Return hourly average spindle load for the given date.

    Args:
        date: ISO date string YYYY-MM-DD.

    Returns:
        List of hourly averages.
    """
    try:
        return services.get_hourly_average_spindle_load(db_conn, date)
    except Exception as e:
        db_conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hourly_temp_avg")
def get_hourly_temp_avg(date: str = Query(...)):
    """Return hourly average temperature for the given date.

    Args:
        date: ISO date string YYYY-MM-DD.

    Returns:
        List of hourly averages.
    """
    try:
        return services.get_hourly_average_temp(db_conn, date)
    except Exception as e:
        db_conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
# Add this to main.py
@app.get("/api/hourly_combined")
def get_hourly_combined(date: str = Query(...)):
    """Return hourly averages of both temperature and spindle load.

    Args:
        date: ISO date string YYYY-MM-DD.

    Returns:
        List of dicts with hour, avg_temp, and avg_spindle.
    """
    try:
        return services.get_hourly_combined_stats(db_conn, date)
    except Exception as e:
        db_conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))