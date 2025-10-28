from database import get_connection
import csv
from datetime import datetime
from psycopg2 import sql


# Function to query by ID(s)

def get_run(db_conn, table: str, id_list: list, limit: int = 100, newest_first: bool = True):
    """
    Fetch rows from public.variable_log_[table] for specific variable IDs,
    sorted by id_var and timestamp.
    """
    try:
        cursor = db_conn.cursor()

        # Choose timestamp expression:
        # If your 'date' values are UNIX milliseconds (most common) use /1000.0
        # If they are UNIX seconds, change to: to_timestamp("date")
        ts_expr = sql.SQL('to_timestamp("date"/1000.0)')

        order_dir = sql.SQL("DESC") if newest_first else sql.SQL("ASC")

        query = sql.SQL("""
            SELECT
                "id_var",
                {ts} AS real_date,
                "value"
            FROM {schema}.{table}
            WHERE "id_var" = ANY(%s)
            ORDER BY "id_var" ASC, real_date {order_dir}
            LIMIT %s
        """).format(
            ts=ts_expr,
            schema=sql.Identifier("public"),
            table=sql.Identifier(f"variable_log_{table}"),
            order_dir=order_dir
        )

        cursor.execute(query, (id_list, limit))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    except Exception as e:
        print("Error in get_run:", e)
        return []


# Helper: Write results to CSV

def write_to_csv(rows, filename):
    if not rows:
        print(f"No data to save for {filename}")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows to '{filename}'")


# Main script

try:
    conn = get_connection()
    print("Connected to database.")

    # Example: fetch multiple IDs from each table
    float_ids = [828,829]
    string_ids = []

    # newest_first=True → sort by descending date within each ID
    float_rows = get_run(conn, "float", float_ids, limit=500, newest_first=True)
    string_rows = get_run(conn, "string", string_ids, limit=200, newest_first=True)

    print(f"Float rows retrieved: {len(float_rows)}")
    print(f"String rows retrieved: {len(string_rows)}")

    # Save to timestamped CSV files
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    write_to_csv(float_rows, f"float_data_{timestamp}.csv")
    write_to_csv(string_rows, f"string_data_{timestamp}.csv")

except Exception as e:
    print("An error occurred:", e)

finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")
