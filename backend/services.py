

def get_run(db_conn,limit):
    try:
        #print(conn)
        cursor = db_conn.cursor()
        cursor.execute(f"""SELECT "id_var", TO_TIMESTAMP("date"/1000) AS date, "value"
                       FROM "public"."variable_log_string" 
                       WHERE id_var=890 ORDER BY date DESC LIMIT {limit}""")
        rows = cursor.fetchone()
        cursor.close()
        return rows
    except Exception as e:
        raise e
    
def get_active_zones(db_conn,limit=1):
    zone1 = 806
    zone2 = 884
    zone3 = 798
    zone4 = 877

    zones = [zone1,zone2,zone3,zone4]

    zone_values = []

    try:
        cursor = db_conn.cursor()
        zone_values = []

        for id in zones:
            cursor.execute(f"""SELECT "id_var", TO_TIMESTAMP("date"/1000) AS date, "value"
                       FROM "public"."variable_log_float" 
                       WHERE id_var={id} ORDER BY date DESC LIMIT {limit};""")
            result = cursor.fetchone()
            zone_values.append(result['value'] if result else None)
        return {"zones": zone_values}

    except Exception as e:
        #raise HTTPException(status_code=500, detail=str(e))
        raise e

        