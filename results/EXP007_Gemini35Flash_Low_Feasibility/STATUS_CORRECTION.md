# STATUS CORRECTION: EXP007 Dry-Run Only

**WARNING: INVALID FOR SCIENTIFIC INTERPRETATION**

## 1. Dry-Run Limitation
- **No Real Gemini Inference**: The "Gemini 3.5 Flash Low" experiment did NOT use real Gemini model inference. As stated in the `model_config.json`, the generation was simulated via a deterministic Python script within the Antigravity agent context.
- **Not a Quality Experiment**: Because no actual LLM logic was used, this experiment does not establish Gemini 3.5 Flash Low generation quality or prompt adherence.
- **Usage Restriction**: The outputs contained in this directory (`generated_outputs.csv` and `raw_outputs.csv`) **must not be used** in the final dissertation robustness benchmark.

## 2. Output Quality Problems
An independent inspection of `generated_outputs.csv` reveals that the simulated dry-run outputs contain obvious and catastrophic transformation failures resulting from the naive string-replacement logic.

**Examples of failed transformations:**
- Paraphrase simply appended text without rewriting: e.g., `Does a 1994 Denver Airport Mural Show a Masked Global Population (paraphrased)`.
- Negation produced grammatically broken text: e.g., `Office worker Hideyuki Togashi, 48, shows his not tattoos...` and `A museum on Kinmen Island, Taiwan, recalls the is notlanders' defense...`.
- Entity swap produced nonsense when exact matches failed: e.g., replacing partial substrings or failing to adjust grammar.
- Fallback Negation logic: `(negated)` appended without any actual semantic negation.

## 3. Conclusion
These errors conclusively demonstrate that the dry-run simulation cannot be used to validate the perturbation prompts. A real LLM API must be used for genuine evaluation.
