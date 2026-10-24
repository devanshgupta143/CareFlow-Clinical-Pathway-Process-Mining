import pandas as pd
from datetime import datetime

def test_timestamp_anomalies():
    print("--- Running Timestamp Anomaly Test Suite ---")
    df = pd.read_csv('mock_hospital_logs.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Check for future dates
    current_time = pd.Timestamp.now()
    future_dates = (df['Timestamp'] > current_time).sum()
    
    print(f"Future-dated event records found: {future_dates}")
    assert future_dates == 0, "Data Quality Error: Future-dated timestamps detected!"
    print("Timestamp Anomaly Check Passed: All event times are valid.")

if __name__ == "__main__":
    test_timestamp_anomalies()
