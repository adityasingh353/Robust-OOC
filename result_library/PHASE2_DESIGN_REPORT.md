# Phase 2: Robustness Experiment Design Report

## 1. Research Objective
To systematically evaluate the robustness of cheapfakes/Out-of-Context (OOC) detection models (Baseline A: NLI+CLIP, Baseline B: LLaVA+RoBERTa) against adversarial and semantic perturbations in the image captions. By carefully modifying the frozen `COSMOS-FIXED-v1` evaluation set (900 samples), we aim to measure the performance degradation (robustness gap) of these methods when faced with paraphrasing, entity swapping, negation, date shifting, and location shifting.

## 2. Perturbation Taxonomy
We will generate five distinct perturbations for `caption1` of every sample, *only when applicable* (e.g., if a caption has no date, Date Shift is marked NOT APPLICABLE):
1. **Paraphrase**: Changes syntax/vocabulary, preserves exact semantic meaning.
2. **Entity Swap**: Changes the primary named entity, preserving actions/context.
3. **Negation**: Inverts the primary action/verb.
4. **Date Shift**: Modifies the temporal anchor.
5. **Location Shift**: Modifies the spatial anchor.
*See `results/PHASE2_PERTURBATION_DESIGN/perturbation_protocol.md` for exact transformation rules.*

## 3. Label Semantics & Validity
We **do not** automatically assign expected labels. Because OOC is a 3-way relationship (image + caption1 + caption2), perturbations can have unintended effects. Every generated sample is independently evaluated for:
1. **Transformation Success**: Did the requested change actually happen?
2. **Semantic Integrity**: Did it preserve what it should and change ONLY what it should?
3. **Label Validity**: Can the final pair be confidently classified?
   - **VALID**: Intended relationship is unambiguous.
   - **AMBIGUOUS**: Requires missing visual/world knowledge, or accidental collision occurred.
   - **INVALID**: Transformation failed or output is nonsensical.
Only **VALID** samples are included in final metrics.
*See `results/PHASE2_PERTURBATION_DESIGN/label_validity_rules_v2.md` and `label_semantics.md`.*

## 4. Pilot Design
We will execute a **100-sample pilot** (50 NOOC, 50 OOC, seeded at 42). 
We will calculate and report the following rates (overall, per-type, and per-original-label):
- Transformation Success Rate
- Semantic Validity Rate
- Valid Evaluation Rate
- Failure Rate
- Ambiguity Rate
*See `results/PHASE2_PERTURBATION_DESIGN/pilot_sampling_plan.md`.*

## 5. Gemini Prompt Strategy
Prompts are designed as strict zero-shot system instructions that explicitly define the transformation.
*See `prompts/perturbation_prompts_v1.md`.*

## 6. Quality Control
- **Automated**: Detection of duplicates, massive length changes, format violations, and failure tags.
- **LLM-as-a-Judge**: A secondary prompt pass to verify semantic integrity (e.g., checking for hallucinations).
- **Manual**: 100% manual review of the 100-sample pilot. 5% stratified random sampling + 100% review of flagged items for the final 900-sample generation.
*See `results/PHASE2_PERTURBATION_DESIGN/quality_control_plan.md`.*

## 7. Dataset Schema
The original `cosmos_test_900.csv` will remain completely frozen and untouched. We will generate a new dataset: `cosmos_robustness_v1.csv` with the following columns:
- `original_sample_id`
- `original_caption`
- `perturbation_type`
- `perturbed_caption`
- `original_label`
- `expected_label`
- `transformation_status` (SUCCESS / FAILED / NOT_APPLICABLE)
- `semantic_validity` (VALID / AMBIGUOUS / INVALID)
- `exclusion_reason`
- `generation_method`
- `generation_prompt_version`

## 8. File Structure
```
RobustOOC/
├── prompts/
│   └── perturbation_prompts_v1.md
├── results/
│   └── PHASE2_PERTURBATION_DESIGN/
│       ├── label_semantics.md
│       ├── label_validity_rules_v2.md
│       ├── perturbation_protocol.md
│       ├── pilot_sampling_plan.md
│       └── quality_control_plan.md
└── result_library/
    └── PHASE2_DESIGN_REPORT.md
```

## 9. Reproducibility Plan
- **Isolation**: The robustness dataset is generated completely blind to Baseline A/B performance. 
- **Versioning**: Prompts and generation parameters (seed, temperature=0.0) are strictly versioned.
- **Data Integrity**: Failed, ambiguous, or not applicable transformations will be explicitly excluded from metrics and logged with reasons.

## 10. Risks and Mitigation
- **Risk**: Label ambiguity (e.g., an entity swap accidentally matches a different event in the same image).
  - *Mitigation*: The `label_validity_rules_v2.md` explicitly screens for this and forces exclusion as AMBIGUOUS.
