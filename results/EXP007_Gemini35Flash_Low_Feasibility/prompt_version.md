# Prompt Version Used

The prompts used for this feasibility test match the strict zero-shot constraints defined in `prompts/perturbation_prompts_v1.md`.
The LLM was instructed to execute Paraphrase, Entity Swap, Negation, Date Shift, and Location Shift where applicable, returning a clear `[FAILED_TRANSFORMATION]` or `NOT_APPLICABLE` equivalent when the target text lacked the required anchors (e.g. no dates to shift).
