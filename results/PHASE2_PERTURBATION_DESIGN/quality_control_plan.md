# Quality Control Plan for Captions

Before exposing robust evaluation datasets to the models, we must guarantee the integrity of the generated perturbations. 

## 1. Three Separate Quality Questions
For every generated caption, we must independently evaluate three specific aspects. Do not collapse these into one score:
1. **Transformation Success**: Did the requested change actually happen? (e.g., Was the location actually swapped?)
2. **Semantic Integrity**: Did the transformation preserve everything it was supposed to preserve and change ONLY what it was supposed to change?
3. **Label Validity**: Can we confidently determine the modified pair's expected OOC/NOOC label as VALID, AMBIGUOUS, or INVALID? (See `label_validity_rules_v2.md`).

## 2. Automated Checks (Rule-Based)
After LLM generation, the following automated heuristics will be run:
- **Duplicate Check**: If `perturbed_caption == original_caption`, flag as a failed generation.
- **Length Check**: If `len(perturbed_caption) < 0.5 * len(original_caption)` or `> 2.0 * len(original_caption)`, flag for hallucination or data loss.
- **Keyword Existence (for shifts/swaps)**: Use basic NLP (e.g., SpaCy NER) to ensure that the newly requested entity/location actually exists in the output.
- **Format Adherence**: Ensure the LLM didn't wrap the output in quotes, markdown, or conversational filler.

## 3. LLM-as-a-Judge (Semantic Verification)
A strict, zero-temperature prompt will be used to automatically review the generated outputs against the **Three Separate Quality Questions** defined above.

## 4. Manual Review Strategy
For the 100-sample pilot:
- **100% Manual Review**: A human researcher will read every single generated caption to manually answer the Three Quality Questions and establish the Pilot Success Rates.

For the full 900-sample run:
- **Stratified Random Sampling**: 5% of the accepted generated captions per category will be manually reviewed.
- **Flagged Review**: 100% of captions flagged by the Automated Checks or LLM-as-a-Judge will be manually reviewed to either be corrected or discarded. If a caption is discarded, the original sample is excluded from the final robustness metric for that specific perturbation category to ensure perfect dataset integrity.
