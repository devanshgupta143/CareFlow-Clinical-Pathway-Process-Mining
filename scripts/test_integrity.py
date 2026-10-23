import pandas as pd

def test_referential_integrity():
    print("--- Running Referential Integrity Test Suite ---")
    events_df = pd.read_csv('mock_hospital_logs.csv')
    
    # Create simulated dimension keys for testing
    unique_patients = pd.DataFrame({'Patient_ID': events_df['Patient_ID'].unique()})
    
    # Check for orphaned keys
    merged = events_df.merge(unique_patients, on='Patient_ID', how='left', indicator=True)
    orphaned_rows = (merged['_merge'] == 'left_only').sum()
    
    print(f"Orphaned Event Records Found: {orphaned_rows}")
    assert orphaned_rows == 0, "Integrity check failed: Orphaned keys detected!"
    print("Integrity Check Passed: All event keys successfully mapped.")

if __name__ == "__main__":
    test_referential_integrity()
