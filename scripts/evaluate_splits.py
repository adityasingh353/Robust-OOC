import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from pathlib import Path

FEATURES_CSV = Path("results/full_features_A.csv")
PREDICTIONS_CSV = Path("results/baseline_A_predictions.csv")

def evaluate_rule(df, rule_name, t_nli, t_clip=None):
    true_y = (df['true_label'] == 'OOC').astype(int)
    
    if t_clip is None:
        # NLI only
        pred_y_int = (df['nli_contra_prob'] > t_nli).astype(int)
    else:
        # Combined
        pred_y_int = ((df['nli_contra_prob'] > t_nli) | (df['clip_sim_diff'] > t_clip)).astype(int)
        
    acc = accuracy_score(true_y, pred_y_int)
    prec = precision_score(true_y, pred_y_int, zero_division=0)
    rec = recall_score(true_y, pred_y_int, zero_division=0)
    f1 = f1_score(true_y, pred_y_int, zero_division=0)
    
    print(f"\n--- {rule_name} ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    return pred_y_int

def main():
    print("Loading extracted features from", FEATURES_CSV)
    df_features = pd.read_csv(FEATURES_CSV)
    
    # The first 100 samples were used for tuning.
    df_tuning = df_features.head(100)
    df_heldout = df_features.tail(len(df_features) - 100)
    
    print(f"\nTotal samples: {len(df_features)}")
    print(f"Tuning set size: {len(df_tuning)}")
    print(f"Held-out set size: {len(df_heldout)}")
    
    # 1. Tuning Set Performance (Combined Rule)
    print("\n================ EVALUATION ON TUNING SET (100) ================")
    evaluate_rule(df_tuning, "Combined Rule (NLI > 0.1 OR CLIP_Diff > 9.0)", t_nli=0.1, t_clip=9.0)
    
    # 2. Held-out Set Performance
    print("\n================ EVALUATION ON HELD-OUT SET (900) ================")
    
    # NLI Only
    evaluate_rule(df_heldout, "NLI-Only Rule (NLI > 0.1)", t_nli=0.1)
    
    # Combined Rule
    pred_y_combined = evaluate_rule(df_heldout, "Combined Rule (NLI > 0.1 OR CLIP_Diff > 9.0)", t_nli=0.1, t_clip=9.0)
    
    # 3. Save predictions for the held-out set
    predictions = []
    for i, (idx, row) in enumerate(df_heldout.iterrows()):
        pred_label = "OOC" if pred_y_combined.iloc[i] == 1 else "NOOC"
        conf_score = max(row['nli_contra_prob'], min(1.0, row['clip_sim_diff'] / 20.0))
        
        predictions.append({
            "image_id": row["image_id"],
            "true_label": row["true_label"],
            "predicted_label": pred_label,
            "confidence_score": conf_score,
            "split": "held-out"
        })
        
    df_preds = pd.DataFrame(predictions)
    df_preds.to_csv(PREDICTIONS_CSV, index=False)
    print(f"\nSaved held-out predictions ({len(df_preds)} rows) to {PREDICTIONS_CSV}")

if __name__ == "__main__":
    main()
