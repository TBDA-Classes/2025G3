import pandas as pd
import ast
from sqlalchemy import text
import matplotlib.pyplot as plt

#create engine for connection to the database

## Parameters ##
date_jour = "2020-12-29"
start_ts = f"{date_jour} 00:00:00"
end_ts   = f"{date_jour} 23:59:59"

# Conversion of timestamps → epoch ms
epoch_query = text("SELECT extract(epoch FROM timestamp :t) AS s")

with engine.connect() as conn:
    start_ms = int(conn.execute(epoch_query, {"t": start_ts}).scalar() * 1000)
    end_ms = int(conn.execute(epoch_query, {"t": end_ts}).scalar() * 1000)

query = text("""
    SELECT 
        to_timestamp(date/1000) AS real_date,
        value
    FROM public.variable_log_string
    WHERE id_var = 447
      AND date BETWEEN :start_ms AND :end_ms
    ORDER BY date;
""")

with engine.connect() as conn:
    df_alarm_raw = pd.read_sql(query, conn, params={"start_ms": start_ms, "end_ms": end_ms})

if df_alarm_raw.empty:
    print("No alarm messages for this day.")
else:
    print(f"Loaded {len(df_alarm_raw)} rows.")

#Cleaning
df_alarm_raw["value"] = df_alarm_raw["value"].fillna("[]")

# Conversion to python list
df_alarm_raw["parsed"] = df_alarm_raw["value"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else []
)

df_exploded = df_alarm_raw.explode("parsed")
df_exploded = df_exploded.dropna(subset=["parsed"])

def extract_alarm_fields(item):
    if not isinstance(item, list) or len(item) < 4:
        return pd.Series({"alarm_code": None, "alarm_msg": None, "alarm_plc": None, "alarm_line": None})
    return pd.Series({
        "alarm_code": item[0],
        "alarm_msg": item[1],
        "alarm_plc": item[2],
        "alarm_line": item[3]
    })

df_details = df_exploded.join(df_exploded["parsed"].apply(extract_alarm_fields))
# Example of data contained in df_detailed
#real_date     : 2020-12-29 05:29:16+00:00
#value         : [[50332149,"EMERGENCIA EXTERNA",3,3], [50332205,"Puerta abierta",2,4]] #original message as there are usually multiple alarms at the same time
#parsed        : [50332149,"EMERGENCIA EXTERNA",3,3]
#alarm_msg     : EMERGENCIA EXTERNA
#alarm_code    : 50332149
#alarm_plc     : 3
#alarm_line    : 3

df_summary = (
    df_details.groupby(["alarm_code", "alarm_msg"])
    .size()
    .reset_index(name="occurrences")
    .sort_values("occurrences", ascending=False)
)

print("\n=== ALARMS SUMMARY TABLE ===")


## Prints alarm timeline per category of alarm for the selected day

if df_details.empty:
    print("No alarm detected this day.")
else:
    df_details["alarm_category_id"], categories = pd.factorize(df_details["alarm_msg"], sort=True)

    plt.figure(figsize=(15, 6))

    # Scatter plot
    plt.scatter(
        df_details["real_date"],
        df_details["alarm_category_id"],
        s=30
    )

    plt.yticks(range(len(categories)), categories)
    plt.title("Alarms timeline per category")
    plt.xlabel("Time")
    plt.ylabel("Alarm category")
    plt.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()
#print(df_summary)