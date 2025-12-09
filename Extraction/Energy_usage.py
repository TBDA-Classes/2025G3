import pandas as pd
from sqlalchemy import create_engine, text
import yaml

# ---------------------------------------------------------
# 1. Load database config
# ---------------------------------------------------------
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

db = config["database"]

engine = create_engine(
    f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['dbname']}"
)

# ---------------------------------------------------------
# 2. Parameters
# ---------------------------------------------------------
date_day = "2021-01-12"
start_ts = f"{date_day} 00:00:00"
end_ts = f"{date_day} 23:59:59"

temp_ids = [630]
names = {
    630: "MANDRINO_CONSUMO_VISUALIZADO",
}

MAX_POWER_KW = 37.0

# ---------------------------------------------------------
# 3. Convert timestamps to epoch ms
# ---------------------------------------------------------
epoch_query = text("SELECT extract(epoch FROM timestamp :t) AS s")
with engine.connect() as conn:
    start_ms = int(conn.execute(epoch_query, {"t": start_ts}).scalar() * 1000)
    end_ms = int(conn.execute(epoch_query, {"t": end_ts}).scalar() * 1000)

# ---------------------------------------------------------
# 4. Fetch data
# ---------------------------------------------------------
dfs = []

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
        dfs.append(df)

# ---------------------------------------------------------
# 5. If no data stop
# ---------------------------------------------------------
if not dfs:
    print("No data retrieved for this day.")
    raise SystemExit

df_all = pd.concat(dfs, ignore_index=True)

# ---------------------------------------------------------
# 6. Power & Energy calculation
# ---------------------------------------------------------
df = df_all[["real_date", "value"]].copy()

# Convert % spindle load to kW
df["power_kW"] = MAX_POWER_KW * (df["value"] / 100.0)

# Sort by time
df = df.sort_values("real_date")

# Compute segment end times (step signal)
df["t_end"] = df["real_date"].shift(-1)
df.loc[df["t_end"].isna(), "t_end"] = df["real_date"].iloc[-1]

# Duration in hours
df["duration_h"] = (df["t_end"] - df["real_date"]).dt.total_seconds() / 3600.0

# Energy per segment
df["energy_kWh"] = df["power_kW"] * df["duration_h"]

# ---------------------------------------------------------
# 7. Hourly average power
# ---------------------------------------------------------
df["real_date"] = pd.to_datetime(df["real_date"])
df = df.set_index("real_date")

df_hourly = df["power_kW"].resample("1H").mean().reset_index()

# ---------------------------------------------------------
# 8. Print only hourly averages
# ---------------------------------------------------------
print(df_hourly)
