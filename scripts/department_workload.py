import pandas as pd

def analyze_department_workload(file_path):
    print("--- Analyzing Department Workload & Wait Times ---")
    df = pd.read_csv(file_path)
    
    # Group by Department and calculate metrics
    workload = df.groupby('Department').agg(
        Total_Events=('Patient_ID', 'count'),
        Unique_Patients=('Patient_ID', 'nunique'),
        Avg_Wait_Minutes=('WaitTimeMinutes', 'mean'),
        Max_Wait_Minutes=('WaitTimeMinutes', 'max')
    ).reset_index()
    
    print("\nDepartment Workload Summary:")
    print(workload)

if __name__ == "__main__":
    analyze_department_workload('mock_hospital_logs.csv')
