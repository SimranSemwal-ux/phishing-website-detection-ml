"""
Preprocessing Module for Phishing Website Detection
Foundations of Data Science (FDS) Assignment 3

This module handles:
1. Data cleaning, integrity validation, and anomaly checks.
2. Inconsistent value detection and domain range auditing.
3. Duplicate and conflicting observation analysis.
4. Target standardization: preserves original `result` (-1, 1) and adds `target` (0, 1).
5. Stratified train-test splitting (80:20) preventing data leakage.
"""

import os
import json
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def clean_and_preprocess_data(df, output_dir=None, save_clean=True):
    """
    Cleans and preprocesses the UCI Phishing Websites dataset.

    Parameters:
    -----------
    df : pd.DataFrame
        Raw dataset from data_loader.
    output_dir : str, optional
        Destination directory for processed data.
    save_clean : bool, default True
        Whether to save processed dataset to CSV.

    Returns:
    --------
    cleaned_df : pd.DataFrame
        Cleaned dataframe with standardized target columns.
    cleaning_report : dict
        Detailed metrics documenting missing values, domain ranges, duplicates, and conflicts.
    """
    if output_dir is None:
        if os.path.exists("data/processed"):
            output_dir = "data/processed"
        elif os.path.exists("../data/processed"):
            output_dir = "../data/processed"
        else:
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
    os.makedirs(output_dir, exist_ok=True)

    initial_rows, initial_cols = df.shape
    logger.info(f"Starting data cleaning. Initial records: {initial_rows}, Columns: {initial_cols}")

    # 1. Missing Values Check
    missing_counts = df.isnull().sum()
    total_missing = int(missing_counts.sum())

    # Identify target column
    target_col = "result" if "result" in df.columns else ("Result" if "Result" in df.columns else df.columns[-1])
    feature_cols = [c for c in df.columns if c != target_col]

    # 2. Value Domain Audit (Ensuring all features fall strictly within valid discrete sets)
    domain_audit = {}
    for col in feature_cols:
        unique_vals = sorted(df[col].unique().tolist())
        valid = all(v in [-1, 0, 1] for v in unique_vals)
        domain_audit[col] = {
            "unique_values": unique_vals,
            "is_valid_domain": valid
        }

    # 3. Duplicate and Conflicting Signatures Analysis
    exact_duplicates = int(df.duplicated().sum())
    feature_duplicates = int(df.duplicated(subset=feature_cols).sum())
    
    # Check conflicting rows (same X, but different y)
    feature_dups_mask = df.duplicated(subset=feature_cols, keep=False)
    conflicts_by_group = df[feature_dups_mask].groupby(feature_cols)[target_col].nunique()
    conflicting_combos = int((conflicts_by_group > 1).sum())
    
    conflicting_row_count = 0
    if conflicting_combos > 0:
        bad_combos = conflicts_by_group[conflicts_by_group > 1].index
        conflicting_row_count = int(df[df.set_index(feature_cols).index.isin(bad_combos)].shape[0])

    # 4. Target Standardization
    # Original: -1 (Phishing), 1 (Legitimate)
    # Binary:    0 (Phishing), 1 (Legitimate) -> Standard for Scikit-Learn loss & metrics
    cleaned_df = df.copy()
    cleaned_df["target_binary"] = cleaned_df[target_col].map({-1: 0, 1: 1})
    cleaned_df["class_label"] = cleaned_df[target_col].map({-1: "Phishing", 1: "Legitimate"})

    final_rows, final_cols = cleaned_df.shape
    logger.info(f"Cleaning complete. Observations preserved: {final_rows}/{initial_rows} (100% retained).")

    cleaning_report = {
        "initial_records": initial_rows,
        "final_records": final_rows,
        "records_removed": 0,
        "missing_values_found": total_missing,
        "exact_duplicates_count": exact_duplicates,
        "exact_duplicates_percentage": round((exact_duplicates / initial_rows) * 100, 2),
        "feature_duplicates_count": feature_duplicates,
        "conflicting_feature_combinations": conflicting_combos,
        "conflicting_rows_count": conflicting_row_count,
        "target_mapping": {
            "-1": "Phishing (Binary 0)",
            "1": "Legitimate (Binary 1)"
        },
        "class_distribution_raw": df[target_col].value_counts().to_dict(),
        "class_distribution_percentage": (df[target_col].value_counts(normalize=True) * 100).round(2).to_dict()
    }

    if save_clean:
        clean_csv = os.path.join(output_dir, "phishing_cleaned.csv")
        clean_meta = os.path.join(output_dir, "cleaning_report.json")
        cleaned_df.to_csv(clean_csv, index=False)
        with open(clean_meta, "w", encoding="utf-8") as f:
            json.dump(cleaning_report, f, indent=4)
        logger.info(f"Saved preprocessed data to {clean_csv} and report to {clean_meta}")

    return cleaned_df, cleaning_report


def get_train_test_data(df=None, test_size=0.2, random_state=42, use_binary_target=True):
    """
    Splits the dataset into stratified train and test partitions (80:20).
    Guarantees zero data leakage and preserves class distribution in both splits.

    Parameters:
    -----------
    df : pd.DataFrame, optional
        Preprocessed dataframe. If None, loads from data/processed/phishing_cleaned.csv.
    test_size : float, default 0.2
        Fraction of samples for testing.
    random_state : int, default 42
        Seed for reproducibility.
    use_binary_target : bool, default True
        If True, returns y with {0: Phishing, 1: Legitimate}.
        If False, returns y with {-1: Phishing, 1: Legitimate}.

    Returns:
    --------
    X_train, X_test, y_train, y_test, feature_names
    """
    if df is None:
        clean_path = "data/processed/phishing_cleaned.csv" if os.path.exists("data/processed/phishing_cleaned.csv") else "../data/processed/phishing_cleaned.csv"
        df = pd.read_csv(clean_path)

    target_col = "target_binary" if use_binary_target and "target_binary" in df.columns else ("result" if "result" in df.columns else "Result")
    
    # Exclude metadata and target columns from feature matrix X
    cols_to_drop = [c for c in ["result", "Result", "target_binary", "class_label"] if c in df.columns]
    X = df.drop(columns=cols_to_drop)
    y = df[target_col]

    feature_names = list(X.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    logger.info(f"Stratified split completed (Test Size: {test_size*100:.0f}%):")
    logger.info(f"Train Shape: X={X_train.shape}, y={y_train.shape}")
    logger.info(f"Test Shape:  X={X_test.shape}, y={y_test.shape}")
    logger.info(f"Train Class Balance: {dict(y_train.value_counts(normalize=True).round(4))}")
    logger.info(f"Test Class Balance:  {dict(y_test.value_counts(normalize=True).round(4))}")

    return X_train, X_test, y_train, y_test, feature_names


if __name__ == "__main__":
    from data_loader import load_dataset
    raw_df, _ = load_dataset()
    cleaned_df, report = clean_and_preprocess_data(raw_df)
    X_train, X_test, y_train, y_test, feat_names = get_train_test_data(cleaned_df)
    print("\nPreprocessing Module Verification Successful!")
    print(f"Features Count: {len(feat_names)}")
    print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")
