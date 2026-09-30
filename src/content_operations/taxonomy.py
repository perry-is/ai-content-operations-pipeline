"""Small controlled vocabularies and a deterministic demo classifier."""

SOURCE_TYPES = {"podcast_episode", "blog_post", "class", "workshop", "coaching_topic", "guide"}
CONTENT_STATUSES = {"draft", "ready_for_review", "published", "archived", "needs_update"}
DEPTH_LEVELS = {"gentle", "steady", "deep"}
PATHWAYS = {
    "nervous_system", "relationships_attachment", "self_trust", "shadow_work",
    "purpose_direction", "grief_letting_go", "communication_truth", "self_mastery",
    "spiritual_growth", "self_worth_identity", "needs_review",
}
MODALITIES = {
    "somatic_awareness", "nervous_system_regulation", "attachment_work", "shadow_work",
    "parts_reflection", "journaling", "mindfulness", "breathwork", "communication_practice",
    "boundary_work", "values_clarification", "emotional_regulation", "grief_reflection",
    "inner_child_reflection", "self_inquiry", "spiritual_reflection", "accountability_practice",
    "relational_repair", "cognitive_reframing", "integration_practice", "needs_review",
}
PRACTICE_TYPES = {
    "reflection", "journaling", "body_scan", "grounding", "breathwork",
    "communication_practice", "boundary_practice", "parts_reflection", "pattern_mapping",
    "values_action", "integration_plan", "aftercare", "self_inquiry",
}


def classify_source(source: dict) -> dict:
    """Return explicit, non-model taxonomy; preserve unresolved modality as review."""
    source_text = " ".join((source.get("topic", ""), source.get("canonical_title", ""), source["transcript"])).lower()
    if "rest" in source_text or "stress" in source_text:
        return {
            "primary_pathway": "nervous_system",
            "secondary_pathways": ["self_trust"],
            "primary_modality": "journaling",
            "secondary_modalities": ["needs_review"],
            "depth_level": "gentle",
            "practice_types": ["reflection", "journaling", "integration_plan"],
            "review_reason": "The source supports reflection and journaling; whether a somatic modality is central is unclear.",
        }
    return {
        "primary_pathway": "needs_review", "secondary_pathways": [],
        "primary_modality": "needs_review", "secondary_modalities": [],
        "depth_level": "gentle", "practice_types": ["reflection"],
        "review_reason": "The source does not support a confident pathway or modality assignment.",
    }
