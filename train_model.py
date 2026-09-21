"""
=============================================================================
IPL MATCH WINNER PREDICTION - COMPLETE TRAINING PIPELINE (STAGES 2 - 5)
=============================================================================
This script loads the IPL dataset, performs preprocessing, splits data into
training and testing sets, constructs a Scikit-Learn Pipeline with OneHotEncoder,
trains a Decision Tree Classifier, evaluates metrics, saves the model via Joblib,
and performs test predictions on saved model artifacts.
=============================================================================
"""

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

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
    X = df[['team1', 'team2', 'toss_winner']]
    y = df['match_winner']
    
    print("\n--- STEP 3: TRAIN / TEST SPLIT (80% Train, 20% Test) ---")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training set size: {X_train.shape[0]} records")
    print(f"Testing set size: {X_test.shape[0]} records")
    
    print("\n--- STEP 4: BUILDING SCIKIT-LEARN PIPELINE ---")
    categorical_features = ['team1', 'team2', 'toss_winner']
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ]
    )
    
    dt_classifier = DecisionTreeClassifier(
        criterion='entropy',
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )
    
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', dt_classifier)
    ])
    
    print("\n--- STEP 5: TRAINING THE MODEL PIPELINE ---")
    model_pipeline.fit(X_train, y_train)
    print("Decision Tree Classifier Pipeline trained successfully!")
    
    return model_pipeline, X_train, X_test, y_train, y_test

def evaluate_machine_learning_model(model_pipeline, X_test, y_test):
    print("\n--- STEP 6: MODEL EVALUATION ON UNSEEN TEST DATA ---")
    y_pred = model_pipeline.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_test, y_pred)
    
    print("==================================================")
    print("         ACTUAL MODEL EVALUATION METRICS          ")
    print("==================================================")
    print(f"  Accuracy:  {acc * 100:.2f}%  ({acc:.4f})")
    print(f"  Precision: {precision * 100:.2f}%  ({precision:.4f})")
    print(f"  Recall:    {recall * 100:.2f}%  ({recall:.4f})")
    print(f"  F1-Score:  {f1 * 100:.2f}%  ({f1:.4f})")
    print("==================================================")
    
    return {
        'accuracy': float(acc),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1)
    }

def save_model_pipeline(model_pipeline, output_path="model/ipl_model.pkl"):
    print("\n--- STEP 7: SERIALIZING & SAVING MODEL PIPELINE ---")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(model_pipeline, output_path)
    print(f"Trained ML Pipeline successfully saved to: '{output_path}'")

def test_saved_model_pipeline(model_path="model/ipl_model.pkl"):
    print("\n--- STEP 8: TESTING SAVED MODEL FILE ON SAMPLE INPUTS ---")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
        
    loaded_pipeline = joblib.load(model_path)
    
    # Test sample match inputs
    sample_matches = [
        {'team1': 'Mumbai Indians', 'team2': 'Chennai Super Kings', 'toss_winner': 'Mumbai Indians'},
        {'team1': 'Royal Challengers Bangalore', 'team2': 'Kolkata Knight Riders', 'toss_winner': 'Royal Challengers Bangalore'},
        {'team1': 'Sunrisers Hyderabad', 'team2': 'Delhi Capitals', 'toss_winner': 'Delhi Capitals'}
    ]
    
    sample_df = pd.DataFrame(sample_matches)
    predictions = loaded_pipeline.predict(sample_df)
    
    print("Sample Match Predictions:")
    for idx, sample in enumerate(sample_matches):
        print(f"  Match {idx+1}: {sample['team1']} vs {sample['team2']} (Toss: {sample['toss_winner']})")
        print(f"  ==> Predicted Winner: {predictions[idx]}\n")

if __name__ == "__main__":
    dataset_path = "dataset/matches.csv"
    model_save_path = "model/ipl_model.pkl"
    
    df = load_and_preprocess_data(dataset_path)
    pipeline, X_train, X_test, y_train, y_test = train_machine_learning_model(df)
    evaluate_machine_learning_model(pipeline, X_test, y_test)
    save_model_pipeline(pipeline, model_save_path)
    test_saved_model_pipeline(model_save_path)
