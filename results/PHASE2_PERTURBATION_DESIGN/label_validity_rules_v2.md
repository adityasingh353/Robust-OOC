# Label Validity Rules v2

Because OOC/NOOC is a three-way relationship (image + caption1 + caption2), and because perturbations can have unintended semantic effects, every generated perturbation must be classified into one of three validity categories: **VALID**, **AMBIGUOUS**, or **INVALID**.

Only **VALID** samples will be included in the final robustness metrics.

## 1. VALID
The intended semantic relationship (OOC or NOOC) is unambiguous after the perturbation.
- **Criteria**: The modified caption has a clear, confident relationship with the unperturbed caption2 and the underlying context.
- **Example**: If Original NOOC is "A man stands in Delhi" + "A guy is standing in Delhi", and the location shift produces "A man stands in Paris", it is confidently **VALID** (Expected OOC) because it clearly contradicts the unperturbed caption.

## 2. AMBIGUOUS
The perturbation could plausibly make the modified pair either OOC or NOOC, or the image/context does not provide enough evidence to determine the result confidently without seeing the actual image.
- **Criteria**: Determining the new expected label requires visual or world knowledge not present in the captions, or the perturbation accidentally created a semantic collision.
- **Example**: If Original OOC is "A man is in Delhi" + "A man is in Mumbai". If the first caption is location-shifted to "A man is in Mumbai", the captions now match. Without seeing the image to know if it's actually Mumbai, we cannot confidently label it NOOC or OOC. This must be marked **AMBIGUOUS**.
- **Action**: Exclude from the final robustness metric for this perturbation category. Retain in the dataset archive with an exclusion reason.

## 3. INVALID
The transformation itself failed, introduced unrelated changes, or produced malformed/nonsensical text.
- **Criteria**: The LLM failed to follow instructions, hallucinated extra facts, or produced grammatically broken output.
- **Action**: Exclude from the final robustness metric. Retain in the dataset archive with an exclusion reason.

## Summary of Independent Quality Checks
For every generated caption, we must evaluate three separate criteria. **Do not collapse these into one score.**
1. **Transformation Success**: Did the requested change actually happen? (e.g., Was the location actually swapped?)
2. **Semantic Integrity**: Did the transformation preserve everything it was supposed to preserve and change ONLY what it was supposed to change?
3. **Label Validity**: Can we confidently determine the modified pair's expected OOC/NOOC label as VALID, AMBIGUOUS, or INVALID?
