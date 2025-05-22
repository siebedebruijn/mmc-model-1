import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.config import CLEANED_DATA_PATH, IMAGES_DIR, REPORTS_DIR
from utils.config import DAILY_BATTERY_CAPACITY_WH, SEASONAL_BATTERY_CAPACITY_WH
import os

def analyze_load_duration_curves():
    """Create load duration curves for different battery scenarios."""
    # Read the cleaned data
    df = pd.read_csv(CLEANED_DATA_PATH)
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Use DAILY_BATTERY_CAPACITY_WH from config.py
    # Convert power to absolute values
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Calculate net load (positive means demand exceeds production)
    df['Net_Load_No_Battery'] = df['Pdemand(W)'] - df['Pprod(W)']
    
    # Sort values in descending order for duration curves
    sorted_no_battery = np.sort(df['Net_Load_No_Battery'].values)[::-1]
    
    # Create hour points for x-axis (0-8760 hours)
    # Convert 15-minute intervals to hours (multiply by 0.25)
    x_points = np.arange(len(sorted_no_battery)) * 0.25
    
    # Simulate daily battery operation
    df['Battery_State_Daily'] = 0.0
    df['Net_Load_Daily_Battery'] = df['Net_Load_No_Battery'].copy()
    
    # Reset battery state at the start of each day
    df['DayOfYear'] = df['Time'].dt.dayofyear
    
    # Calculate battery state and net load with daily battery
    for i in range(1, len(df)):
        # Reset battery at start of day
        if df['DayOfYear'].iloc[i] != df['DayOfYear'].iloc[i-1]:
            df.loc[df.index[i], 'Battery_State_Daily'] = 0.0
            continue
            
        # Calculate energy surplus/deficit
        power_difference = df['Pprod(W)'].iloc[i] - df['Pdemand(W)'].iloc[i]
        energy_flow = power_difference * 0.25  # 15-minute intervals
        current_state = df['Battery_State_Daily'].iloc[i-1]
        new_state = current_state + energy_flow
        
        # Apply battery capacity constraints
        df.loc[df.index[i], 'Battery_State_Daily'] = max(0, min(new_state, DAILY_BATTERY_CAPACITY_WH))
        
        # Calculate how much power was actually absorbed/provided by the battery
        if power_difference > 0:  # Excess production (charging)
            if current_state >= DAILY_BATTERY_CAPACITY_WH:  # Battery full
                absorbed_power = 0
            else:
                absorbed_power = min(power_difference, (DAILY_BATTERY_CAPACITY_WH - current_state) / 0.25)
            df.loc[df.index[i], 'Net_Load_Daily_Battery'] = -(power_difference - absorbed_power)
        else:  # Power deficit (discharging)
            if current_state <= 0:  # Battery empty
                provided_power = 0
            else:
                provided_power = min(-power_difference, current_state / 0.25)
            df.loc[df.index[i], 'Net_Load_Daily_Battery'] = power_difference + provided_power

    # Simulate seasonal battery operation
    df['Battery_State_Seasonal'] = SEASONAL_BATTERY_CAPACITY_WH * 0.5  # Start at 50%
    df['Net_Load_Seasonal_Battery'] = df['Net_Load_No_Battery'].copy()
    
    # Calculate battery state and net load with seasonal battery
    for i in range(1, len(df)):
        # Calculate energy surplus/deficit
        power_difference = df['Pprod(W)'].iloc[i] - df['Pdemand(W)'].iloc[i]
        energy_flow = power_difference * 0.25  # 15-minute intervals
        current_state = df['Battery_State_Seasonal'].iloc[i-1]
        new_state = current_state + energy_flow
        
        # Apply battery capacity constraints
        df.loc[df.index[i], 'Battery_State_Seasonal'] = max(0, min(new_state, SEASONAL_BATTERY_CAPACITY_WH))
        
        # Calculate how much power was actually absorbed/provided by the battery
        if power_difference > 0:  # Excess production (charging)
            if current_state >= SEASONAL_BATTERY_CAPACITY_WH:  # Battery full
                absorbed_power = 0
            else:
                absorbed_power = min(power_difference, (SEASONAL_BATTERY_CAPACITY_WH - current_state) / 0.25)
            df.loc[df.index[i], 'Net_Load_Seasonal_Battery'] = -(power_difference - absorbed_power)
        else:  # Power deficit (discharging)
            if current_state <= 0:  # Battery empty
                provided_power = 0
            else:
                provided_power = min(-power_difference, current_state / 0.25)
            df.loc[df.index[i], 'Net_Load_Seasonal_Battery'] = power_difference + provided_power

    # Sort values for duration curves
    sorted_daily = np.sort(df['Net_Load_Daily_Battery'].values)[::-1]
    sorted_seasonal = np.sort(df['Net_Load_Seasonal_Battery'].values)[::-1]
    
    # Create plots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))
    
    # Plot 1: No Battery
    ax1.plot(x_points, sorted_no_battery/1000, color='red', linewidth=2)
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlabel('Hours per Year')
    ax1.set_ylabel('Net Load (kW)')
    ax1.set_title('Load Duration Curve - No Battery Storage')
    
    # Plot 2: Daily Battery
    ax2.plot(x_points, sorted_daily/1000, color='blue', linewidth=2)
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlabel('Hours per Year')
    ax2.set_ylabel('Net Load (kW)')
    ax2.set_title(f'Load Duration Curve - Daily Battery Storage ({DAILY_BATTERY_CAPACITY_WH/1000:.0f} kWh)')
    
    # Plot 3: Seasonal Battery
    ax3.plot(x_points, sorted_seasonal/1000, color='green', linewidth=2)
    ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax3.grid(True, alpha=0.3)
    ax3.set_xlabel('Hours per Year')
    ax3.set_ylabel('Net Load (kW)')
    ax3.set_title(f'Load Duration Curve - Seasonal Battery Storage ({SEASONAL_BATTERY_CAPACITY_WH/1000/1000:.0f} MWh)')
    
    # Add explanatory text to each plot
    for ax in [ax1, ax2, ax3]:
        ax.text(0.02, 0.98, 'Grid Import →', 
                transform=ax.transAxes, va='top', fontsize=10)
        ax.text(0.02, 0.02, '← Grid Export', 
                transform=ax.transAxes, va='bottom', fontsize=10)
    
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(IMAGES_DIR, 'load_duration_curves_separate.png'), dpi=300, bbox_inches='tight')
    
    # Also create a combined plot for comparison
    plt.figure(figsize=(12, 8))
    plt.plot(x_points, sorted_no_battery/1000, label='No Battery', color='red', linewidth=2)
    plt.plot(x_points, sorted_daily/1000, label=f'Daily Battery ({DAILY_BATTERY_CAPACITY_WH/1000:.0f} kWh)', 
             color='blue', linewidth=2)
    plt.plot(x_points, sorted_seasonal/1000, label=f'Seasonal Battery ({SEASONAL_BATTERY_CAPACITY_WH/1000/1000:.0f} MWh)', 
             color='green', linewidth=2)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.grid(True, alpha=0.3)
    plt.xlabel('Duration (hours)')
    plt.ylabel('Net Load (kW)')
    plt.title('Load Duration Curves - All Configurations Compared')
    plt.legend()
    
    # Save the combined plot
    plt.savefig(os.path.join(IMAGES_DIR, 'load_duration_curves_combined.png'), dpi=300, bbox_inches='tight')
    
    # Calculate and save statistics
    with open(os.path.join(REPORTS_DIR, 'load_duration_analysis.txt'), 'w') as f:
        f.write("Load Duration Curve Analysis\n")
        f.write("=" * 50 + "\n\n")
        
        # Calculate total annual energy production and demand
        total_production = df['Pprod(W)'].sum() * 0.25 / 1000000  # Convert Wh to MWh
        total_demand = df['Pdemand(W)'].sum() * 0.25 / 1000000  # Convert Wh to MWh
        
        f.write("Annual Energy Overview:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total Energy Production: {total_production:.2f} MWh\n")
        f.write(f"Total Energy Demand: {total_demand:.2f} MWh\n\n")
        
        # Create a table header for the KPIs
        f.write("\nKey Performance Indicators:\n")
        f.write("-" * 90 + "\n")
        f.write(f"{'Metric':<30} | {'No Battery':^18} | {'Daily Battery':^18} | {'Seasonal Battery':^18}\n")
        f.write("-" * 90 + "\n")
        
        scenarios = {
            'No Battery': sorted_no_battery,
            'Daily Battery': sorted_daily,
            'Seasonal Battery': sorted_seasonal
        }
        
        # Calculate KPIs for each scenario
        kpis = {}
        for name, data in scenarios.items():
            positive_loads = data[data > 0]  # Grid imports
            negative_loads = data[data < 0]  # Grid exports
            
            # Convert from W to MWh (15-minute intervals)
            total_import = positive_loads.sum() * 0.25 / 1000000
            total_export = -negative_loads.sum() * 0.25 / 1000000
            
            kpis[name] = {
                'Peak Import (kW)': data.max()/1000,
                'Peak Export (kW)': -data.min()/1000,
                'Annual Grid Import (MWh)': total_import,
                'Annual Grid Export (MWh)': total_export,
                'Grid Dependency (hours)': len(positive_loads) * 0.25,
                'Self-Sufficiency (%)': (1 - total_import/total_demand) * 100,
                'Self-Consumption (%)': (1 - total_export/total_production) * 100
            }
        
        # Write KPIs in table format
        metrics = [
            'Peak Import (kW)',
            'Peak Export (kW)',
            'Annual Grid Import (MWh)',
            'Annual Grid Export (MWh)',
            'Grid Dependency (hours)',
            'Self-Sufficiency (%)',
            'Self-Consumption (%)'
        ]
        
        for metric in metrics:
            f.write(f"{metric:<30} | {kpis['No Battery'][metric]:>18.1f} | {kpis['Daily Battery'][metric]:>18.1f} | {kpis['Seasonal Battery'][metric]:>18.1f}\n")
        
        f.write("-" * 90 + "\n\n")
        
        # Add definitions
        f.write("\nMetric Definitions:\n")
        f.write("-" * 30 + "\n")
        f.write("Peak Import: Maximum power drawn from the grid\n")
        f.write("Peak Export: Maximum power sent to the grid\n")
        f.write("Grid Dependency: Hours per year when power is imported from the grid\n")
        f.write("Self-Sufficiency: Percentage of demand met by local generation\n")
        f.write("Self-Consumption: Percentage of production consumed locally\n")
    
    print("Load duration curve analysis complete! Results saved to:")
    print(f"- {os.path.join(IMAGES_DIR, 'load_duration_curves.png')}")
    print(f"- {os.path.join(REPORTS_DIR, 'load_duration_analysis.txt')}")
    
    return df
