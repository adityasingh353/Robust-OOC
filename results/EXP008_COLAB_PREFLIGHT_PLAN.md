# EXP008 Colab Preflight Plan

This document outlines the preflight check intended to verify if the required legacy environment for EXP008 ("A Textual-Visual-Entailment-based Unsupervised Algorithm for Cheapfake Detection") can be successfully initialized on Google Colab GPU instances.

## Objective
To determine if we can compile and import the complex legacy dependencies (PyTorch 1.9.0, CUDA 11.1, Detectron2, OFA) without encountering breaking errors, before committing to running any evaluation pipelines.

## Generated Artifacts
- **Notebook File**: `colab/EXP008_COLAB_PREFLIGHT.ipynb`

## Notebook Workflow
1. **GPU & Driver Check**: Executes `nvidia-smi` and `nvcc --version` to capture the base Colab hardware and CUDA driver version.
2. **Environment Initialization**: Downloads and installs Miniconda to establish a clean `Python 3.7` environment within the Colab runtime.
3. **Legacy Dependencies**: Installs the precise versions required by the target paper (`torch==1.9.0+cu111 torchvision==0.10.0+cu111`).
4. **Repository & Custom Modules**: Clones the original GitHub repository, installs the bundled `Detectron2` package (which requires native C++/CUDA operator compilation), and sets up `OFA`.
5. **Model Acquisition**: Downloads the required `OFA` checkpoint and `spaCy` NLP models.
6. **Import Verification**: Runs a python script (`test_imports.py`) to verify that PyTorch recognizes the GPU, and that both `Detectron2` and `OFA` can be imported successfully.

## Expected Outcomes

**PASS**:
- Miniconda successfully installs Python 3.7.
- PyTorch 1.9.0 successfully imports and `torch.cuda.is_available()` returns `True`.
- `Detectron2` compiles its custom C++ operators and imports without `ImportError`.
- `OFA` modules import without missing dependencies.

**FAIL**:
- If Colab's native Nvidia driver is incompatible with CUDA 11.1 / PyTorch 1.9.
- If `Detectron2` fails to compile due to C++ standard mismatch or missing headers.
- If the required models/checkpoints are no longer available for download.

## Instructions
1. Upload the generated `EXP008_COLAB_PREFLIGHT.ipynb` to Google Colab.
2. Go to **Runtime -> Change runtime type** and select **GPU** (T4 or V100 is recommended).
3. Run all cells sequentially.
4. Record the final status (PASS or FAIL) and the specific error logs if it fails.
