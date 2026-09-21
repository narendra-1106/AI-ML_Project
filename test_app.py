"""
=============================================================================
IPL MATCH WINNER PREDICTION - STAGE 13: AUTOMATED INTEGRATION TEST SUITE
=============================================================================
This test module performs unit and integration tests across dataset integrity,
saved model inference, Flask routes, input validation, and SQLite database logging.
=============================================================================
"""

import os
import unittest
import pandas as pd
import joblib
import sqlite3
import app

class TestIPLMatchWinnerPrediction(unittest.TestCase):

    def setUp(self):
        """Set up test client before each test execution."""
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()

    def test_01_dataset_file_exists(self):
        """Verify that dataset/matches.csv exists and contains valid records."""
        dataset_path = "dataset/matches.csv"
        self.assertTrue(os.path.exists(dataset_path), "dataset/matches.csv is missing!")
        df = pd.read_csv(dataset_path)
        self.assertGreater(len(df), 1000, "Dataset contains fewer than 1000 records!")
        for col in ['team1', 'team2', 'toss_winner', 'match_winner']:
            self.assertIn(col, df.columns, f"Missing essential column '{col}' in dataset!")

    def test_02_model_file_exists_and_predicts(self):
        """Verify that model/ipl_model.pkl exists and generates predictions."""
        model_path = "model/ipl_model.pkl"
        self.assertTrue(os.path.exists(model_path), "model/ipl_model.pkl is missing!")
        pipeline = joblib.load(model_path)
        
        sample_input = pd.DataFrame([{
            'team1': 'Mumbai Indians',
            'team2': 'Chennai Super Kings',
            'toss_winner': 'Mumbai Indians'
        }])
        prediction = pipeline.predict(sample_input)[0]
        self.assertIn(prediction, ['Mumbai Indians', 'Chennai Super Kings'], "Invalid model prediction!")

    def test_03_flask_routes_render(self):
        """Verify that all 5 HTML GET routes return HTTP status 200."""
        routes = ['/', '/prediction', '/dashboard', '/history', '/about']
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route '{route}' failed with status {response.status_code}!")

    def test_04_prediction_validation_same_team(self):
        """Verify that selecting identical teams returns a validation error."""
        response = self.client.post('/predict', data={
            'team1': 'Mumbai Indians',
            'team2': 'Mumbai Indians',
            'toss_winner': 'Mumbai Indians'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'cannot be the same team', response.data)

    def test_05_prediction_validation_invalid_toss(self):
        """Verify that selecting a toss winner not playing in the match returns an error."""
        response = self.client.post('/predict', data={
            'team1': 'Mumbai Indians',
            'team2': 'Chennai Super Kings',
            'toss_winner': 'Rajasthan Royals'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Toss Winner must be either', response.data)

    def test_06_prediction_submission_and_db_logging(self):
        """Verify successful prediction submission and SQLite database insertion."""
        response = self.client.post('/predict', data={
            'team1': 'Kolkata Knight Riders',
            'team2': 'Royal Challengers Bangalore',
            'toss_winner': 'Kolkata Knight Riders'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Predicted Match Winner', response.data)

        # Query database to confirm insertion
        conn = sqlite3.connect("database/ipl.db")
        cursor = conn.cursor()
        cursor.execute("SELECT team1, team2, toss_winner FROM predictions ORDER BY id DESC LIMIT 1")
        last_record = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(last_record, "Prediction was not logged into SQLite database!")
        self.assertEqual(last_record[0], 'Kolkata Knight Riders')
        self.assertEqual(last_record[1], 'Royal Challengers Bangalore')

if __name__ == '__main__':
    print("\n==================================================")
    print("      RUNNING IPL PREDICTOR INTEGRATION TESTS     ")
    print("==================================================")
    unittest.main()
