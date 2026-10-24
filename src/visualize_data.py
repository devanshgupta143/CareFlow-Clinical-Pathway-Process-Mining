import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from data_loader import load_event_log

def create_activity_chart(df):
    print("Generating activity frequency chart...")
    
    # Count how many times each activity occurs
    activity_counts = df['concept:name'].value_counts().reset_index()
    activity_counts.columns = ['Activity', 'Count']
    
    # Set up the visual style
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Count', y='Activity', data=activity_counts, palette='viridis')
    
    plt.title('Frequency of Clinical Activities', fontsize=16)
    plt.xlabel('Number of Occurrences', fontsize=12)
    plt.ylabel('Activity', fontsize=12)
    plt.tight_layout()
    
    # Save the chart
    output_path = '../data/activity_frequency.png'
    plt.savefig(output_path)
    print(f"Chart saved successfully to {output_path}")
    
    # Display it (optional, might pop up a window)
    # plt.show()

if __name__ == "__main__":
    df = load_event_log('../data/sepsis_log.csv')
    create_activity_chart(df)