import pandas as pd
import pm4py
from data_loader import load_event_log

def check_conformance(df):
    print("--- Starting Conformance Checking ---")
    
    # 1. Define the "Standard Protocol" (A Petri Net representing the ideal path)
    # For this example, our rule is simple: Admission -> Blood Test -> Discharge
    # Any path that skips Blood Test, or does Discharge before Blood Test, is a deviation.
    
    # We will use PM4Py to discover the standard model from just ONE perfect case
    perfect_case = pd.DataFrame({
        'case:concept:name': ['Perfect_Patient'] * 3,
        'concept:name': ['Admission', 'Blood Test', 'Discharge'],
        'time:timestamp': pd.to_datetime(['2024-01-01 10:00', '2024-01-01 12:00', '2024-01-01 15:00'])
    })
    
    # Discover the "gold standard" model
    net, im, fm = pm4py.discover_petri_net_inductive(perfect_case)
    print("Standard Protocol Model Created.")
    
    # 2. Perform Token-Based Replay
    # This maps the real patient data onto the standard model to see where they fail
    print("Replaying real patient logs against the standard model...")
    replayed_traces = pm4py.conformance_diagnostics_token_based_replay(df, net, im, fm)
    
    # 3. Analyze the results
    deviations_found = 0
    total_patients = len(df['case:concept:name'].unique())
    
    print("\n--- Conformance Results ---")
    for result in replayed_traces:
        # 'trace_is_fit' is True if the patient followed the protocol perfectly
        if not result['trace_is_fit']:
            deviations_found += 1
            
            # Find which specific activity caused the deviation
            # 'activated_transitions' shows where the tokens got stuck
            if result['missing_tokens'] > 0:
                print(f"Patient {result['case_id']} DEVIATED: Missing required steps (e.g., skipped Blood Test).")
                
    print(f"\nSummary: {deviations_found} out of {total_patients} patients deviated from the standard protocol.")
    print(f"Conformance Rate: {((total_patients - deviations_found) / total_patients) * 100:.2f}%")

if __name__ == "__main__":
    # Load the data
    df = load_event_log('../data/sepsis_log.csv')
    
    # Run the check
    check_conformance(df)