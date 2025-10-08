import psycopg2
from psycopg2.extras import RealDictCursor

""" 
TODO:
Enter correct credentials below

"""

def get_connection():
    conn = psycopg2.connect(
        host="138.100.82.184",       # e.g., "127.0.0.1" or "db.example.com"
        port="2345",
        database="2207",       # name of your database
        user="lectura",           # database username
        password="ncorrea#2022",   # database password
        cursor_factory=RealDictCursor  # returns rows as dicts instead of tuples
    )
    return conn