from datetime import date, timedelta
import pandas as pd # Make sure pandas is imported in utils.py if not already
from pandas import Timestamp # Add this import

def get_at_risk_merchants(df):
    # Ensure 'date' column is datetime, though you already do this in routes.py
    # df['date'] = pd.to_datetime(df['date']) # This line might not be needed if df['date'] is already datetime64[ns] from routes.py

    today = date.today()

    # Convert the date object to a Pandas Timestamp for proper comparison
    # This is the key change
    thirty_days_ago = Timestamp(today - timedelta(days=30))

    at_risk_merchants = []
    # Assuming 'merchant_id' is the column that uniquely identifies merchants
    for merchant_id in df['merchant_id'].unique():
        sub = df[df['merchant_id'] == merchant_id]

        # Use the Timestamp object for comparison
        recent = sub[sub['date'] > thirty_days_ago]['volume'].sum()
        total = sub['volume'].sum()

        if total > 0: # Avoid division by zero
            retention_rate = (recent / total) * 100
        else:
            retention_rate = 0 # Or handle as appropriate

        if retention_rate < 50: # Example threshold
            at_risk_merchants.append({
                'id': merchant_id,
                'retention_rate': round(retention_rate, 2)
            })

    # Calculate overall retention rate for the entire dataset
    # This part might also need a similar date conversion if 'today' is used
    total_volume_overall = df['volume'].sum()
    if total_volume_overall > 0:
        overall_recent_volume = df[df['date'] > thirty_days_ago]['volume'].sum()
        overall_retention_rate = (overall_recent_volume / total_volume_overall) * 100
    else:
        overall_retention_rate = 0

    return at_risk_merchants, round(overall_retention_rate, 2)
