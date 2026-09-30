# Uncertainty and human review

The workflow preserves uncertainty as data. When the supporting notes recommend a body scan but the transcript does not mention it, the pipeline follows the transcript for factual output and marks modality as `needs_review`. The metadata carries a review reason and a confidence score; the report can pass structural validation while still saying editorial review is required.

Unknown publication and media URLs remain blank. Empty relationships remain empty unless a synthetic library record is a useful candidate. A recommendation is a suggestion, not an automatic link insertion decision.

The prototype does not infer missing source facts, clinical suitability, or final editorial intent. A human reviews the source, generated layers, and any open metadata fields before publication.
