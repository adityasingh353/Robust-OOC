# Reproducibility Audits Summary

This document summarizes the attempts to reproduce external state-of-the-art (SOTA) methods for Out-of-Context (OOC) detection on the COSMOS dataset. These findings are crucial for the dissertation's literature review and methodology sections to justify why certain baselines were not included in the final robustness benchmarking.

## General Finding
A recurring issue in the cheapfakes detection literature is the reliance on complex, heavily pre-processed visual and textual features (such as Scene Graphs or specialized embeddings) that are provided as proprietary `.joblib` or `.pkl` files by the authors for specific challenge splits. The code to actually generate these features from raw images is frequently omitted, rendering the methods non-reproducible on custom dataset splits or real-world data.

---

## 1. EXP005: Unified Network 
**Paper**: *Detecting out-of-context images with unified network*
**Classification**: **D — Not reproducible with publicly available artifacts**

### Reason for Failure
While the official repository and checkpoints were available, the entire inference pipeline strictly required data formatted into a highly specific multimodal structure (visual embeddings, text graphs) that was assumed to already exist in pre-processed serialized files. The authors did not provide the preprocessing scripts required to convert raw images and captions into this format. Consequently, it was impossible to run their model on the `COSMOS-FIXED-v1` evaluation set.

---

## 2. EXP006: CSGM
**Paper**: *Multimodal scene-graph matching for cheapfakes detection* (ICMR2024)
**Classification**: **D — Not reproducible with publicly available artifacts**

### Reason for Failure
Similar to EXP005, the CSGM architecture relies heavily on visual Scene Graphs (object bounding boxes and relational predicates). The training and inference scripts load these graphs from a pre-extracted `.joblib` file (`cheapfake_test_lowered_images_data.joblib`). 

The repository completely omits the Scene Graph Generation (SGG) pipeline (e.g., Pe-NET or Neural-Motifs) required to generate these graphs from raw images. The authors only provided a Dropbox link containing pre-extracted features for their specific data split. Without the ability to extract scene graphs from new, raw images, the model cannot be evaluated on our standardized 1000-sample benchmark.
