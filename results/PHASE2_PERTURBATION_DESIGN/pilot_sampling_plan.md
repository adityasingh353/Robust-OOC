# Pilot Sampling Plan

Before unleashing LLM generation across the entire 900-sample evaluation set (which would result in 900 * 5 = 4500 API calls and manual verifications), we will run a controlled pilot test.

## 1. Pilot Dataset Size
We will sample exactly **100** samples from `cosmos_test_900.csv` to act as our pilot set.
- 50 samples with original label `NOOC`
- 50 samples with original label `OOC`

## 2. Selection Methodology
We will use a fixed random seed (`seed=42`) to select the 100 samples from the 900-sample pool to ensure reproducible stratification.

## 3. Pilot Execution Steps
1. Feed the 100 `caption1` strings into the Gemini API using the prompts defined in `prompts/perturbation_prompts_v1.md`.
2. Generate all 5 perturbations (Paraphrase, Entity Swap, Negation, Date Shift, Location Shift) for all 100 samples.
3. Save the outputs into `results/EXP007_Pilot_Perturbations/pilot_generated.csv`.
4. Apply the automated checks and LLM-as-a-Judge verifications.
5. Manually review all 500 outputs.
6. Calculate the "Prompt Success Rate" (percentage of outputs that perfectly adhere to the transformation instructions without hallucinations or grammar issues).

## 4. Acceptance Criteria
We will proceed to the full 900-sample generation ONLY IF the Prompt Success Rate exceeds **95%** on the pilot dataset. If the rate is lower, the prompts in `perturbation_prompts_v1.md` must be iteratively refined and re-tested on the pilot set.
