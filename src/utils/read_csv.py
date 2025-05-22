import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import RAW_DATA_PATH, CLEANED_DATA_PATH, ensure_directories

def read_csv_file():
    """Read and clean the raw Aardehuizen dataset."""
    ensure_directories()
    
    # Define the CSV file path
    csv_file = RAW_DATA_PATH
    
    try:
        df = pd.read_csv(csv_file, 
                        sep=',',  
                        usecols=[0, 1, 2, 3],  
                        names=['Time', 'Pprod(W)', 'Pdemand(W)', 'Pimb'],  
                        skiprows=1)  
        

        df = df[~df['Time'].str.contains('Time Interval|Energy Production|Energy Demand|Total Energy Imbalance|% Overproduction', na=False)]
        
        # Convert Time column to datetime
        df['Time'] = pd.to_datetime(df['Time'], format='%d/%m/%Y %H:%M')
        
        # Convert numeric columns to float
        numeric_columns = ['Pprod(W)', 'Pdemand(W)', 'Pimb']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove any rows with NaN values
        df = df.dropna()
        
        # Display basic information about the dataset
        print("\nDataset Information:")
        print("-" * 50)
        print(f"Number of rows: {len(df)}")
        print(f"Number of columns: {len(df.columns)}")
        print("\nColumn names:")
        for col in df.columns:
            print(f"- {col}")
        
        # Display first few rows of the data
        print("\nFirst 5 rows of the data:")
        print("-" * 50)
        print(df.head())
        
        # Display basic statistics
        print("\nBasic statistics:")
        print("-" * 50)
        print(df.describe())
        
        # Save the cleaned data to a new CSV file
        # Save the cleaned data
        df.to_csv(CLEANED_DATA_PATH, index=False)
        print(f"\nCleaned data has been saved to: {CLEANED_DATA_PATH}")
        
        return df
        
    except FileNotFoundError:
        print(f"Error: Could not find the CSV file at {csv_file}")
        return None
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return None

if __name__ == "__main__":
    df = read_csv_file() 