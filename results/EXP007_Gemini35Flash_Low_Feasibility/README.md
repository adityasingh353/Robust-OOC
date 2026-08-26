# EXP007: Gemini 3.5 Flash Low Feasibility Test

This directory contains the artifacts from the 20-sample feasibility test for caption perturbations in the RobustOOC project.

## Execution Context
- **Model**: Gemini 3.5 Flash Low (simulated natively via the Antigravity agent context).
- **Environment**: Google Antigravity IDE (Agent conversational environment).
- **Dataset**: 20 samples from `data/cosmos_test_fixed.csv` (seed=42).

## Files
- `raw_outputs.csv`: The unfiltered tabular output of all 100 generated perturbations.
- `generated_outputs.csv`: Same as raw, formatted for easy downstream evaluation.
- `quality_report.md`: Detailed breakdown of transformation success rates and semantic validity.
- `model_config.json`: The agent context settings used during generation.
- `prompt_version.md`: Log of the zero-shot instructions applied.

## Objective
To prove that the strict Phase 2 protocol (allowing `NOT_APPLICABLE` and applying the 3-tier `VALID`/`AMBIGUOUS`/`INVALID` semantic check) functions correctly on a small scale before launching the full generation pipeline.
