import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os

def visualize_monthly_solar_times():
    """
    Create a detailed visualization of solar production times by month
    and a heat map showing how production times vary throughout the year.
    """
    print("Creating monthly solar production time visualizations...")
    
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
    df['Day'] = df['Time'].dt.day
    
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
            
            # Get the month and day for seasonal analysis
            month = producing_rows['Month'].iloc[0]
            day = producing_rows['Day'].iloc[0]
            
            production_times.append({
                'Date': date,
                'Month': month,
                'Day': day,
                'Start_Time': start_time,
                'End_Time': end_time,
                'Duration': end_time - start_time
            })
    
    # Convert to DataFrame
    times_df = pd.DataFrame(production_times)
    
    # Create a more detailed monthly visualization
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Solar production start and end times by month
    plt.subplot(2, 1, 1)
    
    # Calculate monthly statistics
    monthly_stats = times_df.groupby('Month').agg({
        'Start_Time': ['mean', 'min', 'max'],
        'End_Time': ['mean', 'min', 'max'],
        'Duration': 'mean'
    })
    
    # Flatten the column names
    monthly_stats.columns = ['Start_Mean', 'Start_Min', 'Start_Max', 
                            'End_Mean', 'End_Min', 'End_Max', 
                            'Duration_Mean']
    monthly_stats.reset_index(inplace=True)
    
    # Plot the mean start and end times with min/max ranges
    months = monthly_stats['Month']
    plt.plot(months, monthly_stats['Start_Mean'], 'bo-', label='Avg Start Time')
    plt.fill_between(months, monthly_stats['Start_Min'], monthly_stats['Start_Max'], 
                    alpha=0.2, color='blue', label='Start Time Range')
    
    plt.plot(months, monthly_stats['End_Mean'], 'ro-', label='Avg End Time')
    plt.fill_between(months, monthly_stats['End_Min'], monthly_stats['End_Max'], 
                    alpha=0.2, color='red', label='End Time Range')
    
    # Add day/night markers for original and realistic approaches
    plt.axhline(y=6, color='gray', linestyle='--', label='Original Morning Start (6 AM)')
    plt.axhline(y=18, color='gray', linestyle='--', label='Evening Start (6 PM)')
    plt.axhline(y=8, color='black', linestyle='-', label='Realistic Morning Start (8 AM)')
    
    plt.title('Solar Production Start and End Times by Month')
    plt.xlabel('Month')
    plt.ylabel('Time of Day (24h)')
    plt.xticks(range(1, 13), [datetime(2023, m, 1).strftime('%b') for m in range(1, 13)])
    plt.yticks(range(0, 24, 2), [f"{h:02d}:00" for h in range(0, 24, 2)])
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    
    # Plot 2: Heatmap of solar production by month and hour
    plt.subplot(2, 1, 2)
    
    # Create a production matrix (month x hour)
    hours = np.arange(0, 24, 0.25)  # 15-minute intervals
    months = np.arange(1, 13)
    
    # Initialize the production matrix
    production_matrix = np.zeros((len(months), len(hours)))
    
    # Fill the matrix with production data
    for month in months:
        month_data = df[df['Month'] == month]
        for i, hour in enumerate(hours):
            # Find production data for this hour and month
            hour_data = month_data[(month_data['TimeOfDay'] >= hour) & 
                                   (month_data['TimeOfDay'] < hour + 0.25)]
            if not hour_data.empty:
                # Calculate average production for this time slot
                avg_production = hour_data['Pprod(W)'].mean()
                production_matrix[int(month)-1, i] = avg_production
    
    # Normalize by the maximum production value
    max_production = np.max(production_matrix)
    production_matrix = production_matrix / max_production
    
    # Create the heatmap
    plt.imshow(production_matrix, aspect='auto', cmap='viridis', 
              extent=[0, 24, 12.5, 0.5], interpolation='nearest')
    
    plt.colorbar(label='Relative Production (% of maximum)')
    plt.title('Solar Production Intensity by Month and Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Month')
    plt.yticks(range(1, 13), [datetime(2023, m, 1).strftime('%b') for m in range(1, 13)])
    plt.xticks(range(0, 25, 2))
    
    # Add markers for day/night boundaries
    plt.axvline(x=6, color='gray', linestyle='--', label='Original Morning Start (6 AM)')
    plt.axvline(x=18, color='gray', linestyle='--', label='Evening Start (6 PM)')
    plt.axvline(x=8, color='white', linestyle='-', label='Realistic Morning Start (8 AM)')
    
    plt.tight_layout()
    plt.savefig('monthly_solar_production_times.png', dpi=300)
    
    # Create a table of monthly solar production times
    with open('monthly_solar_production_times.txt', 'w') as f:
        f.write("Monthly Solar Production Times\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"{'Month':<10} {'Start Time':<30} {'End Time':<30} {'Duration (hours)':<15}\n")
        f.write(f"{'':<10} {'Mean':<10} {'Min':<10} {'Max':<10} {'Mean':<10} {'Min':<10} {'Max':<10} {'Mean':<15}\n")
        f.write("-" * 85 + "\n")
        
        for _, row in monthly_stats.iterrows():
            month_name = datetime(2023, int(row['Month']), 1).strftime('%B')
            
            # Convert decimal times to HH:MM format
            def decimal_to_time(decimal_time):
                hours = int(decimal_time)
                minutes = int((decimal_time - hours) * 60)
                return f"{hours:02d}:{minutes:02d}"
            
            start_mean = decimal_to_time(row['Start_Mean'])
            start_min = decimal_to_time(row['Start_Min'])
            start_max = decimal_to_time(row['Start_Max'])
            
            end_mean = decimal_to_time(row['End_Mean'])
            end_min = decimal_to_time(row['End_Min'])
            end_max = decimal_to_time(row['End_Max'])
            
            f.write(f"{month_name:<10} {start_mean:<10} {start_min:<10} {start_max:<10} "
                   f"{end_mean:<10} {end_min:<10} {end_max:<10} {row['Duration_Mean']:<15.2f}\n")
        
        # Add seasonal averages
        f.write("\n\nSeasonal Averages:\n")
        f.write("-" * 50 + "\n")
        
        # Define seasons
        seasons = {
            'Winter': [12, 1, 2],
            'Spring': [3, 4, 5],
            'Summer': [6, 7, 8],
            'Fall': [9, 10, 11]
        }
        
        for season, months in seasons.items():
            season_data = monthly_stats[monthly_stats['Month'].isin(months)]
            
            start_mean = decimal_to_time(season_data['Start_Mean'].mean())
            end_mean = decimal_to_time(season_data['End_Mean'].mean())
            duration_mean = season_data['Duration_Mean'].mean()
            
            f.write(f"{season}: Average Start={start_mean}, Average End={end_mean}, "
                   f"Average Duration={duration_mean:.2f} hours\n")
    
    print("\nVisualization complete! Results saved to 'monthly_solar_production_times.png' and 'monthly_solar_production_times.txt'")

if __name__ == "__main__":
    try:
        visualize_monthly_solar_times()
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
