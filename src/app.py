import os
import json
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)

# Apply global CORS rule transformations to permit frontend data cross-fetching
@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET"
    return response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw_brent_prices.csv")
EVENTS_PATH = os.path.join(BASE_DIR, "data", "significant_events.csv")
METRICS_PATH = os.path.join(BASE_DIR, "data", "model_output.json")

@app.route('/api/metrics')
def get_metrics():
    if not os.path.exists(METRICS_PATH):
        return jsonify({"error": "Model summary parameters missing"}), 404
    with open(METRICS_PATH, 'r') as f:
        return jsonify(json.load(f))

@app.route('/api/prices')
def get_prices():
    try:
        df = pd.read_csv(DATA_PATH)
        df['Date'] = pd.to_datetime(df['Date'], format='mixed')
        df = df.sort_values('Date')
        df_weekly = df.resample('W', on='Date').mean().reset_index()
        formatted_data = [
            {"date": row["Date"].strftime("%Y-%m-%d"), "price": float(row["Price"])}
            for _, row in df_weekly.iterrows()
        ]
        return jsonify(formatted_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/events')
def get_events():
    if not os.path.exists(EVENTS_PATH):
        return jsonify([])
    df = pd.read_csv(EVENTS_PATH)
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)