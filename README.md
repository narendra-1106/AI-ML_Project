# 🏏 IPL Match Winner Prediction Using Machine Learning

A complete web-based AI/ML application built with **Python, Flask, Scikit-Learn, Pandas, Chart.js, and SQLite** that predicts the winner of an Indian Premier League (IPL) cricket match using historical match data.

---

## 📌 Project Overview

This project uses supervised machine learning classification to predict IPL match outcomes based on pre-match conditions: **Team 1**, **Team 2**, and **Toss Winner**.

* **Dataset Size**: 1,212 historical IPL match records.
* **Primary ML Algorithm**: Decision Tree Classifier inside a Scikit-Learn `Pipeline` with `OneHotEncoder`.
* **Backend**: Flask Web Server managing RESTful routes and SQLite database logging.
* **Frontend**: Responsive Dark IPL Theme built with HTML5, Vanilla CSS3, JavaScript, and Chart.js.

---

## 🛠️ Technology Stack

| Domain | Technologies |
| :--- | :--- |
| **Language** | Python 3.13 |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy, Joblib |
| **Backend Framework** | Flask 3.1.0 |
| **Database** | SQLite 3 (`database/ipl.db`) |
| **Frontend UI** | HTML5, CSS3, JavaScript |
| **Data Visualizations** | Chart.js (CDN) |

---

## 📂 Project Structure

```text
IPL-Match-Winner-Prediction/
│
├── app.py                      # Flask Backend Server & Routes
├── train_model.py              # ML Data Processing & Training Pipeline
├── test_app.py                 # Automated Integration Test Suite
├── requirements.txt            # Project Dependencies
├── README.md                   # Project Documentation
│
├── dataset/
│   └── matches.csv             # Cleaned IPL Historical Dataset
│
├── model/
│   └── ipl_model.pkl           # Saved Scikit-Learn Pipeline Object
│
├── database/
│   └── ipl.db                  # SQLite Prediction Log Database
│
├── templates/
│   ├── index.html              # Home Landing Page
│   ├── prediction.html         # Live Prediction Form & Result Card
│   ├── dashboard.html          # Interactive Analytics Dashboard
│   ├── history.html            # SQLite Stored Predictions Log
│   └── about.html              # Architecture & Viva Study Guide
│
└── static/
    ├── css/
    │   └── style.css           # Custom Dark/IPL Theme Styling
    └── js/
        └── script.js           # Form Validation & Chart.js Visuals
```

---

## ⚙️ Installation & Setup Guide

### 1. Clone or Download Repository
```bash
git clone https://github.com/<your-username>/IPL-Match-Winner-Prediction.git
cd IPL-Match-Winner-Prediction
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the Machine Learning Model
```bash
python train_model.py
```
*Outputs evaluation metrics ($\approx 48.15\%$ multi-class accuracy across 13 teams) and serializes `model/ipl_model.pkl`.*

### 4. Run Automated Tests
```bash
python test_app.py
```

### 5. Launch the Flask Web Application
```bash
python app.py
```
*Open your web browser and navigate to `http://127.0.0.1:5000`.*

---

## 🌐 Application Routes

* `/` - **Home Page**: Project pitch, CTA buttons, and feature overview.
* `/prediction` - **Prediction Form**: Select Team 1, Team 2, and Toss Winner.
* `/predict` - **POST Endpoint**: Executes ML pipeline inference and logs to SQLite.
* `/dashboard` - **Analytics Dashboard**: Chart.js charts for total wins and toss correlation.
* `/history` - **Prediction Log**: View all previous queries stored in SQLite.
* `/about` - **About Page**: Project specification, methodology, and viva guide.

---

## 🎓 Academic Review & Viva Q&A

**Q1: Why use a Scikit-Learn Pipeline?**  
*Answer*: Encapsulating `OneHotEncoder` and `DecisionTreeClassifier` into a single `Pipeline` ensures that raw text inputs passed by Flask undergo the exact same feature transformation without data leakage.

**Q2: How does the model handle categorical team names?**  
*Answer*: `OneHotEncoder` converts text team strings into binary indicator columns ($0$ or $1$) before feeding them into the Decision Tree node splits.

**Q3: Is the model prediction hardcoded?**  
*Answer*: No. Predictions are generated dynamically at runtime by loading `model/ipl_model.pkl` and passing a 1-row Pandas DataFrame into `model_pipeline.predict()`.

---

## 📜 License
Developed as an AI/ML Mini Project. Free to use for educational purposes.
