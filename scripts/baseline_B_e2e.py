import os
import sys
import pandas as pd
from PIL import Image
from tqdm import tqdm
from sklearn.metrics import accuracy_score, classification_report

# Add the root directory to the python path to allow imports from models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.baseline_B_vlm import BaselineBVLM
from models.baseline_B_classifier import BaselineBClassifier

def run_e2e_evaluation(mock_vlm=True, sample_size=10):
    print(f"Starting E2E Evaluation for Baseline B (Sample Size: {sample_size})")
    
    # Initialize Models
    print("Loading VLM...")
    vlm = BaselineBVLM(mock=mock_vlm)
    print("Loading Classifier...")
    classifier = BaselineBClassifier(device="cpu") # Use CPU to avoid VRAM exhaustion alongside VLM
    
    # Load dataset
    data_path = os.path.join("data", "cosmos_test_fixed.csv")
    df = pd.read_csv(data_path)
    
    # Limit to sample size for testing
    if sample_size is not None and sample_size > 0:
        df = df.head(sample_size)
        
    results = []
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Evaluating Pipeline"):
        image_path = os.path.join(os.getcwd(), row['image_path_or_url'])
        caption1 = row['caption1']
        caption2 = row['caption2']
        ground_truth_label = row['label']
        
        # Ground truth mapping: OOC=1, NOOC=0
        gt_int = 1 if ground_truth_label == "OOC" else 0
        
        try:
            # 1. Load Image
            if os.path.exists(image_path):
                img = Image.open(image_path).convert('RGB')
            else:
                # Fallback to dummy if missing
                img = Image.new('RGB', (224, 224), color = 'gray')
                
            # 2. Generate Contexts using VLM
            context1 = vlm.generate_context(img, caption1)
            context2 = vlm.generate_context(img, caption2)
            
            # 3. Predict using RoBERTa
            pred_int = classifier.predict(context1, context2)
            
            # Record result
            results.append({
                "image_id": row["image_id"],
                "caption1": caption1,
                "caption2": caption2,
                "context1": context1,
                "context2": context2,
                "ground_truth": gt_int,
                "prediction": pred_int
            })
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            
    # Save intermediate contexts
    results_df = pd.DataFrame(results)
    
    # Ensure directories exist
    os.makedirs(os.path.join("data", "baseline_B"), exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    intermediate_path = os.path.join("data", "baseline_B", "intermediate_contexts.csv")
    results_df.to_csv(intermediate_path, index=False)
    print(f"\nSaved intermediate contexts to {intermediate_path}")
    
    # Calculate metrics
    y_true = results_df["ground_truth"].tolist()
    y_pred = results_df["prediction"].tolist()
    
    acc = accuracy_score(y_true, y_pred)
    print(f"\nEvaluation Complete!")
    print(f"Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=["NOOC (0)", "OOC (1)"], zero_division=0))
    
    # Save final results summary
    report_md = f"""# Baseline B Results Summary
    
- **Sample Size**: {len(results_df)}
- **Mock VLM**: {mock_vlm}
- **Accuracy**: {acc:.4f}

## Classification Report
```text
{classification_report(y_true, y_pred, target_names=["NOOC (0)", "OOC (1)"], zero_division=0)}
```
"""
    with open(os.path.join("result_library", "baseline_B_summary.md"), "w") as f:
        f.write(report_md)
    print("Saved results to result_library/baseline_B_summary.md")

if __name__ == "__main__":
    run_e2e_evaluation(mock_vlm=True, sample_size=5)
