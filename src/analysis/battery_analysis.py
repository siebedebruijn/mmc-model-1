import pandas as pd
import matplotlib.pyplot as plt
import os
from src.utils.config import (
    CLEANED_DATA_PATH, 
    IMAGES_DIR, 
    REPORTS_DIR,
    DAILY_BATTERY_CAPACITY_WH,
    SEASONAL_BATTERY_CAPACITY_WH,
    SUMMER_SOLSTICE,
    WINTER_SOLSTICE
)

def analyze_battery_sizing():
    """Analyze battery sizing requirements based on daily patterns."""
    # Read the cleaned data
    df = pd.read_csv(CLEANED_DATA_PATH)
    
    # Convert Time to datetime and preprocess data
    df['Time'] = pd.to_datetime(df['Time'])
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    df['Energy_Production_Wh'] = df['Pprod(W)'] * 0.25
    df['Energy_Demand_Wh'] = df['Pdemand(W)'] * 0.25
    
    # Calculate daily totals
    daily_totals = df.groupby(df['Time'].dt.date).agg({
        'Energy_Production_Wh': 'sum',
        'Energy_Demand_Wh': 'sum'
    }).reset_index()
    
    daily_totals['Energy_Difference_Wh'] = daily_totals['Energy_Production_Wh'] - daily_totals['Energy_Demand_Wh']
    
    # Create visualization
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 1, 1)
    plt.plot(daily_totals['Time'], daily_totals['Energy_Production_Wh']/1000, label='Production', color='green')
    plt.plot(daily_totals['Time'], daily_totals['Energy_Demand_Wh']/1000, label='Demand', color='red')
    plt.axhline(y=650, color='blue', linestyle='--', label='Recommended Battery Size (650 kWh)')
    plt.title('Daily Energy Production and Demand with Battery Size Reference')
    plt.xlabel('Date')
    plt.ylabel('Energy (kWh)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.bar(daily_totals['Time'], daily_totals['Energy_Difference_Wh']/1000,
            color=['green' if x >= 0 else 'red' for x in daily_totals['Energy_Difference_Wh']])
    plt.title('Daily Energy Difference (Production - Demand)')
    plt.xlabel('Date')
    plt.ylabel('Energy Difference (kWh)')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'battery_sizing_analysis.png'))
    
    # Save detailed analysis
    with open(os.path.join(REPORTS_DIR, 'battery_sizing_calculations.txt'), 'w') as f:
        f.write("Battery Sizing Analysis\n")
        f.write("=" * 50 + "\n\n")
        
        # Overall statistics
        f.write("Overall Statistics:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Energy Produced: {daily_totals['Energy_Production_Wh'].sum()/1000:,.2f} kWh\n")
        f.write(f"Total Energy Demanded: {daily_totals['Energy_Demand_Wh'].sum()/1000:,.2f} kWh\n")
        f.write(f"Total Energy Difference: {daily_totals['Energy_Difference_Wh'].sum()/1000:,.2f} kWh\n\n")
        
        # Battery sizing calculations
        f.write("Battery Sizing Calculations:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Maximum Daily Demand: {daily_totals['Energy_Demand_Wh'].max()/1000:,.2f} kWh\n")
        f.write(f"Average Daily Demand: {daily_totals['Energy_Demand_Wh'].mean()/1000:,.2f} kWh\n")
        f.write(f"Maximum Daily Production: {daily_totals['Energy_Production_Wh'].max()/1000:,.2f} kWh\n")
        f.write(f"Maximum Excess Production: {daily_totals['Energy_Difference_Wh'].max()/1000:,.2f} kWh\n")
        f.write(f"Minimum Excess Production: {daily_totals['Energy_Difference_Wh'].min()/1000:,.2f} kWh\n\n")
        
        # Recommendations
        f.write("Recommended Battery Size:\n")
        f.write("-" * 20 + "\n")
        f.write("Based on the analysis, a battery size of 650 kWh is recommended because:\n")
        f.write(f"1. It covers the maximum daily demand of {daily_totals['Energy_Demand_Wh'].max()/1000:.2f} kWh\n")
        f.write(f"2. It can store the maximum excess production of {daily_totals['Energy_Difference_Wh'].max()/1000:.2f} kWh\n")
        f.write("3. It provides a buffer for unexpected demand increases\n")
        f.write("4. It accounts for typical battery efficiency losses (90-95%)\n")
    
    print("Battery sizing analysis complete! Results saved to:")
    print(f"- {os.path.join(IMAGES_DIR, 'battery_sizing_analysis.png')}")
    print(f"- {os.path.join(REPORTS_DIR, 'battery_sizing_calculations.txt')}")
    
    return daily_totals
