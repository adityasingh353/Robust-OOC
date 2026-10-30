# EXP010: ICME 2023 MULTI-MODELS EVIDENCE LOG

## 1. Notebook Inspection (`icme2023_cheapfakes_challenge.ipynb`)
- The notebook contains explicit `gdown` commands downloading checkpoints from Google Drive.
  - `!gdown 1WLsMrtVFTftSJiGHg7iALNFImtefHtOT` (Downloads to `/content/icme2023/grit/grit_checkpoint_4ds.pth`)
  - `https://drive.google.com/uc?id=1BFXgyNAzfvCeweIpqFCBd4g7IKrhP3xe` (Downloads to `/content/icme2023/models_final/img_use_rcnn_margin_10boxes_jitter_rotate_aug_ner.pt`)
- There are multiple methods evaluated: `evaluate_ooc_method_1.py`, `evaluate_ooc_method_2.py`, etc.
- The notebook installs `detectron2` from source, copies custom modifications (`detectron2_changes/`), and compiles `grit/models/ops/` using C++.

## 2. Directory Structure (`ls -la`)
- `detectron2_changes/` is present.
- `models_final/` is **MISSING** from the Git tree and must be created dynamically during setup, with weights downloaded externally.
- `grit/grit_checkpoint_4ds.pth` is **MISSING** from the Git tree and downloaded externally.

## 3. Dependency Hell
- `detectron2` requires specific PyTorch/CUDA versions.
- `grit/models/ops` requires C++ compilation (`python setup.py build develop`). This is notorious for failing on modern Colab/local machines due to GCC/CUDA version mismatches.

## 4. Inference Scripts (`evaluate_ooc_*.py`)
- The inference pipeline involves running `search_engine.py` (which uses Selenium and WebDriver to scrape Google Images!), `grit` (for captioning the images), and then aggregating features using the downloaded PyTorch models (`img_use_rcnn_...pt`).

## 5. Input Data format
The notebook specifies: `INPUT_FOLDER should has structure as same as requirement of organizer, contain "test.json"`. It relies on the original COSMOS formatting.
