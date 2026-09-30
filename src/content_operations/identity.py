"""Stable machine identity helpers."""

import re

CONTENT_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")


def validate_content_id(content_id: str) -> bool:
    return bool(CONTENT_ID_PATTERN.fullmatch(content_id))


def draft_id(seed: str) -> str:
    """Create a visibly temporary ID; callers must not treat it as finalized."""
    slug = re.sub(r"[^a-z0-9]+", "_", seed.lower()).strip("_")
    return f"draft_{slug or 'untitled'}"


def finalize_id(current_id: str | None, proposed_id: str) -> str:
    """Finalize an ID once and reject silent changes to an existing final ID."""
    if not validate_content_id(proposed_id) or proposed_id.startswith("draft_"):
        raise ValueError("Final content IDs must be lowercase underscore-separated IDs.")
    if current_id and not current_id.startswith("draft_") and current_id != proposed_id:
        raise ValueError("A finalized content_id is stable and cannot be silently changed.")
    return proposed_id
