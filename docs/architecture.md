# Architecture

The pipeline keeps one source item and its derivatives connected by a stable identifier while separating factual input, editorial transformations, publisher actions, and machine-readable library data.

## Processing path

`source.py` normalizes the supplied transcript and notes. Its `resolve_fact` helper gives the primary source priority and uses notes only when the primary source does not supply a value. `identity.py` validates stable IDs and prevents silent changes after finalization. `taxonomy.py` assigns a small controlled vocabulary deterministically and returns explicit uncertainty. `reference_library.py` ranks synthetic library records by simple term overlap. `workflow.py` generates four human-readable layers and one metadata record, then validates and writes the results.

The example is intentionally deterministic. This makes source-to-output behavior inspectable and repeatable without a network service, paid provider, or model call. A future model integration would belong at interpretation or drafting boundaries and should preserve provenance, contracts, and review flags.

## Output responsibilities

| Output | Primary reader | Job |
|---|---|---|
| Public companion | Audience | Invite a short interaction with the source |
| Deep guide | Audience | Provide a longer, educational reflection path |
| Publishing sheet | Publisher | Reduce manual assembly and mark unknown links |
| Future-library note | Content operator | Capture fit, tags, and possible future reuse |
| `metadata.json` | Software | Support consistent filtering, relationships, and migration |
| Validation report | Operator | Show structural errors and unresolved review state |

## Separate concerns

Human-readable outputs are written for people and can contain natural-language explanations. Structured metadata uses controlled values, stable IDs, and explicit empty values. Dynamic tags are not used as substitutes for controlled taxonomy. Related items point to IDs so a title change does not break a relationship.
