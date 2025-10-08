from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection

app = FastAPI()

#CORS 
origins = [
    "http://localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Example GET Endpoint

@app.get("/api")
def get_example(limit: int = 20):
    try:
        print("get")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM "public"."units" LIMIT {limit}')
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))