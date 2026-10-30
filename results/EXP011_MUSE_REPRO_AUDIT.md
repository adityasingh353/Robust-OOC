# REPRODUCIBILITY AUDIT: EXP011 (MUSE - WACV 2025)

## 1. Paper Metadata
- **Title**: Similarity over Factuality: Are we Making Progress on Multimodal Out-of-Context Misinformation Detection?
- **Venue/Year**: WACV 2025
- **DOI**: 10.1109/WACV61041.2025.00544
- **Authors**: Papadopoulos, Stefanos-Iordanis et al.

## 2. The MUSE Method
The MUSE (MUltimodal SimilaritiEs) method extracts CLIP embeddings for the input image and text, and also extracts embeddings for **external web evidence** (related images and text scraped from the web). It computes cosine similarities between these elements and feeds them into a conventional classifier (MLP, Decision Tree, Random Forest) to predict OOC/NOOC.

## 3. Datasets Used
The paper evaluates on NewsCLIPpings and VERITE datasets.

## 4. Easiest/Most Appropriate Dataset for External Benchmark
The method is completely bound to NewsCLIPpings and VERITE because it fundamentally requires the pre-collected web evidence datasets associated with those specific benchmarks. **It does not support COSMOS.**

## 5. Dataset Availability
Yes, the NewsCLIPpings and VERITE datasets (along with their pre-collected web evidence) are publicly downloadable via links in the README.

## 6. Exact Preprocessing Steps
`extract_encoder_features()` to get CLIP embeddings for the raw images/text, followed by `extract_features_for_evidence()` to embed the web evidence, and then `rank_evidence()` to sort the evidence by similarity.

## 7. Required Models/Checkpoints
- Standard `open_clip` Vision Transformer (`ViT-L/14`).
- Trained classification weights (MLP, RF, DT).

## 8. Checkpoint Accessibility
The CLIP model is public. However, **no pre-trained classification weights are provided in the repository.** 

## 9. Is Custom Training Required?
**YES.** Because the authors do not provide pre-trained MLP weights, the scripts (`muse_mlp_experiment.py`) explicitly train the classifier on the target dataset's training split before evaluating. 

## 10. Can Evaluation Be Reproduced Without Training?
**NO.** We would be forced to train the MLP on COSMOS. Since we only have the frozen 900-sample test set and are forbidden from training on it, we cannot use this method.

## 11. Script Inspection
All code in `src/` relies heavily on predefined directory structures mapped specifically to NewsCLIPpings and VERITE. There is no generalized inference script for arbitrary single images.

## 12. CLIP Weights
Standard public weights.

## 13. Precomputed Features
Requires extracting and caching `.npy` files for all images and evidence text before running the classifier.

## 14. Web Evidence Requirement
**CRITICAL:** The method fundamentally requires external evidence files (reverse image search results, captions from other websites where the image appeared).

## 15. Works Directly from Raw Image + Text?
**NO.** It will crash without the accompanying folder of web evidence for that specific image.

## 16. GPU/VRAM
Minimal (~4-8 GB VRAM for CLIP ViT-L/14).

## 17. Colab Feasibility
High for their exact datasets, but impossible for ours without the missing evidence.

## 18. API Keys / External Services
None provided. The authors used pre-scraped evidence from other papers (e.g., Abdelnabi et al.) or scraped VERITE themselves offline. There is no scraper included in this repo.

## 19. Can it run on a 10-sample pilot?
**NO.** We have no web evidence scraped for our 10 COSMOS samples.

## 20. Can the full 900-sample test set be processed?
**NO.** We would have to build a custom reverse-image-search scraping pipeline, execute it for all 900 images, and pray the evidence matches the format MUSE expects.

## 21. Classification
**NOT REPRODUCIBLE** (On our custom external benchmark).

## 22. Most Important: Suitability for our Dissertation
**NOT SUITABLE.** This method evaluates "evidence-based" OOC detection, meaning it compares the claim against a database of web search results. Our dataset (COSMOS-FIXED-v1) does not come with pre-scraped web search results, and this repository does not provide a tool to scrape them. Furthermore, the method requires training a classifier, which violates our rule against training on the test set.

***

# FINAL DECISION

**DROP**
