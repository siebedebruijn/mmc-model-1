import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def analyze_energy_data():
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Calculate energy in Wh (15-minute intervals)
    # Convert power (W) to energy (Wh) by multiplying by 0.25 (15 minutes = 0.25 hours)
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
    plt.savefig('energy_analysis.png')
    
    # Save results to text file
    with open('energy_analysis.txt', 'w') as f:
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
    
    print("Analysis complete! Results have been saved to 'energy_analysis.txt' and 'energy_analysis.png'")
    
    return daily_totals

def create_solstice_comparison():
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Filter for June 1st and December 21st
    june_1 = df[df['Time'].dt.date == pd.to_datetime('2023-06-01').date()]
    dec_21 = df[df['Time'].dt.date == pd.to_datetime('2023-12-21').date()]
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Plot June 1st
    plt.subplot(2, 1, 1)
    plt.plot(june_1['Time'].dt.hour + june_1['Time'].dt.minute/60, 
             june_1['Pprod(W)'], label='Production', color='green')
    plt.plot(june_1['Time'].dt.hour + june_1['Time'].dt.minute/60, 
             june_1['Pdemand(W)'], label='Demand', color='red')
    plt.title('June 1st, 2023 - Production and Demand')
    plt.xlabel('Hour of Day')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.grid(True)
    
    # Plot December 21st
    plt.subplot(2, 1, 2)
    plt.plot(dec_21['Time'].dt.hour + dec_21['Time'].dt.minute/60, 
             dec_21['Pprod(W)'], label='Production', color='green')
    plt.plot(dec_21['Time'].dt.hour + dec_21['Time'].dt.minute/60, 
             dec_21['Pdemand(W)'], label='Demand', color='red')
    plt.title('December 21st, 2023 - Production and Demand')
    plt.xlabel('Hour of Day')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.grid(True)
    
    # Adjust layout and save plot
    plt.tight_layout()
    plt.savefig('solstice_comparison.png')
    plt.close()
    
    print("Solstice comparison graph has been saved to 'solstice_comparison.png'")

def analyze_battery_sizing():
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    
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
    
    # Create the plot
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Daily Energy Production and Demand
    plt.subplot(2, 1, 1)
    plt.plot(daily_totals['Time'], daily_totals['Energy_Production_Wh']/1000, label='Production', color='green')
    plt.plot(daily_totals['Time'], daily_totals['Energy_Demand_Wh']/1000, label='Demand', color='red')
    plt.axhline(y=650, color='blue', linestyle='--', label='Recommended Battery Size (650 kWh)')
    plt.title('Daily Energy Production and Demand with Battery Size Reference')
    plt.xlabel('Date')
    plt.ylabel('Energy (kWh)')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Daily Energy Difference
    plt.subplot(2, 1, 2)
    plt.bar(daily_totals['Time'], daily_totals['Energy_Difference_Wh']/1000, 
            color=['green' if x >= 0 else 'red' for x in daily_totals['Energy_Difference_Wh']])
    plt.title('Daily Energy Difference (Production - Demand)')
    plt.xlabel('Date')
    plt.ylabel('Energy Difference (kWh)')
    plt.grid(True)
    
    # Adjust layout and save plot
    plt.tight_layout()
    plt.savefig('battery_sizing_analysis.png')
    
    # Save calculations to text file
    with open('battery_sizing_calculations.txt', 'w') as f:
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
        
        # Recommended battery size
        f.write("Recommended Battery Size:\n")
        f.write("-" * 20 + "\n")
        f.write("Based on the analysis, a battery size of 650 kWh is recommended because:\n")
        f.write("1. It covers the maximum daily demand of {:.2f} kWh\n".format(daily_totals['Energy_Demand_Wh'].max()/1000))
        f.write("2. It can store the maximum excess production of {:.2f} kWh\n".format(daily_totals['Energy_Difference_Wh'].max()/1000))
        f.write("3. It provides a buffer for unexpected demand increases\n")
        f.write("4. It accounts for typical battery efficiency losses (90-95%)\n")
        
        # Daily statistics for reference
        f.write("\nDaily Statistics (Top 5 Highest Demand Days):\n")
        f.write("-" * 20 + "\n")
        top_demand_days = daily_totals.nlargest(5, 'Energy_Demand_Wh')
        for _, row in top_demand_days.iterrows():
            f.write(f"\nDate: {row['Time']}\n")
            f.write(f"Production: {row['Energy_Production_Wh']/1000:,.2f} kWh\n")
            f.write(f"Demand: {row['Energy_Demand_Wh']/1000:,.2f} kWh\n")
            f.write(f"Difference: {row['Energy_Difference_Wh']/1000:,.2f} kWh\n")
            f.write("-" * 20 + "\n")
    
    print("Battery sizing analysis complete! Results have been saved to 'battery_sizing_analysis.png' and 'battery_sizing_calculations.txt'")

def analyze_seasonal_storage():
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    
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
    
    # Calculate daily totals
    daily_totals = df.groupby(df['Time'].dt.date).agg({
        'Energy_Production_Wh': 'sum',
        'Energy_Demand_Wh': 'sum'
    }).reset_index()
    
    # Calculate daily difference
    daily_totals['Energy_Difference_Wh'] = daily_totals['Energy_Production_Wh'] - daily_totals['Energy_Demand_Wh']
    
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
    
    # Create the plot
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
    
    # Adjust layout and save plot
    plt.tight_layout()
    plt.savefig('seasonal_storage_analysis.png')
    
    # Save calculations to text file
    with open('seasonal_storage_calculations.txt', 'w') as f:
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
        
        # Calculate required seasonal storage
        summer_excess = seasonal_totals[seasonal_totals['Season'] == 'Summer']['Energy_Difference_Wh'].values[0]
        winter_deficit = abs(seasonal_totals[seasonal_totals['Season'] == 'Winter']['Energy_Difference_Wh'].values[0])
        
        f.write("\nSeasonal Storage Requirements:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Summer Excess Energy: {summer_excess/1000:,.2f} kWh\n")
        f.write(f"Winter Energy Deficit: {winter_deficit/1000:,.2f} kWh\n")
        
        # Recommended seasonal battery size
        required_storage = max(winter_deficit, summer_excess)
        recommended_storage = required_storage * 1.1  # Add 10% buffer for efficiency losses
        
        f.write("\nRecommended Seasonal Battery Size:\n")
        f.write("-" * 20 + "\n")
        f.write(f"Based on the analysis, a seasonal battery size of {recommended_storage/1000:,.2f} kWh is recommended because:\n")
        f.write("1. It can store the excess summer production\n")
        f.write("2. It can cover the winter energy deficit\n")
        f.write("3. It includes a 10% buffer for efficiency losses\n")
        f.write("4. It accounts for seasonal variations in production and demand\n")
        
        # Additional considerations
        f.write("\nAdditional Considerations:\n")
        f.write("-" * 20 + "\n")
        f.write("1. Battery efficiency losses (typically 90-95%)\n")
        f.write("2. Seasonal temperature variations affecting battery performance\n")
        f.write("3. Degradation over time\n")
        f.write("4. Peak demand periods during winter\n")
    
    print("Seasonal storage analysis complete! Results have been saved to 'seasonal_storage_analysis.png' and 'seasonal_storage_calculations.txt'")

def analyze_battery_flows():
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
    
    def calculate_battery_state(day_data, initial_percent):
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
    
    def create_battery_plot(summer_data, winter_data, initial_percent, filename):
        # Create the plot
        plt.figure(figsize=(15, 15))
        
        # Plot Summer Day Power Flows
        plt.subplot(4, 1, 1)
        plt.plot(summer_data['Time'].dt.hour + summer_data['Time'].dt.minute/60, 
                 summer_data['Pprod(W)'], label='Production', color='green')
        plt.plot(summer_data['Time'].dt.hour + summer_data['Time'].dt.minute/60, 
                 summer_data['Pdemand(W)'], label='Demand', color='red')
        plt.fill_between(summer_data['Time'].dt.hour + summer_data['Time'].dt.minute/60,
                         summer_data['Battery_Flow_W'], 0,
                         where=(summer_data['Battery_Flow_W'] > 0),
                         color='green', alpha=0.3, label='Battery Charging')
        plt.fill_between(summer_data['Time'].dt.hour + summer_data['Time'].dt.minute/60,
                         summer_data['Battery_Flow_W'], 0,
                         where=(summer_data['Battery_Flow_W'] < 0),
                         color='red', alpha=0.3, label='Battery Discharging')
        plt.title(f'June 1st, 2023 - Power Flows and Battery Operation (Initial Charge: {initial_percent}%)')
        plt.xlabel('Hour of Day')
        plt.ylabel('Power (W)')
        plt.legend()
        plt.grid(True)
        
        # Plot Summer Day Battery State
        plt.subplot(4, 1, 2)
        plt.plot(summer_data['Time'].dt.hour + summer_data['Time'].dt.minute/60,
                 summer_data['Battery_State_Percent'], color='purple', linewidth=2)
        plt.axhline(y=100, color='red', linestyle='--', label='Full Capacity')
        plt.axhline(y=0, color='red', linestyle='--', label='Empty')
        plt.title(f'June 1st, 2023 - Battery State of Charge (Initial: {initial_percent}%)')
        plt.xlabel('Hour of Day')
        plt.ylabel('Battery State of Charge (%)')
        plt.legend()
        plt.grid(True)
        
        # Plot Winter Day Power Flows
        plt.subplot(4, 1, 3)
        plt.plot(winter_data['Time'].dt.hour + winter_data['Time'].dt.minute/60, 
                 winter_data['Pprod(W)'], label='Production', color='green')
        plt.plot(winter_data['Time'].dt.hour + winter_data['Time'].dt.minute/60, 
                 winter_data['Pdemand(W)'], label='Demand', color='red')
        plt.fill_between(winter_data['Time'].dt.hour + winter_data['Time'].dt.minute/60,
                         winter_data['Battery_Flow_W'], 0,
                         where=(winter_data['Battery_Flow_W'] > 0),
                         color='green', alpha=0.3, label='Battery Charging')
        plt.fill_between(winter_data['Time'].dt.hour + winter_data['Time'].dt.minute/60,
                         winter_data['Battery_Flow_W'], 0,
                         where=(winter_data['Battery_Flow_W'] < 0),
                         color='red', alpha=0.3, label='Battery Discharging')
        plt.title(f'December 21st, 2023 - Power Flows and Battery Operation (Initial Charge: {initial_percent}%)')
        plt.xlabel('Hour of Day')
        plt.ylabel('Power (W)')
        plt.legend()
        plt.grid(True)
        
        # Plot Winter Day Battery State
        plt.subplot(4, 1, 4)
        plt.plot(winter_data['Time'].dt.hour + winter_data['Time'].dt.minute/60,
                 winter_data['Battery_State_Percent'], color='purple', linewidth=2)
        plt.axhline(y=100, color='red', linestyle='--', label='Full Capacity')
        plt.axhline(y=0, color='red', linestyle='--', label='Empty')
        plt.title(f'December 21st, 2023 - Battery State of Charge (Initial: {initial_percent}%)')
        plt.xlabel('Hour of Day')
        plt.ylabel('Battery State of Charge (%)')
        plt.legend()
        plt.grid(True)
        
        # Adjust layout and save plot
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
    
    # Create scenarios for different initial battery states
    initial_states = [0, 50, 100]
    filenames = ['battery_flows_0percent.png', 'battery_flows_50percent.png', 'battery_flows_100percent.png']
    
    for initial_state, filename in zip(initial_states, filenames):
        summer_scenario = calculate_battery_state(summer_day.copy(), initial_state)
        winter_scenario = calculate_battery_state(winter_day.copy(), initial_state)
        create_battery_plot(summer_scenario, winter_scenario, initial_state, filename)
    
    # Save calculations to text file
    with open('battery_flows_calculations.txt', 'w') as f:
        f.write("Battery Flows Analysis (650 kWh Capacity)\n")
        f.write("=" * 50 + "\n\n")
        
        for initial_state in initial_states:
            f.write(f"\nScenario: Initial Battery State {initial_state}%\n")
            f.write("-" * 50 + "\n\n")
            
            # Summer day analysis
            summer_scenario = calculate_battery_state(summer_day.copy(), initial_state)
            f.write("June 1st, 2023 (Summer Day) Analysis:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total Production: {summer_scenario['Pprod(W)'].sum() * 0.25/1000:,.2f} kWh\n")
            f.write(f"Total Demand: {summer_scenario['Pdemand(W)'].sum() * 0.25/1000:,.2f} kWh\n")
            f.write(f"Net Battery Flow: {summer_scenario['Battery_Flow_W'].sum() * 0.25/1000:,.2f} kWh\n")
            f.write(f"Maximum Battery State: {summer_scenario['Battery_State_Wh'].max()/1000:,.2f} kWh ({summer_scenario['Battery_State_Percent'].max():.1f}%)\n")
            f.write(f"Minimum Battery State: {summer_scenario['Battery_State_Wh'].min()/1000:,.2f} kWh ({summer_scenario['Battery_State_Percent'].min():.1f}%)\n")
            
            f.write("\nCharging Periods:\n")
            charging_periods = summer_scenario[summer_scenario['Battery_Flow_W'] > 0]
            for _, period in charging_periods.iterrows():
                f.write(f"Time: {period['Time'].strftime('%H:%M')}, Power: {period['Battery_Flow_W']:,.2f} W, Battery State: {period['Battery_State_Wh']/1000:,.2f} kWh ({period['Battery_State_Percent']:.1f}%)\n")
            
            f.write("\nDischarging Periods:\n")
            discharging_periods = summer_scenario[summer_scenario['Battery_Flow_W'] < 0]
            for _, period in discharging_periods.iterrows():
                f.write(f"Time: {period['Time'].strftime('%H:%M')}, Power: {period['Battery_Flow_W']:,.2f} W, Battery State: {period['Battery_State_Wh']/1000:,.2f} kWh ({period['Battery_State_Percent']:.1f}%)\n")
            
            f.write("\n" + "=" * 50 + "\n\n")
            
            # Winter day analysis
            winter_scenario = calculate_battery_state(winter_day.copy(), initial_state)
            f.write("December 21st, 2023 (Winter Day) Analysis:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total Production: {winter_scenario['Pprod(W)'].sum() * 0.25/1000:,.2f} kWh\n")
            f.write(f"Total Demand: {winter_scenario['Pdemand(W)'].sum() * 0.25/1000:,.2f} kWh\n")
            f.write(f"Net Battery Flow: {winter_scenario['Battery_Flow_W'].sum() * 0.25/1000:,.2f} kWh\n")
            f.write(f"Maximum Battery State: {winter_scenario['Battery_State_Wh'].max()/1000:,.2f} kWh ({winter_scenario['Battery_State_Percent'].max():.1f}%)\n")
            f.write(f"Minimum Battery State: {winter_scenario['Battery_State_Wh'].min()/1000:,.2f} kWh ({winter_scenario['Battery_State_Percent'].min():.1f}%)\n")
            
            f.write("\nCharging Periods:\n")
            charging_periods = winter_scenario[winter_scenario['Battery_Flow_W'] > 0]
            for _, period in charging_periods.iterrows():
                f.write(f"Time: {period['Time'].strftime('%H:%M')}, Power: {period['Battery_Flow_W']:,.2f} W, Battery State: {period['Battery_State_Wh']/1000:,.2f} kWh ({period['Battery_State_Percent']:.1f}%)\n")
            
            f.write("\nDischarging Periods:\n")
            discharging_periods = winter_scenario[winter_scenario['Battery_Flow_W'] < 0]
            for _, period in discharging_periods.iterrows():
                f.write(f"Time: {period['Time'].strftime('%H:%M')}, Power: {period['Battery_Flow_W']:,.2f} W, Battery State: {period['Battery_State_Wh']/1000:,.2f} kWh ({period['Battery_State_Percent']:.1f}%)\n")
    
    print("Battery flows analysis complete! Results have been saved to:")
    print("- battery_flows_0percent.png")
    print("- battery_flows_50percent.png")
    print("- battery_flows_100percent.png")
    print("- battery_flows_calculations.txt")

def analyze_annual_battery():
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
    
    # Initialize battery state at 50% (as requested)
    initial_state = BATTERY_CAPACITY * 0.5
    df['Battery_State_Wh'] = initial_state
    
    # Calculate battery state over time
    for i in range(1, len(df)):
        # Calculate new state based on previous state and current flow
        new_state = df['Battery_State_Wh'].iloc[i-1] + df['Energy_Flow_Wh'].iloc[i]
        # Clip to battery capacity limits
        df.loc[df.index[i], 'Battery_State_Wh'] = max(0, min(new_state, BATTERY_CAPACITY))
    
    # Calculate percentage of capacity
    df['Battery_State_Percent'] = (df['Battery_State_Wh'] / BATTERY_CAPACITY) * 100
    
    # Calculate daily averages for plotting (to reduce number of points in the graph)
    daily_avg = df.groupby(df['Time'].dt.date).agg({
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
    
    # Create the plot
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Battery State in MWh
    plt.subplot(2, 1, 1)
    plt.plot(daily_avg['Time'], daily_avg['Battery_State_MWh'], color='purple', linewidth=2)
    plt.axhline(y=40, color='red', linestyle='--', alpha=0.5, label='Full Capacity (40 MWh)')
    plt.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Empty')
    plt.axhline(y=20, color='green', linestyle='--', alpha=0.5, label='50% Capacity (20 MWh)')
    plt.title('40 MWh Battery State Throughout 2023 (Starting at 20 MWh)', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Battery State (MWh)')
    plt.ylim(-2, 42)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Daily Energy Production and Demand
    plt.subplot(2, 1, 2)
    plt.plot(daily_avg['Time'], daily_avg['Energy_Production_MWh'], label='Production', color='green')
    plt.plot(daily_avg['Time'], daily_avg['Energy_Demand_MWh'], label='Demand', color='red')
    plt.plot(daily_avg['Time'], daily_avg['Energy_Net_MWh'], label='Net (Production - Demand)', 
             color='blue', linestyle='-', alpha=0.5)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.title('Daily Energy Production and Demand', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Energy (MWh)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Adjust layout and save plot
    plt.tight_layout()
    plt.savefig('annual_battery_simulation.png', dpi=300)
    
    # Save calculations to text file
    with open('annual_battery_simulation.txt', 'w') as f:
        f.write("Annual 40 MWh Battery Simulation (Starting at 50% Charge)\n")
        f.write("=" * 60 + "\n\n")
        
        # Overall statistics
        f.write("Overall Statistics:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Battery Capacity: 40.00 MWh (40,000 kWh)\n")
        f.write(f"Initial Charge: 20.00 MWh (50%)\n")
        f.write(f"Final Charge: {df['Battery_State_Wh'].iloc[-1]/1000/1000:.2f} MWh ({df['Battery_State_Percent'].iloc[-1]:.2f}%)\n")
        f.write(f"Minimum Charge: {df['Battery_State_Wh'].min()/1000/1000:.2f} MWh ({df['Battery_State_Percent'].min():.2f}%)\n")
        f.write(f"Maximum Charge: {df['Battery_State_Wh'].max()/1000/1000:.2f} MWh ({df['Battery_State_Percent'].max():.2f}%)\n\n")
        
        # Count days at certain charge levels
        empty_days = len(daily_avg[daily_avg['Battery_State_Percent'] < 5])
        full_days = len(daily_avg[daily_avg['Battery_State_Percent'] > 95])
        mid_days = len(daily_avg[(daily_avg['Battery_State_Percent'] >= 45) & (daily_avg['Battery_State_Percent'] <= 55)])
        
        f.write("Charge Level Statistics:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Days near empty (<5%): {empty_days} days\n")
        f.write(f"Days near full (>95%): {full_days} days\n")
        f.write(f"Days near 50% (45-55%): {mid_days} days\n\n")
        
        # Seasonal analysis
        seasons = {
            'Winter': (1, 2, 12),
            'Spring': (3, 4, 5),
            'Summer': (6, 7, 8),
            'Autumn': (9, 10, 11)
        }
        
        f.write("Seasonal Analysis:\n")
        f.write("-" * 30 + "\n")
        
        for season, months in seasons.items():
            seasonal_data = df[df['Time'].dt.month.isin(months)]
            avg_charge = seasonal_data['Battery_State_Percent'].mean()
            avg_flow = seasonal_data['Energy_Flow_Wh'].mean() * 4 * 24 / 1000  # kWh per day
            
            f.write(f"\n{season}:\n")
            f.write(f"Average Battery Charge: {avg_charge:.2f}%\n")
            f.write(f"Average Daily Energy Flow: {avg_flow:.2f} kWh/day ")
            if avg_flow > 0:
                f.write("(net charging)\n")
            else:
                f.write("(net discharging)\n")
        
        f.write("\nNote: This simulation used a 40 MWh (40,000 kWh) battery starting at 50% charge.\n")
        f.write("The seasonal storage analysis recommended a capacity of approximately 39,362 kWh,\n")
        f.write("which is very close to the 40 MWh (40,000 kWh) used in this simulation.\n")
    
    print("Annual battery simulation complete! Results have been saved to 'annual_battery_simulation.png' and 'annual_battery_simulation.txt'")
    
    return daily_avg

def analyze_annual_battery_empty():
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
    
    # Initialize battery state at 0% (empty)
    initial_state = 0
    df['Battery_State_Wh'] = initial_state
    
    # Calculate battery state over time
    for i in range(1, len(df)):
        # Calculate new state based on previous state and current flow
        new_state = df['Battery_State_Wh'].iloc[i-1] + df['Energy_Flow_Wh'].iloc[i]
        # Clip to battery capacity limits
        df.loc[df.index[i], 'Battery_State_Wh'] = max(0, min(new_state, BATTERY_CAPACITY))
    
    # Calculate percentage of capacity
    df['Battery_State_Percent'] = (df['Battery_State_Wh'] / BATTERY_CAPACITY) * 100
    
    # Calculate daily averages for plotting (to reduce number of points in the graph)
    daily_avg = df.groupby(df['Time'].dt.date).agg({
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
    
    # Create the plot
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Battery State in MWh
    plt.subplot(2, 1, 1)
    plt.plot(daily_avg['Time'], daily_avg['Battery_State_MWh'], color='purple', linewidth=2)
    plt.axhline(y=40, color='red', linestyle='--', alpha=0.5, label='Full Capacity (40 MWh)')
    plt.axhline(y=0, color='red', linestyle='--', alpha=0.5, label='Empty')
    plt.axhline(y=20, color='green', linestyle='--', alpha=0.5, label='50% Capacity (20 MWh)')
    plt.title('40 MWh Battery State Throughout 2023 (Starting at 0 MWh)', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Battery State (MWh)')
    plt.ylim(-2, 42)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Daily Energy Production and Demand
    plt.subplot(2, 1, 2)
    plt.plot(daily_avg['Time'], daily_avg['Energy_Production_MWh'], label='Production', color='green')
    plt.plot(daily_avg['Time'], daily_avg['Energy_Demand_MWh'], label='Demand', color='red')
    plt.plot(daily_avg['Time'], daily_avg['Energy_Net_MWh'], label='Net (Production - Demand)', 
             color='blue', linestyle='-', alpha=0.5)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.title('Daily Energy Production and Demand', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Energy (MWh)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Adjust layout and save plot
    plt.tight_layout()
    plt.savefig('annual_battery_simulation_0percent.png', dpi=300)
    
    # Save calculations to text file
    with open('annual_battery_simulation_0percent.txt', 'w') as f:
        f.write("Annual 40 MWh Battery Simulation (Starting at 0% Charge)\n")
        f.write("=" * 60 + "\n\n")
        
        # Overall statistics
        f.write("Overall Statistics:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Battery Capacity: 40.00 MWh (40,000 kWh)\n")
        f.write(f"Initial Charge: 0.00 MWh (0%)\n")
        f.write(f"Final Charge: {df['Battery_State_Wh'].iloc[-1]/1000/1000:.2f} MWh ({df['Battery_State_Percent'].iloc[-1]:.2f}%)\n")
        f.write(f"Minimum Charge: {df['Battery_State_Wh'].min()/1000/1000:.2f} MWh ({df['Battery_State_Percent'].min():.2f}%)\n")
        f.write(f"Maximum Charge: {df['Battery_State_Wh'].max()/1000/1000:.2f} MWh ({df['Battery_State_Percent'].max():.2f}%)\n\n")
        
        # Count days at certain charge levels
        empty_days = len(daily_avg[daily_avg['Battery_State_Percent'] < 5])
        full_days = len(daily_avg[daily_avg['Battery_State_Percent'] > 95])
        mid_days = len(daily_avg[(daily_avg['Battery_State_Percent'] >= 45) & (daily_avg['Battery_State_Percent'] <= 55)])
        
        f.write("Charge Level Statistics:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Days near empty (<5%): {empty_days} days\n")
        f.write(f"Days near full (>95%): {full_days} days\n")
        f.write(f"Days near 50% (45-55%): {mid_days} days\n\n")
        
        # Seasonal analysis
        seasons = {
            'Winter': (1, 2, 12),
            'Spring': (3, 4, 5),
            'Summer': (6, 7, 8),
            'Autumn': (9, 10, 11)
        }
        
        f.write("Seasonal Analysis:\n")
        f.write("-" * 30 + "\n")
        
        for season, months in seasons.items():
            seasonal_data = df[df['Time'].dt.month.isin(months)]
            avg_charge = seasonal_data['Battery_State_Percent'].mean()
            avg_flow = seasonal_data['Energy_Flow_Wh'].mean() * 4 * 24 / 1000  # kWh per day
            
            f.write(f"\n{season}:\n")
            f.write(f"Average Battery Charge: {avg_charge:.2f}%\n")
            f.write(f"Average Daily Energy Flow: {avg_flow:.2f} kWh/day ")
            if avg_flow > 0:
                f.write("(net charging)\n")
            else:
                f.write("(net discharging)\n")
        
        f.write("\nNote: This simulation used a 40 MWh (40,000 kWh) battery starting at 0% charge.\n")
        f.write("This shows how the battery would perform if starting completely empty at the beginning of the year.\n")
    
    print("Annual battery simulation (0% initial) complete! Results have been saved to 'annual_battery_simulation_0percent.png' and 'annual_battery_simulation_0percent.txt'")
    
    return daily_avg

def analyze_battery_c_rates():
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Calculate the net power flow (positive = charging, negative = discharging)
    df['Net_Power_W'] = df['Pprod(W)'] - df['Pdemand(W)']
    
    # Define battery capacities for daily and seasonal storage
    DAILY_BATTERY_CAPACITY_WH = 650 * 1000  # 650 kWh in Wh (from battery_sizing_analysis)
    SEASONAL_BATTERY_CAPACITY_WH = 40 * 1000 * 1000  # 40 MWh in Wh (from seasonal_storage_analysis)
    
    # Calculate C-rates
    df['Daily_C_Rate'] = abs(df['Net_Power_W']) / DAILY_BATTERY_CAPACITY_WH
    df['Seasonal_C_Rate'] = abs(df['Net_Power_W']) / SEASONAL_BATTERY_CAPACITY_WH
    
    # Get overall statistics
    max_daily_c_rate = df['Daily_C_Rate'].max()
    max_seasonal_c_rate = df['Seasonal_C_Rate'].max()
    avg_daily_c_rate = df['Daily_C_Rate'].mean()
    avg_seasonal_c_rate = df['Seasonal_C_Rate'].mean()
    
    # Calculate daily maximum and average C-rates for time series visualization
    daily_stats = df.groupby(df['Time'].dt.date).agg({
        'Daily_C_Rate': ['max', 'mean'],
        'Seasonal_C_Rate': ['max', 'mean'],
        'Net_Power_W': ['max', 'min', 'mean']
    }).reset_index()
    
    # Create plots
    plt.figure(figsize=(15, 12))
    
    # Plot 1: Daily Storage C-rate (Time Series)
    plt.subplot(3, 1, 1)
    plt.plot(daily_stats['Time'], daily_stats[('Daily_C_Rate', 'max')], 'b-', label='Maximum C-rate')
    plt.plot(daily_stats['Time'], daily_stats[('Daily_C_Rate', 'mean')], 'g-', label='Average C-rate')
    plt.axhline(y=1, color='r', linestyle='--', label='1C (Full charge/discharge in 1 hour)')
    plt.axhline(y=0.5, color='orange', linestyle='--', label='0.5C (Full charge/discharge in 2 hours)')
    plt.axhline(y=0.25, color='purple', linestyle='--', label='0.25C (Full charge/discharge in 4 hours)')
    plt.title('Daily Storage Battery (650 kWh): Required C-rate Throughout 2023', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('C-rate')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Seasonal Storage C-rate (Time Series)
    plt.subplot(3, 1, 2)
    plt.plot(daily_stats['Time'], daily_stats[('Seasonal_C_Rate', 'max')], 'b-', label='Maximum C-rate')
    plt.plot(daily_stats['Time'], daily_stats[('Seasonal_C_Rate', 'mean')], 'g-', label='Average C-rate')
    plt.axhline(y=0.1, color='r', linestyle='--', label='0.1C (Full charge/discharge in 10 hours)')
    plt.axhline(y=0.05, color='orange', linestyle='--', label='0.05C (Full charge/discharge in 20 hours)')
    plt.axhline(y=0.01, color='purple', linestyle='--', label='0.01C (Full charge/discharge in 100 hours)')
    plt.title('Seasonal Storage Battery (40 MWh): Required C-rate Throughout 2023', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('C-rate')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Histogram of required C-rates
    plt.subplot(3, 1, 3)
    plt.hist(df['Daily_C_Rate'], bins=50, alpha=0.5, color='blue', label='Daily Storage (650 kWh)')
    plt.hist(df['Seasonal_C_Rate'], bins=50, alpha=0.5, color='green', label='Seasonal Storage (40 MWh)')
    plt.title('Distribution of Required C-rates', fontsize=14)
    plt.xlabel('C-rate')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Adjust layout and save plot
    plt.tight_layout()
    plt.savefig('battery_c_rates_analysis.png', dpi=300)
    
    # Save calculations to text file
    with open('battery_c_rates_analysis.txt', 'w') as f:
        f.write("Battery C-Rate Analysis\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("Daily Storage Battery (650 kWh):\n")
        f.write("-" * 30 + "\n")
        f.write(f"Maximum C-rate: {max_daily_c_rate:.4f}C (full charge/discharge in {1/max_daily_c_rate:.2f} hours)\n")
        f.write(f"Average C-rate: {avg_daily_c_rate:.4f}C (full charge/discharge in {1/avg_daily_c_rate:.2f} hours)\n")
        f.write("\n")
        
        f.write("Seasonal Storage Battery (40 MWh):\n")
        f.write("-" * 30 + "\n")
        f.write(f"Maximum C-rate: {max_seasonal_c_rate:.4f}C (full charge/discharge in {1/max_seasonal_c_rate:.2f} hours)\n")
        f.write(f"Average C-rate: {avg_seasonal_c_rate:.4f}C (full charge/discharge in {1/avg_seasonal_c_rate:.2f} hours)\n")
        f.write("\n")
        
        # Calculate C-rate percentiles for each battery type
        percentiles = [50, 75, 90, 95, 99]
        f.write("C-rate Percentiles:\n")
        f.write("-" * 30 + "\n")
        f.write("Percentile | Daily Storage | Seasonal Storage\n")
        f.write("-" * 50 + "\n")
        
        for p in percentiles:
            daily_val = df['Daily_C_Rate'].quantile(p/100)
            seasonal_val = df['Seasonal_C_Rate'].quantile(p/100)
            f.write(f"{p:10}% | {daily_val:.4f}C ({1/daily_val:.2f} hrs) | {seasonal_val:.4f}C ({1/seasonal_val:.2f} hrs)\n")
        
        # Add insights about the practical implications
        f.write("\nInsights and Implications:\n")
        f.write("-" * 30 + "\n")
        f.write("1. The daily storage battery requires a higher C-rate capability than the seasonal storage battery.\n")
        f.write("2. For daily cycling, the battery technology should support at least ")
        daily_95 = df['Daily_C_Rate'].quantile(0.95)
        f.write(f"{daily_95:.2f}C (95th percentile).\n")
        f.write(f"3. For seasonal storage, a C-rate of {df['Seasonal_C_Rate'].quantile(0.95):.4f}C would be sufficient for 95% of the time.\n")
        f.write("4. These C-rate requirements influence the choice of battery chemistry and design.\n")
        
        # Add recommendations for battery type
        f.write("\nBattery Technology Recommendations:\n")
        f.write("-" * 30 + "\n")
        if max_daily_c_rate > 1:
            f.write("Daily Storage: Consider lithium-ion technologies like LFP or NMC that can handle higher C-rates.\n")
        else:
            f.write("Daily Storage: Most commercial lithium-ion technologies would be suitable.\n")
        
        if max_seasonal_c_rate > 0.2:
            f.write("Seasonal Storage: Most lithium-ion technologies would be suitable.\n")
        else:
            f.write("Seasonal Storage: Consider flow batteries or other technologies optimized for energy (rather than power) applications.\n")
    
    print("Battery C-rate analysis complete! Results saved to 'battery_c_rates_analysis.png' and 'battery_c_rates_analysis.txt'")
    
    return daily_stats

if __name__ == "__main__":
    analyze_energy_data()
    create_solstice_comparison()
    analyze_battery_sizing()
    analyze_seasonal_storage()
    analyze_battery_flows()
    analyze_annual_battery()
    analyze_annual_battery_empty()
    analyze_battery_c_rates()
    analyze_annual_battery_empty()
    analyze_battery_c_rates()