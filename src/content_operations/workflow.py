"""Deterministic transformation of one source into coordinated output layers."""

import json
from pathlib import Path

from .metadata import build_metadata
from .reference_library import load_library, recommend
from .source import normalize_source
from .validation import validate_metadata


def _companion(source: dict, refs: list[dict]) -> str:
    title = source["canonical_title"]
    related = ", ".join(ref["canonical_title"] for ref in refs) or "No related item selected yet."
    return f"""# {title}\n\nContent ID: `{source['content_id']}`\n\n## A short pause\n\nThis companion turns the episode's idea into a small moment of practice. It is not a summary of the conversation.\n\n## Try this\n\nChoose one ordinary transition today. Before moving to the next task, take a moment to notice what you are carrying forward. Write one sentence about what can wait.\n\n## Reflect\n\n- What makes a pause feel difficult today?\n- What would a small, realistic rest look like?\n\n## Continue exploring\n\n{related}\n"""


def _guide(source: dict) -> str:
    return f"""# Guided Reflection: {source['canonical_title']}\n\nContent ID: `{source['content_id']}`\n\n## How to use this guide\n\nMove at your own pace. Skip any prompt that does not feel useful. This educational reflection is not therapy or medical care.\n\n## Check in\n\nBefore changing anything, notice what rest means to you right now. There is no preferred answer.\n\n## Teaching\n\nAfter a prolonged demanding period, a quiet moment can feel unfamiliar. The source describes noticing that unfamiliarity without treating it as a problem to solve immediately.\n\n## Map the pattern\n\nWrite down a recent moment when you moved quickly from one task to another. What was happening? What did you expect would happen if you paused? Keep observations separate from conclusions.\n\n## Main practice\n\nChoose a low-stakes transition. Pause briefly, look around, and name one thing that is complete and one thing that can wait. Stop if the exercise feels unhelpful.\n\n## Integration and aftercare\n\nLater, note whether the pause changed anything. If it did not, that is still information. Return to an ordinary grounding activity that feels comfortable to you.\n\n## Next step\n\nConsider the short companion for a smaller practice. Related content suggestions are listed in the publishing materials.\n"""


def _publishing_sheet(source: dict) -> str:
    return f"""# Publishing Sheet\n\n- **Page title:** {source['canonical_title']}\n- **Subtitle:** A short reflection on making room for rest after a demanding season\n- **Content type:** {source['source_type']}\n- **Content ID:** `{source['content_id']}`\n- **Estimated use:** 5–8 minutes\n- **Known demo page:** {source['urls']['website_page']}\n- **Podcast / video links:** Unknown; add only after a publisher confirms them.\n- **Suggested slug:** making-room-for-rest\n- **SEO title:** Making Room for Rest After Stress\n- **Meta description:** A practical reflection on noticing transitions and making space for a small pause.\n- **Keywords / categories:** rest, transitions, reflection\n\n## Copy/paste content block\n\n{_companion(source, [])}\n\n## Publisher checklist\n\n1. Confirm title and page URL.\n2. Review the companion and guide for source fidelity.\n3. Add only confirmed media links.\n4. Review metadata and resolve the open taxonomy question.\n"""


def _optimization(source: dict, metadata: dict, refs: list[dict]) -> str:
    related = ", ".join(f"`{r['content_id']}` ({r['canonical_title']})" for r in refs) or "None selected"
    return f"""# Future Library Note\n\n- **Content identity:** `{source['content_id']}`\n- **Topic:** Rest after prolonged demands; small transitions; permission to pause\n- **Source type:** {source['source_type']}\n- **Controlled pathway:** {metadata['taxonomy']['primary_pathway']}\n- **Controlled modality:** {metadata['taxonomy']['primary_modality']}\n- **Dynamic listener language:** {', '.join(metadata['tags']['dynamic_search_tags'])}\n- **Emotional fit:** For a reader who finds stopping unfamiliar or feels pressure to keep producing\n- **Best used when:** A short reflective practice is appropriate and the reader wants a low-effort next step\n- **Depth:** {metadata['taxonomy']['depth_level']}\n- **Related content IDs:** {related}\n- **Review question:** {metadata['review']['review_reason']}\n- **Possible future use:** Search and recommendation systems could combine controlled fields with listener-language tags.\n"""


def run_workflow(source: dict, library_path: Path, output_dir: Path) -> dict:
    source = normalize_source(source)
    library = load_library(library_path)
    refs = recommend(source, library)
    metadata = build_metadata(source, refs)
    validation = validate_metadata(metadata, {item["content_id"] for item in library} | {source["content_id"]})
    outputs = {
        "public_companion.md": _companion(source, refs),
        "deep_guide.md": _guide(source),
        "publishing_sheet.md": _publishing_sheet(source),
        "future_optimization.md": _optimization(source, metadata, refs),
        "metadata.json": json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        "validation_report.txt": "METADATA VALIDATION\n"
        + ("PASS\n" if validation["valid"] else "FAIL\n")
        + ("Warnings:\n" + "\n".join(f"- {item}" for item in validation["warnings"]) + "\n" if validation["warnings"] else "")
        + ("Errors:\n" + "\n".join(f"- {item}" for item in validation["errors"]) + "\n" if validation["errors"] else "No errors.\n"),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        (output_dir / name).write_text(content, encoding="utf-8")
    return {"metadata": metadata, "validation": validation, "recommendations": refs, "outputs": list(outputs)}
