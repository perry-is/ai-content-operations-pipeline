"""Source hierarchy and source normalization."""

SOURCE_PRIORITY = (
    "primary_source", "supporting_notes", "output_template", "metadata_standard",
    "reference_library", "system_instructions", "implementation_judgment",
)


def resolve_fact(primary: dict, supporting: dict, key: str):
    """Use the primary source for factual content; fall back only when it is absent."""
    if key in primary and primary[key] not in (None, "", []):
        return primary[key], "primary_source"
    if key in supporting and supporting[key] not in (None, "", []):
        return supporting[key], "supporting_notes"
    return None, "unavailable"


def normalize_source(source: dict) -> dict:
    required = ("content_id", "canonical_title", "source_type", "transcript", "created_date")
    missing = [key for key in required if not source.get(key)]
    if missing:
        raise ValueError(f"Missing required source fields: {', '.join(missing)}")
    return {**source, "transcript": source["transcript"].strip(), "show_notes": source.get("show_notes", "").strip()}
