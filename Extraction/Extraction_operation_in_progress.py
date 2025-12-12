import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from sqlalchemy import create_engine, text
import yaml
import matplotlib.patches as mpatches

# -----------------------------
# 1. Load database config
# -----------------------------
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

db = config["database"]

engine = create_engine(
    f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['dbname']}"
)

# -----------------------------
# 2. Parameters
# -----------------------------
date_day = "2021-01-12"
start_ts = f"{date_day} 00:00:00"
end_ts   = f"{date_day} 23:59:59"

target_var = 597   # MACHINE_IN_OPERATION

# -----------------------------
# 3. Convert timestamps to epoch ms
# -----------------------------
epoch_query = text("SELECT extract(epoch FROM timestamp :t) AS s")
with engine.connect() as conn:
    start_ms = int(conn.execute(epoch_query, {"t": start_ts}).scalar() * 1000)
    end_ms   = int(conn.execute(epoch_query, {"t": end_ts}).scalar() * 1000)

# -----------------------------
# 4. Fetch raw data
# -----------------------------
q = text("""
    SELECT to_timestamp(date/1000) AS real_date, value
    FROM public.variable_log_float
    WHERE id_var = :vid
      AND date BETWEEN :start_ms AND :end_ms
    ORDER BY date;
""")

with engine.connect() as conn:
    df = pd.read_sql(q, conn, params={"vid": target_var, "start_ms": start_ms, "end_ms": end_ms})

if df.empty:
    print("No data found for ID 597.")
    raise SystemExit

df["value"] = pd.to_numeric(df["value"], errors="coerce")

# -----------------------------
# 5. Define state: ON / IDLE / OFF
# -----------------------------
# 2 = ON (>0), 1 = IDLE (=0), 0 = OFF / No Signal (NaN or missing)
def classify_state(val):
    if pd.isna(val):
        return 0   # OFF / No Signal → röd
    elif val == 0:
        return 1   # IDLE → gul
    else:  # val > 0
        return 2   # ON → grön

df["state"] = df["value"].apply(classify_state)

# -----------------------------
# 6. Build intervals for plotting
# -----------------------------
intervals = []
start_time = df["real_date"].iloc[0]
prev_state = df["state"].iloc[0]

for i in range(1, len(df)):
    current_time = df["real_date"].iloc[i]
    current_state = df["state"].iloc[i]

    if current_state != prev_state:
        intervals.append((start_time, current_time, prev_state))
        start_time = current_time
        prev_state = current_state

# -----------------------------
# NEW: Extend final segment to day end
# -----------------------------
day_end = pd.to_datetime(end_ts)
intervals.append((start_time, day_end, prev_state))


# Convert intervals to matplotlib float-date format
bar_data = []
colors = []

for start, end, state in intervals:
    start_num = mdates.date2num(start)
    duration = mdates.date2num(end) - start_num
    bar_data.append((start_num, duration))

    if state == 2:
        colors.append("tab:green")   # ON
    elif state == 1:
        colors.append("gold")        # IDLE
    else:
        colors.append("tab:red")     # OFF / no signal

# -----------------------------
# 7. Plot timeline
# -----------------------------
fig, ax = plt.subplots(figsize=(16, 3))

ax.broken_barh(bar_data, (0, 1), facecolors=colors, alpha=0.9)

# Time axis: 5-minute intervals
ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

ax.set_ylim(0, 1)
ax.set_yticks([])
ax.set_xlabel("Time of Day")
ax.set_title(f"Machine Operation Timeline — ID 597 — {date_day}", fontsize=15)

# Legend
legend_patches = [
    mpatches.Patch(color="tab:green", label="ON"),
    mpatches.Patch(color="gold", label="IDLE"),
    mpatches.Patch(color="tab:red", label="OFF / No Signal")
]
ax.legend(handles=legend_patches, loc="upper right")

plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()
print(df[['real_date', 'value', 'state']].to_string(index=False))
