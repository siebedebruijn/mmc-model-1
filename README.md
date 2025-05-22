# MCC Model: Energy Analysis and Battery Sizing

This repository contains Python scripts for analyzing energy production and demand data, visualizing seasonal and daily trends, and simulating battery storage requirements for a microgrid or similar system.

## Project Structure

```
mmc-model-1/
├── src/
│   ├── analysis/        # Analysis modules
│   ├── visualization/   # Visualization modules
│   ├── utils/          # Utility functions and configuration
│   ├── data/           # Raw data storage
│   └── main.py         # Main execution script
├── outputs/
│   ├── data/           # Processed data files
│   ├── images/         # Generated plots and visualizations
│   └── reports/        # Analysis reports and calculations
├── setup.py            # Project setup script
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Features

- **Data Preprocessing**: Clean and format raw energy data
- **Energy Analysis**: 
  - Daily production and demand patterns
  - Seasonal energy variations
  - Solar production time analysis
- **Battery Sizing**:
  - Daily storage requirements
  - Seasonal storage optimization
  - C-rate analysis
  - Battery state simulation
- **Visualizations**:
  - Energy flow plots
  - Solstice comparisons
  - Battery state simulations
  - Seasonal storage analysis

## Project Setup

1. Clone the repository
2. Create a Python virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run setup script to create required directories:
   ```bash
   python setup.py
   ```
5. Place your raw data in `src/data/` (CSV format)

## How to Run the Code

### 1. Install Dependencies
Make sure you have Python 3.8+ installed. Then, install the required packages:

```bash
pip install -r requirements.txt
```

### Data Requirements

The input data file should be a CSV with the following columns:
- `Time` (datetime format: DD/MM/YYYY HH:MM)
- `Pprod(W)` (power production in Watts)
- `Pdemand(W)` (power demand in Watts)

### Running the Analysis

1. **Preprocess the data**:
   ```bash
   python src/utils/read_csv.py
   ```
   This will:
   - Clean and format the raw data
   - Convert data types appropriately
   - Handle missing values
   - Save processed data to `outputs/data/cleaned_data.csv`

2. **Run the complete analysis**:
Run the main script to execute all analyses:

```bash 
python src/main.py
```

This will generate:
- Daily and seasonal energy analyses
- Battery sizing calculations
- Visualizations and reports

### Output Files

All output files are organized in the `outputs` directory:

**Images** (`outputs/images/`):
- Energy flow visualizations
  - `energy_analysis.png`: Daily production and demand
  - `solstice_comparison.png`: Summer vs winter comparison
  - `seasonal_storage_analysis.png`: Seasonal patterns
- Battery analysis
  - `battery_sizing_analysis.png`: Capacity requirements
  - `battery_flows_*.png`: State simulations
  - `battery_c_rates_analysis.png`: Power requirements
  - `realistic_battery_sizing.png`: Time-based analysis

**Reports** (`outputs/reports/`):
- Analysis summaries
  - `energy_analysis.txt`: Overall statistics
  - `seasonal_storage_calculations.txt`: Storage requirements
  - `solar_time_battery_sizing_report.md`: Detailed findings
- Battery calculations
  - `battery_sizing_calculations.txt`: Capacity analysis
  - `realistic_battery_sizing.txt`: Time-based results

### Configuration

Key settings can be adjusted in `src/utils/config.py`:
- File paths and directories
- Battery parameters
- Analysis timeframes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.