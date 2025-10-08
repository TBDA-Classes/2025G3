import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

""" 
TODO:
Enter correct credentials below

"""

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),      
        port=os.get("DB_PORT"),
        database=os.get("DB_NAME"),      
        user=os.getenv("DB_USER"),          
        password=os.getenv("DB_PASSWORD"), 
        cursor_factory=RealDictCursor  
    )
    return conn