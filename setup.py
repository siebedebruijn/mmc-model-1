import os
import sys
from pathlib import Path

def setup_project_structure():
    """Set up the initial project structure with required directories."""
    # Get the project root directory
    project_root = Path(__file__).parent
    
    # Define directories to create
    directories = [
        project_root / 'outputs' / 'data',
        project_root / 'outputs' / 'images',
        project_root / 'outputs' / 'reports',
        project_root / 'src' / 'data'
    ]
    
    # Create directories if they don't exist
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")
    
    print("\nProject structure setup complete!")
    print("\nDirectory structure created:")
    print("outputs/")
    print("├── data/    (for processed data files)")
    print("├── images/  (for generated plots)")
    print("└── reports/ (for analysis reports)")
    print("src/")
    print("└── data/    (for raw data files)")

if __name__ == "__main__":
    setup_project_structure()
