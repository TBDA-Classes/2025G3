user = "lectura"
password = "ncorrea#2022"
host = "138.100.82.184"    
port = "2345"               
database = "2207"           

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")