# EXP011: MUSE EVIDENCE LOG

## 1. README Analysis
The README clearly states that to reproduce the experiments, one must download datasets AND their corresponding evidence datasets:
- VisualNews
- NewsCLIPings
- NewsCLIPings evidence (`queries_dataset`)
- VERITE and VERITE evidence

There is absolutely no mention of the COSMOS dataset, nor any instruction on how to run the method without the `queries_dataset`.

## 2. Code Inspection (`src/main.py`)
Lines 22-32 explicitly extract features and re-rank evidence for NewsCLIPpings and VERITE:
```python
# Extract CLIP features for NewsCLIPpings Evidence
extract_features_for_evidence(data_path=DATA_PATH, output_path=EVIDENCE_PATH, data_name_X=DATA_NAME_X, encoder=ENCODER, choose_encoder_version=ENCODER_VERSION, choose_gpu=0)
# Re-rank NewsCLIPpings evidence
rank_evidence(data_path=DATA_PATH, data_name=DATA_NAME, data_name_X=DATA_NAME_X, output_path=EVIDENCE_PATH, encoder=ENCODER, choose_encoder_version=ENCODER_VERSION)
```
The method `muse_similarity_importance` relies on calculating similarities to this evidence. The method cannot proceed without it.

## 3. Classifier Training
Lines 40+ show the method runs `run_muse_mlp()`:
```python
# Experiments for Table 4 (Ablation of MUSE-MLP)
run_muse_mlp(DATA_PATH, EVIDENCE_PATH, VERITE_PATH, full_ablation=True, encoder = ENCODER, encoder_version = ENCODER_VERSION)
```
MUSE does not supply a zero-shot OOC classifier. The architecture extracts similarities and trains a supervised classifier (MLP/RF/DT) on the specific dataset splits. Because we are forbidden from training on the COSMOS test set, we have no weights to perform inference with.
