"""
Temperature Analysis Module
===========================

This module retrieves motor temperature data from a PostgreSQL database,
resamples the measurements into 30-minute intervals, and generates a plot
showing the mean and maximum temperature per motor axis.

The script is designed for industrial machine monitoring and batch analysis
of historical sensor data.

Functions
---------
- load_config : Load YAML configuration file (database credentials).
- create_db_engine : Build SQLAlchemy engine from configuration data.
- convert_timestamp_to_epoch_ms : Convert PostgreSQL timestamp to epoch (ms).
- fetch_temperature_data : Retrieve raw temperature logs for a list of variables.
- resample_temperature_data : Resample temperature signals (mean & max) every 30 minutes.
- plot_temperature_resampled : Plot the resulting resampled temperature curves.
"""

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine, text
import yaml


def load_config(path: str) -> dict:
    """
    Load YAML configuration file.

    Parameters
    ----------
    path : str
        Path to the YAML configuration file.

    Returns
    -------
    dict
        Parsed YAML content containing database credentials.
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)


def create_db_engine(cfg: dict):
    """
    Create a SQLAlchemy engine using database credentials from the config.

    Parameters
    ----------
    cfg : dict
        Dictionary containing database connection information.

    Returns
    -------
    sqlalchemy.Engine
        SQLAlchemy engine ready for queries.
    """
    db = cfg["database"]
    return create_engine(
        f"postgresql+psycopg2://{db['user']}:{db['password']}@"
        f"{db['host']}:{db['port']}/{db['dbname']}"
    )


def convert_timestamp_to_epoch_ms(engine, timestamp: str) -> int:
    """
    Convert a PostgreSQL timestamp string to epoch milliseconds.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        SQLAlchemy engine connected to the database.
    timestamp : str
        Timestamp in format 'YYYY-MM-DD HH:MM:SS'.

    Returns
    -------
    int
        Timestamp converted to epoch time in milliseconds.
    """
    epoch_query = text("SELECT extract(epoch FROM timestamp :t) AS s")
    with engine.connect() as conn:
        seconds = conn.execute(epoch_query, {"t": timestamp}).scalar()
    return int(seconds * 1000)


def fetch_temperature_data(engine, var_ids: list, names: dict,
                           start_ms: int, end_ms: int) -> pd.DataFrame:
    """
    Retrieve motor temperature logs for a list of variables.

    Parameters
    ----------
    engine : sqlalchemy.Engine
        SQLAlchemy connection engine.
    var_ids : list of int
        List of variable IDs to retrieve.
    names : dict
        Mapping from variable ID to human-readable label.
    start_ms : int
        Start timestamp in epoch milliseconds.
    end_ms : int
        End timestamp in epoch milliseconds.

    Returns
    -------
    pandas.DataFrame
        Combined dataframe containing:
        - real_date (datetime)
        - value (float)
        - id_var
        - name
    """
    dfs = []
    query = text("""
        SELECT to_timestamp(date/1000) AS real_date, value
        FROM public.variable_log_float
        WHERE id_var = :vid
          AND date BETWEEN :start_ms AND :end_ms
        ORDER BY date;
    """)

    for vid in var_ids:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params={"vid": vid,
                                                  "start_ms": start_ms,
                                                  "end_ms": end_ms})
        if df.empty:
            print(f"No data found for {names[vid]}")
            continue

        df["id_var"] = vid
        df["name"] = names[vid]
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df.set_index("real_date", inplace=True)

        dfs.append(df)

    return pd.concat(dfs) if dfs else pd.DataFrame()


def resample_temperature_data(df: pd.DataFrame, freq: str = "30T") -> dict:
    """
    Resample each temperature signal to compute mean and max values.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw temperature log data indexed by datetime.
    freq : str, optional
        Resampling frequency (default "30T" = 30 minutes).

    Returns
    -------
    dict
        Mapping: variable ID → resampled DataFrame (mean & max).
    """
    results = {}
    for vid in df["id_var"].unique():
        sub = df[df["id_var"] == vid]
        resampled = sub["value"].resample(freq).agg(["mean", "max"])
        results[vid] = resampled
    return results


def plot_temperature_resampled(resampled_dict: dict, names: dict, date_day: str):
    """
    Plot mean and max temperature curves for each motor axis.

    Parameters
    ----------
    resampled_dict : dict
        Mapping variable ID → resampled temperature DataFrame.
    names : dict
        Mapping variable ID → descriptive name.
    date_day : str
        Day of analysis (YYYY-MM-DD).
    """
    plt.figure(figsize=(14, 6))

    for vid, df_res in resampled_dict.items():
        plt.scatter(df_res.index, df_res["mean"],
                    label=f"{names[vid]} - mean")
        plt.scatter(df_res.index, df_res["max"],
                    label=f"{names[vid]} - max")

    plt.title(f"Motor Axis Temperatures — {date_day} (30-min average & max)")
    plt.xlabel("Time of Day")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def main():
    """
    Full workflow:
    1. Load config
    2. Connect to DB
    3. Compute timestamps
    4. Retrieve & resample temperature data
    5. Plot results
    """
    cfg = load_config("config.yaml")
    engine = create_db_engine(cfg)

    date_day = "2021-01-12"
    start_ms = convert_timestamp_to_epoch_ms(engine, f"{date_day} 00:00:00")
    end_ms = convert_timestamp_to_epoch_ms(engine, f"{date_day} 23:59:59")

    temp_ids = [449, 453, 456, 448, 454]
    names = {
        449: "TEMPERATURA_MOTOR_8",
        453: "TEMPERATURA_MOTOR_7",
        456: "TEMPERATURA_MOTOR_6",
        448: "TEMPERATURA_MOTOR_5",
        454: "TEMPERATURA_MOTOR_4",
    }

    df = fetch_temperature_data(engine, temp_ids, names, start_ms, end_ms)
    if df.empty:
        print("No data retrieved for this day.")
        return

    resampled = resample_temperature_data(df)
    plot_temperature_resampled(resampled, names, date_day)


if __name__ == "__main__":
    main()
