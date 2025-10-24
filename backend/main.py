from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from contextlib import asynccontextmanager
import services 

# uvicorn main:app --reload

#CORS 
origins = [
    "http://localhost:5173"
]

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


@app.get("/api/recent_run")
def get_run(limit: int = 1):

    try:
        row = services.get_run(db_conn,limit)
        if row is None:
            return {}
        return {
            "date": row['date'].isoformat(),
            "value": row['value']
        }
    except Exception as e:
        db_conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/api/active_zones")
def get_zones():

    try:
        print(services.get_active_zones(db_conn))
        return services.get_active_zones(db_conn)
    except Exception as e:
        db_conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))