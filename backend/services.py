
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
    

import json

def get_critical_alerts(db_conn, date):
    try:
        # Convert string to datetime
        date = datetime.strptime(date, "%Y-%m-%d")
        #date_with_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        start_ts = int(date.timestamp() * 1000)          # start of day in ms
        end_ts = int((date + timedelta(days=1)).timestamp() * 1000)  # start of next day in ms

        print(date)
        with db_conn.cursor() as cursor:
            cursor.execute("""
            SELECT
                TO_TIMESTAMP(t.date / 1000) AS log_time,
                (event_data ->> 1) AS event_description
            FROM
                public.variable_log_string t,
                jsonb_array_elements(t.value::jsonb) AS event_data
            WHERE
                t.id_var = 447
                AND t.date >= %s
                AND t.date < %s
                AND (event_data ->> 1) IN (
                    'EMERGENCIA EXTERNA',
                    'PARADA DE AVANCES',
                    'Falta tensión externa reles'
                )
            ORDER BY
                t.date;
            """, (start_ts, end_ts))
            return cursor.fetchall()

            
    except Exception as e:
        raise e

def get_number_daily_alerts(db_conn, date):
    try:
        # Convert string to datetime
        date = datetime.strptime(date, "%Y-%m-%d")
        start_ts = int(date.timestamp() * 1000)          # start of day in ms
        end_ts = int((date + timedelta(days=1)).timestamp() * 1000)  # start of next day in ms

        print(date)
        with db_conn.cursor() as cursor:
            cursor.execute("""
            SELECT COUNT(*) as alarm_snapshot_count
            FROM public.variable_log_string
            WHERE id_var = 447
              AND date >= %s
              AND date < %s
              AND value::text != '[]' 
            """, (start_ts, end_ts))
            #return len(cursor.fetchone())

            result = cursor.fetchone()
            
            count = result["alarm_snapshot_count"] if result else 0
            return {"num_alarms": count}
            #return cursor.fetchone()
            
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
        ``None`` if no data exists for that date. """
    try:
        # Convert string to datetime
        date = datetime.strptime(date, "%Y-%m-%d")
        start_ts = int(date.timestamp() * 1000)  # start of day in ms
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

        