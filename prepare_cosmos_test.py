"""
Prepare the COSMOS test dataset for benchmarking.

This script:
1. Loads COSMOS test JSON data
2. Extracts image paths, caption pairs, and OOC/NOOC labels
3. Creates a fixed pandas DataFrame: [image_id, image_path_or_url, caption1, caption2, label]
4. Saves to data/cosmos_test_fixed.csv
5. Reports statistics and sample rows

The COSMOS dataset must be downloaded from: https://github.com/shivangi-aneja/COSMOS
Follow instructions at: https://docs.google.com/forms/d/13kJQ2wlv7sxyXoaM1Ddon6Nq7dUJY_oftl-6xzwTGow
"""

import json
import os
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
TEMP_COSMOS_DIR = PROJECT_ROOT / "temp_cosmos"

def load_cosmos_test_json(json_path: str) -> List[Dict]:
    """Load COSMOS test JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)

def extract_test_samples(data: List[Dict]) -> List[Dict]:
    """
    Extract test samples from COSMOS JSON.
    
    COSMOS test set format:
    - Each sample has: img_local_path, caption1, caption2, label (OOC/NOOC)
    - caption1, caption2: two captions for the same image
    - label: 1 if out-of-context (OOC), 0 if not out-of-context (NOOC)
    """
    samples = []
    
    for idx, sample in enumerate(data):
        # Extract required fields
        image_id = f"cosmos_test_{idx:04d}"
        image_path = sample.get('img_local_path', '')
        caption1 = sample.get('caption1', '')
        caption2 = sample.get('caption2', '')
        label = sample.get('label', -1)  # -1 if missing
        
        # Convert label to string (OOC/NOOC)
        label_str = 'OOC' if label == 1 else 'NOOC' if label == 0 else 'UNKNOWN'
        
        samples.append({
            'image_id': image_id,
            'image_path_or_url': image_path,
            'caption1': caption1,
            'caption2': caption2,
            'label': label_str,
            'label_numeric': label
        })
    
    return samples

def create_fixed_test_dataframe(samples: List[Dict]) -> pd.DataFrame:
    """Create pandas DataFrame from samples."""
    df = pd.DataFrame(samples)
    # Reorder columns to match spec
    return df[['image_id', 'image_path_or_url', 'caption1', 'caption2', 'label']]

def verify_image_availability(df: pd.DataFrame, cosmos_dir: Path) -> Tuple[int, int]:
    """
    Check how many images are available.
    
    Returns:
        (available_count, missing_count)
    """
    available = 0
    missing = 0
    
    for image_path in df['image_path_or_url']:
        if not image_path:
            missing += 1
            continue
        
        full_path = cosmos_dir / image_path
        if full_path.exists():
            available += 1
        else:
            missing += 1
    
    return available, missing

def main():
    """Main pipeline."""
    
    print("=" * 80)
    print("COSMOS Test Dataset Preparation")
    print("=" * 80)
    
    # Expected path to COSMOS test.json
    test_json_path = TEMP_COSMOS_DIR / "test.json"
    
    if not test_json_path.exists():
        print(f"\n[ERROR] Could not find test.json at: {test_json_path}")
        print("\nTo get the COSMOS dataset:")
        print("1. Visit: https://github.com/shivangi-aneja/COSMOS")
        print("2. Fill form: https://docs.google.com/forms/d/13kJQ2wlv7sxyXoaM1Ddon6Nq7dUJY_oftl-6xzwTGow")
        print("3. Download the dataset")
        print("4. Extract test.json to: temp_cosmos/test.json")
        print("5. Extract image files to: temp_cosmos/images/")
        print("6. Re-run this script")
        return False
    
    print(f"\n[INFO] Loading COSMOS test.json from: {test_json_path}")
    
    try:
        data = load_cosmos_test_json(str(test_json_path))
        print(f"[INFO] Loaded {len(data)} samples from JSON")
    except Exception as e:
        print(f"[ERROR] Failed to load JSON: {e}")
        return False
    
    # Extract samples
    print("\n[INFO] Extracting test samples...")
    samples = extract_test_samples(data)
    
    # Create DataFrame
    print("[INFO] Creating fixed test DataFrame...")
    df = create_fixed_test_dataframe(samples)
    
    # Check image availability
    print("\n[INFO] Verifying image availability...")
    available, missing = verify_image_availability(df, TEMP_COSMOS_DIR)
    print(f"  - Available: {available}")
    print(f"  - Missing/URLs: {missing}")
    print(f"  - Coverage: {100 * available / len(df):.1f}%")
    
    # Save to fixed test CSV
    output_path = DATA_DIR / "cosmos_test_fixed.csv"
    print(f"\n[INFO] Saving to: {output_path}")
    df.to_csv(str(output_path), index=False)
    
    # Report statistics
    print("\n" + "=" * 80)
    print("DATASET STATISTICS")
    print("=" * 80)
    print(f"Total samples: {len(df)}")
    print(f"\nLabel distribution:")
    label_counts = df['label'].value_counts()
    for label, count in label_counts.items():
        pct = 100 * count / len(df)
        print(f"  - {label}: {count} ({pct:.1f}%)")
    
    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Show sample rows
    print("\n" + "=" * 80)
    print("SAMPLE ROWS (first 5)")
    print("=" * 80)
    for idx, row in df.head(5).iterrows():
        print(f"\n[{idx}] {row['image_id']}")
        print(f"    Label: {row['label']}")
        print(f"    Image: {row['image_path_or_url']}")
        print(f"    Caption 1: {row['caption1'][:80]}...")
        print(f"    Caption 2: {row['caption2'][:80]}...")
    
    print("\n" + "=" * 80)
    print(f"✓ Fixed test set saved to: {output_path}")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
