
from datetime import datetime, timedelta

def get_daily_average_temp(db_conn, date):
    """Compute the average temperature for a single day.

    Args:
        db_conn: PostgreSQL connection.
        date: ISO date string YYYY-MM-DD.

    Returns:
        Dict with log_time and avg_temp.
    """
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

def get_critical_alerts(db_conn, date):
    """Fetch all critical alerts for the specified date.

    Args:
        db_conn: PostgreSQL connection.
        date: ISO date string YYYY-MM-DD.

    Returns:
        List of dicts with timestamp and alert description.
    """
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
    """Count how many alert snapshots exist for the date.

    Args:
        db_conn: PostgreSQL connection.
        date: ISO date string YYYY-MM-DD.

    Returns:
        Dict containing the number of alerts.
    """
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
    """Compute the average spindle load for a single day.

    Args:
        db_conn: PostgreSQL connection.
        date: ISO date string YYYY-MM-DD.

    Returns:
        Dict with log_time and avg_spindle.
    """
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
    """Return hourly averages of temperature, spindle load, AND power usage.

    Args:
        db_conn: PostgreSQL connection.
        date_str: ISO date string YYYY-MM-DD.

    Returns:
        List of dicts with log_hour, avg_temp, avg_spindle, and power_kW.
    """
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        start_ts = int(target_date.timestamp() * 1000)
        end_ts = int((target_date + timedelta(days=1)).timestamp() * 1000)

        # Constant for the machine's max power
        MAX_POWER = 37.0 

        with db_conn.cursor() as cursor:
            query = """
                SELECT 
                    date_trunc('hour', to_timestamp(date / 1000.0)) AS log_hour,
                    
                    -- Temperature (ID 618)
                    ROUND(AVG(CASE WHEN id_var = 618 THEN value END)::numeric, 1) as avg_temp,
                    
                    -- Spindle Load (ID 630)
                    ROUND(AVG(CASE WHEN id_var = 630 THEN value END)::numeric, 1) as avg_spindle,

                    -- Power Calculation (Based on Spindle ID 630)
                    -- Formula: (Avg_Spindle / 100) * 37.0
                    ROUND(
                        (AVG(CASE WHEN id_var = 630 THEN value END) / 100.0 * %s)::numeric, 
                        2
                    ) as "power_kW"

                FROM "public"."variable_log_float"
                WHERE id_var IN (618, 630)
                  AND date >= %s
                  AND date < %s
                GROUP BY 1
                ORDER BY 1 ASC;
            """
            # Pass MAX_POWER as the first parameter, then start_ts, then end_ts
            cursor.execute(query, (MAX_POWER, start_ts, end_ts))
            return cursor.fetchall()

    except Exception as e:
        raise e

from sqlalchemy import create_engine, text

def get_energy_usage(db_conn, date_str):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        start_ts = int(target_date.timestamp() * 1000)
        end_ts = int((target_date + timedelta(days=1)).timestamp() * 1000)

        MAX_POWER_KW = 37.0

        with db_conn.cursor() as cursor:
            query = """
                SELECT 
                    date_trunc('hour', to_timestamp(date/1000)) AS hour_bin,
                    AVG(value) AS avg_value
                FROM public.variable_log_float
                WHERE id_var = 630
                AND date >= %s
                AND date < %s
                GROUP BY hour_bin
                ORDER BY hour_bin;
            """
            cursor.execute(query, (start_ts, end_ts))
            rows = cursor.fetchall()

        energy_data = []
        for row in rows:
            # HÄR ÄR ÄNDRINGEN: Vi hämtar värdena med nyckel istället för att packa upp
            # Använd row['hour_bin'] och row['avg_value']
            
            # OBS: Kontrollera om avg_value är None (om ingen data fanns den timmen)
            if row['avg_value'] is None:
                continue

            power_kw = MAX_POWER_KW * (float(row['avg_value']) / 100.0)
            
            energy_data.append({
                "real_date": row['hour_bin'].isoformat(),
                "power_kW": round(power_kw, 2)
            })

        return energy_data

    except Exception as e:
        # Bra för debugging att se vad som faktiskt gick fel i terminalen
        print(f"Error in get_energy_usage: {e}") 
        raise e

def get_daily_average_power(db_conn, date_str):
    """Beräknar genomsnittlig effekt (kW) för hela dygnet."""
    try:
        # Konvertera datum
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        start_ts = int(target_date.timestamp() * 1000)
        end_ts = int((target_date + timedelta(days=1)).timestamp() * 1000)

        MAX_POWER_KW = 37.0

        with db_conn.cursor() as cursor:
            # Här behöver vi ingen GROUP BY, vi vill bara ha ett snitt för allt
            query = """
                SELECT AVG(value) AS daily_avg
                FROM public.variable_log_float
                WHERE id_var = 630
                AND date >= %s
                AND date < %s;
            """
            cursor.execute(query, (start_ts, end_ts))
            result = cursor.fetchone()

        # Om det inte finns data för dagen
        if not result or result['daily_avg'] is None:
            return {"date": date_str, "avg_power_kW": 0.0}

        # Räkna om % till kW
        avg_percent = float(result['daily_avg'])
        avg_power_kw = MAX_POWER_KW * (avg_percent / 100.0)

        return {
            "date": date_str, 
            "avg_power_kW": round(avg_power_kw, 2)
        }

    except Exception as e:
        print(f"Error in get_daily_average_power: {e}")
        raise e