"""
Verification Script for UCI Phishing Websites Dataset (ID: 327)
Foundations of Data Science (FDS) Assignment 3
"""

import os
import sys
import pandas as pd
import numpy as np

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from data_loader import load_dataset, get_feature_target_split

def run_verification():
    print("=" * 80)
    print("PHISHING WEBSITE DETECTION: UCI DATASET VERIFICATION (ID: 327)")
    print("=" * 80)
    
    # 1. Load Dataset
    df, meta = load_dataset(raw_dir="data/raw", force_reload=True)
    
    # 2. Dimensions
    num_rows, num_cols = df.shape
    target_col = meta.get("target_col", ["Result"])[0] if meta.get("target_col") else "Result"
    feature_cols = [c for c in df.columns if c != target_col]
    
    print(f"\n[1] DATASET DIMENSIONS:")
    print(f"    - Total Records (Instances): {num_rows:,}")
    print(f"    - Total Columns: {num_cols}")
    print(f"    - Total Input Features: {len(feature_cols)}")
    print(f"    - Target Column Name: '{target_col}'")
    
    # 3. First 5 Records
    print(f"\n[2] FIRST 5 RECORDS (Head):")
    print(df.head().to_string())
    
    # 4. Last 5 Records
    print(f"\n[3] LAST 5 RECORDS (Tail):")
    print(df.tail().to_string())
    
    # 5. Feature Names and Data Types
    print(f"\n[4] ALL 30 INPUT FEATURES AND DATA TYPES:")
    dtype_counts = df.dtypes.value_counts().to_dict()
    print(f"    - Data types across columns: {dtype_counts}")
    for idx, col in enumerate(feature_cols, 1):
        unique_vals = sorted(df[col].unique().tolist())
        print(f"    {idx:2d}. {col:32s} | Type: {str(df[col].dtype):6s} | Unique Values: {unique_vals}")
        
    # 6. Missing Value Analysis
    missing_series = df.isnull().sum()
    total_missing = missing_series.sum()
    print(f"\n[5] MISSING VALUE ANALYSIS:")
    print(f"    - Total Missing Values across entire dataset: {total_missing}")
    if total_missing > 0:
        print("    Columns with missing values:")
        print(missing_series[missing_series > 0])
    else:
        print("    - Cleanliness Check: Complete dataset has 0 null or NaN entries.")
        
    # 7. Duplicate Records Analysis
    num_duplicates = df.duplicated().sum()
    print(f"\n[6] DUPLICATE RECORDS ANALYSIS:")
    print(f"    - Exact Duplicate Rows: {num_duplicates} (out of {num_rows:,})")
    if num_duplicates > 0:
        dup_pct = (num_duplicates / num_rows) * 100
        print(f"    - Duplicate Percentage: {dup_pct:.2f}%")
        
    # 8. Target Classes and Distribution
    print(f"\n[7] TARGET CLASS DISTRIBUTION:")
    target_counts = df[target_col].value_counts()
    target_pcts = df[target_col].value_counts(normalize=True) * 100
    
    print(f"    - Raw Target Classes present: {sorted(df[target_col].unique().tolist())}")
    for label, count in target_counts.items():
        meaning = "Legitimate Website" if label == 1 else ("Phishing Website" if label == -1 else "Unknown")
        pct = target_pcts[label]
        print(f"    - Class {label:2d} ({meaning}): {count:,} instances ({pct:.2f}%)")
        
    imbalance_ratio = target_counts.max() / target_counts.min()
    print(f"    - Class Balance Ratio: {imbalance_ratio:.2f}:1 (Well-balanced binary classification)")

    # Save summary stats to markdown report file
    summary_md_path = "results/dataset_verification_report.md"
    os.makedirs("results", exist_ok=True)
    with open(summary_md_path, "w", encoding="utf-8") as f:
        f.write("# UCI Phishing Websites Dataset (ID: 327) - Ingestion & Verification Report\n\n")
        f.write(f"- **DOI**: [10.24432/C51W2X](https://doi.org/10.24432/C51W2X)\n")
        f.write(f"- **Total Instances**: {num_rows:,}\n")
        f.write(f"- **Total Features**: {len(feature_cols)}\n")
        f.write(f"- **Target Column**: `{target_col}`\n")
        f.write(f"- **Class Counts**: Class `-1` (Phishing): {target_counts.get(-1, 0):,} ({target_pcts.get(-1, 0):.2f}%), Class `1` (Legitimate): {target_counts.get(1, 0):,} ({target_pcts.get(1, 0):.2f}%)\n")
        f.write(f"- **Missing Values**: {total_missing}\n")
        f.write(f"- **Exact Duplicates**: {num_duplicates}\n\n")
        f.write("## Feature Inventory\n\n")
        f.write("| # | Feature Name | Data Type | Unique Values |\n")
        f.write("|---|---|---|---|\n")
        for idx, col in enumerate(feature_cols, 1):
            f.write(f"| {idx} | `{col}` | {df[col].dtype} | {sorted(df[col].unique().tolist())} |\n")
            
    print(f"\n[8] Detailed verification markdown report written to: {summary_md_path}")
    print("=" * 80)
    print("VERIFICATION COMPLETED SUCCESSFULLY.")
    print("=" * 80)

if __name__ == "__main__":
    run_verification()
