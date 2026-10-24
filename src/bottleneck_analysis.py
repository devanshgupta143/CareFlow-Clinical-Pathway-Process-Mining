import pandas as pd
import pm4py
from data_loader import load_event_log

def analyze_bottlenecks(df):
    print("--- Starting Bottleneck Analysis ---")
    
    # 1. Calculate the duration of the entire case (patient visit)
    case_durations = pm4py.get_all_case_durations(df)
    avg_duration_hours = (sum(case_durations) / len(case_durations)) / 3600
    print(f"Average total time in hospital: {avg_duration_hours:.2f} hours")
    print(f"Longest single patient stay: {(max(case_durations) / 3600):.2f} hours\n")

    # 2. Find the slowest transitions between activities
    # This calculates the time between every pair of steps (e.g., Admission -> Triage)
    performance_dfg = pm4py.discover_performance_dfg(df)
    
    # Sort the transitions by average time (descending) to find the biggest bottlenecks
    # performance_dfg[1] contains the times, performance_dfg[0] contains the (source, target) pairs
    transitions_with_time = []
    for pair, time_stats in performance_dfg[1].items():
        mean_time_hours = time_stats['mean'] / 3600
        transitions_with_time.append((pair, mean_time_hours))
        
    # Sort the list to show the top 5 slowest steps
    transitions_with_time.sort(key=lambda x: x[1], reverse=True)
    
    print("Top 5 Slowest Transitions (Bottlenecks):")
    for i, (pair, time_hours) in enumerate(transitions_with_time[:5]):
        source_activity = pair[0]
        target_activity = pair[1]
        print(f"{i+1}. {source_activity} -> {target_activity}: {time_hours:.2f} hours on average")

if __name__ == "__main__":
    # Load the data we generated earlier
    df = load_event_log('../data/sepsis_log.csv')
    
    # Run the analysis
    analyze_bottlenecks(df)