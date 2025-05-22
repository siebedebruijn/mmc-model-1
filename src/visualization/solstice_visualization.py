import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import (
    CLEANED_DATA_PATH, 
    IMAGES_DIR,
    SUMMER_SOLSTICE,
    WINTER_SOLSTICE
)

def create_solstice_comparison():
    """Create a comparison of energy patterns between summer and winter solstice."""
    # Read the cleaned data
    df = pd.read_csv(CLEANED_DATA_PATH)
    
    # Convert Time to datetime
    df['Time'] = pd.to_datetime(df['Time'])
    
    # Convert negative production values to positive
    df['Pprod(W)'] = df['Pprod(W)'].abs()
    
    # Filter for summer and winter solstice
    summer_day = df[df['Time'].dt.date == pd.to_datetime(SUMMER_SOLSTICE).date()]
    winter_day = df[df['Time'].dt.date == pd.to_datetime(WINTER_SOLSTICE).date()]
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Plot Summer Day
    plt.subplot(2, 1, 1)
    plt.plot(summer_day['Time'].dt.hour + summer_day['Time'].dt.minute/60,
             summer_day['Pprod(W)'], label='Production', color='green')
    plt.plot(summer_day['Time'].dt.hour + summer_day['Time'].dt.minute/60,
             summer_day['Pdemand(W)'], label='Demand', color='red')
    plt.title(f'Summer Day ({SUMMER_SOLSTICE}) - Production and Demand')
    plt.xlabel('Hour of Day')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.grid(True)
    
    # Plot Winter Day
    plt.subplot(2, 1, 2)
    plt.plot(winter_day['Time'].dt.hour + winter_day['Time'].dt.minute/60,
             winter_day['Pprod(W)'], label='Production', color='green')
    plt.plot(winter_day['Time'].dt.hour + winter_day['Time'].dt.minute/60,
             winter_day['Pdemand(W)'], label='Demand', color='red')
    plt.title(f'Winter Day ({WINTER_SOLSTICE}) - Production and Demand')
    plt.xlabel('Hour of Day')
    plt.ylabel('Power (W)')
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGES_DIR, 'solstice_comparison.png'))
    plt.close()
    
    print(f"Solstice comparison graph has been saved to {os.path.join(IMAGES_DIR, 'solstice_comparison.png')}")
    
    return {'summer_day': summer_day, 'winter_day': winter_day}
