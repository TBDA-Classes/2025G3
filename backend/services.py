

def get_run(db_conn,limit):
    """
    Return the latest run from the `variable_log_string` table.

    Parameters
    ----------
    db_conn :
        An open database connection.
    limit :
        Number of latest rows to consider.

    Returns
    -------
    dict | None
        A row with keys `id_var`, `date`, `value`, or None if no data.
    """
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
    """
    Return the latest values for the configured zones.

    Parameters
    ----------
    db_conn :
        An open database connection.
    limit : int, optional
        Number of latest rows per zone to consider (default is 1).

    Returns
    -------
    dict
        Dictionary of the form ``{"zones": [v1, v2, v3, v4]}`` where each
        entry is the latest value for that zone, or ``None`` if no data
        exists for that zone.
    """
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

from datetime import datetime, timedelta

def get_daily_average_temp(db_conn, date):
    try:
        # Convert string to datetime
        date = datetime.strptime(date, "%Y-%m-%d")
        start_ts = int(date.timestamp() * 1000)          # start of day in ms
        end_ts = int((date + timedelta(days=1)).timestamp() * 1000)  # start of next day in ms

        with db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT %s::date AS log_time,
                       ROUND(AVG(value)::numeric, 1) AS avg_temp
                FROM "public"."variable_log_float"
                WHERE id_var = 618
                  AND date >= %s
                  AND date < %s;
            """, (date, start_ts, end_ts))

            return cursor.fetchone()
    except Exception as e:
        raise e
    
def get_daily_average_spindle_load(db_conn, date):
    """
    Compute the daily average temperature for a given date.

    The data is read from the ``variable_log_float`` table for ``id_var = 618``,
    using all samples within the given calendar day.

    Parameters
    ----------
    db_conn :
        An open database connection.
    date : str
        Date string in the format ``"YYYY-MM-DD"``.

    Returns
    -------
    dict | None
        A row with keys ``log_time`` (date) and ``avg_temp`` (numeric), or
        ``None`` if no data exists for that date.
    """
    try:
        # Convert string to datetime
        date = datetime.strptime(date, "%Y-%m-%d")
        start_ts = int(date.timestamp() * 1000)          # start of day in ms
        end_ts = int((date + timedelta(days=1)).timestamp() * 1000)  # start of next day in ms

        with db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT %s::date AS log_time,
                       ROUND(AVG(value)::numeric, 1) AS avg_spindle
                FROM "public"."variable_log_float"
                WHERE id_var = 630
                  AND date >= %s
                  AND date < %s;
            """, (date, start_ts, end_ts))
            return cursor.fetchone()
    except Exception as e:
        raise e
        