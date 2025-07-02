# models/agent_brain.py

import pandas as pd
from prophet import Prophet
import datetime
import os

EMAIL_CSV = "email_times.csv"
PROPHET_MODEL_PATH = "prophet_model.pkl"

def prepare_prophet_data():
    if not os.path.isfile(EMAIL_CSV):
        #If No data, just return empty DataFrame
        return pd.DataFrame(columns=["ds", "y"])
    df = pd.read_csv(EMAIL_CSV, parse_dates=["received_datetime"])
    # Grouping by hour and emails count
    df_hourly = df.groupby(df["received_datetime"].dt.floor("h")).size().reset_index(name="y")
    df_hourly.rename(columns={"received_datetime": "ds"}, inplace=True)
    return df_hourly

def train_prophet_model(df_hourly):
    m = Prophet()
    if len(df_hourly) > 0:
        m.fit(df_hourly)
    return m

def predict_emails_next_hour(model):
    # Prediction for the next 2 hours
    now = pd.Timestamp.now().floor('H')
    future = pd.DataFrame({'ds': [now]})
    forecast = model.predict(future)
    yhat = forecast.loc[0, "yhat"]
    return yhat

def should_run_now(threshold=0.5):
    df_hourly = prepare_prophet_data()
    if df_hourly.empty:
        return True, "No email history yet; running by default."

    # Training Prophet model
    model = train_prophet_model(df_hourly)

    # Prediction for the current hour
    yhat = predict_emails_next_hour(model)
    if yhat > threshold:
        reason = f"Prophet predicts {yhat:.2f} emails this hour; running."
        return True, reason
    else:
        reason = f"Prophet predicts {yhat:.2f} emails this hour; skipping run."
        return False, reason

def log_run(emails_processed, rejections, offers):
    import json
    LOG_FILE = "agent_log.json"
    entry = {
        "run_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "emails_processed": emails_processed,
        "rejections": rejections,
        "offers": offers
    }
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    logs.append(entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
    

def get_next_best_time(min_gap_minutes=5):
    """
    Predicts the next hour in which significant email activity is expected,
    returns a datetime object of when the agent should next check.
    """
    df_hourly = prepare_prophet_data()
    now = pd.Timestamp.now().floor('h')
    if df_hourly.shape[0] < 2:
        return (now + pd.Timedelta(minutes=min_gap_minutes)).to_pydatetime()

    model = train_prophet_model(df_hourly)

    # Prediction for next 24 hours
    future_hours = [now + pd.Timedelta(hours=i) for i in range(1, 25)]
    future = pd.DataFrame({'ds': future_hours})
    forecast = model.predict(future)

    idx_max = forecast['yhat'].idxmax()
    next_best = forecast.loc[idx_max, 'ds']

    min_next = now + pd.Timedelta(minutes=min_gap_minutes)
    if next_best < min_next:
        next_best = min_next

    return pd.Timestamp(next_best).to_pydatetime()