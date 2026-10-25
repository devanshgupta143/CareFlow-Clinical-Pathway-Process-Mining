import pandas as pd
import pm4py
import os

def load_event_log(filepath):
    """
    Loads and standardizes the clinical event log.
    Handles .xes files (real dataset) and .csv files (dummy data).
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found at {filepath}")
    
    print(f"Loading data from {filepath}...")
    
    # Check if the file is a .xes file (the real Sepsis dataset)
    if filepath.endswith('.xes') or filepath.endswith('.xes.gz'):
        print("Detected XES format. Reading with PM4Py...")
        # PM4Py reads XES files into an EventLog object, then converts to DataFrame
        event_log = pm4py.read_xes(filepath)
        df = pm4py.convert_to_dataframe(event_log)
        
        # Ensure standard column names (PM4Py usually handles this, but just in case)
        rename_map = {
            'case:concept:name': 'case:concept:name',
            'concept:name': 'concept:name',
            'time:timestamp': 'time:timestamp'
        }
        df = df.rename(columns=rename_map)
        
    else:
        # Fallback for CSV files (our dummy dataset)
        print("Detected CSV format. Reading with Pandas...")
        df = pd.read_csv(filepath)
        
        # Check if this is the real Sepsis dataset in CSV format
        if 'Case ID' in df.columns:
            rename_map = {
                'Case ID': 'case:concept:name',
                'Activity': 'concept:name',
                'Timestamp': 'time:timestamp'
            }
            df = df.rename(columns=rename_map)
        else:
            # Fallback for our dummy dataset
            rename_map = {
                'PatientID': 'case:concept:name',
                'Action': 'concept:name',
                'Time': 'time:timestamp'
            }
            df = df.rename(columns=rename_map)
    
    # Ensure timestamp is datetime format
    if 'time:timestamp' in df.columns:
        df['time:timestamp'] = pd.to_datetime(df['time:timestamp'])
    
    # Drop rows with missing critical data
    df = df.dropna(subset=['case:concept:name', 'concept:name', 'time:timestamp'])
    
    print(f"Data loaded successfully. {len(df)} events found for {df['case:concept:name'].nunique()} patients.")
    return df