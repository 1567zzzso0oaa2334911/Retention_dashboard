from flask import Blueprint, render_template
import pandas as pd
from datetime import date, timedelta
from .utils import get_at_risk_merchants

main = Blueprint('main', __name__)

@main.route("/")
def dashboard():
    df = pd.read_csv("data/transactions.csv", parse_dates=['date'])
    risk_merchants, retention_rate = get_at_risk_merchants(df)
    return render_template("dashboard.html", risks=risk_merchants, retention=retention_rate)
