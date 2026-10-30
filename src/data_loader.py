"""
Data Loader Module for Phishing Website Detection
Author: Foundations of Data Science Project
Dataset: UCI Machine Learning Repository - Phishing Websites (ID: 327)
DOI: 10.24432/C51W2X

This module handles:
1. Fetching the official dataset via ucimlrepo API.
2. Fallback to direct HTTP download/parsing if API connectivity fails.
3. Saving a pristine raw copy of the dataset to data/raw/phishing_websites.csv.
4. Extracting and returning features (X), targets (y), and metadata.
"""

import os
import json
import logging
import zipfile
import io
import requests
import pandas as pd
from ucimlrepo import fetch_ucirepo

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

UCI_DATASET_ID = 327
FALLBACK_ZIP_URL = "https://archive.ics.uci.edu/static/public/327/phishing+websites.zip"


def load_dataset(raw_dir=None, force_reload=False):
    """
    Loads the UCI Phishing Websites dataset.
    
    If raw_dir contains 'phishing_websites.csv' and force_reload is False,
    it reads from the local cached file for fast, offline reproducibility.
    Otherwise, it fetches the dataset via ucimlrepo or fallback URL and caches it.

    Parameters:
    -----------
    raw_dir : str, optional
        Path to the data/raw folder. Defaults to '../data/raw' or 'data/raw'.
    force_reload : bool, default False
        Whether to re-download even if a cached file exists.

    Returns:
    --------
    df : pd.DataFrame
        Complete dataset including all 30 features and the target variable.
    metadata : dict
        Metadata including feature names, target description, citations, etc.
    """
    if raw_dir is None:
        # Determine appropriate path relative to current working directory
        if os.path.exists("data/raw"):
            raw_dir = "data/raw"
        elif os.path.exists("../data/raw"):
            raw_dir = "../data/raw"
        else:
            raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
    
    os.makedirs(raw_dir, exist_ok=True)
    csv_path = os.path.join(raw_dir, "phishing_websites.csv")
    meta_path = os.path.join(raw_dir, "dataset_metadata.json")

    # If cached file exists and force_reload is False, load from local disk
    if os.path.exists(csv_path) and not force_reload:
        logger.info(f"Loading cached dataset from {csv_path}")
        df = pd.read_csv(csv_path)
        metadata = {}
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        return df, metadata

    logger.info(f"Fetching UCI Dataset ID {UCI_DATASET_ID} via ucimlrepo API...")
    try:
        phishing_repo = fetch_ucirepo(id=UCI_DATASET_ID)
        X = phishing_repo.data.features
        y = phishing_repo.data.targets
        
        # Combine into a single complete dataframe
        df = pd.concat([X, y], axis=1)
        
        metadata = {
            "name": phishing_repo.metadata.get("name", "Phishing Websites"),
            "uci_id": UCI_DATASET_ID,
            "doi": "10.24432/C51W2X",
            "num_instances": int(phishing_repo.metadata.get("num_instances", len(df))),
            "num_features": int(phishing_repo.metadata.get("num_features", len(X.columns))),
            "target_col": list(y.columns),
            "feature_names": list(X.columns),
            "citation": "Mohammad, R. (2015). Phishing Websites. UCI Machine Learning Repository. https://doi.org/10.24432/C51W2X."
        }
        logger.info("Successfully fetched dataset via ucimlrepo.")
    except Exception as e:
        logger.warning(f"ucimlrepo fetch failed ({e}). Attempting fallback download from UCI archive...")
        df, metadata = _fetch_fallback()

    # Save to local raw directory for offline preservation
    df.to_csv(csv_path, index=False)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)
    logger.info(f"Saved pristine raw dataset to {csv_path} and metadata to {meta_path}")

    return df, metadata


def _fetch_fallback():
    """
    Fallback method: downloads the official zip archive from UCI and parses the ARFF/CSV file.
    """
    resp = requests.get(FALLBACK_ZIP_URL, timeout=30)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        # Search for .arff or .csv in the zip archive
        arff_candidates = [n for n in z.namelist() if n.endswith(".arff")]
        csv_candidates = [n for n in z.namelist() if n.endswith(".csv")]
        
        if arff_candidates:
            from scipy.io import arff
            with z.open(arff_candidates[0]) as f:
                data, meta = arff.loadarff(io.StringIO(f.read().decode("utf-8", errors="ignore")))
                df = pd.DataFrame(data)
                # Decode byte strings to integers or strings if needed
                for col in df.columns:
                    if df[col].dtype == object:
                        try:
                            df[col] = df[col].str.decode("utf-8").astype(int)
                        except Exception:
                            pass
        elif csv_candidates:
            with z.open(csv_candidates[0]) as f:
                df = pd.read_csv(f)
        else:
            raise FileNotFoundError("Could not find ARFF or CSV file in UCI zip archive.")

    target_col = [col for col in df.columns if col.lower() in ["result", "target", "class"]]
    features = [c for c in df.columns if c not in target_col]
    
    metadata = {
        "name": "Phishing Websites",
        "uci_id": UCI_DATASET_ID,
        "doi": "10.24432/C51W2X",
        "num_instances": len(df),
        "num_features": len(features),
        "target_col": target_col,
        "feature_names": features,
        "citation": "Mohammad, R. (2015). Phishing Websites. UCI Machine Learning Repository. https://doi.org/10.24432/C51W2X."
    }
    return df, metadata


def get_feature_target_split(df, target_col="Result"):
    """
    Splits DataFrame into features (X) and target (y).
    """
    if target_col not in df.columns:
        possible = [c for c in df.columns if c.lower() == target_col.lower()]
        if possible:
            target_col = possible[0]
        else:
            target_col = df.columns[-1]
            
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y


if __name__ == "__main__":
    df, meta = load_dataset()
    print("Dataset Shape:", df.shape)
    print("Target column:", meta.get("target_col"))
    print("Class counts:\n", df[meta.get("target_col")[0] if meta.get("target_col") else df.columns[-1]].value_counts())
