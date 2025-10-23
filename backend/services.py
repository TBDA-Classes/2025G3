

def get_example(db_conn,limit):
    try:
        #print(conn)
        cursor = db_conn.cursor()
        cursor.execute(f"""SELECT "id_var", TO_TIMESTAMP("date"/1000) AS date, "value"
                       FROM "public"."variable_log_string" 
                       WHERE id_var=890 ORDER BY date DESC LIMIT {limit}""")
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except Exception as e:
        raise e
    
def get_active_zones(db_conn):
    zone1 = 806
    zone2 = 884
    zone3 = 798
    zone4 = 877
    try:
        cursor = db_conn.cursor()
        cursor.execute(f"""SELECT "id_var", TO_TIMESTAMP("date"/1000) AS date, "value"
                       FROM "public"."variable_log_float" 
                       WHERE id_var={zone1} ORDER BY date DESC;""")
        zone1_data = cursor.fetchall()

        cursor.execute(f"""SELECT "id_var", TO_TIMESTAMP("date"/1000) AS date, "value"
                       FROM "public"."variable_log_float" 
                       WHERE id_var={zone2} ORDER BY date DESC;""")
        zone2_data = cursor.fetchall()

        cursor.execute(f"""SELECT "id_var", TO_TIMESTAMP("date"/1000) AS date, "value"
                       FROM "public"."variable_log_float" 
                       WHERE id_var={zone3} ORDER BY date DESC;""")
        zone3_data = cursor.fetchall()

        cursor.execute(f"""SELECT "id_var", TO_TIMESTAMP("date"/1000) AS date, "value"
                       FROM "public"."variable_log_float" 
                       WHERE id_var={zone4} ORDER BY date DESC;""")
        zone4_data = cursor.fetchall()

        return{"table1": zone1_data,
               "table2": zone2_data,
               "table3": zone3_data,
               "table4": zone4_data}
    except Exception as e:
        #raise HTTPException(status_code=500, detail=str(e))
        raise e

        