# Perturbation Protocol Specification

This protocol defines the exact transformations applied to `caption1` of the evaluation dataset to test the robustness of Out-of-Context detection models.

**IMPORTANT:** Not every caption supports every perturbation. Do NOT invent a date, location, or entity merely to force a transformation. If the original caption lacks the necessary elements, the perturbation for that specific category is marked **NOT APPLICABLE**.

## 1. Paraphrase
- **Transformation**: Rewrite the caption using different vocabulary and syntactic structure.
- **Intended Semantic Effect**: Preserve the exact original meaning and factual claims.
- **Must Remain Unchanged**: Entities, dates, locations, numbers, core actions, and sentiment.
- **Intentionally Changed**: Vocabulary (synonyms), syntax (active/passive voice), clause ordering.
- **Example**: 
  - *Original*: "A large crowd gathered outside the capitol building to protest the new tax laws on Tuesday."
  - *Perturbed*: "On Tuesday, numerous protestors assembled outside the capitol to demonstrate against the recently passed tax legislation."

## 2. Entity Swap
- **Transformation**: Identify the primary subject/object (person, organization, or object) and replace it with a plausible alternative belonging to the same category. (If no suitable named entity exists, mark as **NOT APPLICABLE**).
- **Intended Semantic Effect**: Alter the "who" or "what" of the event.
- **Must Remain Unchanged**: All actions, verbs, dates, locations, and surrounding context.
- **Intentionally Changed**: One specific named entity or primary noun.
- **Example**:
  - *Original*: "President Joe Biden delivers a speech in Washington."
  - *Perturbed*: "President Emmanuel Macron delivers a speech in Washington."

## 3. Negation
- **Transformation**: Invert the polarity of the main verb or action in the sentence.
- **Intended Semantic Effect**: Create a logical inversion of the original event.
- **Must Remain Unchanged**: Entities, dates, locations, and the core topic.
- **Intentionally Changed**: Addition/removal of "not", "failed to", "denied", or swapping antonym verbs (won -> lost).
- **Example**:
  - *Original*: "The local football team won the championship match."
  - *Perturbed*: "The local football team lost the championship match."

## 4. Date Shift
- **Transformation**: Identify temporal anchors (years, days, months, relative times) and alter them. (If no date exists, mark as **NOT APPLICABLE**).
- **Intended Semantic Effect**: Shift the event in time.
- **Must Remain Unchanged**: Entities, locations, actions.
- **Intentionally Changed**: Timeframes.
- **Example**:
  - *Original*: "Protests erupted in the city streets in 2020."
  - *Perturbed*: "Protests erupted in the city streets in 2014."

## 5. Location Shift
- **Transformation**: Identify spatial anchors (cities, countries, buildings, geographical features) and replace them with plausible alternatives. (If no location exists, mark as **NOT APPLICABLE**).
- **Intended Semantic Effect**: Shift the event in space.
- **Must Remain Unchanged**: Entities, actions, dates.
- **Intentionally Changed**: Locations.
- **Example**:
  - *Original*: "A massive earthquake struck the coast of Japan."
  - *Perturbed*: "A massive earthquake struck the coast of California."
