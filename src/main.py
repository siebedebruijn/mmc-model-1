import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import ensure_directories
from analysis.daily_energy_analysis import analyze_daily_energy
from analysis.storage_analysis import analyze_seasonal_storage
from analysis.battery_analysis import analyze_battery_sizing
from analysis.load_duration_analysis import analyze_load_duration_curves
from visualization.solstice_visualization import create_solstice_comparison

def main():
    """Run all analyses in the correct sequence."""
    # Ensure output directories exist
    ensure_directories()
    
    # Run analyses
    print("Starting energy analysis...")
    daily_totals = analyze_daily_energy()
    
    print("\nCreating solstice comparison...")
    solstice_data = create_solstice_comparison()
    
    print("\nAnalyzing battery sizing requirements...")
    battery_sizing_results = analyze_battery_sizing()
    
    print("\nAnalyzing seasonal storage requirements...")
    seasonal_results = analyze_seasonal_storage()
    
    print("\nGenerating load duration curves...")
    load_duration_results = analyze_load_duration_curves()
    
    print("\nAll analyses complete!")
    
if __name__ == "__main__":
    main()
