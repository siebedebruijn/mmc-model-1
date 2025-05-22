import pandas as pd
import matplotlib.pyplot as plt
import os
from src.utils.config import CLEANED_DATA_PATH, IMAGES_DIR, REPORTS_DIR

def analyze_daily_energy():
    """Analyze daily energy production and demand patterns."""
    # Read the cleaned data
    df = pd.read_csv(CLEANED_DATA_PATH)
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Calculate energy in Wh (15-minute intervals)
    df['Energy_Production_Wh'] = df['Pprod(W)'] * 0.25
    df['Energy_Demand_Wh'] = df['Pdemand(W)'] * 0.25
    
    # Calculate daily totals
    daily_totals = df.groupby(df['Time'].dt.date).agg({
        'Energy_Production_Wh': 'sum',
        'Energy_Demand_Wh': 'sum'
    }).reset_index()
    
    # Calculate daily difference
    daily_totals['Energy_Difference_Wh'] = daily_totals['Energy_Production_Wh'] - daily_totals['Energy_Demand_Wh']
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Daily Energy Production and Demand
    plt.subplot(2, 1, 1)
    plt.plot(daily_totals['Time'], daily_totals['Energy_Production_Wh'], label='Production', color='green')
    plt.plot(daily_totals['Time'], daily_totals['Energy_Demand_Wh'], label='Demand', color='red')
    plt.title('Daily Energy Production and Demand')
    plt.xlabel('Date')
    plt.ylabel('Energy (Wh)')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Daily Energy Difference
    plt.subplot(2, 1, 2)
    plt.bar(daily_totals['Time'], daily_totals['Energy_Difference_Wh'],
            color=['green' if x >= 0 else 'red' for x in daily_totals['Energy_Difference_Wh']])
    plt.title('Daily Energy Difference (Production - Demand)')
    plt.xlabel('Date')
    plt.ylabel('Energy Difference (Wh)')
    plt.grid(True)
    
    # Adjust layout and save plot
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'energy_analysis.png'))
    
    # Save results to text file
    with open(os.path.join(REPORTS_DIR, 'energy_analysis.txt'), 'w') as f:
        f.write("Energy Analysis Results\n")
        f.write("=" * 50 + "\n\n")
        
        # Overall statistics
        f.write("Overall Statistics:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Energy Produced: {daily_totals['Energy_Production_Wh'].sum():,.2f} Wh\n")
        f.write(f"Total Energy Demanded: {daily_totals['Energy_Demand_Wh'].sum():,.2f} Wh\n")
        f.write(f"Total Energy Difference: {daily_totals['Energy_Difference_Wh'].sum():,.2f} Wh\n\n")
        
        # Daily statistics
        f.write("Daily Statistics:\n")
        f.write("-" * 20 + "\n")
        for _, row in daily_totals.iterrows():
            f.write(f"\nDate: {row['Time']}\n")
            f.write(f"Production: {row['Energy_Production_Wh']:,.2f} Wh\n")
            f.write(f"Demand: {row['Energy_Demand_Wh']:,.2f} Wh\n")
            f.write(f"Difference: {row['Energy_Difference_Wh']:,.2f} Wh\n")
            f.write("-" * 20 + "\n")
    
    print("Energy analysis complete! Results have been saved to:")
    print(f"- {os.path.join(IMAGES_DIR, 'energy_analysis.png')}")
    print(f"- {os.path.join(REPORTS_DIR, 'energy_analysis.txt')}")
    
    return daily_totals
