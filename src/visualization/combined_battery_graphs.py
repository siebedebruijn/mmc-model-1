import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import os
from analyze_energy import calculate_battery_state

def create_combined_daynight_battery_graph():
    """
    Creates separate graphs showing battery simulations at different initial charge levels
    (0%, 50%, 100%) for summer and winter days with power flows on separate graphs.
    """
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Filter for June 1st (summer) and December 21st (winter)
    summer_day = df[df['Time'].dt.date == pd.to_datetime('2023-06-01').date()]
    winter_day = df[df['Time'].dt.date == pd.to_datetime('2023-12-21').date()]
    
    # Battery capacity in Wh
    BATTERY_CAPACITY = 650 * 1000  # 650 kWh in Wh
    
    # Create scenarios for different initial battery states
    initial_states = [0, 50, 100]
    colors = ['blue', 'green', 'purple']
    
    # Calculate battery state for each scenario
    summer_scenarios = []
    winter_scenarios = []
    
    for initial_state in initial_states:
        summer_scenarios.append(calculate_battery_state(summer_day.copy(), initial_state, BATTERY_CAPACITY))
        winter_scenarios.append(calculate_battery_state(winter_day.copy(), initial_state, BATTERY_CAPACITY))
    
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
    
    plt.title('June 1st, 2023 - Power Flows', fontsize=14)
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
    plt.title('June 1st, 2023 - Battery State of Charge at Different Initial Levels', fontsize=14)
    plt.xlabel('Hour of Day')
    plt.ylabel('Battery State of Charge (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Adjust layout and save summer plot
    plt.tight_layout()
    plt.savefig('summer_battery_simulation.png', dpi=300)
    plt.close()
    
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
    
    plt.title('December 21st, 2023 - Power Flows', fontsize=14)
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
    plt.title('December 21st, 2023 - Battery State of Charge at Different Initial Levels', fontsize=14)
    plt.xlabel('Hour of Day')
    plt.ylabel('Battery State of Charge (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Adjust layout and save winter plot
    plt.tight_layout()
    plt.savefig('winter_battery_simulation.png', dpi=300)
    plt.close()
    
    print("Summer and winter battery simulation graphs have been saved to separate files:")
    print("- summer_battery_simulation.png")
    print("- winter_battery_simulation.png")

def create_combined_seasonal_battery_graph():
    """
    Creates a combined graph showing annual battery simulations at different 
    initial charge levels (0%, 50%) for seasonal storage.
    """
    # Read the seasonal battery data for 0% and 50% scenarios
    # We'll need to rerun the simulations because the data isn't saved in the previous runs
    
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Calculate energy in Wh (15-minute intervals)
    df['Energy_Production_Wh'] = df['Pprod(W)'] * 0.25
    df['Energy_Demand_Wh'] = df['Pdemand(W)'] * 0.25
    
    # Calculate power difference (battery flow)
    df['Battery_Flow_W'] = df['Pprod(W)'] - df['Pdemand(W)']
    
    # Calculate energy flow in Wh (15-minute intervals)
    df['Energy_Flow_Wh'] = df['Battery_Flow_W'] * 0.25
    
    # Battery capacity in Wh - 40 MWh = 40,000 kWh = 40,000,000 Wh
    BATTERY_CAPACITY = 40 * 1000 * 1000  # 40 MWh in Wh
    
    # Initialize battery states for both scenarios
    initial_states = [0, 50]
    
    # Prepare the data frames to store the results
    dfs = []
    
    for initial_percent in initial_states:
        # Make a copy of the original data
        scenario_df = df.copy()
        
        # Initialize battery state at specified percentage
        initial_state_wh = BATTERY_CAPACITY * (initial_percent / 100)
        scenario_df['Battery_State_Wh'] = initial_state_wh
        
        # Calculate battery state over time
        for i in range(1, len(scenario_df)):
            # Calculate new state based on previous state and current flow
            new_state = scenario_df['Battery_State_Wh'].iloc[i-1] + scenario_df['Energy_Flow_Wh'].iloc[i]
            # Clip to battery capacity limits
            scenario_df.loc[scenario_df.index[i], 'Battery_State_Wh'] = max(0, min(new_state, BATTERY_CAPACITY))
        
        # Calculate percentage of capacity
        scenario_df['Battery_State_Percent'] = (scenario_df['Battery_State_Wh'] / BATTERY_CAPACITY) * 100
        
        # Calculate daily averages for plotting
        daily_avg = scenario_df.groupby(scenario_df['Time'].dt.date).agg({
            'Battery_State_Percent': 'mean',
            'Battery_State_Wh': 'mean',
            'Energy_Production_Wh': 'sum',
            'Energy_Demand_Wh': 'sum',
            'Energy_Flow_Wh': 'sum'
        }).reset_index()
        
        # Convert to MWh for better readability
        daily_avg['Battery_State_MWh'] = daily_avg['Battery_State_Wh'] / 1000 / 1000
        daily_avg['Energy_Production_MWh'] = daily_avg['Energy_Production_Wh'] / 1000 / 1000
        daily_avg['Energy_Demand_MWh'] = daily_avg['Energy_Demand_Wh'] / 1000 / 1000
        daily_avg['Energy_Net_MWh'] = daily_avg['Energy_Flow_Wh'] / 1000 / 1000
        
        # Add initial state for reference
        daily_avg['Initial_State'] = initial_percent
        
        dfs.append(daily_avg)
    
    # Create the plot
    plt.figure(figsize=(15, 10))
    
    # Plot: Battery State in MWh
    plt.subplot(2, 1, 1)
    
    colors = ['blue', 'green']
    for i, df in enumerate(dfs):
        plt.plot(df['Time'], df['Battery_State_MWh'], 
                 color=colors[i], linewidth=2, 
                 label=f'Initial: {initial_states[i]}%')
    
    plt.axhline(y=40, color='red', linestyle='--', alpha=0.5, label='Full Capacity (40 MWh)')
    plt.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Empty')
    plt.axhline(y=20, color='purple', linestyle='--', alpha=0.5, label='50% Capacity (20 MWh)')
    plt.title('40 MWh Battery State Throughout 2023 (Different Initial States)', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Battery State (MWh)')
    plt.ylim(-2, 42)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot: Daily Energy Production and Demand
    plt.subplot(2, 1, 2)
    plt.plot(dfs[0]['Time'], dfs[0]['Energy_Production_MWh'], label='Production', color='green')
    plt.plot(dfs[0]['Time'], dfs[0]['Energy_Demand_MWh'], label='Demand', color='red')
    plt.plot(dfs[0]['Time'], dfs[0]['Energy_Net_MWh'], label='Net (Production - Demand)', 
             color='blue', linestyle='-', alpha=0.5)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.title('Daily Energy Production and Demand', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Energy (MWh)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Adjust layout and save plot
    plt.tight_layout()
    plt.savefig('combined_seasonal_battery_simulation.png', dpi=300)
    plt.close()
    
    print("Combined seasonal battery simulation graph has been saved to 'combined_seasonal_battery_simulation.png'")

if __name__ == "__main__":
    create_combined_daynight_battery_graph()
    create_combined_seasonal_battery_graph()
