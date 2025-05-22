import os

# Get the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Define paths relative to project root
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, 'outputs')
DATA_DIR = os.path.join(OUTPUTS_DIR, 'data')
IMAGES_DIR = os.path.join(OUTPUTS_DIR, 'images')
REPORTS_DIR = os.path.join(OUTPUTS_DIR, 'reports')

# Data files
CLEANED_DATA_PATH = os.path.join(DATA_DIR, 'cleaned_data.csv')
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, 'src', 'data', 'Aardehuizen_15min_ 2023 MMC dataset.csv')

# Analysis dates
SUMMER_SOLSTICE = '2023-06-01'  # Sample summer day
WINTER_SOLSTICE = '2023-12-21'  # Sample winter day

# Battery configurations
DAILY_BATTERY_CAPACITY_WH = 240 * 1000  # 240 kWh in Wh
SEASONAL_BATTERY_CAPACITY_WH = 40 * 1000 * 1000  # 40 MWh in Wh

def ensure_directories():
    """Create output directories if they don't exist"""
    for directory in [DATA_DIR, IMAGES_DIR, REPORTS_DIR]:
        os.makedirs(directory, exist_ok=True)
