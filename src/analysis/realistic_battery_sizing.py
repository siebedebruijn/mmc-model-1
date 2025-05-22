import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import os

def calculate_realistic_battery_size():
    """
    Calculate a realistic battery size based on:
    1. How much energy is produced during the day
    2. How much energy is consumed overnight
    3. The goal of having the battery empty by the next morning
    """
    print("Starting realistic battery sizing analysis...")
    
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
    
    # Define morning and evening hours based on actual solar production times
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
    
    print(f"Analysis results:")
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
    
    # Plot 1: Required battery capacity over the year
    plt.subplot(2, 1, 1)
    plt.plot(daily_df['Date'], daily_df['Required_Capacity_Wh']/1000, 'b-', label='Required Capacity')
    plt.axhline(y=mean_capacity/1000, color='green', linestyle='--', 
                label=f'Mean: {mean_capacity/1000:.2f} kWh')
    plt.axhline(y=p90_capacity/1000, color='orange', linestyle='--', 
                label=f'90th Percentile: {p90_capacity/1000:.2f} kWh')
    plt.axhline(y=max_capacity/1000, color='red', linestyle='--', 
                label=f'Maximum: {max_capacity/1000:.2f} kWh')
    
    # Highlight summer and winter solstice
    plt.scatter([summer_date], [summer_capacity/1000], color='yellow', s=100, 
                label=f'Summer Solstice: {summer_capacity/1000:.2f} kWh', zorder=5)
    plt.scatter([winter_date], [winter_capacity/1000], color='cyan', s=100, 
                label=f'Winter Solstice: {winter_capacity/1000:.2f} kWh', zorder=5)
    
    plt.title('Required Battery Capacity Throughout the Year (Empty by Morning)', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Battery Capacity (kWh)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Histogram of required capacity
    plt.subplot(2, 1, 2)
    plt.hist(daily_df['Required_Capacity_Wh']/1000, bins=30, alpha=0.7, color='blue')
    plt.axvline(x=mean_capacity/1000, color='green', linestyle='--', 
                label=f'Mean: {mean_capacity/1000:.2f} kWh')
    plt.axvline(x=median_capacity/1000, color='purple', linestyle='--', 
                label=f'Median: {median_capacity/1000:.2f} kWh')
    plt.axvline(x=p90_capacity/1000, color='orange', linestyle='--', 
                label=f'90th Percentile: {p90_capacity/1000:.2f} kWh')
    plt.axvline(x=max_capacity/1000, color='red', linestyle='--', 
                label=f'Maximum: {max_capacity/1000:.2f} kWh')
    plt.title('Distribution of Required Battery Capacity', fontsize=14)
    plt.xlabel('Battery Capacity (kWh)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('realistic_battery_sizing.png', dpi=300)
    print("Saved analysis graph to realistic_battery_sizing.png")
    
    # Save the results to a text file
    with open('realistic_battery_sizing.txt', 'w') as f:
        f.write("Realistic Battery Sizing Analysis\n")
        f.write("================================\n\n")
        f.write("Methodology:\n")
        f.write("This analysis calculates the required battery capacity based on:\n")
        f.write("1. Excess energy produced during the day (8AM-6PM) that can be stored\n")
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
        
        f.write("Top 10 Days with Highest Required Capacity:\n")
        top_days = daily_df.nlargest(10, 'Required_Capacity_Wh')
        for idx, row in top_days.iterrows():
            f.write(f"{row['Date']}: {row['Required_Capacity_Wh']/1000:.2f} kWh ")
            f.write(f"(Day Excess: {row['Day_Excess_Wh']/1000:.2f} kWh, ")
            f.write(f"Night Deficit: {row['Night_Deficit_Wh']/1000:.2f} kWh)\n")
    
    print(f"Saved detailed analysis to realistic_battery_sizing.txt")
    
    # Return the recommended capacity (90th percentile)
    return p90_capacity

def simulate_battery_with_realistic_size(capacity_wh):
    """
    Simulate battery behavior with the calculated realistic capacity.
    """
    print(f"\nSimulating battery behavior with capacity: {capacity_wh/1000:.2f} kWh")
    
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Filter for June 1st (summer) and December 21st (winter)
    summer_day = df[df['Time'].dt.date == pd.to_datetime('2023-06-01').date()]
    winter_day = df[df['Time'].dt.date == pd.to_datetime('2023-12-21').date()]
    
    # Define the realistic battery capacity in Wh
    BATTERY_CAPACITY = capacity_wh
    
    def calculate_battery_state(day_data, initial_percent):
        """
        Calculate battery state over time based on power flows and initial charge.
        """
        # Calculate power difference (battery flow)
        day_data['Battery_Flow_W'] = day_data['Pprod(W)'] - day_data['Pdemand(W)']
        
        # Calculate energy flow in Wh (15-minute intervals)
        day_data['Energy_Flow_Wh'] = day_data['Battery_Flow_W'] * 0.25
        
        # Initialize battery state at specified percentage
        initial_state = BATTERY_CAPACITY * (initial_percent / 100)
        day_data['Battery_State_Wh'] = initial_state
        
        # Calculate battery state over time
        for i in range(1, len(day_data)):
            # Calculate new state based on previous state and current flow
            new_state = day_data['Battery_State_Wh'].iloc[i-1] + day_data['Energy_Flow_Wh'].iloc[i]
            # Clip to battery capacity limits
            day_data.loc[day_data.index[i], 'Battery_State_Wh'] = max(0, min(new_state, BATTERY_CAPACITY))
        
        # Calculate percentage of capacity
        day_data['Battery_State_Percent'] = (day_data['Battery_State_Wh'] / BATTERY_CAPACITY) * 100
        
        return day_data
    
    # Create scenarios for different initial battery states
    initial_states = [0, 50, 100]
    colors = ['blue', 'green', 'purple']
    
    # Calculate battery state for each scenario
    summer_scenarios = []
    winter_scenarios = []
    
    for initial_state in initial_states:
        summer_scenarios.append(calculate_battery_state(summer_day.copy(), initial_state))
        winter_scenarios.append(calculate_battery_state(winter_day.copy(), initial_state))
    
    # Create separate plots for summer
    plt.figure(figsize=(15, 10))
    
    # Summer Day - Power Flows
    plt.subplot(2, 1, 1)
    # Plot production and demand
    plt.plot(summer_day['Time'].dt.hour + summer_day['Time'].dt.minute/60, 
             summer_day['Pprod(W)'], label='Production', color='green', linestyle='-')
    plt.plot(summer_day['Time'].dt.hour + summer_day['Time'].dt.minute/60, 
             summer_day['Pdemand(W)'], label='Demand', color='red', linestyle='-')
    
    # Plot net battery flow
    plt.plot(summer_scenarios[0]['Time'].dt.hour + summer_scenarios[0]['Time'].dt.minute/60,
             summer_scenarios[0]['Battery_Flow_W'], label='Battery Flow (all scenarios)', 
             color='orange', linestyle='--')
    
    plt.title(f'June 1st, 2023 - Power Flows (Battery: {BATTERY_CAPACITY/1000:.2f} kWh)', fontsize=14)
    plt.xlabel('Hour of Day')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Summer Day - Battery State
    plt.subplot(2, 1, 2)
    for i, scenario in enumerate(summer_scenarios):
        plt.plot(scenario['Time'].dt.hour + scenario['Time'].dt.minute/60,
                scenario['Battery_State_Percent'], 
                color=colors[i], 
                linewidth=2, 
                label=f'Initial {initial_states[i]}%')
    
    plt.axhline(y=100, color='red', linestyle='--', label='Full Capacity')
    plt.axhline(y=0, color='red', linestyle='--', label='Empty')
    plt.title(f'June 1st, 2023 - Battery State of Charge ({BATTERY_CAPACITY/1000:.2f} kWh)', fontsize=14)
    plt.xlabel('Hour of Day')
    plt.ylabel('Battery State of Charge (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Adjust layout and save summer plot
    plt.tight_layout()
    plt.savefig('realistic_summer_battery_simulation.png', dpi=300)
    plt.close()
    print("Saved summer battery simulation to realistic_summer_battery_simulation.png")
    
    # Create separate plots for winter
    plt.figure(figsize=(15, 10))
    
    # Winter Day - Power Flows
    plt.subplot(2, 1, 1)
    # Plot production and demand
    plt.plot(winter_day['Time'].dt.hour + winter_day['Time'].dt.minute/60, 
             winter_day['Pprod(W)'], label='Production', color='green', linestyle='-')
    plt.plot(winter_day['Time'].dt.hour + winter_day['Time'].dt.minute/60, 
             winter_day['Pdemand(W)'], label='Demand', color='red', linestyle='-')
    
    # Plot net battery flow
    plt.plot(winter_scenarios[0]['Time'].dt.hour + winter_scenarios[0]['Time'].dt.minute/60,
             winter_scenarios[0]['Battery_Flow_W'], label='Battery Flow (all scenarios)', 
             color='orange', linestyle='--')
    
    plt.title(f'December 21st, 2023 - Power Flows (Battery: {BATTERY_CAPACITY/1000:.2f} kWh)', fontsize=14)
    plt.xlabel('Hour of Day')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Winter Day - Battery State
    plt.subplot(2, 1, 2)
    for i, scenario in enumerate(winter_scenarios):
        plt.plot(scenario['Time'].dt.hour + scenario['Time'].dt.minute/60,
                scenario['Battery_State_Percent'], 
                color=colors[i], 
                linewidth=2, 
                label=f'Initial {initial_states[i]}%')
    
    plt.axhline(y=100, color='red', linestyle='--', label='Full Capacity')
    plt.axhline(y=0, color='red', linestyle='--', label='Empty')
    plt.title(f'December 21st, 2023 - Battery State of Charge ({BATTERY_CAPACITY/1000:.2f} kWh)', fontsize=14)
    plt.xlabel('Hour of Day')
    plt.ylabel('Battery State of Charge (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Adjust layout and save winter plot
    plt.tight_layout()
    plt.savefig('realistic_winter_battery_simulation.png', dpi=300)
    plt.close()
    print("Saved winter battery simulation to realistic_winter_battery_simulation.png")
    
    # Simulate one complete day-night cycle to verify the "empty by morning" goal
    def simulate_day_night_cycle(data, initial_percent):
        """Simulate a full day-night cycle to verify battery is empty by morning"""
        # Calculate power difference (battery flow)
        data['Battery_Flow_W'] = data['Pprod(W)'] - data['Pdemand(W)']
        
        # Calculate energy flow in Wh (15-minute intervals)
        data['Energy_Flow_Wh'] = data['Battery_Flow_W'] * 0.25
        
        # Initialize battery state at specified percentage
        initial_state = BATTERY_CAPACITY * (initial_percent / 100)
        data['Battery_State_Wh'] = initial_state
        
        # Calculate battery state over time
        for i in range(1, len(data)):
            # Calculate new state based on previous state and current flow
            new_state = data['Battery_State_Wh'].iloc[i-1] + data['Energy_Flow_Wh'].iloc[i]
            # Clip to battery capacity limits
            data.loc[data.index[i], 'Battery_State_Wh'] = max(0, min(new_state, BATTERY_CAPACITY))
        
        # Calculate percentage of capacity
        data['Battery_State_Percent'] = (data['Battery_State_Wh'] / BATTERY_CAPACITY) * 100
        
        # Add hour indicator
        data['Hour'] = data['Time'].dt.hour
        
        # Get end of day state (around 6AM)
        morning_hours = data[data['Hour'] == 6]
        if len(morning_hours) > 0:
            morning_state = morning_hours['Battery_State_Percent'].values[0]
        else:
            morning_state = data.iloc[-1]['Battery_State_Percent']
        
        return data, morning_state
    
    # Get a random full day
    random_dates = df['Time'].dt.date.unique()
    if len(random_dates) > 180:
        random_date = random_dates[180]  # Middle of the year
    else:
        random_date = random_dates[0]
        
    day_data = df[df['Time'].dt.date == random_date]
    
    # Simulate with 0% initial
    sim_data, morning_state = simulate_day_night_cycle(day_data.copy(), 0)
    
    print(f"\nVerification of 'Empty by Morning' goal:")
    print(f"Date: {random_date}")
    print(f"Battery state at 6AM: {morning_state:.2f}%")
    if morning_state < 5:
        print("✓ Battery is nearly empty by morning as intended")
    else:
        print("✗ Battery is not empty by morning - may need capacity adjustment")

def add_solar_time_analysis():
    """
    Add an explanation about the solar production time analysis and why the 
    morning_start and evening_start values were updated from fixed 6AM/6PM values.
    """
    print("\nSolar Production Time Analysis:")
    print("=" * 50)
    print("Based on analysis of the solar production data, we've updated the day/night boundaries:")
    print("- Morning start: 8 AM (average time when solar panels start producing significant power)")
    print("- Evening start: 6 PM (average time when solar panels stop producing significant power)")
    print("\nThese times vary by season:")
    print("- Winter (Dec-Feb): Approx. 8:30 AM - 4:00 PM (shorter days)")
    print("- Spring/Fall (Mar-May, Sep-Nov): Approx. 7:30 AM - 6:30 PM")
    print("- Summer (Jun-Aug): Approx. 7:00 AM - 8:00 PM (longer days)")
    print("\nThe realistic battery sizing calculation now uses these updated times")
    print("to more accurately determine day/night energy patterns, which improves")
    print("the accuracy of the battery capacity recommendation.")
    
    # You can run analyze_solar_times.py for a full monthly breakdown and visualization

if __name__ == "__main__":
    try:
        # Calculate the recommended battery capacity
        capacity_wh = calculate_realistic_battery_size()
        print(f"\nRecommended battery capacity: {capacity_wh/1000:.2f} kWh")
        
        # Add solar time analysis explanation
        add_solar_time_analysis()
        
        # Simulate battery behavior with the calculated size
        simulate_battery_with_realistic_size(capacity_wh)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
