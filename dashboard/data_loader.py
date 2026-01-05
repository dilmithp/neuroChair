import pandas as pd
import os
import numpy as np

# Path to datasets - cross-platform detection
# Get the directory where this file is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)  # Go up one level from dashboard/

# Try to find Datasets in common locations
possible_paths = [
    os.path.join(PROJECT_ROOT, "Datasets"),  # Project root/Datasets (most reliable)
    "/app/Datasets",  # Docker
    os.path.join(SCRIPT_DIR, "..", "Datasets"),  # Relative from dashboard
    "Datasets",  # Current working directory
]

DATASET_PATH = None
for p in possible_paths:
    if os.path.exists(p):
        DATASET_PATH = p
        print(f"Found Datasets at: {p}")
        break

if DATASET_PATH is None:
    print(f"Warning: Datasets folder not found! Checked: {possible_paths}")
    DATASET_PATH = os.path.join(PROJECT_ROOT, "Datasets")  # Default

def load_user_data(user_id="U01"):
    """
    Load historical data for a specific user from CSV files.
    """
    try:
        # Load features file
        features_file = os.path.join(DATASET_PATH, "posture_features.csv")
        if not os.path.exists(features_file):
            print(f"Dataset not found at {features_file}")
            return None

        df = pd.read_csv(features_file)
        
        # Filter for specific user
        user_df = df[df['User_ID'] == user_id].copy()
        
        if user_df.empty:
            return None
            
        return user_df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def get_user_stats(user_id="U01"):
    """
    Get aggregated statistics for the user.
    """
    df = load_user_data(user_id)
    if df is None:
        return {
            "stress_avg": 5.0,
            "posture_avg": 70,
            "sitting_hours": 4.5,
            "breaks": 3
        }

    # Calculate actual stats from CSV
    # Using 'Posture_Class' (0-3) to estimate %: 0=Good(100%), 1=Fair(75%), 2=Poor(50%), 3=Bad(25%)
    posture_map = {0: 95, 1: 75, 2: 50, 3: 25}
    df['Posture_Score_Est'] = df['Posture_Class'].map(posture_map)
    
    # Stress estimation (mock from features if not explicit)
    stats = {
        "stress_avg": round(np.random.uniform(3, 7), 1), # Mock for now as CSV lacks stress col
        "posture_avg": int(df['Posture_Score_Est'].mean()),
        "sitting_hours": 5.2, # Constant for presentation or calc from rows * duration
        "breaks": 4
    }
    
    return stats

def get_recent_history(user_id="U01", limit=10):
    """
    Get recent data points for charts.
    """
    df = load_user_data(user_id)
    if df is None:
        return []
        
    # Convert to list of dicts for the dashboard
    data = []
    
    # Use last 'limit' rows
    recent = df.tail(limit)
    
    for _, row in recent.iterrows():
        posture_score = {0: 95, 1: 75, 2: 50, 3: 25}.get(row['Posture_Class'], 70)
        
        data.append({
            "stress_level": np.random.randint(3, 8), # Mock
            "posture_score": posture_score,
            "hrv": np.random.randint(60, 90),
            "gsr": round(row['FSR_Left'] / 1000, 2) # Proxy using FSR
        })
        
    return data
