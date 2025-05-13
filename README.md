# MCC Model: Energy Analysis and Battery Sizing

This repository contains Python scripts for analyzing energy production and demand data, visualizing seasonal and daily trends, and simulating battery storage requirements for a microgrid or similar system.

## Contents
- `analyze_energy.py`: Main script for energy analysis, visualization, and battery/storage calculations.
- `calculate_model.py`: (Describe its purpose here if needed)
- `read_csv.py`: (Describe its purpose here if needed)
- `requirements.txt`: Python dependencies for running the analysis.
- `.gitignore`: Excludes data, output, and temporary files from version control.

## What the Code Does
- **Energy Analysis**: Calculates daily and seasonal energy production and demand from a CSV dataset.
- **Visualization**: Generates plots for daily/seasonal energy trends and battery operation.
- **Battery Sizing**: Simulates battery charge/discharge for summer and winter days, and recommends battery sizes.
- **Solstice Comparison**: Compares energy flows on June 1st and December 21st.

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
- `energy_analysis.png`, `battery_sizing_analysis.png`, `seasonal_storage_analysis.png`, `solstice_comparison.png`, `battery_flows_0percent.png`, etc.: Plots of the analysis
- `energy_analysis.txt`, `battery_sizing_calculations.txt`, `seasonal_storage_calculations.txt`, `battery_flows_calculations.txt`: Text summaries of results

### 5. Script Order
The main script (`analyze_energy.py`) runs all analyses in the correct order. You do not need to run the other scripts separately unless you want to customize or extend the analysis.

## Notes
- The `.gitignore` is set to exclude `.txt` and `.png` output files (except `requirements.txt`).
- If you want to analyze different days or change battery parameters, edit `analyze_energy.py` as needed.