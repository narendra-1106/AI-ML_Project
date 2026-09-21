"""
=============================================================================
IPL MATCH WINNER PREDICTION - STAGE 2: DATASET LOADING & PREPROCESSING
=============================================================================
This script loads the IPL matches dataset, inspects its structure, cleans missing
values, standardizes team names across seasons, and prepares features for ML training.
=============================================================================
"""

import pandas as pd
import numpy as np

def load_and_preprocess_data(file_path):
    print("\n--- STEP 1: LOADING DATASET ---")
    # Load dataset using Pandas
    df = pd.read_csv(file_path)
    
    print(f"Dataset Loaded Successfully!")
    print(f"Total Rows (Matches): {df.shape[0]}")
    print(f"Total Columns (Attributes): {df.shape[1]}")
    
    print("\n--- STEP 2: DATASET COLUMNS ---")
    print(list(df.columns))
    
    print("\n--- STEP 3: SAMPLE RECORDS (FIRST 3 ROWS) ---")
    print(df[['season', 'team1', 'team2', 'toss_winner', 'toss_decision', 'match_winner']].head(3))
    
    print("\n--- STEP 4: CHECKING MISSING VALUES ---")
    missing_summary = df[['team1', 'team2', 'toss_winner', 'match_winner']].isnull().sum()
    print("Missing values in core columns:")
    print(missing_summary)
    
    print("\n--- STEP 5: STANDARDIZING TEAM NAMES ---")
    # Standardize team names that changed over IPL seasons
    team_name_mapping = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Kings XI Punjab': 'Punjab Kings',
        'Rising Pune Supergiants': 'Rising Pune Supergiant',
        'Royal Challengers Bengaluru': 'Royal Challengers Bangalore',
        'Deccan Chargers': 'Sunrisers Hyderabad'
    }
    
    # Apply mapping to team columns
    for col in ['team1', 'team2', 'toss_winner', 'match_winner']:
        df[col] = df[col].replace(team_name_mapping)
        
    print("Team names standardized!")
    
    print("\n--- STEP 6: CLEANING INVALID / MISSING RECORDS ---")
    initial_count = len(df)
    
    # Drop records where target (match_winner) or core features are null
    df = df.dropna(subset=['team1', 'team2', 'toss_winner', 'match_winner'])
    
    # Ensure match_winner is either team1 or team2 (filters out abandoned/no-result matches)
    df = df[(df['match_winner'] == df['team1']) | (df['match_winner'] == df['team2'])]
    
    final_count = len(df)
    print(f"Removed {initial_count - final_count} invalid/no-result match records.")
    print(f"Cleaned Dataset Size: {final_count} matches.")
    
    print("\n--- STEP 7: ACTIVE TEAMS IN CLEANED DATASET ---")
    unique_teams = sorted(df['team1'].unique())
    print(f"Total Unique Teams ({len(unique_teams)}):")
    for idx, team in enumerate(unique_teams, 1):
        print(f"  {idx}. {team}")
        
    return df

if __name__ == "__main__":
    dataset_path = "dataset/matches.csv"
    cleaned_df = load_and_preprocess_data(dataset_path)
