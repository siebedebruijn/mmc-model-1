import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def analyze_solar_production_times():
    """
    Analyze solar production data to determine average times when solar panels 
    start and stop producing power throughout the year.
    """
    print("Starting solar production time analysis...")
    
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    print(f"Loaded data with {len(df)} rows")
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Add date and time components
    df['Date'] = df['Time'].dt.date
    df['Hour'] = df['Time'].dt.hour
    df['Minute'] = df['Time'].dt.minute
    df['TimeOfDay'] = df['Hour'] + df['Minute']/60
    df['Month'] = df['Time'].dt.month
    
    # Define a significant production threshold (e.g., 5% of the daily maximum)
    # Group by date to calculate daily statistics
    daily_stats = df.groupby('Date').agg({'Pprod(W)': ['max', 'mean']})
    daily_stats.columns = ['Daily_Max_Prod', 'Daily_Avg_Prod']
    daily_stats.reset_index(inplace=True)
    
    # Merge daily stats back to the main dataframe
    df = pd.merge(df, daily_stats, on='Date')
    
    # Define threshold as 5% of daily maximum production
    df['Threshold'] = df['Daily_Max_Prod'] * 0.05
    
    # Identify when production is above threshold
    df['IsProducing'] = df['Pprod(W)'] > df['Threshold']
    
    # Group by date to find the first and last time of production for each day
    production_times = []
    
    for date, group in df.groupby('Date'):
        if group['IsProducing'].any():
            # Get rows where production is happening
            producing_rows = group[group['IsProducing']]
            
            # Find first and last time of production
            start_time = producing_rows['TimeOfDay'].min()
            end_time = producing_rows['TimeOfDay'].max()
            
            # Get the month for seasonal analysis
            month = producing_rows['Month'].iloc[0]
            
            production_times.append({
                'Date': date,
                'Start_Time': start_time,
                'End_Time': end_time,
                'Duration': end_time - start_time,
                'Month': month
            })
    
    # Convert to DataFrame
    times_df = pd.DataFrame(production_times)
    
    # Overall statistics
    print("\nOverall Statistics:")
    print(f"Average start time: {times_df['Start_Time'].mean():.2f} hours (decimal time)")
    print(f"Average end time: {times_df['End_Time'].mean():.2f} hours (decimal time)")
    print(f"Average duration: {times_df['Duration'].mean():.2f} hours")
    
    # Calculate statistics by month
    monthly_stats = times_df.groupby('Month').agg({
        'Start_Time': 'mean',
        'End_Time': 'mean',
        'Duration': 'mean'
    }).reset_index()
    
    # Format the times for better readability
    def decimal_to_time(decimal_time):
        hours = int(decimal_time)
        minutes = int((decimal_time - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"
    
    print("\nMonthly Statistics:")
    for _, row in monthly_stats.iterrows():
        month_name = datetime(2023, int(row['Month']), 1).strftime('%B')
        print(f"{month_name}: Start={decimal_to_time(row['Start_Time'])} End={decimal_to_time(row['End_Time'])} Duration={row['Duration']:.2f}h")
    
    # Create visualizations
    plt.figure(figsize=(15, 10))
    
    # Plot start and end times by month
    plt.subplot(2, 1, 1)
    plt.plot(monthly_stats['Month'], monthly_stats['Start_Time'], 'b-o', label='Start Time')
    plt.plot(monthly_stats['Month'], monthly_stats['End_Time'], 'r-o', label='End Time')
    plt.title('Solar Production Start and End Times by Month')
    plt.xlabel('Month')
    plt.ylabel('Time of Day (decimal hours)')
    plt.xticks(range(1, 13), [datetime(2023, m, 1).strftime('%b') for m in range(1, 13)])
    plt.grid(True)
    plt.legend()
    
    # Plot duration by month
    plt.subplot(2, 1, 2)
    plt.bar(monthly_stats['Month'], monthly_stats['Duration'], color='orange')
    plt.title('Solar Production Duration by Month')
    plt.xlabel('Month')
    plt.ylabel('Duration (hours)')
    plt.xticks(range(1, 13), [datetime(2023, m, 1).strftime('%b') for m in range(1, 13)])
    plt.grid(True, axis='y')
    
    plt.tight_layout()
    plt.savefig('solar_production_times.png')
    
    # Calculate morning_start and evening_start values for realistic_battery_sizing.py
    # These are rounded to the nearest integer hour for simplicity
    # Take the average of the entire year
    morning_start = round(times_df['Start_Time'].mean())
    evening_start = round(times_df['End_Time'].mean())
    
    print(f"\nRecommended values for realistic_battery_sizing.py:")
    print(f"morning_start = {morning_start}  # {decimal_to_time(times_df['Start_Time'].mean())}")
    print(f"evening_start = {evening_start}  # {decimal_to_time(times_df['End_Time'].mean())}")
    
    return morning_start, evening_start

if __name__ == "__main__":
    morning_start, evening_start = analyze_solar_production_times()
