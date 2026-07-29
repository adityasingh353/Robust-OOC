# Baseline A: NLI + CLIP (Zero-Shot)

## Methodology
- **Textual Entailment**: Used `roberta-large-mnli` to compute the contradiction probability between the two captions.
- **Image-Text Similarity**: Used `openai/clip-vit-base-patch32` to compute the absolute difference in cosine similarity between the image and each caption.
- **Rule Tuned**: `NLI_Contra > 0.1` OR `|CLIP_Sim1 - CLIP_Sim2| > 9.0`
- **Data Split**: Tuned on the first 100 samples; Evaluated strictly on the remaining **900 held-out samples** to prevent data leakage.

## Results on Held-Out Test Set (900 samples)

| Model | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: |
| **NLI-Only Rule** | 75.22% | 82.66% | 65.73% | **73.23%** |
| **Combined Rule (NLI+CLIP)** | 75.67% | 81.17% | 68.75% | **74.45%** |

## Key Findings for Dissertation
- **NLI Dominates**: The problem of Out-of-Context detection in the COSMOS dataset is largely solved by determining if the two captions contradict each other. 
- **CLIP's Minor Contribution**: Adding image-level similarity metrics via CLIP only marginally improved the F1-score (+1.22%). It boosted recall slightly (detecting more OOC samples) but decreased precision (more false positives).
