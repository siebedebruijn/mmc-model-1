import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os

def calculate_realistic_battery_size():
    try:
        print("Starting battery sizing analysis...")
        # Read the cleaned data
        df = pd.read_csv('cleaned_data.csv')
        print(f"Loaded data with {len(df)} rows")
        
        # Convert Time to datetime
        df['Time'] = pd.to_datetime(df['Time'])
        
        # Convert negative production values to positive
        df['Pprod(W)'] = df['Pprod(W)'].abs()
        
        # Calculate energy in Wh (15-minute intervals)
        df['Energy_Production_Wh'] = df['Pprod(W)'] * 0.25
        df['Energy_Demand_Wh'] = df['Pdemand(W)'] * 0.25
        df['Energy_Net_Wh'] = df['Energy_Production_Wh'] - df['Energy_Demand_Wh']
        
        # Define morning and evening hours
        morning_start = 6  # 6 AM
        evening_start = 18  # 6 PM
        
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
        daily_df['Required_Capacity_Wh'] = daily_df.apply(
            lambda row: min(row['Day_Excess_Wh'], row['Night_Deficit_Wh']), axis=1
        )
        
        # Get statistics
        mean_capacity = daily_df['Required_Capacity_Wh'].mean()
        median_capacity = daily_df['Required_Capacity_Wh'].median()
        p90_capacity = daily_df['Required_Capacity_Wh'].quantile(0.9)
        max_capacity = daily_df['Required_Capacity_Wh'].max()
        
        print(f"Analysis results:")
        print(f"Mean required capacity: {mean_capacity/1000:.2f} kWh")
        print(f"Median required capacity: {median_capacity/1000:.2f} kWh")
        print(f"90th percentile capacity: {p90_capacity/1000:.2f} kWh")
        print(f"Maximum required capacity: {max_capacity/1000:.2f} kWh")
        
        # Create a simple plot to verify
        plt.figure(figsize=(10, 6))
        plt.plot(daily_df['Date'], daily_df['Required_Capacity_Wh']/1000)
        plt.axhline(y=p90_capacity/1000, color='r', linestyle='--')
        plt.title('Required Battery Capacity (kWh)')
        plt.ylabel('Capacity (kWh)')
        plt.savefig('simple_battery_sizing.png')
        print("Saved plot to simple_battery_sizing.png")
        
        # Return the 90th percentile capacity
        return p90_capacity
    
    except Exception as e:
        print(f"Error in calculation: {str(e)}")
        import traceback
        traceback.print_exc()
        return 100000  # Default 100 kWh if there's an error

if __name__ == "__main__":
    try:
        capacity_wh = calculate_realistic_battery_size()
        print(f"Recommended battery capacity: {capacity_wh/1000:.2f} kWh")
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()
