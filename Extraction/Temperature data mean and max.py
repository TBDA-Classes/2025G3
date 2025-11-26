import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
import yaml

# --- Database connection ---
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

db = config["database"]

engine = create_engine(
    f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['dbname']}"
)

# --- Parameters ---
date_day = "2021-01-12"
start_ts = f"{date_day} 00:00:00"
end_ts   = f"{date_day} 23:59:59"

temp_ids = [449, 453, 456, 448, 454]
names = {
    449: "TEMPERATURA_MOTOR_8",
    453: "TEMPERATURA_MOTOR_7",
    456: "TEMPERATURA_MOTOR_6",
    448: "TEMPERATURA_MOTOR_5",
    454: "TEMPERATURA_MOTOR_4"
}

# --- Convert timestamps to epoch (ms) ---
epoch_query = text("SELECT extract(epoch FROM timestamp :t) AS s")
with engine.connect() as conn:
    start_ms = int(conn.execute(epoch_query, {"t": start_ts}).scalar() * 1000)
    end_ms   = int(conn.execute(epoch_query, {"t": end_ts}).scalar() * 1000)

dfs = []

# --- Fetch data for each variable ---
for vid in temp_ids:
    q = text("""
        SELECT to_timestamp(date/1000) AS real_date, value
        FROM public.variable_log_float
        WHERE id_var = :vid
          AND date BETWEEN :start_ms AND :end_ms
        ORDER BY date;
    """)
    with engine.connect() as conn:
        df = pd.read_sql(q, conn, params={"vid": vid, "start_ms": start_ms, "end_ms": end_ms})
    
    if not df.empty:
        df["id_var"] = vid
        df["name"] = names[vid]
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df.set_index("real_date", inplace=True)  # Important pour resample
        dfs.append(df)
    else:
        print(f"No data found for {names[vid]}")

# --- Combine and resample every 30 minutes ---
if not dfs:
    print("No data retrieved for this day.")
else:
    df_all = pd.concat(dfs)

    plt.figure(figsize=(14, 6))

    for vid in temp_ids:
        sub = df_all[df_all["id_var"] == vid]
        if not sub.empty:
            # Resample toutes les 30 minutes
            resampled = sub["value"].resample("30T").agg(["mean", "max"])
            
            plt.scatter(resampled.index, resampled["mean"], label=f"{names[vid]} - mean", linewidth=2)
            plt.scatter(resampled.index, resampled["max"], label=f"{names[vid]} - max", linestyle="--", linewidth=1.5)

    plt.title(f"Motor Axis Temperatures — {date_day} (30-min average & max)")
    plt.xlabel("Time of Day")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()