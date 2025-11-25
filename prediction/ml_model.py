import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib
import os
from django.conf import settings

class DrugRecoveryModel:
    def __init__(self):
        self.clf_model = None
        self.reg_model = None
        self.scaler = None
        self.label_encoders = {}
        self.model_dir = os.path.join(settings.BASE_DIR, 'prediction', 'saved_models')
        
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
    
    def train_models(self, csv_path):
        """Train both classification and regression models"""
        df = pd.read_csv(csv_path)
        
        # Encode categorical columns
        self.label_encoders = {}
        for col in df.columns:
            if df[col].dtype == "object":
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
                self.label_encoders[col] = le
        
        # Create recovery classes
        def convert_to_class(x):
            if x <= 6:
                return 0   # Short
            elif x <= 12:
                return 1   # Medium
            else:
                return 2   # Long
        
        df["Recovery_Class"] = df["Recovery_Time_Months"].apply(convert_to_class)
        
        # Prepare features and targets
        X = df.drop(["Recovery_Time_Months", "Recovery_Class"], axis=1)
        y_class = df["Recovery_Class"]
        y_reg = df["Recovery_Time_Months"]
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train classification model
        X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
            X_scaled, y_class, test_size=0.2, random_state=42
        )
        self.clf_model = RandomForestClassifier(n_estimators=200, random_state=42)
        self.clf_model.fit(X_train_c, y_train_c)
        
        # Train regression model
        X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
            X_scaled, y_reg, test_size=0.2, random_state=42
        )
        self.reg_model = RandomForestRegressor(n_estimators=300, random_state=42)
        self.reg_model.fit(X_train_r, y_train_r)
        
        # Save models
        self.save_models()
        
        return True
    
    def save_models(self):
        """Save trained models to disk"""
        joblib.dump(self.clf_model, os.path.join(self.model_dir, 'classifier.pkl'))
        joblib.dump(self.reg_model, os.path.join(self.model_dir, 'regressor.pkl'))
        joblib.dump(self.scaler, os.path.join(self.model_dir, 'scaler.pkl'))
        joblib.dump(self.label_encoders, os.path.join(self.model_dir, 'encoders.pkl'))
    
    def load_models(self):
        """Load trained models from disk"""
        try:
            self.clf_model = joblib.load(os.path.join(self.model_dir, 'classifier.pkl'))
            self.reg_model = joblib.load(os.path.join(self.model_dir, 'regressor.pkl'))
            self.scaler = joblib.load(os.path.join(self.model_dir, 'scaler.pkl'))
            self.label_encoders = joblib.load(os.path.join(self.model_dir, 'encoders.pkl'))
            return True
        except FileNotFoundError:
            return False
    
    def predict(self, age, gender, drug_type, addiction_severity, 
                daily_usage, years_using, mental_health_score, recovery_program):
        """Make prediction for new data"""
        
        # Encode inputs
        gender_encoded = self.label_encoders['Gender'].transform([gender])[0]
        drug_encoded = self.label_encoders['Drug_Type'].transform([drug_type])[0]
        
        # Create dataframe
        custom_df = pd.DataFrame({
            "Age": [age],
            "Gender": [gender_encoded],
            "Drug_Type": [drug_encoded],
            "Addiction_Severity": [addiction_severity],
            "Daily_Usage": [daily_usage],
            "Years_Using": [years_using],
            "Mental_Health_Score": [mental_health_score],
            "Recovery_Program": [recovery_program]
        })
        
        # Scale
        scaled = self.scaler.transform(custom_df)
        
        # Predictions
        pred_class = self.clf_model.predict(scaled)[0]
        pred_prob = self.clf_model.predict_proba(scaled)[0]
        exact_months = round(self.reg_model.predict(scaled)[0], 2)
        
        class_labels = {
            0: "Short (0–6 months)",
            1: "Medium (6–12 months)",
            2: "Long (12+ months)"
        }
        
        return {
            'class': class_labels[pred_class],
            'months': exact_months,
            'prob_short': round(pred_prob[0] * 100, 2),
            'prob_medium': round(pred_prob[1] * 100, 2),
            'prob_long': round(pred_prob[2] * 100, 2)
        }