import os
import torch
import pandas as pd
from PIL import Image
from transformers import AutoTokenizer, AutoModelForSequenceClassification, CLIPProcessor, CLIPModel
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pathlib import Path
import warnings

# Suppress some transformers warnings
warnings.filterwarnings("ignore")

DATA_CSV = Path("data/cosmos_test_fixed.csv")
RESULTS_DIR = Path("results")
PREDICTIONS_CSV = RESULTS_DIR / "baseline_A_predictions.csv"
FEATURES_CSV = RESULTS_DIR / "full_features_A.csv"

def extract_features(df, nli_model, nli_tokenizer, clip_model, clip_processor, device):
    features = []
    
    print("Extracting features for full dataset...")
    for idx, row in df.iterrows():
        if idx % 100 == 0:
            print(f"Processed {idx}/{len(df)} samples")
            
        cap1 = row['caption1']
        cap2 = row['caption2']
        img_path = row['image_path_or_url']
        label = row['label']
        
        # --- NLI ---
        inputs_nli = nli_tokenizer(cap1, cap2, return_tensors="pt", truncation=True).to(device)
        with torch.no_grad():
            outputs_nli = nli_model(**inputs_nli)
            probs = outputs_nli.logits.softmax(dim=-1)[0]
            
            id2label = nli_model.config.id2label
            contradiction_id = -1
            for k, v in id2label.items():
                if "contradict" in v.lower():
                    contradiction_id = k
                    break
            if contradiction_id == -1:
                contradiction_id = 2
                
            nli_contra_prob = probs[contradiction_id].item()

        # --- CLIP ---
        try:
            image = Image.open(img_path).convert("RGB")
            # Added truncation=True to prevent crashes on long captions
            inputs_clip = clip_processor(text=[cap1, cap2], images=image, return_tensors="pt", padding=True, truncation=True).to(device)
            with torch.no_grad():
                outputs_clip = clip_model(**inputs_clip)
                sims = outputs_clip.logits_per_image[0]
                clip_sim_1 = sims[0].item()
                clip_sim_2 = sims[1].item()
        except Exception as e:
            print(f"Error loading image {img_path}: {e}")
            clip_sim_1, clip_sim_2 = 0.0, 0.0
            
        features.append({
            "image_id": row["image_id"],
            "true_label": label,
            "nli_contra_prob": nli_contra_prob,
            "clip_sim_1": clip_sim_1,
            "clip_sim_2": clip_sim_2,
            "clip_sim_diff": abs(clip_sim_1 - clip_sim_2)
        })
        
    return pd.DataFrame(features)

def evaluate(df_features, t_nli, t_clip):
    print(f"\n--- Evaluating Full Set ---")
    print(f"Rule: OOC if NLI_Contra > {t_nli} OR |CLIP_Sim1 - CLIP_Sim2| > {t_clip}")
    
    true_y = (df_features['true_label'] == 'OOC').astype(int)
    pred_y_int = ((df_features['nli_contra_prob'] > t_nli) | (df_features['clip_sim_diff'] > t_clip)).astype(int)
    
    # Calculate metrics
    acc = accuracy_score(true_y, pred_y_int)
    prec = precision_score(true_y, pred_y_int, zero_division=0)
    rec = recall_score(true_y, pred_y_int, zero_division=0)
    f1 = f1_score(true_y, pred_y_int, zero_division=0)
    
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    # Prepare predictions dataframe
    predictions = []
    for i, row in df_features.iterrows():
        # Confidence score could be just max of the normalized signals
        conf_score = max(row['nli_contra_prob'], min(1.0, row['clip_sim_diff'] / 20.0))
        pred_label = "OOC" if pred_y_int[i] == 1 else "NOOC"
        
        predictions.append({
            "image_id": row["image_id"],
            "true_label": row["true_label"],
            "predicted_label": pred_label,
            "confidence_score": conf_score
        })
        
    df_preds = pd.DataFrame(predictions)
    df_preds.to_csv(PREDICTIONS_CSV, index=False)
    print(f"\nSaved predictions to {PREDICTIONS_CSV}")

def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    df = pd.read_csv(DATA_CSV)
    
    if FEATURES_CSV.exists():
        print(f"Loading cached full features from {FEATURES_CSV}")
        df_features = pd.read_csv(FEATURES_CSV)
    else:
        print("Loading models...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        nli_tokenizer = AutoTokenizer.from_pretrained("roberta-large-mnli")
        nli_model = AutoModelForSequenceClassification.from_pretrained("roberta-large-mnli").to(device)
        nli_model.eval()
        
        clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
        clip_model.eval()
        
        df_features = extract_features(df, nli_model, nli_tokenizer, clip_model, clip_processor, device)
        df_features.to_csv(FEATURES_CSV, index=False)
        
    # Evaluate using the tuned thresholds
    T_NLI = 0.1
    T_CLIP = 9.0
    evaluate(df_features, T_NLI, T_CLIP)

if __name__ == "__main__":
    main()
