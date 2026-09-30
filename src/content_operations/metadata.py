"""Metadata record builder. Human-readable tags remain separate from taxonomy."""

from .taxonomy import classify_source


def build_metadata(source: dict, recommendations: list[dict]) -> dict:
    tax = classify_source(source)
    unresolved = tax["primary_pathway"] == "needs_review" or "needs_review" in tax["secondary_modalities"]
    return {
        "schema_version": "1.0",
        "content_id": source["content_id"],
        "canonical_title": source["canonical_title"],
        "working_title": source.get("working_title", source["canonical_title"]),
        "source_type": source["source_type"],
        "content_status": "ready_for_review",
        "created_date": source["created_date"],
        "published_date": source.get("published_date"),
        "hosts": ["Rowan Vale"],
        "guests": [],
        "urls": {
            "website_page": source.get("urls", {}).get("website_page", ""),
            "spotify": "", "youtube": "", "blog": "",
        },
        "assets": {
            "content_folder": "", "combined_source": "", "public_companion": "",
            "deep_guide": "", "publishing_sheet": "", "future_optimization_sheet": "",
        },
        "taxonomy": {key: tax[key] for key in (
            "primary_pathway", "secondary_pathways", "primary_modality", "secondary_modalities",
            "depth_level", "practice_types",
        )},
        "tags": {
            "theme_tags": ["rest after stress", "permission to pause", "small transitions"],
            "emotional_tags": ["rest feels unfamiliar", "pressure to stay productive"],
            "dynamic_search_tags": ["I feel guilty when I stop", "peace feels unfamiliar"],
        },
        "related_content": {
            "related_episodes": [x["content_id"] for x in recommendations if x["source_type"] == "podcast_episode"],
            "related_blogs": [x["content_id"] for x in recommendations if x["source_type"] == "blog_post"],
            "related_guides": [x["content_id"] for x in recommendations if x["source_type"] == "guide"],
            "next_best_content": [],
        },
        "review": {
            "needs_review": unresolved,
            "review_reason": tax["review_reason"] if unresolved else "",
            "confidence_score": 0.78 if not unresolved else 0.62,
        },
    }
