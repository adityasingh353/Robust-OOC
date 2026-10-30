# Reproducibility Audit: Multimodal Scene-Graph Matching for Cheapfakes Detection (CSGM)

## 1. Paper Details
1. **Full title**: Multimodal scene-graph matching for cheapfakes detection
2. **Authors**: Tam N.M., Hoa-Vien Vo-Hoang (inferring from repository handle `Tam1032` and previous context)
3. **Venue/year**: ICMR2024 (Under Review as per README)
4. **Dataset used**: ICME2023 Grand Challenge on Cheapfakes detection (derived from COSMOS)
5. **Method/architecture**: Graph Convolutional Network (GCN) that matches visual scene graphs (extracted via Pe-NET/Neural-Motifs and embedded via EfficientNet-b5) with textual graphs.
6. **Official repository**: `https://github.com/Tam1032/LGSGM---CheapFake`

## 2. Artifact Availability
7. **Official code**: Yes, available in the repository.
8. **Official checkpoints**: Yes, hosted on a public Google Drive link.
9. **Pretrained models**: Yes (same as above).
10. **Training scripts**: Yes (`main_train.py`).
11. **Inference scripts**: Yes (`main_train.py` -> `run_evaluate()`).
12. **Dataset preprocessing**: Partially available. The script `extract_visual_features.py` exists to extract EfficientNet features, but it **strictly requires pre-existing bounding boxes and scene graphs**.
13. **Exact prompts/configuration**: Configuration is hardcoded in an `info_dict` in `main_train.py`.

## 3. Evaluation Feasibility
14. **Can trained model be obtained TODAY?**: Yes, the Google Drive link is active (HTTP 200).
15. **Can inference be performed without retraining?**: Yes, using the `run_evaluate()` pipeline.
16. **Can the method be evaluated on COSMOS-FIXED-v1?**: **NO**.
17. **Hardware/software requirements**: Python 3.7.9, PyTorch, EfficientNet-PyTorch.
18. **Missing components**: The Scene Graph Generation (SGG) pipeline. 

## 4. Classification & Justification
**Classification**: **D — Not reproducible with publicly available artifacts**

**Explanation**: 
While the authors provide their training/inference scripts and pre-trained checkpoints, the pipeline relies entirely on pre-extracted visual scene graphs (bounding boxes and predicates) loaded from a proprietary serialized format (`cheapfake_{subset}_lowered_images_data.joblib`). 

The repository **does not** contain the code necessary to generate these scene graphs from raw images (e.g., using Pe-NET or Neural-Motifs). The authors only provide a Dropbox link to download the *pre-extracted* features for their specific dataset split. 

Because we cannot generate the required scene graph `.joblib` structures for arbitrary raw images or our specific `COSMOS-FIXED-v1` split, it is impossible to evaluate their method on our benchmark. Re-implementing and configuring Pe-NET/Neural-Motifs from scratch to perfectly match their undocumented extraction process is out of scope and highly prone to methodological mismatch.

## 5. Artifact Inventory

| Artifact | Found | Accessible | Location | Notes |
| :--- | :---: | :---: | :--- | :--- |
| Official Repository | Yes | Yes | GitHub (`Tam1032/LGSGM---CheapFake`) | Contains training/inference code. |
| Pretrained Models | Yes | Yes | Google Drive | GCN checkpoints. |
| Feature Extraction Code | Partial | Yes | `extract_visual_features.py` | Requires pre-existing bounding boxes. |
| Scene Graph Generator Code | **No** | **No** | N/A | **CRITICAL MISSING COMPONENT**. Needed to process raw images. |
| Pre-extracted Features | Yes | Yes | Dropbox | Only valid for their specific dataset splits. |
