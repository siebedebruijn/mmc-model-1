# MCC Model: Energy Analysis and Battery Sizing

This repository contains Python scripts for analyzing energy production and demand data, visualizing seasonal and daily trends, and simulating battery storage requirements for a microgrid or similar system.

## Contents
- `analyze_energy.py`: Main script for energy analysis, visualization, and battery/storage calculations.
- `read_csv.py`: Data preprocessing script that imports and cleans the Aardehuizen dataset.
- `requirements.txt`: Python dependencies for running the analysis.
- `.gitignore`: Excludes data, output, and temporary files from version control.

## What the Code Does
- **Data Preprocessing**: Cleans and formats raw energy data from the Aardehuizen dataset.
- **Energy Analysis**: Calculates daily and seasonal energy production and demand patterns.
- **Visualization**: Generates plots for daily/seasonal energy trends and battery operation.
- **Battery Sizing**: Simulates battery charge/discharge for different scenarios and recommends optimal battery capacities.
- **Seasonal Storage**: Analyzes seasonal energy imbalances and required storage capacity.
- **C-Rate Analysis**: Calculates power requirements and C-rates for different storage applications.
- **Solstice Comparison**: Compares energy flows on summer and winter solstice days.

## How to Run the Code

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data
Place your cleaned data file as `cleaned_data.csv` in the project directory. The CSV should have at least these columns:
- `Time` (datetime)
- `Pprod(W)` (production in Watts)
- `Pdemand(W)` (demand in Watts)

### 2. Run the Data Preprocessing
First, run the preprocessing script to convert the raw Aardehuizen dataset into a clean format:

```bash
python read_csv.py
```

This script performs several important tasks:
- Imports the raw `Aardehuizen_15min_ 2023 MMC dataset.csv` file
- Cleans and formats the time series data
- Converts text data to the appropriate numerical formats
- Handles missing or inconsistent values
- Saves the processed data as `cleaned_data.csv`

### 3. Run the Main Analysis
Run the main script to generate all analyses and plots:

```bash
python analyze_energy.py
```

This will:
- Analyze daily and seasonal energy
- Create visualizations (`.png` files)
- Output calculation summaries (`.txt` files)

### 4. Output Files
The analysis generates multiple visualization and data files:

**Visualization Files (.png):**
- `energy_analysis.png`: Daily energy production and demand trends
- `solstice_comparison.png`: Comparison of energy flows on summer and winter days
- `battery_sizing_analysis.png`: Battery capacity sizing analysis
- `seasonal_storage_analysis.png`: Seasonal storage requirement visualization
- `battery_flows_*.png`: Battery state simulations with different initial charge levels
- `annual_battery_simulation.png`: Year-long 40 MWh battery state simulation (50% initial)
- `annual_battery_simulation_0percent.png`: Year-long simulation starting with empty battery
- `battery_c_rates_analysis.png`: Required C-rates for daily and seasonal storage

**Data Summary Files (.txt):**
- `energy_analysis.txt`: Summary of overall energy statistics
- `battery_sizing_calculations.txt`: Detailed battery capacity requirements
- `seasonal_storage_calculations.txt`: Seasonal energy imbalance analysis
- `battery_flows_calculations.txt`: Battery operation statistics for sample days
- `annual_battery_simulation.txt`: Annual cycle statistics for 40 MWh battery
- `annual_battery_simulation_0percent.txt`: Analysis of battery starting at 0% charge
- `battery_c_rates_analysis.txt`: Analysis of required charge/discharge rates

### 5. Script Order
The main script (`analyze_energy.py`) runs all analyses in the correct order. You do not need to run the other scripts separately unless you want to customize or extend the analysis.

## Notes
- The `.gitignore` is set to exclude `.txt` and `.png` output files (except `requirements.txt`).
- If you want to analyze different days or change battery parameters, edit `analyze_energy.py` as needed.