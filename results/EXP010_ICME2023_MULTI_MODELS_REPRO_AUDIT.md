# REPRODUCIBILITY AUDIT: EXP010 (ICME 2023)

## 1. Paper Metadata
- **Title**: Multi-Models from Computer Vision to Natural Language Processing for Cheapfakes Detection
- **Venue/Year**: IEEE ICMEW 2023
- **DOI**: 10.1109/ICMEW59549.2023.00023
- **Authors**: Thanh-Son Nguyen, et al.

## 2. Legitimacy
Yes, this is genuinely a published OOC/cheapfake detection method reporting performance on the COSMOS dataset, utilizing multi-modal NLP/CV pipelines.

## 3. Proposed Method
The method uses a combination of Detectron2 (for bounding box extraction), GRIT (Grid-to-Region Image Text) for generating synthetic image captions, DeBERTa-xlarge for NLI entailment between the generated captions and the provided captions, and a custom final classification head to output the OOC/NOOC prediction.

## 4. Inference Scripts
- `evaluate_ooc_method_1.py`
- `evaluate_ooc_method_2.py`
- `evaluate_ooc_original_cosmos.py`
These are orchestrated by the `icme2023_cheapfakes_challenge.ipynb` notebook.

## 5. Complete Inference Pipeline
Raw Image + Caption1 + Caption2 -> Detectron2 (Bboxes) -> GRIT (Synthetic Caption Generation) -> SBERT/DeBERTa (Similarity & NLI Entailment) -> Custom Checkpoint (e.g., `img_use_rcnn_margin_10boxes_jitter_rotate_aug_ner.pt`) -> OOC/NOOC label.

## 6. Required Models / Checkpoints
1. `microsoft/deberta-xlarge-mnli` (HuggingFace)
2. `sentence-transformers/stsb-bert-base` (HuggingFace)
3. `grit/grit_checkpoint_4ds.pth` (GRIT weights)
4. `models_final/img_use_rcnn_margin_10boxes_jitter_rotate_aug_ner.pt` (Custom trained final layer)

## 7. Checkpoint Analysis
- **Present in repository?**: NO. Only the HuggingFace models are automatically resolved. The custom weights and GRIT weights are missing from the Git tree.
- **Downloadable / Link alive?**: The notebook provides `gdown` IDs (e.g., `1WLsMrtVFTftSJiGHg7iALNFImtefHtOT` and `1BFXgyNAzfvCeweIpqFCBd4g7IKrhP3xe`). These are personal Google Drive links. While they may work today, they are highly ephemeral, subject to quota exhaustion, and not scientifically archived.
- **Trained/Custom**: Custom trained on COSMOS data.

## 8. Missing / Hidden Weights
- The `models_final/` directory is completely omitted from the repository and is created dynamically via `!mkdir /content/icme2023/models_final` in the Colab notebook.

## 9. Git Tree Inspection
Verified: The `.gitignore` ignores `models_final`, `*.pt`, and `*.pth`. No GitHub Releases or Git-LFS objects exist containing the weights.

## 10. Raw COSMOS Images
Yes, raw images are processed directly. The code uses `Detectron2` to extract bounding boxes on the fly.

## 11. Input JSON/Data Format
Requires the original COSMOS formatting (`test.json` containing `img_local_path`, `caption1`, `caption2`).

## 12. Compatibility with 900 Samples
Yes. Our `cosmos_test_900.csv` can be trivially mapped to `test.json` without modifying IDs or splits.

## 13. Training Required?
No, assuming the Google Drive links remain alive. If the Drive links die, the custom classification head is permanently lost and would require re-training on COSMOS (which is forbidden in this phase).

## 14. GPU/VRAM Requirements
High VRAM requirement. Needs to load Detectron2, GRIT, DeBERTa-xlarge, and SBERT simultaneously into memory.

## 15. Colab Feasibility
The authors specifically provide a Colab notebook. However, compiling the `grit/models/ops` C++ extensions in modern Colab environments (CUDA 12+) frequently fails due to GCC mismatches.

## 16. Legacy Dependencies & Likely Failures
- **Detectron2**: Brittle dependency heavily tied to specific PyTorch/CUDA versions.
- **GRIT C++ Ops**: Requires `python setup.py build develop` for custom CUDA extensions.

## 17. Notebook Inspection
The notebook performs undocumented setup steps (downloading weights from personal Google Drives, copying `detectron2_changes/` directly into the cloned `detectron2` repository).

## 18. Checkpoint Recovery
There are no official Zenodo/HuggingFace mirrors. If the Gdown links break, the model is dead.

## 19. Reproducibility Classification
**NOT REPRODUCIBLE** (Practically speaking, for a stable dissertation benchmark. The absolute reliance on personal Google Drive links and custom C++ CUDA compilation makes it incredibly brittle and unstable.)

## 20. Exact Deviations Required
If we were to force it to run, we would have to download the weights from Drive, manually patch the CUDA C++ compilation for modern GPUs, and rewrite the inference script to bypass any Task 2 scraping dependencies if they exist.

## 21. Fair Evaluation on 900 Samples
Yes, if the dependencies successfully compiled, the model could fairly evaluate the 900 samples. 

## 22. FINAL DECISION

**DROP — NOT REPRODUCIBLE**

**Reasons for DROP**:
1. **Critical Weights on Google Drive**: The custom trained models (`models_final/*.pt`) are stored on personal Google Drive accounts via `gdown`, which frequently fail due to rate limits or deletion. This violates the standard for a stable, scientifically reproducible benchmark.
2. **C++ CUDA Compilation**: The `grit` captioning module requires compiling custom C++/CUDA operations (`python setup.py build develop`). This is notoriously unstable across different GPU architectures and CUDA versions (especially CUDA 12+), presenting a massive, unnecessary engineering risk.
3. **Hidden Modifications**: The notebook relies on blindly copying modified files (`detectron2_changes/`) over a freshly cloned Facebook `detectron2` repository, which is an extremely fragile setup process.
