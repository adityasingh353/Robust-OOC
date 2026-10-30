# EXP012: Sentiment-aware Classifier EVIDENCE LOG

## 1. Directory State
The `detectron2/` directory was committed into the repository along with an absolute path build folder `detectron2/build/temp.linux-x86_64-3.6/hdd3/malkaddour/datasets/cheapfakes/2021-grandchallenge-cheapfakes-cosmosonsteroids`. This triggers a "Filename too long" git error on Windows unless `core.longpaths=true` is used, highlighting significant issues with the original repository structure.

## 2. Checkpoint Existence
The MLP weights:
- `PT_1000.h5`
- `PT_600.h5`
- `Train_full.h5`
are present in `newresults/modelweights/`.

The COSMOS text-image model:
- `img_use_rcnn_margin_10boxes_jitter_rotate_aug_ner.pt`
is present in `models_final/`.

## 3. The `run_cheapfake.py` Script
Inspection of `run_cheapfake.py` lines 78-79 and 190 reveals:
```python
img_path = os.path.join(DATA_DIR, v_data["img_local_path"])
bbox_list = v_data['maskrcnn_bboxes']
...
bboxes = test_data['maskrcnn_bboxes']
score_c1, score_c2 = get_scores(test_data)
textual_sim = float(test_data['bert_base_score'])
```
The script crashes instantly if the input JSON does not already contain `maskrcnn_bboxes` and `bert_base_score`. There is no code in the repository that runs Detectron2 or SBERT to populate these fields from raw images.

## 4. Dockerfile Legacy Environment
The `Dockerfile` requests:
- `nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04`
- `python3.8`
- `tensorflow==2.3.0`
- `torch==1.8.1`
This configuration requires hardware compatible with CUDA 10.2 (Turing or older). It will not run on modern Ampere/Hopper GPUs out of the box without complex manual upgrades to the source code.
