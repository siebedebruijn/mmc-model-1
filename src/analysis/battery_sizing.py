import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import (CLEANED_DATA_PATH, IMAGES_DIR, REPORTS_DIR, 
                         MORNING_START, EVENING_START, ensure_directories)

def calculate_battery_size():
    """
    Calculate the required battery capacity based on realistic solar production times:
    Using 8 AM to 6 PM as day period based on actual solar production analysis
    """
    print("Calculating battery size with realistic day/night boundaries...")
    ensure_directories()
    
    # Read the cleaned data
    df = pd.read_csv(CLEANED_DATA_PATH)
    print(f"Loaded data with {len(df)} rows")
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Calculate energy in Wh (15-minute intervals)
    df['Energy_Production_Wh'] = df['Pprod(W)'] * 0.25
    df['Energy_Demand_Wh'] = df['Pdemand(W)'] * 0.25
    df['Energy_Net_Wh'] = df['Energy_Production_Wh'] - df['Energy_Demand_Wh']
    
    # Define the realistic day/night boundaries based on solar production analysis
    morning_start = 8  # 7:53 AM (average time when solar panels start producing)
    evening_start = 18  # 6:17 PM (average time when solar panels stop producing)
    
    # Add time of day indicators
    df['Hour'] = df['Time'].dt.hour
    df['IsDay'] = (df['Hour'] >= morning_start) & (df['Hour'] < evening_start)
    
    # Group by date and calculate day/night energy
    daily_data = []
    
    # Get unique dates
    unique_dates = df['Time'].dt.date.unique()
    print(f"Processing {len(unique_dates)} unique dates")
    
    for date in unique_dates:
        day_data = df[df['Time'].dt.date == date]
        
        # Day energy (excess energy that could be stored)
        day_excess = day_data[day_data['IsDay']]['Energy_Net_Wh'].sum()
        day_excess = max(0, day_excess)  # Only consider positive excess during day
        
        # Night energy (deficit that needs battery)
        night_deficit = abs(min(0, day_data[~day_data['IsDay']]['Energy_Net_Wh'].sum()))
        
        # Track which date this is
        daily_data.append({
            'Date': date,
            'Day_Excess_Wh': day_excess,
            'Night_Deficit_Wh': night_deficit
        })
    
    # Convert to DataFrame
    daily_df = pd.DataFrame(daily_data)
    
    # Calculate the ideal battery size for each day
    # For each day, we need enough capacity to store the daytime excess
    # and enough to cover the nighttime deficit
    daily_df['Required_Capacity_Wh'] = daily_df.apply(
        lambda row: min(row['Day_Excess_Wh'], row['Night_Deficit_Wh']), axis=1
    )
    
    # Get statistics
    mean_capacity = daily_df['Required_Capacity_Wh'].mean()
    median_capacity = daily_df['Required_Capacity_Wh'].median()
    p90_capacity = daily_df['Required_Capacity_Wh'].quantile(0.9)
    max_capacity = daily_df['Required_Capacity_Wh'].max()
    
    print(f"Results:")
    print(f"Mean required capacity: {mean_capacity/1000:.2f} kWh")
    print(f"Median required capacity: {median_capacity/1000:.2f} kWh")
    print(f"90th percentile capacity: {p90_capacity/1000:.2f} kWh")
    print(f"Maximum required capacity: {max_capacity/1000:.2f} kWh")
    
    # Select summer and winter solstice (or nearby dates)
    summer_solstice = pd.to_datetime('2023-06-21').date()
    winter_solstice = pd.to_datetime('2023-12-21').date()
    
    # Find closest dates
    summer_date = min(unique_dates, key=lambda x: abs((x - summer_solstice).days))
    winter_date = min(unique_dates, key=lambda x: abs((x - winter_solstice).days))
    
    # Get required capacity for these days
    summer_capacity = daily_df[daily_df['Date'] == summer_date]['Required_Capacity_Wh'].values[0]
    winter_capacity = daily_df[daily_df['Date'] == winter_date]['Required_Capacity_Wh'].values[0]
    
    print(f"Summer solstice capacity: {summer_capacity/1000:.2f} kWh")
    print(f"Winter solstice capacity: {winter_capacity/1000:.2f} kWh")
    
    # Create visualization
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Daily Required Battery Capacity
    plt.subplot(2, 1, 1)
    plt.plot(daily_df['Date'], daily_df['Required_Capacity_Wh'] / 1000, 'b-', label='Required Capacity')
    plt.axhline(y=p90_capacity/1000, color='r', linestyle='--', 
                label=f'90th Percentile: {p90_capacity/1000:.2f} kWh')
    plt.title('Daily Required Battery Capacity')
    plt.xlabel('Date')
    plt.ylabel('Capacity (kWh)')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Day Excess vs Night Deficit
    plt.subplot(2, 1, 2)
    plt.plot(daily_df['Date'], daily_df['Day_Excess_Wh'] / 1000, 'g-', label='Day Excess')
    plt.plot(daily_df['Date'], daily_df['Night_Deficit_Wh'] / 1000, 'r-', label='Night Deficit')
    plt.title('Day Excess vs Night Deficit')
    plt.xlabel('Date')
    plt.ylabel('Energy (kWh)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'battery_sizing.png'))
    
    # Generate detailed report
    with open(os.path.join(REPORTS_DIR, 'battery_sizing.txt'), 'w') as f:
        f.write("Battery Sizing Analysis\n")
        f.write("================================\n\n")
        
        f.write("Methodology:\n")
        f.write("This analysis calculates the required battery capacity based on:\n")
        f.write(f"1. Excess energy produced during the day ({morning_start}AM-{evening_start}PM) that can be stored\n")
        f.write("2. Energy deficit during the night that needs to be covered by the battery\n")
        f.write("3. The goal of having the battery empty by the next morning\n\n")
        
        f.write("Results:\n")
        f.write(f"Mean Required Capacity: {mean_capacity/1000:.2f} kWh\n")
        f.write(f"Median Required Capacity: {median_capacity/1000:.2f} kWh\n")
        f.write(f"90th Percentile Capacity: {p90_capacity/1000:.2f} kWh\n")
        f.write(f"Maximum Required Capacity: {max_capacity/1000:.2f} kWh\n\n")
        
        f.write("Seasonal Variation:\n")
        f.write(f"Summer Solstice (approx. {summer_date}): {summer_capacity/1000:.2f} kWh\n")
        f.write(f"Winter Solstice (approx. {winter_date}): {winter_capacity/1000:.2f} kWh\n\n")
        
        f.write("Recommendations:\n")
        f.write(f"Based on this analysis, a battery capacity of {p90_capacity/1000:.2f} kWh would cover\n")
        f.write("90% of daily needs, allowing the battery to be empty by the next morning most days.\n")
        f.write(f"For maximum coverage, a capacity of {max_capacity/1000:.2f} kWh would be required.\n\n")
        
        # Get top 10 days with highest required capacity
        f.write("Top 10 Days with Highest Required Capacity:\n")
        top_days = daily_df.sort_values('Required_Capacity_Wh', ascending=False).head(10)
        for _, row in top_days.iterrows():
            f.write(f"{row['Date']}: {row['Required_Capacity_Wh']/1000:.2f} kWh ")
            f.write(f"(Day Excess: {row['Day_Excess_Wh']/1000:.2f} kWh, ")
            f.write(f"Night Deficit: {row['Night_Deficit_Wh']/1000:.2f} kWh)\n")
    
    print(f"Analysis complete! Results saved to 'battery_sizing.png' and 'battery_sizing.txt'")
    return p90_capacity

if __name__ == "__main__":
    try:
        capacity_wh = calculate_battery_size()
        print(f"\nRecommended battery capacity: {capacity_wh/1000:.2f} kWh")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
