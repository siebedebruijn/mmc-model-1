import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.analyze_energy import calculate_battery_state
from utils.config import CLEANED_DATA_PATH, IMAGES_DIR, ensure_directories

def create_battery_visualizations():
    """
    Creates battery state visualizations for different scenarios.
    """
    print("Creating battery visualizations...")
    ensure_directories()
    
    # Read the cleaned data
    df = pd.read_csv(CLEANED_DATA_PATH)
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Filter for June 1st (summer) and December 21st (winter)
    summer_day = df[df['Time'].dt.date == pd.to_datetime('2023-06-01').date()]
    winter_day = df[df['Time'].dt.date == pd.to_datetime('2023-12-21').date()]
    
    # Battery capacity in Wh
    BATTERY_CAPACITY = 231.62 * 1000  # 231.62 kWh in Wh
    
    # Create scenarios for different initial battery states
    initial_states = [0, 50, 100]  # Initial charge percentages
    colors = ['blue', 'green', 'purple']
    
    # Calculate battery state for each scenario
    summer_scenarios = []
    winter_scenarios = []
    
    for initial_state in initial_states:
        summer_scenarios.append(calculate_battery_state(summer_day.copy(), initial_state))
        winter_scenarios.append(calculate_battery_state(winter_day.copy(), initial_state))
    
    # Create summer day visualization
    plt.figure(figsize=(15, 10))
    
    # Summer - Power Flows
    plt.subplot(2, 1, 1)
    plt.plot(summer_day['Time'].dt.hour + summer_day['Time'].dt.minute/60,
             summer_day['Pprod(W)'], label='Production', color='green')
    plt.plot(summer_day['Time'].dt.hour + summer_day['Time'].dt.minute/60,
             summer_day['Pdemand(W)'], label='Demand', color='red')
    plt.title('Summer Day Power Flows (June 1st)')
    plt.xlabel('Hour of Day')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.grid(True)
    
    # Summer - Battery State
    plt.subplot(2, 1, 2)
    for i, scenario in enumerate(summer_scenarios):
        plt.plot(scenario['Time'].dt.hour + scenario['Time'].dt.minute/60,
                scenario['Battery_State_Percent'],
                label=f'Initial {initial_states[i]}%',
                color=colors[i])
    
    plt.axhline(y=100, color='red', linestyle='--', label='Full Capacity')
    plt.axhline(y=0, color='red', linestyle='--', label='Empty')
    plt.title('Summer Day Battery State')
    plt.xlabel('Hour of Day')
    plt.ylabel('Battery State (%)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'summer_battery_simulation.png'))
    plt.close()
    
    # Create winter day visualization
    plt.figure(figsize=(15, 10))
    
    # Winter - Power Flows
    plt.subplot(2, 1, 1)
    plt.plot(winter_day['Time'].dt.hour + winter_day['Time'].dt.minute/60,
             winter_day['Pprod(W)'], label='Production', color='green')
    plt.plot(winter_day['Time'].dt.hour + winter_day['Time'].dt.minute/60,
             winter_day['Pdemand(W)'], label='Demand', color='red')
    plt.title('Winter Day Power Flows (December 21st)')
    plt.xlabel('Hour of Day')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.grid(True)
    
    # Winter - Battery State
    plt.subplot(2, 1, 2)
    for i, scenario in enumerate(winter_scenarios):
        plt.plot(scenario['Time'].dt.hour + scenario['Time'].dt.minute/60,
                scenario['Battery_State_Percent'],
                label=f'Initial {initial_states[i]}%',
                color=colors[i])
    
    plt.axhline(y=100, color='red', linestyle='--', label='Full Capacity')
    plt.axhline(y=0, color='red', linestyle='--', label='Empty')
    plt.title('Winter Day Battery State')
    plt.xlabel('Hour of Day')
    plt.ylabel('Battery State (%)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'winter_battery_simulation.png'))
    plt.close()
    
    # Create combined seasonal visualization
    plt.figure(figsize=(15, 10))
    
    # Filter unique days and sort chronologically
    days = sorted(df['Time'].dt.date.unique())
    daily_stats = []
    
    for day in days:
        day_data = df[df['Time'].dt.date == day]
        stats = {
            'Date': day,
            'Production_kWh': day_data['Pprod(W)'].sum() * 0.25 / 1000,
            'Demand_kWh': day_data['Pdemand(W)'].sum() * 0.25 / 1000
        }
        stats['Net_kWh'] = stats['Production_kWh'] - stats['Demand_kWh']
        daily_stats.append(stats)
    
    daily_df = pd.DataFrame(daily_stats)
    
    plt.subplot(2, 1, 1)
    plt.plot(daily_df['Date'], daily_df['Production_kWh'],
             label='Production', color='green')
    plt.plot(daily_df['Date'], daily_df['Demand_kWh'],
             label='Demand', color='red')
    plt.title('Daily Energy Production and Demand')
    plt.xlabel('Date')
    plt.ylabel('Energy (kWh)')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(daily_df['Date'], daily_df['Net_kWh'],
             label='Net Energy (Production - Demand)', color='blue')
    plt.axhline(y=0, color='red', linestyle='--')
    plt.title('Daily Net Energy')
    plt.xlabel('Date')
    plt.ylabel('Net Energy (kWh)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'seasonal_battery_analysis.png'))
    plt.close()
    
    print("Battery visualizations have been created:")
    print(f"- {os.path.join(IMAGES_DIR, 'summer_battery_simulation.png')}")
    print(f"- {os.path.join(IMAGES_DIR, 'winter_battery_simulation.png')}")
    print(f"- {os.path.join(IMAGES_DIR, 'seasonal_battery_analysis.png')}")

if __name__ == "__main__":
    create_battery_visualizations()
