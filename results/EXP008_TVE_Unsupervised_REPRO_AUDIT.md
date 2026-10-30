# REPRODUCIBILITY AUDIT: Target Paper 3

**Paper**: A Textual-Visual-Entailment-based Unsupervised Algorithm for Cheapfake Detection (ACM Multimedia 2022)
**Repository**: https://github.com/pwnyniche/acmmmcheapfake2022

## 1. Exact Repository
https://github.com/pwnyniche/acmmmcheapfake2022

## 2. Relevant Files
- `acmmm.py` (main script)
- `predict.py` (heuristic rules)
- `online_search.py`, `sbert.py`
- `COSMOS/evaluate_ooc.py` (Visual feature extraction)
- `OFA/main.py`

## 3. Inference Script
`acmmm.py`

## 4. Preprocessing Pipeline
The pipeline relies heavily on the original `COSMOS` architecture (which in turn uses `detectron2` and Mask R-CNN to extract bounding boxes and compute Intersection over Union (IoU)) and `OFA` (One-For-All) to compute visual entailment scores.

## 5. Required Checkpoints/Models
- `microsoft/deberta-xlarge-mnli` (HuggingFace)
- Detectron2 object detection models (for COSMOS)
- OFA models

## 6. Checkpoint Accessibility TODAY
Deberta is readily available on HuggingFace. OFA and Detectron2 models require downloading from their respective original repositories, which may have link rot, but they are generally still available. 

## 7. Required External Datasets
No external datasets required for Task 1 (OOC detection) other than the raw images and the JSON annotations.

## 8. External APIs/Services
`online_search.py` uses an online search tool/API, but it appears primarily designed for Task 2 (finding original images online). For Task 1 (OOC detection on our 900 samples), it might not be required, though `acmmm.py` does seem to import and use it in `predict_final`. 

## 9. Input Format
A `test_data.json` file and an image directory.

## 10. Can Raw COSMOS Images Be Processed?
Yes. The script calls the `COSMOS` module (`evaluate_ooc.main()`) which theoretically processes raw images to generate bounding boxes on the fly. 

## 11. Can Our Exact Frozen 900-Sample IDs Be Evaluated?
Yes, by formatting our `cosmos_test_900.csv` into the expected `test_data.json` schema and placing the 900 images in the `public_test_mmsys` folder.

## 12. Is Training Required?
No. The method is entirely unsupervised (heuristic rules over DeBERTa NLI, SBERT semantic similarity, and OFA/COSMOS visual features).

## 13. GPU/RAM Requirement
Requires a GPU with minimum 10GB memory.

## 14. Colab Feasibility
Feasible, but installing Detectron2, OFA, and all dependencies in a modern Colab environment (CUDA 12+) may cause severe dependency conflicts given the `pytorch 1.9.0` and `cuda 11.1` requirement from 2022.

## 15. Exact Deviations Needed
We would need to modify `acmmm.py` to only output the labels for our 900 samples, bypass the Task 2 (online search) components if they rate-limit or fail, and potentially patch the COSMOS module to work with modern PyTorch if we don't use their exact Docker container.

## 16. Exact vs Approximate Reproduction
Exact Reproduction is possible if using their provided Dockerfile (`docker build -t acmmmcheapfakes:submission .`).

## 17. Major Reproducibility Risks
- The original COSMOS codebase is notorious for brittle Detectron2 dependencies.
- `online_search.py` may break if it relies on web scraping or a deprecated API.

## 18. Expected Engineering Effort
Medium. The Dockerfile simplifies the environment setup, but making sure the 900-sample dataset flows through smoothly without crashing on missing bounding boxes will take some effort.
