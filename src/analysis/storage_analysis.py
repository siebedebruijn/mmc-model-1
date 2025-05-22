import pandas as pd
import matplotlib.pyplot as plt
import os
from src.utils.config import (
    CLEANED_DATA_PATH, 
    IMAGES_DIR, 
    REPORTS_DIR,
    DAILY_BATTERY_CAPACITY_WH,
    SEASONAL_BATTERY_CAPACITY_WH
)

def analyze_seasonal_storage():
    """Analyze seasonal energy storage requirements."""
    # Read the cleaned data
    df = pd.read_csv(CLEANED_DATA_PATH)
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Calculate energy in Wh (15-minute intervals)
    df['Energy_Production_Wh'] = df['Pprod(W)'] * 0.25
    df['Energy_Demand_Wh'] = df['Pdemand(W)'] * 0.25
    
    # Add month and season columns
    df['Month'] = df['Time'].dt.month
    df['Season'] = pd.cut(df['Time'].dt.month, 
                         bins=[0, 2, 5, 8, 11, 12],
                         labels=['Winter1', 'Spring', 'Summer', 'Autumn', 'Winter2'],
                         ordered=False)
    
    # Calculate seasonal totals
    seasonal_totals = df.groupby('Season').agg({
        'Energy_Production_Wh': 'sum',
        'Energy_Demand_Wh': 'sum'
    }).reset_index()
    
    # Combine Winter1 and Winter2
    winter1 = seasonal_totals[seasonal_totals['Season'] == 'Winter1']
    winter2 = seasonal_totals[seasonal_totals['Season'] == 'Winter2']
    winter_combined = pd.DataFrame({
        'Season': ['Winter'],
        'Energy_Production_Wh': [winter1['Energy_Production_Wh'].sum() + winter2['Energy_Production_Wh'].sum()],
        'Energy_Demand_Wh': [winter1['Energy_Demand_Wh'].sum() + winter2['Energy_Demand_Wh'].sum()]
    })
    
    seasonal_totals = pd.concat([
        seasonal_totals[~seasonal_totals['Season'].isin(['Winter1', 'Winter2'])],
        winter_combined
    ])
    
    seasonal_totals['Energy_Difference_Wh'] = seasonal_totals['Energy_Production_Wh'] - seasonal_totals['Energy_Demand_Wh']
    
    # Create visualization
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Seasonal Energy Production and Demand
    plt.subplot(2, 1, 1)
    x = range(len(seasonal_totals['Season']))
    width = 0.35
    
    plt.bar([i - width/2 for i in x], seasonal_totals['Energy_Production_Wh']/1000, 
            width, label='Production', color='green')
    plt.bar([i + width/2 for i in x], seasonal_totals['Energy_Demand_Wh']/1000, 
            width, label='Demand', color='red')
    plt.xlabel('Season')
    plt.ylabel('Energy (kWh)')
    plt.title('Seasonal Energy Production and Demand')
    plt.xticks(x, seasonal_totals['Season'])
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Seasonal Energy Difference
    plt.subplot(2, 1, 2)
    plt.bar(seasonal_totals['Season'], seasonal_totals['Energy_Difference_Wh']/1000,
            color=['green' if x >= 0 else 'red' for x in seasonal_totals['Energy_Difference_Wh']])
    plt.title('Seasonal Energy Difference (Production - Demand)')
    plt.xlabel('Season')
    plt.ylabel('Energy Difference (kWh)')
    plt.grid(True)
    
    # Save results
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'seasonal_storage_analysis.png'))
    
    # Calculate required seasonal storage
    summer_excess = seasonal_totals[seasonal_totals['Season'] == 'Summer']['Energy_Difference_Wh'].values[0]
    winter_deficit = abs(seasonal_totals[seasonal_totals['Season'] == 'Winter']['Energy_Difference_Wh'].values[0])
    required_storage = max(winter_deficit, summer_excess)
    recommended_storage = required_storage * 1.1  # Add 10% buffer

    # Save detailed analysis
    with open(os.path.join(REPORTS_DIR, 'seasonal_storage_calculations.txt'), 'w') as f:
        f.write("Seasonal Storage Analysis\n")
        f.write("=" * 50 + "\n\n")
        
        # Overall statistics
        f.write("Overall Statistics:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Energy Produced: {df['Energy_Production_Wh'].sum()/1000:,.2f} kWh\n")
        f.write(f"Total Energy Demanded: {df['Energy_Demand_Wh'].sum()/1000:,.2f} kWh\n")
        f.write(f"Total Energy Difference: {(df['Energy_Production_Wh'].sum() - df['Energy_Demand_Wh'].sum())/1000:,.2f} kWh\n\n")
        
        # Seasonal statistics
        f.write("Seasonal Statistics:\n")
        f.write("-" * 20 + "\n")
        for _, row in seasonal_totals.iterrows():
            f.write(f"\n{row['Season']}:\n")
            f.write(f"Production: {row['Energy_Production_Wh']/1000:,.2f} kWh\n")
            f.write(f"Demand: {row['Energy_Demand_Wh']/1000:,.2f} kWh\n")
            f.write(f"Difference: {row['Energy_Difference_Wh']/1000:,.2f} kWh\n")
            f.write("-" * 20 + "\n")
            
        f.write("\nRecommended Seasonal Storage Capacity:\n")
        f.write(f"{recommended_storage/1000:,.2f} kWh\n\n")
        f.write("This includes:\n")
        f.write("1. Summer excess and winter deficit coverage\n")
        f.write("2. 10% buffer for efficiency losses\n")
        f.write("3. Margin for variability between years\n")
    
    print("Seasonal storage analysis complete! Results saved to:")
    print(f"- {os.path.join(IMAGES_DIR, 'seasonal_storage_analysis.png')}")
    print(f"- {os.path.join(REPORTS_DIR, 'seasonal_storage_calculations.txt')}")
    
    return seasonal_totals
