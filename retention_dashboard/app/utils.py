from datetime import date, timedelta

def get_at_risk_merchants(df):
    today = date.today()
    risk = []
    retained = 0
    total = df['merchant_id'].nunique()

    for merchant in df['merchant_id'].unique():
        sub = df[df['merchant_id'] == merchant]
        last_txn = sub['date'].max().date()
        recent = sub[sub['date'] > today - timedelta(days=30)]['volume'].sum()
        past = sub[(sub['date'] <= today - timedelta(days=30)) &
                   (sub['date'] > today - timedelta(days=60))]['volume'].sum()
        
        if (today - last_txn).days > 30 or (past > 0 and recent / past < 0.6):
            risk.append({
                'merchant_id': merchant,
                'last_txn': str(last_txn),
                'drop_pct': round(100 * (1 - recent / past), 1) if past > 0 else "N/A"
            })
        else:
            retained += 1

    retention_rate = round((retained / total) * 100, 1)
    return risk, retention_rate
