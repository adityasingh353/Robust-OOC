# REPRODUCIBILITY AUDIT: Target Paper 4

**Paper**: A Combination of Visual-Semantic Reasoning and Text Entailment-based Boosting Algorithm for Cheapfake Detection (ACM Multimedia 2022)
**Repository**: https://github.com/latuanvinh1998/Cheapfakes_detection_acmmm (Folder: `A Combination of Visual-Semantic Reasoning and Text Entailment-based Boosting Algorithm for Cheapfake Detection`)

## 1. Exact Repository
https://github.com/latuanvinh1998/Cheapfakes_detection_acmmm

## 2. Relevant Files
- `ACMMM/acmmm_evaluate_task_1.py` (inference script)
- `VSRN/train.py` (VSRN training module)

## 3. Inference Script
`ACMMM/acmmm_evaluate_task_1.py`

## 4. Preprocessing Pipeline
The pipeline requires extracting image features using `bottom-up-attention` (which relies on Faster R-CNN in a very old Caffe framework). These features are then saved as `.npy` arrays.

## 5. Required Checkpoints/Models
- `VSRN` model trained on coco (`model_best.pth.tar`)
- `binwang/bert-base-nli-stsb`
- `microsoft/deberta-xlarge-mnli`
- A custom trained neural network: `Model/model_acmmm_best_84,8%.pth`

## 6. Checkpoint Accessibility TODAY
The custom Neural Network model (`model_acmmm_best_84,8%.pth`) and the VSRN checkpoints are NOT included in the GitHub repository (the `Model` and `runs` directories are missing or require downloading from a non-existent link). The author provided a Google Drive link in the README for the `bottom-up-attention` features, which may or may not still be active, but does not provide the final trained Boosting weights. 

## 7. Required External Datasets
The script expects a pre-extracted numpy array of features (`/acmmmcheapfakes/task_1.npy`).

## 8. External APIs/Services
None directly apparent for Task 1, though it relies on standard HuggingFace models.

## 9. Input Format
Pre-extracted `.npy` arrays for images, and `test_data.json` for text.

## 10. Can Raw COSMOS Images Be Processed?
No. The inference script `acmmm_evaluate_task_1.py` loads `images = np.load('/acmmmcheapfakes/task_1.npy')`. It does NOT process raw images. To process raw images, one must successfully run Pete Anderson's `bottom-up-attention` (Caffe).

## 11. Can Our Exact Frozen 900-Sample IDs Be Evaluated?
Only if we can successfully extract the features for those exact 900 images using the ancient `bottom-up-attention` Caffe repository, which is highly prone to failure.

## 12. Is Training Required?
Yes. The method uses a custom trained neural network (the "Boosting Algorithm") to ensemble the features. The inference script loads `Model/model_acmmm_best_84,8%.pth`. If we cannot download this checkpoint, we must train it from scratch using their `VSRN/train.py`, which requires the original COSMOS training dataset (which we do not have/want to use for training).

## 13. GPU/RAM Requirement
Requires GPU for VSRN and bottom-up-attention. 

## 14. Colab Feasibility
Extremely low. Compiling Caffe for `bottom-up-attention` on modern Colab is nearly impossible without a highly customized Docker container running Ubuntu 16.04 and CUDA 8.

## 15. Exact Deviations Needed
We would need to fully replicate the `bottom-up-attention` extraction pipeline, or replace it with a modern PyTorch equivalent (which would alter the paper's exact methodology). We would also need to train the Boosting model ourselves if the checkpoint is missing.

## 16. Exact vs Approximate Reproduction
An exact reproduction is technically possible but practically impossible due to missing checkpoints and legacy Caffe dependencies. An approximate reproduction using a modern Faster R-CNN feature extractor would deviate significantly from the published results.

## 17. Major Reproducibility Risks
- **Caffe Dependency**: `bottom-up-attention` is historically the hardest computer vision repository to compile today.
- **Missing Checkpoints**: The custom trained boosting weights are not in the repository.
- **Data Gap**: We cannot evaluate raw images directly.

## 18. Expected Engineering Effort
Very High / Blocked. The missing trained checkpoints and the Caffe dependency make this a massive engineering project just to get inference running.
