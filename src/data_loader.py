import pandas as pd
import os

def load_event_log(filepath):
    """
    Loads and standardizes the clinical event log.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found at {filepath}")
    
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Standardize column names for Process Mining (PM4Py requirements)
    rename_map = {
        'PatientID': 'case:concept:name',
        'Action': 'concept:name',
        'Time': 'time:timestamp'
    }
    df = df.rename(columns=rename_map)
    
    # Ensure timestamp is datetime format
    df['time:timestamp'] = pd.to_datetime(df['time:timestamp'])
    
    # Drop rows with missing critical data
    df = df.dropna(subset=['case:concept:name', 'concept:name', 'time:timestamp'])
    
    print(f"Data loaded successfully. {len(df)} events found for {df['case:concept:name'].nunique()} patients.")
    return df