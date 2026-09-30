# Metadata design

Each item has one JSON record containing identity, source type, status, dates, participants, URLs, asset placeholders, taxonomy, tags, relationships, and review state. The schema version is explicit so a future migration can distinguish records created under different contracts.

## Controlled fields

`source_type`, `content_status`, pathway, modality, depth, and practice types use controlled vocabularies defined in `taxonomy.py`. Use `needs_review` when the classification is unresolved. Never force an uncertain concept into a nearby category merely to complete a field.

## Dynamic tags

Theme, emotional, and dynamic-search tags retain phrases that are useful for discovery but too specific or variable to belong in a stable enum. The validator bounds tag counts but does not pretend to judge semantic quality.

## Relationships and URLs

Relationship values are content IDs and may be checked against the known synthetic library. Display titles are not accepted as relationship identifiers. Unknown URLs are empty strings. The synthetic known page uses the reserved `example.com` domain; the validator rejects other non-empty URLs in this demo dataset.

## Validation boundary

The validator checks required fields, version, ID syntax, controlled values, ISO date syntax, URL policy, tag bounds, relationship IDs, review state, and one-record uniqueness. A valid result means these mechanical checks passed. It does not prove factual accuracy or editorial readiness.
