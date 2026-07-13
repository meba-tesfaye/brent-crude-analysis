import os
import json
import pandas as pd
from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Resolve structural file paths relative to this module
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "raw_brent_prices.csv")
METRICS_PATH = os.path.join(BASE_DIR, "data", "model_output.json")

def load_prices():
    if not os.path.exists(DATA_PATH):
        return []
    df = pd.read_csv(DATA_PATH)
    # Ensure standard sorting by date
    df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    df = df.sort_values('Date')
    # Resample weekly or monthly if chart rendering lags, or pass raw values
    return df.to_dict(orient='records')

@app.route('/')
def index():
    """Renders the main dashboard interface UI HTML page."""
    return render_template('dashboard.html')

@app.route('/api/metrics')
def get_metrics():
    """API endpoint delivering Task 2 Bayesian inference parameters."""
    if not os.path.exists(METRICS_PATH):
        return jsonify({"error": "Model execution outputs not found"}), 404
    with open(METRICS_PATH, 'r') as f:
        metrics = json.load(f)
    return jsonify(metrics)

@app.route('/api/prices')
def get_prices():
    """API endpoint delivering timeseries historical dates and actual prices."""
    try:
        data = load_prices()
        # Formatting dates for clean frontend presentation
        formatted_data = [
            {"date": pd.to_datetime(row["Date"]).strftime("%Y-%m-%d"), "price": float(row["Price"])}
            for row in data
        ]
        return jsonify(formatted_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Interactive Analytical Dashboard server...")
    app.run(debug=True, port=5000)