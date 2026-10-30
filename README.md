# Robust-OOC: Robustness & Benchmarking Framework for Out-Of-Context Detection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Research%20Benchmark%20Active-brightgreen.svg)]()

> **M.Tech Research Project**: Rigorous, reproducible benchmarking and adversarial perturbation testing for Multimodal Out-of-Context (OOC / "Cheapfake") misinformation detection on the COSMOS dataset.

---

## 📌 Verified Project Records & Evidence Artifacts

The following project records, frozen splits, reproduction audits, and evaluation reports are attached to verify the experimental rigor and progress of the research:

| Evidence / File | What It Proves | Location / Link |
| :--- | :--- | :--- |
| **`DATASET_SPLIT_FREEZE_REPORT.md`** | COSMOS dataset split & leakage-free evaluation partitioning | [`results/DATASET_SPLIT_FREEZE_REPORT.md`](results/DATASET_SPLIT_FREEZE_REPORT.md) |
| **`split_manifest.json`** | Frozen sample IDs (100-dev, 900-test) and SHA-256 checksums | [`data/COSMOS-FIXED-v1/split_manifest.json`](data/COSMOS-FIXED-v1/split_manifest.json) |
| **Baseline A evaluation report** | NLI (`roberta-large-mnli`) + CLIP zero-shot evaluation results | [`result_library/baseline_A_summary.md`](result_library/baseline_A_summary.md) |
| **Baseline B evaluation report** | Approximate reproduction results (LLaVA-1.5 7B + RoBERTa classifier) | [`result_library/baseline_B_summary.md`](result_library/baseline_B_summary.md) |
| **`EXP006_CSGM_REPRO_AUDIT.md`** | Reproducibility audit on Scene-Graph Matching (CSGM / ICMR2024) | [`results/EXP006_CSGM_REPRO_AUDIT.md`](results/EXP006_CSGM_REPRO_AUDIT.md) |
| **Mid-semester PPT / Project Guide** | Overall research explanation, terminology, and progress overview | [`Important/PROJECT_EXPLANATION_FOR_PRESENTATION.md`](Important/PROJECT_EXPLANATION_FOR_PRESENTATION.md) |

---

## 🔬 Project Overview

### 1. The Core Problem
Unlike synthetic *deepfakes* where visual pixels are manipulated by generative models, **cheapfakes** (or *Out-Of-Context* media) repurpose genuine, unedited images with false or misleading captions. Existing published models often:
1. Report scores on inconsistent, arbitrary test splits (e.g. 80% vs 50%).
2. Suffer from critical data leakage (hyperparameter tuning on the full evaluation set).
3. Depend on unreleased or unreproducible scene-graph / feature-extraction pipelines.
4. Have never been systematically stress-tested against deliberate caption perturbations (entity swaps, temporal shifts, negation).

### 2. Our Two-Phase Methodology
* **Phase 1: Reproducibility Audits & Controlled Baselines**
  * Frozen benchmark split: `COSMOS-FIXED-v1` (100 tuning samples, 900 strictly isolated held-out evaluation samples).
  * **Baseline A (NLI + CLIP)**: Zero-shot textual contradiction + image-text alignment.
  * **Baseline B (LLaVA + RoBERTa)**: Surrogate vision-language generation with RoBERTa context classification.
  * Systematic reproducibility auditing of literature (CSGM, Unified Network, etc.).
* **Phase 2: Adversarial Robustness Testing (Perturbation Suite)**
  * Evaluating model degradation under 5 targeted semantic perturbations:
    1. **Paraphrase**: Semantic preservation with lexical variety.
    2. **Entity Swap**: Named entity substitutions (people, organizations).
    3. **Negation**: Logical inversion of factuality.
    4. **Date/Temporal Shift**: Shifting timeline references.
    5. **Location Shift**: Shifting geographic locations.

---

## 📊 Summary of Baseline Results

Evaluated on the frozen **`COSMOS-FIXED-v1`** held-out test benchmark:

| Model / Pipeline | Split | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline A (NLI-Only)** | 900 Held-Out | 75.22% | 82.66% | 65.73% | 73.23% |
| **Baseline A (NLI + CLIP)** | 900 Held-Out | **75.67%** | 81.17% | 68.75% | **74.45%** |
| **Baseline B (LLaVA-1.5 + RoBERTa)** | 1000 Full Fixed | 64.10% | — | — | — |

Comprehensive details available in [`result_library/PROJECT_STATUS_REPORT.md`](result_library/PROJECT_STATUS_REPORT.md).

---

## 📂 Repository Structure

```text
Robust-OOC/
├── data/
│   ├── COSMOS-FIXED-v1/             # Frozen benchmark splits & split manifest
│   │   ├── cosmos_dev_100.csv       # 100 tuning samples
│   │   ├── cosmos_test_900.csv      # 900 held-out evaluation samples
│   │   ├── split_manifest.json      # Cryptographic checksums and sample IDs
│   │   └── SPLIT_DEFINITION.md     # Protocol rules
│   └── cosmos_test_fixed.csv        # Master fixed 1000-sample dataset
├── eval/
│   └── evaluate_splits.py           # Strict leakage-free split evaluation runner
├── Important/
│   └── PROJECT_EXPLANATION_FOR_PRESENTATION.md  # Mid-sem progress explanation
├── models/
│   ├── baseline_B_classifier.py     # RoBERTa context classifier
│   └── baseline_B_vlm.py            # LLaVA prompt & context extraction
├── result_library/
│   ├── baseline_A_summary.md        # Detailed Baseline A report
│   ├── baseline_B_summary.md        # Detailed Baseline B report
│   ├── PROJECT_STATUS_REPORT.md     # Master dissertation status report
│   └── reproducibility_audits_summary.md # Comprehensive paper audit log
├── results/
│   ├── DATASET_SPLIT_FREEZE_REPORT.md # Verification report for frozen splits
│   ├── EXP006_CSGM_REPRO_AUDIT.md     # CSGM paper reproducibility audit
│   └── baseline_A_predictions.csv     # Model predictions on 900 held-out test
├── scripts/
│   ├── baseline_A.py                # Zero-shot feature extraction
│   └── baseline_B_e2e.py            # Baseline B end-to-end pipeline
└── README.md
```

---

## 🚀 Getting Started

### 1. Environment Setup
```bash
git clone https://github.com/adityasingh353/Robust-OOC.git
cd Robust-OOC
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt  # Or install torch, transformers, clip
```

### 2. Verify Dataset Splits & Hashes
```bash
python -c "import json; m=json.load(open('data/COSMOS-FIXED-v1/split_manifest.json')); print('Split loaded:', m['dataset_version'], 'Total Samples:', len(m['splits']['dev_100']['sample_ids']) + len(m['splits']['test_900']['sample_ids']))"
```

### 3. Run Leakage-Free Baseline A Evaluation
```bash
python eval/evaluate_splits.py
```

---

## 📜 Citation & Credits
- **Dataset**: COSMOS Dataset (*Aneja et al., "COSMOS: Catching Out-of-Context Misinformation using Self-Supervised Learning", 2021*)
- **Baseline Architectures**: `roberta-large-mnli`, `openai/clip-vit-base-patch32`, LLaVA-1.5, and RoBERTa Cheapfake Classifier checkpoint.
