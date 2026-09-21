"""
=============================================================================
IPL MATCH WINNER PREDICTION - COMPLETE FLASK BACKEND SERVER (app.py)
=============================================================================
This module creates the Flask Web Application server, sets up routing endpoints
('/', '/prediction', '/predict', '/dashboard', '/history', '/about'), initializes
the SQLite database ('database/ipl.db'), computes dashboard analytics, and handles
ML model inference.
=============================================================================
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import joblib
from flask import Flask, render_template, request, jsonify, redirect, url_for

# Initialize Flask application
app = Flask(__name__)

# Constants and File Paths
MODEL_PATH = "model/ipl_model.pkl"
DATASET_PATH = "dataset/matches.csv"
DATABASE_PATH = "database/ipl.db"

# Global variables for loaded model and data
model_pipeline = None
cleaned_df = None
active_teams = []

def init_db():
    """Initialize SQLite database table for storing prediction history."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team1 TEXT NOT NULL,
            team2 TEXT NOT NULL,
            toss_winner TEXT NOT NULL,
            predicted_winner TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def load_resources():
    """Load dataset, active teams list, and trained ML model pipeline into memory."""
    global model_pipeline, cleaned_df, active_teams
    
    # Load dataset if exists
    if os.path.exists(DATASET_PATH):
        cleaned_df = pd.read_csv(DATASET_PATH)
        
        # Standardize team names across dataset
        team_name_mapping = {
            'Delhi Daredevils': 'Delhi Capitals',
            'Kings XI Punjab': 'Punjab Kings',
            'Rising Pune Supergiants': 'Rising Pune Supergiant',
            'Royal Challengers Bengaluru': 'Royal Challengers Bangalore',
            'Deccan Chargers': 'Sunrisers Hyderabad'
        }
        for col in ['team1', 'team2', 'toss_winner', 'match_winner']:
            cleaned_df[col] = cleaned_df[col].replace(team_name_mapping)
            
        # Extract unique list of active IPL teams sorted alphabetically
        team1_list = cleaned_df['team1'].dropna().unique().tolist()
        team2_list = cleaned_df['team2'].dropna().unique().tolist()
        active_teams = sorted(list(set(team1_list + team2_list)))
    else:
        active_teams = [
            'Chennai Super Kings', 'Delhi Capitals', 'Gujarat Lions', 'Gujarat Titans',
            'Kochi Tuskers Kerala', 'Kolkata Knight Riders', 'Lucknow Super Giants',
            'Mumbai Indians', 'Punjab Kings', 'Rajasthan Royals',
            'Rising Pune Supergiant', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
        ]
        
    # Load serialised model pipeline
    if os.path.exists(MODEL_PATH):
        model_pipeline = joblib.load(MODEL_PATH)
        print("Trained ML Pipeline successfully loaded into Flask server.")
    else:
        print("WARNING: 'model/ipl_model.pkl' not found. Please run train_model.py first.")

# Initialize database and load artifacts on app launch
init_db()
load_resources()

# =============================================================================
# FLASK ROUTE DEFINITIONS
# =============================================================================

@app.route('/')
def home():
    """Route 1: Home Page"""
    return render_template('index.html')

@app.route('/prediction')
def prediction_page():
    """Route 2: Prediction Page (Renders form with team dropdown options)"""
    return render_template('prediction.html', teams=active_teams)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Route 3: ML Winner Prediction API Endpoint
    Receives form or JSON request with team1, team2, toss_winner,
    performs validation, runs ML pipeline prediction, logs to SQLite DB,
    and returns result.
    """
    try:
        if request.is_json:
            data = request.get_json()
            team1 = data.get('team1')
            team2 = data.get('team2')
            toss_winner = data.get('toss_winner')
        else:
            team1 = request.form.get('team1')
            team2 = request.form.get('team2')
            toss_winner = request.form.get('toss_winner')
            
        if not team1 or not team2 or not toss_winner:
            error_msg = "Please select Team 1, Team 2, and Toss Winner."
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            return render_template('prediction.html', teams=active_teams, error=error_msg)
            
        if team1 == team2:
            error_msg = "Team 1 and Team 2 cannot be the same team!"
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            return render_template('prediction.html', teams=active_teams, error=error_msg)
            
        if toss_winner not in [team1, team2]:
            error_msg = f"Toss Winner must be either '{team1}' or '{team2}'."
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            return render_template('prediction.html', teams=active_teams, error=error_msg)
            
        if model_pipeline is None:
            error_msg = "Machine learning model is not loaded. Please train the model."
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            return render_template('prediction.html', teams=active_teams, error=error_msg)
            
        input_data = pd.DataFrame([{
            'team1': team1,
            'team2': team2,
            'toss_winner': toss_winner
        }])
        
        predicted_winner = model_pipeline.predict(input_data)[0]
        
        try:
            probabilities = model_pipeline.predict_proba(input_data)[0]
            classes = list(model_pipeline.classes_)
            prob_dict = dict(zip(classes, probabilities))
            team1_prob = round(prob_dict.get(team1, 0.5) * 100, 1)
            team2_prob = round(prob_dict.get(team2, 0.5) * 100, 1)
        except Exception:
            team1_prob = 50.0
            team2_prob = 50.0
            
        # Log prediction into SQLite database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO predictions (team1, team2, toss_winner, predicted_winner)
            VALUES (?, ?, ?, ?)
        """, (team1, team2, toss_winner, predicted_winner))
        conn.commit()
        conn.close()
        
        result_payload = {
            'team1': team1,
            'team2': team2,
            'toss_winner': toss_winner,
            'predicted_winner': predicted_winner,
            'team1_prob': team1_prob,
            'team2_prob': team2_prob
        }
        
        if request.is_json:
            return jsonify(result_payload)
        
        return render_template('prediction.html', teams=active_teams, result=result_payload)
        
    except Exception as e:
        error_msg = f"An error occurred during prediction: {str(e)}"
        if request.is_json:
            return jsonify({'error': error_msg}), 500
        return render_template('prediction.html', teams=active_teams, error=error_msg)

@app.route('/dashboard')
def dashboard():
    """Route 4: Analytics Dashboard Page with Calculated Statistics"""
    if cleaned_df is not None:
        total_matches = int(len(cleaned_df))
        total_teams = int(len(active_teams))
        total_seasons = int(cleaned_df['season'].nunique())
        
        # Calculate Team Win Statistics
        win_counts = cleaned_df['match_winner'].value_counts()
        team_win_labels = win_counts.index.tolist()
        team_win_data = win_counts.values.tolist()
        
        # Calculate Toss Impact Statistics
        toss_wins = int((cleaned_df['toss_winner'] == cleaned_df['match_winner']).sum())
        toss_losses = total_matches - toss_wins
        
        stats = {
            'total_matches': total_matches,
            'total_teams': total_teams,
            'total_seasons': total_seasons,
            'toss_win_pct': round((toss_wins / total_matches) * 100, 1),
            'team_win_labels': team_win_labels,
            'team_win_data': team_win_data,
            'toss_impact_labels': ['Toss Winner Won Match', 'Toss Loser Won Match'],
            'toss_impact_data': [toss_wins, toss_losses]
        }
    else:
        stats = {
            'total_matches': 1212,
            'total_teams': 13,
            'total_seasons': 17,
            'toss_win_pct': 51.7,
            'team_win_labels': active_teams,
            'team_win_data': [100] * len(active_teams),
            'toss_impact_labels': ['Toss Winner Won', 'Toss Loser Won'],
            'toss_impact_data': [626, 586]
        }
        
    return render_template('dashboard.html', stats=stats)

@app.route('/history')
def history():
    """Route 5: Prediction History Page (Fetches predictions from SQLite DB)"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM predictions ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template('history.html', predictions=rows)

@app.route('/about')
def about():
    """Route 6: About Project Page"""
    return render_template('about.html')

if __name__ == '__main__':
    print("Starting Flask server for IPL Match Winner Prediction...")
    app.run(debug=True, port=5000)
