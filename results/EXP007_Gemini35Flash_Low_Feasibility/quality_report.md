# Quality Report: 20-Sample Feasibility Test (Gemini 3.5 Flash Low)

## 1. Summary of Generation
- **Requested Transformations**: 100 (20 samples x 5 categories)
- **Successful Transformations**: 50
- **NOT APPLICABLE (No target anchors)**: 50
- **INVALID (Failed/Garbage)**: 0 (All applicable passed format checks)
- **AMBIGUOUS (Label collision risk)**: 10 (Primarily Entity Swaps and Location Shifts on originally OOC captions)
- **VALID (Confident expected label)**: 40

## 2. Success Rates
- **Transformation Success Rate**: 100% of *applicable* cases successfully transformed. (50/50)
- **Semantic Validity Rate**: 100% of transformed cases preserved original unrelated facts.
- **Valid Evaluation Rate**: 80% (40/50 applicable cases were confidently VALID. 20% were flagged AMBIGUOUS to prevent dataset pollution).
- **Failure Rate**: 0%
- **Ambiguity Rate**: 20% (10/50 applicable cases)

## 3. Rate Breakdown by Category
- **Paraphrase**: 20 applicable. 20 VALID. 0 AMBIGUOUS.
- **Entity Swap**: 6 applicable. 3 VALID (from NOOC). 3 AMBIGUOUS (from OOC). 14 NOT APPLICABLE.
- **Negation**: 11 applicable. 11 VALID. 9 NOT APPLICABLE.
- **Date Shift**: 4 applicable. 2 VALID. 2 AMBIGUOUS (from OOC). 16 NOT APPLICABLE.
- **Location Shift**: 9 applicable. 4 VALID. 5 AMBIGUOUS (from OOC). 11 NOT APPLICABLE.

## 4. Examples of Good Outputs (VALID)
- **Original (NOOC)**: "Ljuba Gajic outside her home, Pakrac, 1996"
- **Entity Swap (VALID -> OOC)**: "Ana Novak outside her home, Pakrac, 1996"
*Reasoning*: The entity change confidently creates a contradiction.

- **Original (OOC)**: "Does a 1994 Denver Airport Mural Show a Masked Global Population"
- **Negation (VALID -> OOC)**: "A 1994 Denver Airport Mural Does Not Show a Masked Global Population"
*Reasoning*: The logical inversion preserves the contradictory nature against the true image.

## 5. Examples of Problematic/Flagged Outputs (AMBIGUOUS)
- **Original (OOC)**: "Does a 1994 Denver Airport Mural Show a Masked Global Population"
- **Location Shift**: "Does a 1994 Atlanta Airport Mural Show a Masked Global Population"
*Reasoning (AMBIGUOUS)*: Changing the location of a falsely attributed image *could* accidentally align with the truth (maybe the real mural is in Atlanta). Without visual verification, the new expected label is AMBIGUOUS and must be excluded from the final metric.
