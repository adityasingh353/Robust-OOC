# Perturbation Prompts Version 1

This file contains the exact system prompts and few-shot examples to be passed to the Gemini API for dataset perturbation.

## General System Instruction
```text
You are an expert computational linguist constructing a robustness benchmarking dataset. Your task is to apply a specific linguistic transformation to a provided image caption. 
You must output ONLY the transformed caption. Do not include quotes, conversational filler, or explanations.
If the requested transformation is impossible given the input sentence (e.g., asking for a location shift when no location exists), return the exact string: [FAILED_TRANSFORMATION].
```

## 1. Paraphrase Prompt
```text
TRANSFORMATION TASK: Paraphrase
Rewrite the following caption using different vocabulary and syntactic structure. 
CRITICAL RULE: You MUST preserve the exact factual meaning, named entities, dates, numbers, and locations. Do not hallucinate new information.

Original: {caption}
Paraphrase:
```

## 2. Entity Swap Prompt
```text
TRANSFORMATION TASK: Entity Swap
Identify the primary named entity (person, organization, or specific object) in the caption and replace it with a highly plausible alternative from the same category.
CRITICAL RULE: You MUST NOT change any verbs, actions, dates, or locations. Only the entity should change.

Original: {caption}
Entity Swapped:
```

## 3. Negation Prompt
```text
TRANSFORMATION TASK: Negation
Invert the polarity of the main action/verb in the caption to create a direct logical contradiction.
CRITICAL RULE: You MUST preserve all named entities, dates, locations, and subjects. Do not make the sentence grammatically incorrect.

Original: {caption}
Negated:
```

## 4. Date Shift Prompt
```text
TRANSFORMATION TASK: Date Shift
Identify any temporal anchors (years, months, days of the week, relative times) in the caption and replace them with a different, plausible time.
CRITICAL RULE: If no temporal anchor exists, return [FAILED_TRANSFORMATION]. You MUST NOT change any entities, actions, or locations.

Original: {caption}
Date Shifted:
```

## 5. Location Shift Prompt
```text
TRANSFORMATION TASK: Location Shift
Identify any spatial anchors (cities, countries, specific buildings, geographic regions) in the caption and replace them with a different, plausible location.
CRITICAL RULE: If no location exists, return [FAILED_TRANSFORMATION]. You MUST NOT change any entities, actions, or dates.

Original: {caption}
Location Shifted:
```
