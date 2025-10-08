from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection

# uvicorn main:app --reload

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


#Example GET Endpoint for the latest programs
#ran by the machine

@app.get("/api")
def get_example(limit: int = 10):
    try:
        print("get")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""SELECT "id_var", TO_TIMESTAMP("date"/1000) AS date, "value"
                       FROM "public"."variable_log_string" 
                       WHERE id_var=890 ORDER BY date DESC LIMIT {limit}""")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))