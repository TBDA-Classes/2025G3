"""
Motor Utilization Data Extraction and Plotting.

This module connects to a PostgreSQL database, retrieves motor utilization
time-series data for selected axes, and generates a scatter plot showing
their usage over a given day.

Functions
---------
load_db_config :
    Load database connection parameters from a YAML file.
create_engine_from_config :
    Create an SQLAlchemy engine from configuration.
convert_timestamp_to_epoch_ms :
    Convert a timestamp string to epoch milliseconds using SQL.
fetch_motor_utilization :
    Retrieve motor utilization data for a list of variable IDs.
plot_motor_utilization :
    Generate a scatter plot of motor utilization by axis.
"""

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
import yaml

def load_db_config(path: str = "config.yaml") -> dict:
    """
    Load the database configuration from a YAML file.

    Parameters
    ----------
    path : str, optional
        Path to the YAML configuration file (default: "config.yaml").

    Returns
    -------
    dict
        Database configuration, including host, port, database name,
        user and password.

    Raises
    ------
    FileNotFoundError
        If the config file does not exist.
    yaml.YAMLError
        If an error occurs when parsing the YAML.
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)["database"]


def create_engine_from_config(db_config: dict):
    """
    Create a SQLAlchemy engine from the database configuration.

    Parameters
    ----------
    db_config : dict
        Dictionary with the fields `user`, `password`, `host`, `port`, `dbname`.

    Returns
    -------
    sqlalchemy.Engine
        A database engine ready for queries.
    """
    return create_engine(
        f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    )

def convert_timestamp_to_epoch_ms(engine, timestamp: str) -> int:
    """
    Convert a timestamp string to epoch milliseconds using PostgreSQL.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        Active database connection engine.
    timestamp : str
        Timestamp in the format "YYYY-MM-DD HH:MM:SS".

    Returns
    -------
    int
        Epoch time in milliseconds.
    """
    epoch_query = text("SELECT extract(epoch FROM timestamp :t) AS s")
    with engine.connect() as conn:
        return int(conn.execute(epoch_query, {"t": timestamp}).scalar() * 1000)


def fetch_motor_utilization(engine, var_ids, var_names, start_ms, end_ms):
    """
    Retrieve motor utilization for a list of variable IDs.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        Active database connection engine.
    var_ids : list of int
        Variable IDs corresponding to motor utilization axes.
    var_names : dict
        Mapping {id_var: name}.
    start_ms : int
        Start timestamp (epoch ms).
    end_ms : int
        End timestamp (epoch ms).

    Returns
    -------
    pandas.DataFrame
        Combined dataframe with columns:
        - real_date
        - value
        - id_var
        - name
    """
    dfs = []

    for vid in var_ids:
        query = text("""
            SELECT to_timestamp(date/1000) AS real_date, value
            FROM public.variable_log_float
            WHERE id_var = :vid
              AND date BETWEEN :start_ms AND :end_ms
            ORDER BY date;
        """)
        with engine.connect() as conn:
            df = pd.read_sql(query, conn,
                             params={"vid": vid, "start_ms": start_ms, "end_ms": end_ms})

        if not df.empty:
            df["id_var"] = vid
            df["name"] = var_names[vid]
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            dfs.append(df)

    if dfs:
        return pd.concat(dfs, ignore_index=True)

    return pd.DataFrame()


def plot_motor_utilization(df, var_ids, var_names, date_day):
    """
    Plot motor utilization time series for each axis.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe returned by `fetch_motor_utilization`.
    var_ids : list of int
        Ordered list of axis variable IDs.
    var_names : dict
        Mapping of variable ID to descriptive label.
    date_day : str
        The date being plotted (format YYYY-MM-DD).

    Returns
    -------
    None
        Displays a Matplotlib figure.
    """
    plt.figure(figsize=(14, 5))

    for vid in var_ids:
        subset = df[df["id_var"] == vid]
        if not subset.empty:
            plt.scatter(subset["real_date"], subset["value"], s=10, label=var_names[vid])

    plt.title(f"Motor Utilization by Axis (%) — {date_day}")
    plt.xlabel("Time of Day")
    plt.ylabel("Motor Utilization (%)")
    plt.legend()
    plt.tight_layout()
    plt.show()
    

if __name__ == "__main__":
    # Load config & engine
    db_config = load_db_config()
    engine = create_engine_from_config(db_config)

    # Parameters
    date_day = "2021-01-12"
    start_ts = f"{date_day} 00:00:00"
    end_ts = f"{date_day} 23:59:59"

    # Variable IDs
    motor_ids = [584, 593, 598, 565, 514]
    names = {
        584: "Axis_8_Motor_Utilization",
        593: "Axis_7_Motor_Utilization",
        598: "Axis_6_Motor_Utilization",
        565: "Axis_5_Motor_Utilization",
        514: "Axis_4_Motor_Utilization"
    }

    # Convert timestamps
    start_ms = convert_timestamp_to_epoch_ms(engine, start_ts)
    end_ms = convert_timestamp_to_epoch_ms(engine, end_ts)

    # Fetch data
    df_all = fetch_motor_utilization(engine, motor_ids, names, start_ms, end_ms)

    if df_all.empty:
        print("No data retrieved for this day.")
    else:
        plot_motor_utilization(df_all, motor_ids, names, date_day)

