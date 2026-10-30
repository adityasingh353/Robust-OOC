# FINAL QUICK CHECK: EXP013 (COSMOS on Steroids - ACM MMSys 2021)

## 1. Inspect `models_final/`
The `models_final/` directory is present in the repository.

## 2. Contents of `models_final/`
- **Filename**: `img_use_rcnn_margin_10boxes_jitter_rotate_aug_ner.pt`
- **Extension**: `.pt`
- **Size**: 10,240,775 bytes (approx. 10.2 MB)

## 3. Trained Checkpoints
The single `.pt` file is the trained text-image matching head (specifically using Universal Sentence Encoder embeddings).

## 4. What `evaluate_ooc.py` Expects
The script expects either:
- `img_use_rcnn_margin_10boxes_jitter_rotate_aug_ner.pt` (default, if `embed_type == 'use'`)
- `img_lstm_glove_rcnn_margin_10boxes_jitter_rotate_aug_ner.pt` (if `embed_type != 'use'`)

## 5. Do they exist?
Yes, the default required `.pt` file explicitly exists in `models_final/`.

## 6. Can it perform inference directly without training?
Yes, `evaluate_ooc.py` explicitly loads the trained weights directly from `models_final/` using `torch.load()`. No training via `trainer_scipt.py -m train` is required to run the evaluation.

## 7. Can raw COSMOS images be processed directly?
**NO.** 
`evaluate_ooc.py` reads a pre-populated JSON file (`test_data.json`) and requires bounding boxes to already be extracted:
`bbox_list = v_data['maskrcnn_bboxes']`
There is no code in `evaluate_ooc.py` that processes a raw image through a CNN to generate bounding boxes dynamically.

## 8. Is Detectron2 feature extraction contained/configured?
No. The repository provides a modified version of the Detectron2 core library (`detectron2_changes/`), but **it completely lacks the actual preprocessing script** required to feed raw images into Detectron2 and generate the `maskrcnn_bboxes` JSON structure. It assumes you already ran some other missing script (presumably from the original COSMOS authors) to generate the JSON.

## 9. Missing External Artifacts
- **Missing**: The bounding-box extraction script.
- **Missing**: The script that computes `bert_base_score` (which is also read directly from the JSON).
- Without these scripts, we cannot convert our 900 raw images into the specific JSON format this evaluation script requires.

## 10. Dockerfile Environment
The Dockerfile is present but uses extremely old dependencies (`nvidia/cuda:10.1-cudnn7-devel-ubuntu18.04`, Python 3.6/3.8), which would present severe engineering challenges on modern hardware.

## 11. Colab Feasibility for 10-Sample Pilot
**Impossible.** We cannot execute the 10-sample pilot because we do not have a script to extract the required bounding boxes or bert base scores from the raw images.

## 12. FINAL DECISION

**DROP**

**Reason:** Missing critical inference artifacts. While the text-image matching head (`.pt`) is present, the script required to extract bounding boxes from raw images is completely absent. The repository is merely an evaluation script for a pre-computed JSON file. Because we cannot generate this pre-computed JSON for our 900 test images using only the code provided in this repository, it is impossible to evaluate this method end-to-end.
