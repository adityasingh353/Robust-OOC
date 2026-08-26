# Perturbation Protocol Specification

This protocol defines the exact transformations applied to `caption1` of the evaluation dataset to test the robustness of Out-of-Context detection models.

## 1. Paraphrase
- **Transformation**: Rewrite the caption using different vocabulary and syntactic structure.
- **Intended Semantic Effect**: Preserve the exact original meaning and factual claims.
- **Must Remain Unchanged**: Entities, dates, locations, numbers, core actions, and sentiment.
- **Intentionally Changed**: Vocabulary (synonyms), syntax (active/passive voice), clause ordering.
- **Example**: 
  - *Original*: "A large crowd gathered outside the capitol building to protest the new tax laws on Tuesday."
  - *Perturbed*: "On Tuesday, numerous protestors assembled outside the capitol to demonstrate against the recently passed tax legislation."
- **Failure Condition**: The paraphrase drops a key entity or changes the factual meaning.

## 2. Entity Swap
- **Transformation**: Identify the primary subject/object (person, organization, or object) and replace it with a plausible alternative belonging to the same category.
- **Intended Semantic Effect**: Alter the "who" or "what" of the event, creating a factual contradiction.
- **Must Remain Unchanged**: All actions, verbs, dates, locations, and surrounding context.
- **Intentionally Changed**: One specific named entity or primary noun.
- **Example**:
  - *Original*: "President Joe Biden delivers a speech in Washington."
  - *Perturbed*: "President Emmanuel Macron delivers a speech in Washington."
- **Failure Condition**: Swapping an entity with something grammatically nonsensical or changing multiple unrelated parts of the sentence.

## 3. Negation
- **Transformation**: Invert the polarity of the main verb or action in the sentence.
- **Intended Semantic Effect**: Create a direct logical contradiction of the original event.
- **Must Remain Unchanged**: Entities, dates, locations, and the core topic.
- **Intentionally Changed**: Addition/removal of "not", "failed to", "denied", or swapping antonym verbs (won -> lost).
- **Example**:
  - *Original*: "The local football team won the championship match."
  - *Perturbed*: "The local football team lost the championship match."
- **Failure Condition**: Creating a double negative that preserves original meaning, or creating a syntactically broken sentence.

## 4. Date Shift
- **Transformation**: Identify temporal anchors (years, days, months, relative times) and alter them.
- **Intended Semantic Effect**: Shift the event in time to create a chronological contradiction.
- **Must Remain Unchanged**: Entities, locations, actions.
- **Intentionally Changed**: Timeframes.
- **Example**:
  - *Original*: "Protests erupted in the city streets in 2020."
  - *Perturbed*: "Protests erupted in the city streets in 2014."
- **Failure Condition**: Removing the date without replacing it, or inserting a date into a caption that doesn't natively support a temporal anchor without sounding completely unnatural.

## 5. Location Shift
- **Transformation**: Identify spatial anchors (cities, countries, buildings, geographical features) and replace them with plausible alternatives.
- **Intended Semantic Effect**: Shift the event in space to create a geographical contradiction.
- **Must Remain Unchanged**: Entities, actions, dates.
- **Intentionally Changed**: Locations.
- **Example**:
  - *Original*: "A massive earthquake struck the coast of Japan."
  - *Perturbed*: "A massive earthquake struck the coast of California."
- **Failure Condition**: Swapping a location for a non-location (e.g., swapping "Japan" for "Apple").
