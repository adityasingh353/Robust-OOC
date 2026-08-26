# Pilot Sampling Plan

Before unleashing LLM generation across the entire 900-sample evaluation set, we will run a controlled pilot test.

## 1. Pilot Dataset Size
We will sample exactly **100** samples from `cosmos_test_900.csv` to act as our pilot set.
- 50 samples with original label `NOOC`
- 50 samples with original label `OOC`

## 2. Selection Methodology
We will use a fixed random seed (`seed=42`) to select the 100 samples from the 900-sample pool to ensure reproducible stratification.

## 3. Pilot Execution Steps
1. Feed the 100 `caption1` strings into the Gemini API using the prompts defined in `prompts/perturbation_prompts_v1.md`.
2. Generate the *applicable* perturbations (Paraphrase, Entity Swap, Negation, Date Shift, Location Shift) for all 100 samples. Do NOT force exactly 5 outputs per sample (e.g., if a caption has no date, Date Shift is NOT APPLICABLE).
3. Save the outputs into `results/EXP007_Pilot_Perturbations/pilot_generated.csv`.
4. Apply the automated checks and LLM-as-a-Judge verifications.
5. Manually review 100% of the generated outputs.

## 4. Pilot Success Metrics
Instead of a simple "Prompt Success Rate", the pilot must report five key metrics. These metrics must be reported **overall**, **separately for each perturbation type**, and **separately for original NOOC vs OOC**.

1. **Transformation Success Rate**: What percentage of requested changes actually happened?
2. **Semantic Validity Rate**: What percentage preserved everything they were supposed to, changing ONLY the target?
3. **Valid Evaluation Rate**: What percentage resulted in a confident expected label (VALID)?
4. **Failure Rate**: What percentage completely failed or generated nonsensical text (INVALID)?
5. **Ambiguity Rate**: What percentage resulted in label ambiguity or required missing visual context (AMBIGUOUS)?

## 5. Acceptance Criteria
We will proceed to the full 900-sample generation ONLY IF the **Valid Evaluation Rate** is sufficiently high across all applicable categories, verifying that the prompt strategy yields robust, testable perturbations.
