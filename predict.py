"""
Inference Script for Phishing Website Detection
Author: Simran Semwal
Loads the trained machine learning model from models/best_model.joblib
and performs real-time classification with probability confidence scores.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "best_model.joblib")
META_PATH = os.path.join(os.path.dirname(__file__), "models", "model_metadata.json")


def load_champion_model():
    """Loads the trained Random Forest model and metadata."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run 'python src/model_training.py' first.")
    
    model = joblib.load(MODEL_PATH)
    meta = {}
    if os.path.exists(META_PATH):
        with open(META_PATH, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
    return model, meta


def predict_website(features_dict, model=None, meta=None):
    """
    Predicts whether a website is Legitimate or Phishing.

    Parameters:
    -----------
    features_dict : dict or pd.DataFrame
        Dictionary containing values for the 30 heuristic features.
    model : trained estimator, optional
    meta : dict, optional

    Returns:
    --------
    result : dict
        Classification label, probability, risk level, and flagged heuristics.
    """
    if model is None or meta is None:
        model, meta = load_champion_model()

    feature_names = meta.get("feature_names", [])
    
    # Prepare DataFrame matching trained feature order
    if isinstance(features_dict, dict):
        df_input = pd.DataFrame([features_dict])
    else:
        df_input = features_dict.copy()

    # Ensure all required features are present
    for feat in feature_names:
        if feat not in df_input.columns:
            df_input[feat] = 0  # Default neutral if missing

    df_input = df_input[feature_names]

    # Predict class (1 = Phishing, 0 = Legitimate)
    pred_class = model.predict(df_input)[0]
    probs = model.predict_proba(df_input)[0]  # [prob_legit, prob_phish]

    prob_phish = probs[1]
    prob_legit = probs[0]

    label = "PHISHING WEBSITE" if pred_class == 1 else "LEGITIMATE WEBSITE"
    confidence = prob_phish if pred_class == 1 else prob_legit

    # Identify primary suspicious heuristics (where value is -1)
    flagged = []
    input_series = df_input.iloc[0]
    for feat in feature_names:
        if input_series[feat] == -1:
            flagged.append(feat)

    return {
        "prediction": label,
        "is_phishing": bool(pred_class == 1),
        "confidence": round(confidence * 100, 2),
        "phishing_probability": round(prob_phish * 100, 2),
        "legitimate_probability": round(prob_legit * 100, 2),
        "risk_level": "CRITICAL" if prob_phish > 0.8 else ("MODERATE" if prob_phish > 0.5 else "SAFE"),
        "flagged_heuristics": flagged
    }


def demo_predictions():
    print("=" * 80)
    print("PHISHING WEBSITE DETECTION: REAL-TIME INFERENCE DEMO")
    print("=" * 80)
    model, meta = load_champion_model()
    print(f"Loaded Model: {meta.get('champion_model', 'Random Forest')} (Test Accuracy: {meta.get('champion_accuracy', 0.9751)*100:.2f}%)")
    print(f"Model File:   {MODEL_PATH}\n")

    # Sample 1: Authentic Bank / Enterprise Website Profile
    sample_legitimate = {
        "having_ip_address": 1,
        "url_length": 1,
        "shortining_service": 1,
        "having_at_symbol": 1,
        "double_slash_redirecting": 1,
        "prefix_suffix": 1,
        "having_sub_domain": 1,
        "sslfinal_state": 1,             # Valid trusted HTTPS
        "domain_registration_length": 1, # Long registration
        "favicon": 1,
        "port": 1,
        "https_token": 1,
        "request_url": 1,
        "url_of_anchor": 1,              # Internal anchors
        "links_in_tags": 1,
        "sfh": 1,                        # Internal form handler
        "submitting_to_email": 1,
        "abnormal_url": 1,
        "redirect": 0,
        "on_mouseover": 1,
        "rightclick": 1,
        "popupwindow": 1,
        "iframe": 1,
        "age_of_domain": 1,              # Old domain
        "dnsrecord": 1,
        "web_traffic": 1,                # High Alexa rank
        "page_rank": 1,
        "google_index": 1,
        "links_pointing_to_page": 1,
        "statistical_report": 1
    }

    # Sample 2: Typical Malicious Phishing Landing Page Profile
    sample_phishing = {
        "having_ip_address": -1,          # Direct IP address
        "url_length": -1,                 # Very long URL
        "shortining_service": -1,         # bit.ly shortened
        "having_at_symbol": -1,           # @ symbol present
        "double_slash_redirecting": -1,   # // redirect
        "prefix_suffix": -1,              # Hyphen in domain (e.g. paypal-login)
        "having_sub_domain": -1,          # Multi subdomains
        "sslfinal_state": -1,             # No HTTPS / untrusted
        "domain_registration_length": -1, # < 1 year
        "favicon": -1,
        "port": -1,                       # Non-standard port open
        "https_token": -1,                # 'https' in domain name
        "request_url": -1,
        "url_of_anchor": -1,              # Links point to # or foreign domain
        "links_in_tags": -1,
        "sfh": -1,                        # Blank form action
        "submitting_to_email": -1,        # Form mails to attacker
        "abnormal_url": -1,
        "redirect": 1,
        "on_mouseover": -1,
        "rightclick": -1,                 # Disables right click
        "popupwindow": -1,
        "iframe": -1,                     # Invisible iframe
        "age_of_domain": -1,              # Fresh domain (< 6 months)
        "dnsrecord": -1,
        "web_traffic": -1,                # Zero web traffic
        "page_rank": -1,
        "google_index": -1,               # Unindexed
        "links_pointing_to_page": -1,
        "statistical_report": -1          # Listed on PhishTank
    }

    # Run Prediction on Sample 1
    print("--> Test Case 1: Testing Authentic Web Profile...")
    res1 = predict_website(sample_legitimate, model, meta)
    print(f"    Classification:      [{res1['prediction']}]")
    print(f"    Confidence:          {res1['confidence']}%")
    print(f"    Risk Assessment:     {res1['risk_level']}")
    print(f"    Legitimate Prob:     {res1['legitimate_probability']}% | Phishing Prob: {res1['phishing_probability']}%\n")

    # Run Prediction on Sample 2
    print("--> Test Case 2: Testing Deceptive Phishing Profile...")
    res2 = predict_website(sample_phishing, model, meta)
    print(f"    Classification:      [{res2['prediction']}]")
    print(f"    Confidence:          {res2['confidence']}%")
    print(f"    Risk Assessment:     {res2['risk_level']}")
    print(f"    Phishing Prob:       {res2['phishing_probability']}% | Legitimate Prob: {res2['legitimate_probability']}%")
    print(f"    Flagged Heuristics:  {len(res2['flagged_heuristics'])} security red-flags identified")
    print("=" * 80)


if __name__ == "__main__":
    demo_predictions()
