from flask import Blueprint, render_template
import pandas as pd
from datetime import date, timedelta
from .utils import get_at_risk_merchants
import os # Import the os module

main = Blueprint('main', __name__)

@main.route("/")
def dashboard():
    # Get the directory where the current script (routes.py) is located
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the data file relative to the project root
    # Go up one directory from 'app' to 'retention_dashboard', then into 'data'
    data_file_path = os.path.join(current_dir, '..', 'data', 'transactions.csv')

    df = pd.read_csv(data_file_path, parse_dates=['date'])
    risk_merchants, retention_rate = get_at_risk_merchants(df)
    return render_template("dashboard.html", risks=risk_merchants, retention=retention_rate)
