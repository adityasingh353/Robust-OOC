# Label Semantics for Perturbed Captions

The COSMOS dataset labels image-caption pairs as:
- **NOOC (Not Out-Of-Context)**: Both captions describe the same event and match the image.
- **OOC (Out-Of-Context)**: The two captions describe different events, or one caption is falsely associated with the image.

When we systematically perturb one of the captions (`caption1`), the ground-truth label of the pair (`caption1`, `caption2`) may change. 

**IMPORTANT NOTE**: We DO NOT automatically assign an expected label solely based on the original label and the perturbation type. Perturbations can have unintended semantic interactions with the other caption or the image.

## 1. General Principles
- The OOC/NOOC label is a three-way relationship between the **image**, **caption1**, and **caption2**.
- We do not claim a perturbed caption is OOC merely because it differs from `caption2`. The image itself is part of the definition.
- Some perturbations on Original OOC pairs can accidentally create NOOC pairs (e.g., location-shifting a false caption so it accidentally matches the true caption).

## 2. Theoretical Expected Label Transitions
These are the *theoretical* expected transitions, assuming no accidental collisions:

### Original Label: NOOC
* **Paraphrase**: Expected to remain **NOOC**.
* **Entity Swap, Negation, Date Shift, Location Shift**: Expected to become **OOC**, as the modified caption should now contradict the image and the other caption.

### Original Label: OOC
* **Paraphrase**: Expected to remain **OOC**.
* **Entity Swap, Negation, Date Shift, Location Shift**: Expected to remain **OOC**, as the captions generally remain contradictory.

## 3. Resolving Ambiguity
Because accidental collisions (e.g., Original OOC becoming NOOC due to a random entity swap) are possible, every generated sample must be independently evaluated for **Label Validity** (see `label_validity_rules_v2.md`). 

If determining the new relationship requires visual/world knowledge that cannot be established confidently from the text alone, the case must be classified as **AMBIGUOUS** and excluded from that perturbation's final robustness metric.
