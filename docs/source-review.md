# Source review

Three available workflow references were reviewed in place and were not modified:

- Blog Writing Workflow & Request Guide v1
- Podcast & Offers Reference v1
- Published Blog Reference Library v1

The first describes a short pre-writing brief, a complete publishing package, a prioritized human review order, and revision feedback. The second describes selective, usefulness-based cross-linking and a lightweight updateable reference. The third describes using a library to find related material, avoid unnecessary topic repetition, and distinguish structural references from reader-facing links.

The requested Master Project Instructions, Metadata Standard, Future Optimization instructions, Publishing Sheet instructions, Project Setup Read Me, Podcast Template, and Sanctuary Template were not found in the searched local locations. The user has since separately confirmed the production architecture summarized below. This confirmation informs the documentation; the unavailable files themselves were not reviewed, copied, or included.

## Confirmed production architecture

The production workflow is intended to be repeatable and low-friction across podcast episodes, blogs, teachings, classes, workshops, coaching topics, and guides. A full content package separates a short public companion, deeper guided practice resource, immediate publishing sheet, future-optimization/library-data sheet, and `metadata.json`.

Its source priority is primary transcript/content, show notes or outline, template, metadata standard, reference library, project instructions, then assistant or implementation judgment. The primary source controls facts about actual exercises and practices. Missing URLs and uncertain classifications remain unknown or flagged rather than invented.

The Metadata Standard defines the structured machine-readable authority, with stable finalized `content_id` values and a required `schema_version`. For an individual item, standalone `metadata.json` is the preferred machine-readable record, while human-readable metadata copies may appear in generated documents. An operational registry should track workflow and status without duplicating the entire metadata model. Future migration should preserve content IDs and reviewed corrections; relationships use stable content IDs.

The Publishing Sheet serves the immediate human publishing workflow. The Future Optimization Sheet serves long-term search, filtering, recommendations, pathways, AI triage, and app migration. That separation is intended to prepare for future library intelligence without adding heavy data-entry work to weekly publishing.

## Public implementation boundary

These confirmed concepts describe the production architecture; they do not mean the original production documents or source code are part of this repository. The public edition is a clean-room, deterministic implementation using synthetic content. Its demo shows one fictional podcast item and a small reference library, produces generic Markdown outputs and one metadata JSON file, and does not implement a workflow registry, production template system, or migration process.

An archive of article documents was present, but its contents were not used. No article, transcript, branded template, live link, or production asset was copied into this public edition.
