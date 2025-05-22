import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from datetime import datetime, timedelta
import os

def create_daily_energy_animation(date_str=None):
    """
    Create an animation showing how solar production, energy demand, and battery state
    change throughout a specific day. If no date is provided, it uses the summer solstice.
    
    Args:
        date_str: String date in format 'YYYY-MM-DD' or None to use summer solstice
    """
    print("Creating daily energy animation...")
    
    # Read the cleaned data
    df = pd.read_csv('cleaned_data.csv')
    print(f"Loaded data with {len(df)} rows")
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # If no date provided, use summer solstice (or closest available date)
    if not date_str:
        summer_solstice = pd.to_datetime('2023-06-21').date()
        # Find closest date
        unique_dates = df['Time'].dt.date.unique()
        date = min(unique_dates, key=lambda x: abs((x - summer_solstice).days))
        print(f"Using date closest to summer solstice: {date}")
    else:
        date = pd.to_datetime(date_str).date()
        print(f"Using specified date: {date}")
    
    # Filter data for the selected date
    day_data = df[df['Time'].dt.date == date].copy()
    
    if day_data.empty:
        print(f"No data available for date: {date}")
        return
    
    # Add calculated fields
    day_data['Energy_Production_Wh'] = day_data['Pprod(W)'] * 0.25  # 15-minute intervals
    day_data['Energy_Demand_Wh'] = day_data['Pdemand(W)'] * 0.25
    day_data['Energy_Net_Wh'] = day_data['Energy_Production_Wh'] - day_data['Energy_Demand_Wh']
    day_data['Hour'] = day_data['Time'].dt.hour + day_data['Time'].dt.minute/60
    
    # Define battery parameters
    BATTERY_CAPACITY = 231.62 * 1000  # Wh (using the realistic sizing)
    initial_state = 0.5  # Start at 50% charge
    
    # Calculate cumulative battery state
    day_data['Battery_Energy_Wh'] = day_data['Energy_Net_Wh'].cumsum()
    day_data['Battery_Energy_Wh'] += BATTERY_CAPACITY * initial_state
    day_data['Battery_Percentage'] = day_data['Battery_Energy_Wh'] / BATTERY_CAPACITY * 100
    
    # Ensure battery percentage stays within 0-100%
    day_data['Battery_Percentage'] = day_data['Battery_Percentage'].clip(0, 100)
    
    # Create the figure and subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    fig.suptitle(f'Daily Energy Flow Animation: {date}', fontsize=16)
    
    # Initialize lines for power
    power_prod_line, = ax1.plot([], [], 'g-', label='Production (W)')
    power_demand_line, = ax1.plot([], [], 'r-', label='Demand (W)')
    
    # Initialize lines for energy
    energy_prod_line, = ax2.plot([], [], 'g-', label='Production (Wh)')
    energy_demand_line, = ax2.plot([], [], 'r-', label='Demand (Wh)')
    energy_net_line, = ax2.plot([], [], 'b-', label='Net Energy (Wh)')
    
    # Initialize battery state
    battery_line, = ax3.plot([], [], 'b-', linewidth=2, label='Battery State (%)')
    battery_fill = ax3.fill_between([], [], 0, alpha=0.2, color='blue')
    
    # Add vertical lines for sunrise and sunset
    # Find when production exceeds 5% of maximum
    threshold = day_data['Pprod(W)'].max() * 0.05
    producing = day_data[day_data['Pprod(W)'] > threshold]
    
    if not producing.empty:
        sunrise_hour = producing['Hour'].min()
        sunset_hour = producing['Hour'].max()
        
        for ax in [ax1, ax2, ax3]:
            ax.axvline(x=sunrise_hour, color='orange', linestyle='--', alpha=0.5, label='Sunrise')
            ax.axvline(x=sunset_hour, color='navy', linestyle='--', alpha=0.5, label='Sunset')
    
    # Set up the axes
    ax1.set_ylabel('Power (W)')
    ax1.set_title('Instantaneous Power')
    ax1.grid(True)
    ax1.legend(loc='upper right')
    
    ax2.set_ylabel('Energy (Wh)')
    ax2.set_title('Cumulative Energy')
    ax2.grid(True)
    ax2.legend(loc='upper left')
    
    ax3.set_ylabel('Battery State (%)')
    ax3.set_title('Battery State of Charge')
    ax3.set_ylim(0, 100)
    ax3.grid(True)
    ax3.legend(loc='upper right')
    
    ax3.set_xlabel('Hour of Day')
    ax3.set_xlim(0, 24)
    ax3.set_xticks(range(0, 25, 2))
    
    # Add a time indicator line
    time_line = plt.Line2D([0, 0], [0, 1], color='red', linewidth=2, transform=ax1.transAxes)
    ax1.add_line(time_line)
    
    # Text to display current time
    time_text = ax1.text(0.02, 0.95, '', transform=ax1.transAxes, fontsize=12,
                        bbox=dict(facecolor='white', alpha=0.5))
    
    # Animation function
    def animate(i):
        # For the animation, we'll show data up to the i-th hour
        current_hour = i * 0.25  # 15-minute steps
        
        # Get data up to the current time
        mask = day_data['Hour'] <= current_hour
        data_so_far = day_data[mask]
        
        if data_so_far.empty:
            return power_prod_line, power_demand_line, energy_prod_line, energy_demand_line, energy_net_line, battery_line, time_line, time_text
        
        hours = data_so_far['Hour'].values
        
        # Update power lines
        power_prod_line.set_data(hours, data_so_far['Pprod(W)'].values)
        power_demand_line.set_data(hours, data_so_far['Pdemand(W)'].values)
        
        # Update energy lines
        cumulative_prod = data_so_far['Energy_Production_Wh'].cumsum().values
        cumulative_demand = data_so_far['Energy_Demand_Wh'].cumsum().values
        
        energy_prod_line.set_data(hours, cumulative_prod)
        energy_demand_line.set_data(hours, cumulative_demand)
        energy_net_line.set_data(hours, cumulative_prod - cumulative_demand)
        
        # Update battery state
        battery_line.set_data(hours, data_so_far['Battery_Percentage'].values)
        
        # Update the fill for the battery
        # First need to remove old fill then create new one
        for coll in ax3.collections:
            if coll != battery_fill:
                continue
            coll.remove()
        
        ax3.fill_between(hours, 0, data_so_far['Battery_Percentage'].values, 
                        alpha=0.2, color='blue')
        
        # Update time line position
        time_line.set_xdata([current_hour, current_hour])
        
        # Update time text
        hours_int = int(current_hour)
        minutes_int = int((current_hour - hours_int) * 60)
        time_text.set_text(f'Time: {hours_int:02d}:{minutes_int:02d}')
        
        # Adjust y-axis limits if needed
        if len(data_so_far) > 0:
            ax1.set_ylim(0, max(day_data['Pprod(W)'].max(), day_data['Pdemand(W)'].max()) * 1.1)
            ax2.set_ylim(0, max(day_data['Energy_Production_Wh'].cumsum().max(), 
                                day_data['Energy_Demand_Wh'].cumsum().max()) * 1.1)
        
        return power_prod_line, power_demand_line, energy_prod_line, energy_demand_line, energy_net_line, battery_line, time_line, time_text
    
    # Create animation - 96 frames for a full day (15-minute intervals)
    ani = animation.FuncAnimation(fig, animate, frames=97, interval=100, blit=False)
    
    # Save animation
    filename = f"daily_energy_animation_{date}.mp4"
    ani.save(filename, writer='ffmpeg', fps=10, dpi=200)
    
    print(f"Animation saved to: {filename}")
    
    # Also create a static plot showing the full day
    plt.figure(figsize=(12, 10))
    
    # Plot 1: Power
    plt.subplot(3, 1, 1)
    plt.plot(day_data['Hour'], day_data['Pprod(W)'], 'g-', label='Production (W)')
    plt.plot(day_data['Hour'], day_data['Pdemand(W)'], 'r-', label='Demand (W)')
    
    if not producing.empty:
        plt.axvline(x=sunrise_hour, color='orange', linestyle='--', alpha=0.5, label='Sunrise')
        plt.axvline(x=sunset_hour, color='navy', linestyle='--', alpha=0.5, label='Sunset')
    
    plt.title('Instantaneous Power')
    plt.ylabel('Power (W)')
    plt.grid(True)
    plt.legend()
    
    # Plot 2: Energy
    plt.subplot(3, 1, 2)
    plt.plot(day_data['Hour'], day_data['Energy_Production_Wh'].cumsum(), 'g-', label='Production (Wh)')
    plt.plot(day_data['Hour'], day_data['Energy_Demand_Wh'].cumsum(), 'r-', label='Demand (Wh)')
    plt.plot(day_data['Hour'], day_data['Energy_Net_Wh'].cumsum(), 'b-', label='Net Energy (Wh)')
    
    if not producing.empty:
        plt.axvline(x=sunrise_hour, color='orange', linestyle='--', alpha=0.5, label='Sunrise')
        plt.axvline(x=sunset_hour, color='navy', linestyle='--', alpha=0.5, label='Sunset')
    
    plt.title('Cumulative Energy')
    plt.ylabel('Energy (Wh)')
    plt.grid(True)
    plt.legend()
    
    # Plot 3: Battery State
    plt.subplot(3, 1, 3)
    plt.plot(day_data['Hour'], day_data['Battery_Percentage'], 'b-', linewidth=2, label='Battery State (%)')
    plt.fill_between(day_data['Hour'], 0, day_data['Battery_Percentage'], alpha=0.2, color='blue')
    
    if not producing.empty:
        plt.axvline(x=sunrise_hour, color='orange', linestyle='--', alpha=0.5, label='Sunrise')
        plt.axvline(x=sunset_hour, color='navy', linestyle='--', alpha=0.5, label='Sunset')
    
    plt.title('Battery State of Charge')
    plt.ylabel('Battery State (%)')
    plt.ylim(0, 100)
    plt.xlabel('Hour of Day')
    plt.xlim(0, 24)
    plt.xticks(range(0, 25, 2))
    plt.grid(True)
    plt.legend()
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.suptitle(f'Daily Energy Flow: {date}', fontsize=16)
    
    # Save static plot
    static_filename = f"daily_energy_static_{date}.png"
    plt.savefig(static_filename, dpi=200)
    
    print(f"Static plot saved to: {static_filename}")
    
if __name__ == "__main__":
    try:
        # Create animations for summer and winter solstice
        create_daily_energy_animation('2023-06-21')  # Summer solstice
        create_daily_energy_animation('2023-12-21')  # Winter solstice
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
