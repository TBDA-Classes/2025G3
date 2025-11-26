"""
Alarm Extraction, Parsing and Visualization.

This module retrieves alarm messages stored in PostgreSQL under
`variable_log_string`, parses them into structured fields, performs
a summary analysis, and plots a timeline of alarm categories for a
selected day.

The alarms are stored as serialized Python lists inside a string field,
e.g.:
    [[50332149, "EMERGENCIA EXTERNA", 3, 3],
     [50332205, "Puerta abierta", 2, 4]]

This module extracts each alarm, expands them, and builds a
detail dataframe with fields such as:
- alarm_code
- alarm_msg
- alarm_plc
- alarm_line

Functions
---------
load_db_config :
    Load database connection settings from config.yaml.
create_engine_from_config :
    Create SQLAlchemy engine from configuration dictionary.
convert_timestamp_to_epoch_ms :
    Convert human-readable timestamps to epoch milliseconds.
fetch_alarm_raw :
    Load raw alarm string messages for a given day.
parse_alarm_entries :
    Convert serialized alarm lists into structured fields.
summarize_alarms :
    Generate a summary table of alarm occurrences.
plot_alarm_timeline :
    Visualize alarm categories over time.
"""

import ast
import yaml
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text


def load_db_config(path: str = "config.yaml") -> dict:
    """
    Load database connection parameters from a YAML file.

    Parameters
    ----------
    path : str, optional
        Path to the YAML config file (default: "config.yaml").

    Returns
    -------
    dict
        Dictionary containing database parameters.
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)["database"]


def create_engine_from_config(db_config: dict):
    """
    Create an SQLAlchemy engine using database configuration.

    Parameters
    ----------
    db_config : dict
        Must contain keys `user`, `password`, `host`, `port`, `dbname`.

    Returns
    -------
    sqlalchemy.Engine
        Database engine ready for querying.
    """
    return create_engine(
        f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    )



def convert_timestamp_to_epoch_ms(engine, timestamp: str) -> int:
    """
    Convert a timestamp (YYYY-MM-DD HH:MM:SS) to epoch milliseconds.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        SQLAlchemy engine.
    timestamp : str
        Timestamp to convert.

    Returns
    -------
    int
        Epoch milliseconds.
    """
    query = text("SELECT extract(epoch FROM timestamp :t) AS s")
    with engine.connect() as conn:
        return int(conn.execute(query, {"t": timestamp}).scalar() * 1000)



def fetch_alarm_raw(engine, start_ms: int, end_ms: int) -> pd.DataFrame:
    """
    Retrieve raw alarm string messages stored in variable_log_string.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        Database connection engine.
    start_ms : int
        Start timestamp in epoch ms.
    end_ms : int
        End timestamp in epoch ms.

    Returns
    -------
    pandas.DataFrame
        Dataframe with columns:
        - real_date
        - value (string containing list of alarms)
    """
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
        df = pd.read_sql(query, conn, params={"start_ms": start_ms, "end_ms": end_ms})

    return df


def parse_alarm_entries(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Parse serialized alarm lists into a structured dataframe.

    Parameters
    ----------
    df_raw : pandas.DataFrame
        Dataframe with raw alarm strings.

    Returns
    -------
    pandas.DataFrame
        Expanded dataframe where each alarm has:
        - real_date
        - alarm_code
        - alarm_msg
        - alarm_plc
        - alarm_line
    """

    df = df_raw.copy()
    df["value"] = df["value"].fillna("[]")

    # Convert string → list
    df["parsed"] = df["value"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith("[") else []
    )

    # Explode each alarm
    df_exploded = df.explode("parsed").dropna(subset=["parsed"])

    def extract_fields(item):
        if not isinstance(item, list) or len(item) < 4:
            return pd.Series({
                "alarm_code": None,
                "alarm_msg": None,
                "alarm_plc": None,
                "alarm_line": None
            })
        return pd.Series({
            "alarm_code": item[0],
            "alarm_msg": item[1],
            "alarm_plc": item[2],
            "alarm_line": item[3]
        })

    df_details = df_exploded.join(df_exploded["parsed"].apply(extract_fields))

    return df_details



def summarize_alarms(df_details: pd.DataFrame) -> pd.DataFrame:
    """
    Count alarm occurrences and return a summary sorted table.

    Parameters
    ----------
    df_details : pandas.DataFrame
        Detailed parsed alarm dataframe.

    Returns
    -------
    pandas.DataFrame
        Summary table with:
        - alarm_code
        - alarm_msg
        - occurrences
    """
    if df_details.empty:
        return pd.DataFrame()

    return (
        df_details.groupby(["alarm_code", "alarm_msg"])
        .size()
        .reset_index(name="occurrences")
        .sort_values("occurrences", ascending=False)
    )



def plot_alarm_timeline(df_details: pd.DataFrame) -> None:
    """
    Plot alarms timeline per alarm category.

    Parameters
    ----------
    df_details : pandas.DataFrame
        Dataframe with parsed alarm fields.

    Returns
    -------
    None
        Displays a Matplotlib figure.
    """

    if df_details.empty:
        print("No alarm detected this day.")
        return

    df_details = df_details.copy()
    df_details["alarm_category_id"], categories = pd.factorize(
        df_details["alarm_msg"], sort=True
    )

    plt.figure(figsize=(15, 6))
    plt.scatter(df_details["real_date"], df_details["alarm_category_id"], s=30)

    plt.yticks(range(len(categories)), categories)
    plt.title("Alarms timeline per category")
    plt.xlabel("Time")
    plt.ylabel("Alarm category")
    plt.grid(True, linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    date_jour = "2020-12-29"
    start_ts = f"{date_jour} 00:00:00"
    end_ts = f"{date_jour} 23:59:59"

    db_config = load_db_config()
    engine = create_engine_from_config(db_config)

    start_ms = convert_timestamp_to_epoch_ms(engine, start_ts)
    end_ms = convert_timestamp_to_epoch_ms(engine, end_ts)

    # 1. Load raw alarms
    df_raw = fetch_alarm_raw(engine, start_ms, end_ms)

    if df_raw.empty:
        print("No alarm messages for this day.")
        exit()

    # 2. Parse alarm list
    df_details = parse_alarm_entries(df_raw)

    # 3. Summary
    df_summary = summarize_alarms(df_details)
    #print("ALARMS SUMMARY TABLE")
    #print(df_summary)

    # 4. Plot
    plot_alarm_timeline(df_details)
