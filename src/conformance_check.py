import pandas as pd
import pm4py
from data_loader import load_event_log

def check_conformance(df):
    print("--- Starting Conformance Checking ---")
    
    # 1. Define the "Standard Protocol" (A Petri Net representing the ideal path)
    perfect_case = pd.DataFrame({
        'case:concept:name': ['Perfect_Patient'] * 3,
        'concept:name': ['Admission', 'Blood Test', 'Discharge'],
        'time:timestamp': pd.to_datetime(['2024-01-01 10:00', '2024-01-01 12:00', '2024-01-01 15:00'])
    })
    
    # Discover the "gold standard" model
    net, im, fm = pm4py.discover_petri_net_inductive(perfect_case)
    print("Standard Protocol Model Created.")
    
    # 2. Perform Token-Based Replay
    print("Replaying real patient logs against the standard model...")
    replayed_traces = pm4py.conformance_diagnostics_token_based_replay(df, net, im, fm)
    
    # 3. Analyze the results
    deviations_found = 0
    
    # Get the unique case IDs in the order they appear in the dataframe
    unique_cases = df['case:concept:name'].unique()
    total_patients = len(unique_cases)
    
    print("\n--- Conformance Results ---")
    
    # Loop through the results using an index
    for idx, result in enumerate(replayed_traces):
        # 'trace_is_fit' is True if the patient followed the protocol perfectly
        if not result['trace_is_fit']:
            deviations_found += 1
            
            # Find which specific activity caused the deviation
            if result['missing_tokens'] > 0:
                # Look up the patient ID using the index (idx)
                patient_id = unique_cases[idx] if idx < total_patients else "Unknown"
                print(f"Patient {patient_id} DEVIATED: Missing required steps (e.g., skipped Blood Test).")
                
    print(f"\nSummary: {deviations_found} out of {total_patients} patients deviated from the standard protocol.")
    print(f"Conformance Rate: {((total_patients - deviations_found) / total_patients) * 100:.2f}%")

if __name__ == "__main__":
    df = load_event_log('../data/sepsis_log.csv')
    check_conformance(df)