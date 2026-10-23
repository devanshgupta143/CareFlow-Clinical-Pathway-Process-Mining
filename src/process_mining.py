import pm4py
import os
from data_loader import load_event_log

def discover_clinical_pathway(df):
    """
    Takes a dataframe and discovers the process model (Petri Net).
    """
    print("Starting process discovery...")
    
    # 1. Discover the Petri Net using the Inductive Miner
    net, initial_marking, final_marking = pm4py.discover_petri_net_inductive(df)
    
    # 2. Visualize the process and save it as an image
    output_dir = '../data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'clinical_pathway_model.png')
    pm4py.save_vis_petri_net(net, initial_marking, final_marking, output_path)
    print(f"Process model saved to {output_path}")
    
    # 3. Analyze bottlenecks
    print("\n--- Process Mining Complete ---")

if __name__ == "__main__":
    # Load the data
    df = load_event_log('../data/sepsis_log.csv')
    
    # Run discovery
    discover_clinical_pathway(df)