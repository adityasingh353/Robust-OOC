# COMPLETE PROJECT STATUS REPORT: RobustOOC

=========================
## 1. PROJECT GOAL
=========================
**Original Objective**: The primary objective of the "RobustOOC" project is to build a fair benchmarking and robustness-testing framework for cheapfakes (out-of-context, or OOC) image-caption detection methods.

**Research Problem**: Multiple published papers addressing OOC detection on the COSMOS benchmark dataset (Aneja et al., 2021) report accuracy metrics using completely different subsets and splits of the test data (e.g., 80% vs 50%). Furthermore, some papers demonstrate extreme drops in performance between public and private tests (e.g., 95.6% dropping to 61.7%), suggesting severe overfitting. Consequently, the reported numbers in existing literature are incomparable. Additionally, none of the current methods robustly test against adversarial perturbations such as caption paraphrasing or entity swaps.

**Why it is being studied**: Detecting unaltered images used in misleading or false contexts is a critical challenge in fighting misinformation. A standardized, rigorous, and adversarially robust benchmarking framework is necessary to measure true progress in the field rather than dataset-specific overfitting.

=========================
## 2. PROJECT TIMELINE
=========================
**Milestone 1: Dataset Acquisition and Formatting**
- **What was done**: Downloaded the official COSMOS test annotations and test images. Extracted and parsed the JSON files into a structured CSV format.
- **Why it was done**: To establish a fixed, permanent evaluation benchmark that all future methods in this project will be tested against, ensuring fair comparison.
- **Status**: Completed.
- **Output files**: `data/cosmos_test_fixed.csv`

**Milestone 2: Baseline A Implementation (Feature Extraction & Tuning)**
- **What was done**: Extracted NLI textual contradiction scores and CLIP image-text similarity scores for the dataset. Tuned threshold rules on a subset.
- **Why it was done**: To establish a zero-shot, lightweight baseline without fine-tuning, reflecting standard pre-trained capabilities.
- **Status**: Completed.
- **Output files**: `results/full_features_A.csv`, `scripts/baseline_A.py`, `scripts/baseline_A_subset.py`

**Milestone 3: Evaluation Methodology Fix**
- **What was done**: Fixed a data leakage issue where tuning samples overlapped with the final evaluation set. Segregated the dataset into a 100-sample tuning split and a 900-sample held-out split.
- **Why it was done**: To prevent inflated accuracy reporting and adhere to rigorous machine learning evaluation standards.
- **Status**: Completed.
- **Output files**: `eval/evaluate_splits.py`, `results/baseline_A_predictions.csv`

**Milestone 4: Repository Restructuring**
- **What was done**: Created standard project directories (`models/`, `eval/`, `notebooks/`, `result_library/`) and reorganized scripts.
- **Why it was done**: To systematize the workflow and structure the codebase cleanly for the M.Tech dissertation.
- **Status**: Completed.
- **Output files**: Directory structure and `result_library/README.md`.

=========================
## 3. DATASET
=========================
- **Source**: Official COSMOS server (`http://kaldir.vc.in.tum.de/cosmos_anns.zip` and `http://kaldir.vc.in.tum.de/images_test.zip`)
- **Download Location**: Extracted locally to `data/temp/anns/` and `data/images_test/`.
- **Number of Samples**: The raw `test_data.json` contained 1700 samples.
- **Filtering**: Verified physical existence of images. 1699 samples were valid (1 missing image).
- **Random Seed**: `42`
- **Subsampling**: We randomly sampled exactly 1000 samples to form our fixed benchmark.
- **Validation (Tuning) Split**: The first 100 samples of the subsampled 1000.
- **Held-out Split**: The remaining 900 samples.
- **Train/Test Split**: There is no training split in this project scope; we are purely evaluating zero-shot inference pipelines.
- **CSV Files Created**: `data/cosmos_test_fixed.csv` (Columns: `image_id`, `image_path_or_url`, `caption1`, `caption2`, `label`)
- **Label Distribution (Full 1000)**: 513 OOC (Out-Of-Context), 487 NOOC (Not-Out-Of-Context).
- **Design Decision**: We explicitly verified that all 1700 original samples were Task 1 formats (containing both caption1 and caption2) to ensure alignment with standard evaluation methodologies (e.g., Vo-Hoang et al.).

=========================
## 4. DATA LEAKAGE FIXES
=========================
- **The Issue**: During the initial execution of Baseline A, threshold rules were determined by optimizing F1-scores on a 100-sample subset. However, the subsequent "full evaluation" was run on the entire 1000-sample set, which included those exact 100 tuning samples.
- **Why it was wrong**: Evaluating a model or rule on the same data used to tune its hyperparameters constitutes data leakage. It artificially inflates performance metrics because the model has "seen" the evaluation data during optimization.
- **How it was fixed**: We explicitly sliced the feature dataset into two non-overlapping chunks: `df.head(100)` for the tuning set and `df.tail(900)` for the held-out set. The rule was established strictly on the 100 tuning samples, and final metrics were recalculated and officially reported *only* on the 900 held-out samples.
- **Methodology Improvements**: Implemented a dedicated evaluation script (`eval/evaluate_splits.py`) to permanently isolate subset scoring.

=========================
## 5. BASELINE A
=========================
**Complete Pipeline**:
1. Tokenize and pass `caption1` and `caption2` through an NLI model. Extract the probability of the `CONTRADICTION` class.
2. Pass the image along with `caption1` and `caption2` through a CLIP model. Extract the cosine similarity between the image and each caption. Compute the absolute difference: `|CLIP_Sim1 - CLIP_Sim2|`.
3. Apply a logical rule based on optimized thresholds to determine if the sample is OOC.

**Models and Checkpoints**:
- NLI Text Model: `roberta-large-mnli` (HuggingFace)
- Image-Text Similarity Model: `openai/clip-vit-base-patch32` (HuggingFace)

**Tuning Procedure**:
A grid search was executed on the 100-sample tuning split over `T_NLI` values [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 1.1] and `T_CLIP_DIFF` values [1.0, 3.0, 5.0, 7.0, 9.0, 12.0, 100.0]. The combination that maximized the F1-score was selected.

**Thresholds**:
- `T_NLI` = 0.1
- `T_CLIP_DIFF` = 9.0
- Rule: Predict OOC if `(NLI_Contra > 0.1 OR |CLIP_Sim1 - CLIP_Sim2| > 9.0)`.

**Engineering Decisions & Implementation Details**:
- **Tokenizer Truncation**: During initial extraction, CLIP crashed on two samples (`54.jpg`, `1248.png`) due to captions exceeding the maximum 77 token length. `truncation=True` was explicitly added to the `CLIPProcessor` to safely process long captions without dropping data points.
- **Feature Caching**: Because inference on 1000 samples is computationally expensive, raw NLI and CLIP features were cached to `results/full_features_A.csv` to allow instantaneous re-evaluation of threshold rules.

=========================
## 6. EXPERIMENT RESULTS
=========================
All results below reflect performance strictly on the **900 Held-Out Samples**.

**Rule 1: NLI-Only (`NLI_Contra > 0.1`)**
- Accuracy: 75.22%
- Precision: 82.66%
- Recall: 65.73%
- F1-Score: 73.23%

**Rule 2: Combined NLI + CLIP (`NLI_Contra > 0.1 OR |CLIP_Diff| > 9.0`)**
- Accuracy: 75.67%
- Precision: 81.17%
- Recall: 68.75%
- F1-Score: 74.45%

**Runtime**: Feature extraction for 1000 samples on a CPU took approximately 10 minutes. Threshold evaluation takes < 1 second.

=========================
## 7. IMPLEMENTATION STATUS
=========================
**Directories:**
- `data/`: Stores the test images and benchmark CSVs.
- `eval/`: Contains strict evaluation logic ensuring proper dataset splitting.
- `models/`: Initialized for future custom model wrappers.
- `notebooks/`: Initialized for exploratory data analysis.
- `results/`: Stores raw feature outputs and generated prediction files.
- `result_library/`: High-level summaries tailored for dissertation writing.
- `scripts/`: General-purpose data processing and pipeline runners.

**Files & Scripts:**
- `data/cosmos_test_fixed.csv`: The official 1000-sample benchmark dataset.
- `scripts/setup_dataset.py`: Python script responsible for downloading raw TUM data, verifying images, subsampling, and saving the CSV.
- `scripts/baseline_A_subset.py`: Initial script used to run NLI/CLIP on 100 samples and perform a grid search for threshold tuning.
- `scripts/baseline_A.py`: Full pipeline script for downloading models, extracting features across the entire dataset, and caching them.
- `eval/evaluate_splits.py`: Dedicated script that cleanly partitions cached features into 100-tuning and 900-held-out splits, applies logical rules, outputs final metrics, and writes predictions.
- `results/full_features_A.csv`: Cached outputs (NLI probabilities, CLIP similarities) for all 1000 samples.
- `results/baseline_A_predictions.csv`: Final prediction file containing `image_id`, `true_label`, `predicted_label`, and `confidence_score` for the 900 held-out samples.
- `result_library/baseline_A_summary.md`: Human-readable markdown summary of the baseline approach and results.

=========================
## 8. CURRENT PROJECT STATE
=========================
- **Finished**: Dataset acquisition, standard benchmark creation, Baseline A (NLI+CLIP) zero-shot implementation, feature extraction, threshold tuning, data leakage corrections, and initial baseline evaluation.
- **Partially Finished**: The repository structure is fully fleshed out, but `models/` and `notebooks/` are currently empty placeholders waiting for further phases.
- **Not Started**: Baseline B implementation, Phase 2 (Gemini API integrations for caption perturbations: paraphrasing, entity swapping, etc.), and the final robustness evaluation (re-running baselines on perturbed data).

=========================
## 9. REMAINING WORK
=========================
1. **Additional Baselines (Phase A)**
   - Implement Baseline B (and optionally C/D) depending on the scope of the remaining 2-4 target methods.
   - *Estimated Difficulty*: Low to Medium (depending on model availability).
   - *Estimated Time*: 1-2 hours per baseline.
2. **Caption Perturbation Generation (Phase B)**
   - Connect to the Gemini API to systematically generate adversarial variations of the captions (paraphrase, entity-swap, negation).
   - *Estimated Difficulty*: Medium (Requires careful prompting and API management).
   - *Estimated Time*: 2-3 hours.
3. **Robustness Re-Evaluation**
   - Execute the existing baseline models over the newly generated perturbed datasets.
   - Calculate the "robustness drop" (Performance on original vs. Performance on perturbed).
   - *Estimated Difficulty*: Low (Reusing existing evaluation scripts).
   - *Estimated Time*: 1-2 hours.

=========================
## 10. KNOWN RISKS
=========================
- **API Constraints**: Phase 2 relies heavily on the Gemini API. We must monitor rate limits, context windows, and potential financial costs if generating thousands of perturbations. Prompt injection or refusals by the LLM (if it flags captions as sensitive) could cause data gaps.
- **Missing Baseline Details**: For additional baselines (e.g., from specific papers), the authors may not have published their exact model weights or preprocessing steps, threatening strict reproducibility.
- **Hardware Limitations**: Inference on `roberta-large-mnli` and `CLIP` was performed on CPU. If heavier models (e.g., LLaVA) are chosen for Baseline B, execution times may become a bottleneck without GPU acceleration.
- **Methodological Concerns**: The threshold tuning approach (grid search on 100 samples) might still be slightly noisy or brittle compared to learning a linear classifier (e.g., Logistic Regression) over the features, though a logical rule is highly explainable.

=========================
## 11. NEXT RECOMMENDED STEP
=========================
**Implement Baseline B**: Select the next lightweight method from the out-of-context literature, extract its features for the 1000-sample test set, tune it on the 100-sample split, and evaluate it on the 900-sample held-out set to build out the fair comparison table.

=========================
## 12. APPENDIX
=========================
**Environment and Configuration**
- **Language**: Python 3
- **Hardware**: CPU (CUDA/GPU was checked for but fell back to CPU).
- **Random Seed**: `42` (used for `random.sample()` dataset selection).
- **Key Packages**:
  - `torch`, `torchvision`
  - `transformers`
  - `scikit-learn`
  - `pandas`
  - `Pillow`

**Models**
- Text NLI: `roberta-large-mnli`
- Vision-Language: `openai/clip-vit-base-patch32`

**Directory Tree**
```
RobustOOC/
├── data/
│   ├── cosmos_test_fixed.csv
│   ├── images_test/ (1699 image files)
│   └── temp/
├── eval/
│   ├── __init__.py
│   └── evaluate_splits.py
├── models/
│   └── __init__.py
├── notebooks/
│   └── README.md
├── results/
│   ├── baseline_A_predictions.csv
│   └── full_features_A.csv
├── result_library/
│   ├── README.md
│   ├── baseline_A_summary.md
│   └── PROJECT_STATUS_REPORT.md
└── scripts/
    ├── baseline_A.py
    ├── baseline_A_subset.py
    └── setup_dataset.py
```
