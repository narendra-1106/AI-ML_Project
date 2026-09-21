"""
=============================================================================
IPL MATCH WINNER PREDICTION - STAGES 2, 3 & 4: PREPROCESSING, TRAINING & EVALUATION
=============================================================================
This script loads the IPL dataset, performs preprocessing, splits data into
training and testing sets, constructs a Scikit-Learn Pipeline with OneHotEncoder,
trains a Decision Tree Classifier, and evaluates performance using actual metrics.
=============================================================================
"""

import pandas as pd
import numpy as np
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
    # Make predictions on test set
    y_pred = model_pipeline.predict(X_test)
    
    # Calculate real evaluation metrics
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
    
    print("\nConfusion Matrix Shape:", cm.shape)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    return {
        'accuracy': float(acc),
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1)
    }

if __name__ == "__main__":
    dataset_path = "dataset/matches.csv"
    df = load_and_preprocess_data(dataset_path)
    pipeline, X_train, X_test, y_train, y_test = train_machine_learning_model(df)
    metrics = evaluate_machine_learning_model(pipeline, X_test, y_test)
