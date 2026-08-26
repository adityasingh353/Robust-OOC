# Phase 2: Robustness Experiment Design Report

## 1. Research Objective
To systematically evaluate the robustness of cheapfakes/Out-of-Context (OOC) detection models (Baseline A: NLI+CLIP, Baseline B: LLaVA+RoBERTa) against adversarial and semantic perturbations in the image captions. By carefully modifying the frozen `COSMOS-FIXED-v1` evaluation set (900 samples), we aim to measure the performance degradation (robustness gap) of these methods when faced with paraphrasing, entity swapping, negation, date shifting, and location shifting.

## 2. Perturbation Taxonomy
We will generate five distinct perturbations for `caption1` of every sample:
1. **Paraphrase**: Changes syntax/vocabulary, preserves exact semantic meaning.
2. **Entity Swap**: Changes the primary named entity, preserving actions/context.
3. **Negation**: Inverts the primary action/verb.
4. **Date Shift**: Modifies the temporal anchor.
5. **Location Shift**: Modifies the spatial anchor.
*See `results/PHASE2_PERTURBATION_DESIGN/perturbation_protocol.md` for exact transformation rules.*

## 3. Label Semantics
Perturbing one caption fundamentally alters its relationship with the image and the second caption.
- **If Original = NOOC**: Paraphrase keeps the label **NOOC**. All other perturbations introduce a contradiction, changing the ground truth label to **OOC**.
- **If Original = OOC**: All perturbations (Paraphrase, Swap, Negation, Shifts) preserve the contradictory nature, keeping the label **OOC**.
*See `results/PHASE2_PERTURBATION_DESIGN/label_semantics.md` for full semantic mapping.*

## 4. Pilot Design
Before processing the full 900-sample dataset, we will execute a **100-sample pilot** (50 NOOC, 50 OOC, seeded at 42). This limits API costs and allows us to calculate a "Prompt Success Rate" by manually reviewing the 500 generated outputs. We will only proceed to the full dataset if the prompt success rate exceeds 95%.
*See `results/PHASE2_PERTURBATION_DESIGN/pilot_sampling_plan.md`.*

## 5. Gemini Prompt Strategy
Prompts are designed as strict zero-shot system instructions that explicitly define the transformation, what must change, and what must remain identical. If a transformation is impossible (e.g., date shift on a caption without dates), the prompt instructs the model to return a strict `[FAILED_TRANSFORMATION]` tag.
*See `prompts/perturbation_prompts_v1.md`.*

## 6. Quality Control
- **Automated**: Detection of duplicates, massive length changes, format violations, and failure tags.
- **LLM-as-a-Judge**: A secondary prompt pass to verify semantic integrity (e.g., checking for hallucinations).
- **Manual**: 100% manual review of the 100-sample pilot. 5% stratified random sampling + 100% review of flagged items for the final 900-sample generation.
*See `results/PHASE2_PERTURBATION_DESIGN/quality_control_plan.md`.*

## 7. Dataset Schema
The original `cosmos_test_900.csv` will remain completely frozen and untouched. We will generate a new dataset: `cosmos_robustness_v1.csv` with the following columns:
- `original_sample_id`
- `original_caption` (caption1)
- `perturbation_type` (e.g., "Paraphrase", "Entity Swap")
- `perturbed_caption`
- `original_label`
- `expected_label` (computed via the label semantics rules)
- `generation_method` (e.g., "gemini-1.5-pro")
- `generation_prompt_version` (e.g., "v1")

## 8. File Structure
```
RobustOOC/
├── prompts/
│   └── perturbation_prompts_v1.md
├── results/
│   └── PHASE2_PERTURBATION_DESIGN/
│       ├── label_semantics.md
│       ├── perturbation_protocol.md
│       ├── pilot_sampling_plan.md
│       └── quality_control_plan.md
└── result_library/
    └── PHASE2_DESIGN_REPORT.md
```

## 9. Reproducibility Plan
- **Isolation**: The robustness dataset is generated completely blind to Baseline A/B performance. We will not "cherry-pick" perturbations based on whether they trick the models.
- **Versioning**: Prompts and generation parameters (seed, temperature=0.0) are strictly versioned.
- **Data Integrity**: Failed transformations will be explicitly dropped from that specific perturbation category's evaluation, rather than replaced with a different sample, to maintain direct comparability.

## 10. Risks and Mitigation
- **Risk**: The LLM hallucinates new facts during paraphrasing.
  - *Mitigation*: Strict LLM-as-a-judge secondary pass looking for novel entities + manual review strategy.
- **Risk**: Label ambiguity (e.g., an entity swap accidentally matches a different event in the same image).
  - *Mitigation*: The probability is statistically microscopic, but human review of flagged generations will catch edge cases.
- **Risk**: API Rate limits and context failures.
  - *Mitigation*: 100-sample pilot validates the pipeline infrastructure before a heavy 4500-call batch run.
