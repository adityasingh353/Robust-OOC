# REPRODUCIBILITY AUDIT: EXP012 (Sentiment-aware Classifier - ACM Multimedia 2022)

## 1. Paper Metadata
- **Title**: Sentiment-aware Classifier for Out-of-Context Caption Detection
- **Venue/Year**: ACM Multimedia 2022
- **DOI**: 10.1145/3503161.3551603
- **Authors**: Malkaddour et al.

## 2. Legitimacy
Yes, it is a genuine published method explicitly addressing Task 1 of the ACMM 2022 Grand Challenge on Cheapfakes Detection.

## 3. Inspected Files
Inspected `README.md`, `run_cheapfake.py`, `utils/eval_utils.py`, `requirements.txt`, `Dockerfile`, `newresults/modelweights/`, and `models_final/`.

## 4. Exact Inference Pipeline
1. **Pre-processing (External to this repo)**: Raw Image + Text are processed by the original COSMOS codebase to generate a `test.json` containing `maskrcnn_bboxes`, `caption1_modified`, and `bert_base_score`.
2. **Sentiment Extraction**: `run_cheapfake.py` runs NLTK VADER and TextBlob to compute polarity and subjectivity differences between the two captions.
3. **Image-Text Features**: The script runs the precomputed boxes and sentence embeddings through the provided COSMOS head (`models_final/img_use...pt`) to get match/mismatch scores, calculates bbox IoU, and checks for "fake" or "opposite" keywords.
4. **MLP Classification**: A 6-dimensional feature vector is fed into a trained TensorFlow/Keras MLP to predict the final OOC/NOOC label.

## 5. Required Checkpoints
- `newresults/modelweights/PT_1000.h5`, `PT_600.h5`, `Train_full.h5` (MLP Weights). **Present and usable.**
- `models_final/img_use_rcnn_margin_10boxes_jitter_rotate_aug_ner.pt` (COSMOS Image-Text Head). **Present and usable.**

## 6. Verification of MLP Weights
The `.h5` files explicitly exist in the repository under `/newresults/modelweights/` and are actively loaded by `run_cheapfake.py` via TensorFlow/Keras.

## 7. COSMOS Feature Models
The text-image feature model (`img_use_rcnn_margin_10boxes_jitter_rotate_aug_ner.pt`) is included and usable.

## 8. Can Raw Images be Processed Directly?
**NO.** The repository completely lacks the computer vision preprocessing scripts required to extract bounding boxes. It explicitly expects `maskrcnn_bboxes` to already exist inside the input JSON. 

## 9. Exact Input Format & 900-Sample Compatibility
The script expects `test.json` to be pre-populated with COSMOS pipeline outputs (`maskrcnn_bboxes`, `caption1_modified`, `bert_base_score`). We **CANNOT** convert our frozen 900 samples to this format using only this repository, because we do not have the bounding boxes.

## 10. Training Required?
No, the inference weights are provided.

## 11. MLP Weights and Eval Config
Yes, the provided weights map directly to the reported configurations (e.g., PT_1000, Train_full).

## 12. Dockerfile Reproducibility
The Dockerfile relies on ancient base images (`nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04`) and hardcoded GPG keys that have likely expired. Building it today will almost certainly throw apt-get key errors.

## 13. PyTorch/CUDA Versions
Requires PyTorch 1.8.1, TensorFlow 2.3.0, and CUDA 10.2. These are highly likely to crash on any modern GPU architecture (Ampere/Hopper).

## 14. Colab Feasibility
Extremely low. Colab uses CUDA 12+ and Python 3.10+. Forcing CUDA 10.2 and Python 3.6/3.8 is practically impossible in modern Colab environments without complex chroot or Docker-in-Docker hacks.

## 15. GPU/VRAM Requirements
Low (if bounding boxes were provided). The MLP and SBERT take <4GB VRAM.

## 16. External APIs
None.

## 17. 10-Sample Pilot Feasibility
**Impossible**, because we cannot generate the required `maskrcnn_bboxes` using this codebase.

## 18. Necessary Modifications
We would have to install the *entire original COSMOS codebase* (which has broken Detectron2 dependencies) just to generate the `test.json` input required by this method.

## 19. Reproducibility Classification
**NOT REPRODUCIBLE (End-to-End)**
Genuinely missing critical preprocessing scripts (the bounding box extraction pipeline). It only provides the final classifier stage.

## 20. Engineering Difficulty vs Missing Artifacts
The MLP and its weights are present, but the script required to turn a raw image into `maskrcnn_bboxes` is missing. The repository literally tells you to run someone else's code to get the inputs.

## 21. FINAL DECISION

**DROP — NOT SUITABLE**

This method is not an end-to-end OOC detector; it is merely an MLP classifier attached to the end of the original COSMOS preprocessing pipeline. Because it requires precomputed `maskrcnn_bboxes` which we do not have for our 900 samples, and because we already know from prior experience that configuring the legacy COSMOS Detectron2 pipeline is a nightmare, this is a terrible candidate for a clean, stable dissertation benchmark.
