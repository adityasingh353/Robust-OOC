# Label Semantics for Perturbed Captions

The COSMOS dataset labels image-caption pairs as:
- **NOOC (Not Out-Of-Context)**: Both captions describe the same event and match the image.
- **OOC (Out-Of-Context)**: The two captions describe different events, or one caption is falsely associated with the image.

When we systematically perturb one of the captions (`caption1`), the ground-truth label of the pair (`caption1`, `caption2`) may change. This document defines the expected label transitions.

## 1. Original Label: NOOC
The original captions are semantically equivalent regarding the core event.

* **Paraphrase**: Changes phrasing, preserves meaning.
  * **Expected Label**: **NOOC**. The captions still describe the same event.
* **Entity Swap**: Changes the main subject/object (e.g., "Biden" -> "Macron").
  * **Expected Label**: **OOC**. The modified caption now contradicts the image and the other caption.
* **Negation**: Inverts the action/state (e.g., "won the election" -> "lost the election").
  * **Expected Label**: **OOC**. The modified caption directly contradicts the other caption.
* **Date Shift**: Changes the temporal anchor (e.g., "in 2021" -> "in 2018").
  * **Expected Label**: **OOC**. The event is shifted in time, contradicting the other caption.
* **Location Shift**: Changes the spatial anchor (e.g., "in London" -> "in Paris").
  * **Expected Label**: **OOC**. The event is shifted in space, contradicting the other caption.

## 2. Original Label: OOC
The original captions already contradict each other (one is true, one is false/misleading).

* **Paraphrase**: Preserves the misleading meaning of the caption.
  * **Expected Label**: **OOC**. They still contradict.
* **Entity Swap, Negation, Date Shift, Location Shift**: Further alters the already-false caption.
  * **Expected Label**: **OOC**. The captions remain contradictory. *(Note: There is a microscopic theoretical chance that a random perturbation accidentally reverts a false caption back to the true caption, making them match. However, without human-in-the-loop vision evaluation, we must assume the perturbation creates a novel contradiction. Quality control will flag ambiguous cases.)*
