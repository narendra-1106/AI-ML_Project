"""
=============================================================================
IPL MATCH WINNER PREDICTION - STAGE 2 & STAGE 3: DATA PREPROCESSING & MODEL TRAINING
=============================================================================
This script loads the IPL dataset, performs preprocessing, splits data into
training and testing sets, constructs a Scikit-Learn Pipeline with OneHotEncoder,
and trains a Decision Tree Classifier.
=============================================================================
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier

def load_and_preprocess_data(file_path):
    print("\n--- STEP 1: LOADING DATASET ---")
    df = pd.read_csv(file_path)
    
    # Standardize team names across seasons
    team_name_mapping = {
        'Delhi Daredevils': 'Delhi Capitals',
        'Kings XI Punjab': 'Punjab Kings',
        'Rising Pune Supergiants': 'Rising Pune Supergiant',
        'Royal Challengers Bengaluru': 'Royal Challengers Bangalore',
        'Deccan Chargers': 'Sunrisers Hyderabad'
    }
    for col in ['team1', 'team2', 'toss_winner', 'match_winner']:
        df[col] = df[col].replace(team_name_mapping)
        
    df = df.dropna(subset=['team1', 'team2', 'toss_winner', 'match_winner'])
    df = df[(df['match_winner'] == df['team1']) | (df['match_winner'] == df['team2'])]
    
    print(f"Dataset Loaded & Cleaned: {df.shape[0]} total match records.")
    return df

def train_machine_learning_model(df):
    print("\n--- STEP 2: FEATURE SELECTION & TARGET SETTING ---")
    # Features (X): Team 1, Team 2, Toss Winner
    X = df[['team1', 'team2', 'toss_winner']]
    # Target (y): Match Winner
    y = df['match_winner']
    
    print(f"Features (X) shape: {X.shape}")
    print(f"Target (y) shape: {y.shape}")
    
    print("\n--- STEP 3: TRAIN / TEST SPLIT (80% Train, 20% Test) ---")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set size: {X_train.shape[0]} records")
    print(f"Testing set size: {X_test.shape[0]} records")
    
    print("\n--- STEP 4: BUILDING SCIKIT-LEARN PIPELINE ---")
    # Categorical features requiring OneHotEncoding
    categorical_features = ['team1', 'team2', 'toss_winner']
    
    # ColumnTransformer with OneHotEncoder
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ]
    )
    
    # Primary Algorithm: Decision Tree Classifier
    dt_classifier = DecisionTreeClassifier(
        criterion='entropy',
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    
    # Encapsulate preprocessor and estimator into a unified Scikit-learn Pipeline
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', dt_classifier)
    ])
    
    print("\n--- STEP 5: TRAINING THE MODEL PIPELINE ---")
    model_pipeline.fit(X_train, y_train)
    print("Decision Tree Classifier Pipeline trained successfully!")
    
    return model_pipeline, X_train, X_test, y_train, y_test

if __name__ == "__main__":
    dataset_path = "dataset/matches.csv"
    df = load_and_preprocess_data(dataset_path)
    pipeline, X_train, X_test, y_train, y_test = train_machine_learning_model(df)
