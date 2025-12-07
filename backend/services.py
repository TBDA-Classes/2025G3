
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
    
from datetime import datetime, timedelta


import json

def get_critical_alerts(db_conn, date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
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

            result = cursor.fetchone()
            
            count = result["alarm_snapshot_count"] if result else 0
            return {"num_alarms": count}
    except Exception as e:
        raise e

def get_daily_average_spindle_load(db_conn, date):

    try:
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

    
def get_hourly_combined_stats(db_conn, date_str):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        start_ts = int(target_date.timestamp() * 1000)
        end_ts = int((target_date + timedelta(days=1)).timestamp() * 1000)

        with db_conn.cursor() as cursor:
            # We select from the same table, but filter for BOTH IDs (618 and 630)
            # We use MAX(CASE...) to separate them into columns in one row
            query = """
                SELECT 
                    date_trunc('hour', to_timestamp(date / 1000.0)) AS log_hour,
                    ROUND(AVG(CASE WHEN id_var = 618 THEN value END)::numeric, 1) as avg_temp,
                    ROUND(AVG(CASE WHEN id_var = 630 THEN value END)::numeric, 1) as avg_spindle
                FROM "public"."variable_log_float"
                WHERE id_var IN (618, 630)
                  AND date >= %s
                  AND date < %s
                GROUP BY 1
                ORDER BY 1 ASC;
            """
            cursor.execute(query, (start_ts, end_ts))
            return cursor.fetchall()

    except Exception as e:
        raise e