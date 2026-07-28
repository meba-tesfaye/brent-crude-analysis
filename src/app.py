import os
import json
import pandas as pd
from flask import Flask, render_template, jsonify

# Set up paths relative to the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
DATA_PATH = os.path.join(BASE_DIR, "data", "raw_brent_prices.csv")
METRICS_PATH = os.path.join(BASE_DIR, "data", "model_output.json")
EVENTS_PATH = os.path.join(BASE_DIR, "data", "events.csv") # or your events file path

app = Flask(__name__, template_folder=TEMPLATE_DIR)

# 1. Main Dashboard View Route (Fixes the 404 error!)
@app.route("/")
def index():
    return render_template("dashboard.html")

# 2. API Endpoints
@app.route("/api/metrics")
def get_metrics():
    if not os.path.exists(METRICS_PATH):
        return jsonify({"error": "Model summary parameters missing"}), 404
    with open(METRICS_PATH, "r") as f:
        return jsonify(json.load(f))

@app.route("/api/prices")
def get_prices():
    try:
        if not os.path.exists(DATA_PATH):
            return jsonify({"error": f"Data file missing at {DATA_PATH}"}), 404
            
        df = pd.read_csv(DATA_PATH)
        df["Date"] = pd.to_datetime(df["Date"], format="mixed")
        df = df.sort_values("Date")
        df_weekly = df.resample("W", on="Date").mean().reset_index()
        formatted_data = [
            {"date": row["Date"].strftime("%Y-%m-%d"), "price": float(row["Price"])}
            for _, row in df_weekly.iterrows()
        ]
        return jsonify(formatted_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/events")
def get_events():
    if not os.path.exists(EVENTS_PATH):
        return jsonify([])
    df = pd.read_csv(EVENTS_PATH)
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)

