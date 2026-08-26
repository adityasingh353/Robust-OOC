# Quality Control Plan for Captions

Before exposing robust evaluation datasets to the models, we must guarantee the integrity of the generated perturbations. This document specifies the detection protocols for failures.

## 1. Automated Checks (Rule-Based)
After LLM generation, the following automated heuristics will be run:
- **Duplicate Check**: If `perturbed_caption == original_caption`, flag as a failed generation.
- **Length Check**: If `len(perturbed_caption) < 0.5 * len(original_caption)` or `> 2.0 * len(original_caption)`, flag for hallucination or data loss.
- **Keyword Existence (for shifts/swaps)**: Use basic NLP (e.g., SpaCy NER) to ensure that the newly requested entity/location actually exists in the output.
- **Format Adherence**: Ensure the LLM didn't wrap the output in quotes, markdown, or conversational filler (e.g., "Here is your caption:").

## 2. LLM-as-a-Judge (Semantic Verification)
A strict, zero-temperature prompt will be used to automatically review the generated outputs:
- **Meaning accidentally changed (Paraphrase)**: Does the new caption contain any factual claims not present in the original?
- **Entity/Date/Location not changed**: Did the generation fail to alter the intended target?
- **Malformed Negation**: Does the sentence sound grammatically broken or feature a double negative?
- **Ambiguity**: Does the modification make the sentence ambiguous or nonsensical in a real-world context?

## 3. Manual Review Strategy
For the 100-sample pilot:
- **100% Manual Review**: A human researcher will read every single generated caption across all 5 perturbation categories (500 outputs total) to verify semantic integrity and evaluate the LLM-as-a-Judge performance.

For the full 900-sample run:
- **Stratified Random Sampling**: 5% of the accepted generated captions per category will be manually reviewed.
- **Flagged Review**: 100% of captions flagged by the Automated Checks or LLM-as-a-Judge will be manually reviewed to either be corrected or discarded. If a caption is discarded, the original sample is excluded from the final robustness metric for that specific perturbation category to ensure perfect dataset integrity.
