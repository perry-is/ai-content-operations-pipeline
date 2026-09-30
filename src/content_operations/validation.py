"""Readable metadata validation without external schema dependencies."""

from datetime import date

from .identity import validate_content_id
from .taxonomy import CONTENT_STATUSES, DEPTH_LEVELS, MODALITIES, PATHWAYS, PRACTICE_TYPES, SOURCE_TYPES


def validate_metadata(metadata: dict, known_content_ids: set[str] | None = None, record_count: int = 1) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    required = ("schema_version", "content_id", "canonical_title", "working_title", "source_type",
                "content_status", "created_date", "hosts", "guests", "urls", "assets", "taxonomy", "tags",
                "related_content", "review")
    for field in required:
        if field not in metadata:
            errors.append(f"Missing required field: {field}")
    if errors:
        return {"valid": False, "errors": errors, "warnings": warnings}
    if metadata["schema_version"] != "1.0": errors.append("schema_version must be 1.0")
    if not validate_content_id(metadata["content_id"]): errors.append("content_id must be lowercase underscore-separated text")
    if metadata["source_type"] not in SOURCE_TYPES: errors.append("source_type is not in the controlled vocabulary")
    if metadata["content_status"] not in CONTENT_STATUSES: errors.append("content_status is not in the controlled vocabulary")
    for field in ("created_date", "published_date"):
        value = metadata.get(field)
        if value:
            try: date.fromisoformat(value)
            except (TypeError, ValueError): errors.append(f"{field} must use ISO YYYY-MM-DD format")
    tax = metadata["taxonomy"]
    checks = (("primary_pathway", PATHWAYS), ("primary_modality", MODALITIES), ("depth_level", DEPTH_LEVELS))
    for key, allowed in checks:
        if tax.get(key) not in allowed:
            errors.append(f"taxonomy.{key} is not in the controlled vocabulary")
    for key, allowed in (("secondary_pathways", PATHWAYS), ("secondary_modalities", MODALITIES), ("practice_types", PRACTICE_TYPES)):
        for value in tax.get(key, []):
            if value not in allowed: errors.append(f"taxonomy.{key} contains invalid value: {value}")
    urls = metadata["urls"]
    for key in ("website_page", "spotify", "youtube", "blog"):
        value = urls.get(key, "")
        if value and not value.startswith("https://example.com/"):
            errors.append(f"urls.{key} must be blank or use the synthetic example.com domain")
    related = metadata["related_content"]
    for key, ids in related.items():
        if not isinstance(ids, list):
            errors.append(f"related_content.{key} must be a list of content IDs")
            continue
        for value in ids:
            if not isinstance(value, str) or not validate_content_id(value):
                errors.append(f"related_content.{key} entries must be stable content IDs")
            elif known_content_ids is not None and value not in known_content_ids:
                errors.append(f"related_content.{key} references unknown content_id: {value}")
    for group in ("theme_tags", "emotional_tags", "dynamic_search_tags"):
        values = metadata["tags"].get(group, [])
        if not isinstance(values, list) or len(values) > 10:
            errors.append(f"tags.{group} must be a list with at most 10 entries")
    review = metadata["review"]
    uncertain = any("needs_review" == tax.get(k) or "needs_review" in tax.get(k, [])
                    for k in ("primary_pathway", "primary_modality", "secondary_pathways", "secondary_modalities"))
    if uncertain and not review.get("needs_review"):
        errors.append("Uncertain taxonomy must set review.needs_review=true")
    if review.get("needs_review") and not review.get("review_reason"):
        errors.append("review.review_reason is required when needs_review is true")
    if record_count != 1: errors.append("Exactly one metadata record is expected for this content item")
    if not metadata.get("published_date"): warnings.append("published_date is blank because publication has not been confirmed")
    return {"valid": not errors, "errors": errors, "warnings": warnings}
