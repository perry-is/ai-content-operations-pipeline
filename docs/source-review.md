# How the public version relates to the real system

This pipeline is modeled on the operating procedure I use to turn podcast episodes, workshops, and teachings into companion resources and publishing assets. That procedure lives as written instructions, templates, and a metadata standard used with AI assistants. This repository re-implements its structure with fictional content.

## The production system

The production workflow is intended to be repeatable and low-friction across podcast episodes, blogs, teachings, classes, workshops, coaching topics, and guides. A full content package separates a short public companion, deeper guided practice resource, immediate publishing sheet, future-optimization/library-data sheet, and `metadata.json`.

Its source priority is primary transcript/content, show notes or outline, template, metadata standard, reference library, project instructions, then assistant or implementation judgment. The primary source controls facts about actual exercises and practices. Missing URLs and uncertain classifications remain unknown or flagged rather than invented.

The Metadata Standard defines the structured machine-readable authority, with stable finalized `content_id` values and a required `schema_version`. For an individual item, standalone `metadata.json` is the preferred machine-readable record, while human-readable metadata copies may appear in generated documents. An operational registry should track workflow and status without duplicating the entire metadata model. Future migration should preserve content IDs and reviewed corrections; relationships use stable content IDs.

The Publishing Sheet serves the immediate human publishing workflow. The Future Optimization Sheet serves long-term search, filtering, recommendations, pathways, AI triage, and app migration. That separation is intended to prepare for future library intelligence without adding heavy data-entry work to weekly publishing.

## What this repository contains

These confirmed concepts describe the production architecture; they do not mean the original production documents or source code are part of this repository. The public edition is a fresh, deterministic implementation using synthetic content. Its demo shows one fictional podcast item and a small reference library, produces generic Markdown outputs and one metadata JSON file, and does not implement a workflow registry, production template system, or migration process.

No article, transcript, branded template, live link, or production asset from the real system is included.
