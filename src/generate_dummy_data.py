import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_data():
    np.random.seed(42)
    activities = ['Admission', 'Triage', 'Blood Test', 'X-Ray', 'Surgery', 'ICU', 'Discharge']
    data = []
    
    for patient_id in range(1, 100): # 100 patients
        start_time = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
        # Every patient has a random sequence of 3 to 6 activities
        pathway = np.random.choice(activities[1:-1], size=np.random.randint(3, 6), replace=False)
        pathway = ['Admission'] + list(pathway) + ['Discharge']
        
        current_time = start_time
        for step in pathway:
            data.append({
                'PatientID': f'P{patient_id:03d}',
                'Action': step,
                'Time': current_time.strftime('%Y-%m-%d %H:%M:%S')
            })
            # Add random hours between steps
            current_time += timedelta(hours=np.random.randint(1, 48))
            
    df = pd.DataFrame(data)
    
    # Ensure the data directory exists
    os.makedirs('../data', exist_ok=True) 
    df.to_csv('../data/sepsis_log.csv', index=False)
    print("Dummy data generated at data/sepsis_log.csv")

if __name__ == "__main__":
    generate_data()