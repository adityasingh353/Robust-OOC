import os
import torch
import pandas as pd
from PIL import Image
from transformers import AutoTokenizer, AutoModelForSequenceClassification, CLIPProcessor, CLIPModel
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pathlib import Path

DATA_CSV = Path("data/cosmos_test_fixed.csv")
RESULTS_DIR = Path("results")
SUBSET_FEATURES_CSV = RESULTS_DIR / "subset_features_A.csv"

def extract_features(df, nli_model, nli_tokenizer, clip_model, clip_processor, device):
    features = []
    
    print("Extracting features...")
    for idx, row in df.iterrows():
        if idx % 10 == 0:
            print(f"Processed {idx}/{len(df)} samples")
            
        cap1 = row['caption1']
        cap2 = row['caption2']
        img_path = row['image_path_or_url']
        label = row['label']
        
        # --- NLI ---
        # RoBERTa MNLI expects format: premise, hypothesis
        inputs_nli = nli_tokenizer(cap1, cap2, return_tensors="pt", truncation=True).to(device)
        with torch.no_grad():
            outputs_nli = nli_model(**inputs_nli)
            # MNLI label mapping for roberta-large-mnli: 0: CONTRADICTION, 1: NEUTRAL, 2: ENTAILMENT
            # Wait, let's double check. Actually, roberta-large-mnli config: 
            # 0: CONTRADICTION, 1: NEUTRAL, 2: ENTAILMENT
            # Or sometimes: 0: entailment, 1: neutral, 2: contradiction
            # Let's just use logits softmax and take the max contradiction logit.
            probs = outputs_nli.logits.softmax(dim=-1)[0]
            
            # Using model.config.id2label to be safe
            id2label = nli_model.config.id2label
            # Find the ID for contradiction
            contradiction_id = -1
            for k, v in id2label.items():
                if "contradict" in v.lower():
                    contradiction_id = k
                    break
            
            # If not found, fallback to common pattern (2 is contradiction for roberta)
            if contradiction_id == -1:
                contradiction_id = 2
                
            nli_contra_prob = probs[contradiction_id].item()

        # --- CLIP ---
        try:
            image = Image.open(img_path).convert("RGB")
            inputs_clip = clip_processor(text=[cap1, cap2], images=image, return_tensors="pt", padding=True).to(device)
            with torch.no_grad():
                outputs_clip = clip_model(**inputs_clip)
                # Image-text similarity score
                # The logits_per_image represents similarities
                sims = outputs_clip.logits_per_image[0] # Shape: (2,)
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

def tune_thresholds(df_features):
    print("\n--- Tuning Rule on 100 Samples ---")
    
    best_f1 = -1
    best_rule = None
    
    # We will predict OOC if (nli_contra_prob > t_nli) OR (clip_sim_diff > t_clip)
    # Let's try some thresholds
    t_nli_vals = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 1.1] # 1.1 means never use NLI
    t_clip_vals = [1.0, 3.0, 5.0, 7.0, 9.0, 12.0, 100.0] # 100.0 means never use CLIP
    
    true_y = (df_features['true_label'] == 'OOC').astype(int)
    
    results = []
    
    for tn in t_nli_vals:
        for tc in t_clip_vals:
            pred_y = ((df_features['nli_contra_prob'] > tn) | (df_features['clip_sim_diff'] > tc)).astype(int)
            acc = accuracy_score(true_y, pred_y)
            f1 = f1_score(true_y, pred_y, zero_division=0)
            
            results.append((tn, tc, acc, f1))
            
            if f1 > best_f1:
                best_f1 = f1
                best_rule = (tn, tc)
                
    results_df = pd.DataFrame(results, columns=["T_NLI", "T_CLIP_DIFF", "Accuracy", "F1"])
    results_df = results_df.sort_values(by="F1", ascending=False).head(10)
    
    print("\nTop 10 Threshold Combinations (sorted by F1):")
    print(results_df.to_string(index=False))
    print(f"\nRecommended Rule:")
    print(f"Predict OOC if (NLI_Contra > {best_rule[0]} OR |CLIP_Sim1 - CLIP_Sim2| > {best_rule[1]})")
    print(f"F1-Score on subset: {best_f1:.4f}")
    
def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    
    df = pd.read_csv(DATA_CSV)
    df_subset = df.head(100)
    
    if SUBSET_FEATURES_CSV.exists():
        print(f"Loading cached features from {SUBSET_FEATURES_CSV}")
        df_features = pd.read_csv(SUBSET_FEATURES_CSV)
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
        
        df_features = extract_features(df_subset, nli_model, nli_tokenizer, clip_model, clip_processor, device)
        df_features.to_csv(SUBSET_FEATURES_CSV, index=False)
        
    tune_thresholds(df_features)

if __name__ == "__main__":
    main()
