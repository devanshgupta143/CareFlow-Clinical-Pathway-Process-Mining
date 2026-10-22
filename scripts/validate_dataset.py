import pandas as pd

def validate_logs(file_path):
    print(f"--- Running Validation on {file_path} ---")
    df = pd.read_csv(file_path)
    
    # 1. Null Checks
    null_counts = df.isnull().sum()
    print("\n[1] Missing Values Count:")
    print(null_counts)
    
    # 2. Timestamp Ordering Check
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    is_sorted = df.groupby('Patient_ID')['Timestamp'].is_monotonic_increasing
    print(f"\n[2] Chronological Order Valid: {is_sorted.all()}")
    
    # 3. Duplicate Event Check
    duplicates = df.duplicated(subset=['Patient_ID', 'Activity_Name', 'Timestamp']).sum()
    print(f"\n[3] Duplicate Event Records: {duplicates}")
    
    # 4. Outlier Wait Times
    negative_waits = (df['WaitTimeMinutes'] < 0).sum()
    print(f"\n[4] Invalid Wait Times (< 0 mins): {negative_waits}")

if __name__ == "__main__":
    validate_logs('mock_hospital_logs.csv')
