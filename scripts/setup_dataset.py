import os
import urllib.request
import zipfile
import json
import pandas as pd
from pathlib import Path
import random

# Constants
ANNS_URL = "http://kaldir.vc.in.tum.de/cosmos_anns.zip"
TEST_IMG_URL = "http://kaldir.vc.in.tum.de/images_test.zip"
DATA_DIR = Path("data")
TEMP_DIR = DATA_DIR / "temp"

def download_file(url, dest):
    if not dest.exists():
        print(f"Downloading {url} to {dest}...")
        urllib.request.urlretrieve(url, dest)
    else:
        print(f"File {dest} already exists.")

def extract_zip(zip_path, extract_to):
    print(f"Extracting {zip_path} to {extract_to}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Download
    anns_zip = TEMP_DIR / "cosmos_anns.zip"
    test_img_zip = TEMP_DIR / "images_test.zip"
    
    download_file(ANNS_URL, anns_zip)
    download_file(TEST_IMG_URL, test_img_zip)
    
    # 2. Extract
    # test.json is usually directly in the zip or inside a folder.
    extract_zip(anns_zip, TEMP_DIR / "anns")
    # images_test is usually a directory of images
    extract_zip(test_img_zip, DATA_DIR / "images_test")
    
    # Locate test.json
    anns_dir = TEMP_DIR / "anns"
    test_json_path = None
    for path in anns_dir.rglob("*.json"):
        if path.name == "test_data.json":
            test_json_path = path
            break
            
    if not test_json_path:
        print("Error: test_data.json not found in annotations zip.")
        return
        
    print(f"Loading annotations from {test_json_path}")
    with open(test_json_path, 'r', encoding='utf-8') as f:
        # Note: if test.json is an array or a single line per record.
        # Check if it's list of dicts or new line separated json
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # Maybe jsonlines
            f.seek(0)
            data = [json.loads(line) for line in f]
            
    # Assuming test data is a list of dictionaries.
    
    valid_samples = []
    missing_images = 0
    test_img_dir = DATA_DIR / "images_test"
    
    print(f"Total entries in test.json: {len(data)}")
    
    for item in data:
        img_path = item.get("img_local_path", "")
        img_name = Path(img_path).name
        
        # Check if we have this image extracted somewhere
        image_exists = False
        actual_path = ""
        # Let's see if the file exists directly or in subdirectories
        for p in test_img_dir.rglob(img_name):
            image_exists = True
            actual_path = str(p.relative_to(DATA_DIR.parent).as_posix())
            break
            
        if not image_exists:
            missing_images += 1
            continue
            
        # Extract desired fields
        image_id = img_name.split('.')[0]
        # label: 1=Out-of-Context, 0=Not-Out-of-Context
        label_int = item.get("context_label")
        # Ensure label format
        if str(label_int) == "1" or str(label_int).lower() == "ooc":
            label_str = "OOC"
        else:
            label_str = "NOOC"
            
        sample = {
            "image_id": image_id,
            "image_path_or_url": actual_path,
            "caption1": item.get("caption1", ""),
            "caption2": item.get("caption2", ""),
            "label": label_str
        }
        valid_samples.append(sample)
        
    print(f"Images successfully found: {len(valid_samples)}")
    print(f"Missing images: {missing_images}")
    
    # Downsample to exactly 1000 to match user's prompt
    if len(valid_samples) > 1000:
        random.seed(42)
        valid_samples = random.sample(valid_samples, 1000)
        print("Subsampled to 1000 samples for the fixed test set.")
        
    # Convert to DataFrame
    df = pd.DataFrame(valid_samples)
    
    out_csv = DATA_DIR / "cosmos_test_fixed.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nSaved dataset to {out_csv}")
    
    # Print stats
    print("\n--- Dataset Stats ---")
    print(f"Total samples: {len(df)}")
    print("Label distribution:")
    print(df['label'].value_counts())
    
    print("\n--- Sample Rows (first 5) ---")
    print(df.head(5).to_string())

if __name__ == "__main__":
    main()
