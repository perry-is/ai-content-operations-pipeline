"""Run the fully synthetic, deterministic end-to-end example."""

import argparse
from pathlib import Path

from .workflow import run_workflow

ROOT = Path(__file__).resolve().parents[2]

SYNTHETIC_SOURCE = {
    "content_id": "podcast_s01e001_learning_to_rest",
    "canonical_title": "Learning to Rest After a Demanding Season",
    "working_title": "When Quiet Feels Unfamiliar",
    "source_type": "podcast_episode",
    "created_date": "2025-04-12",
    "published_date": None,
    "topic": "rest after stress",
    "transcript": "In this fictional episode, Rowan describes how a demanding season made quiet feel unfamiliar. The conversation suggests noticing small transitions and writing down what can wait. The source does not prescribe a clinical practice.",
    "show_notes": "Synthetic notes: a short conversation about pressure to stay productive, transitions, and gentle reflection. The notes mention a body scan, which is not present in the transcript.",
    "urls": {"website_page": "https://example.com/library/learning-to-rest", "spotify": "", "youtube": "", "blog": ""},
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic content operations outputs.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "generated_example")
    parser.add_argument("--library", type=Path, default=ROOT / "examples" / "synthetic_reference_library.json")
    args = parser.parse_args()
    result = run_workflow(SYNTHETIC_SOURCE, args.library, args.output_dir)
    print(f"Content ID: {result['metadata']['content_id']}")
    print(f"Recommendations: {', '.join(x['content_id'] for x in result['recommendations']) or 'none'}")
    print(f"Needs review: {result['metadata']['review']['needs_review']}")
    print(f"Validation: {'PASS' if result['validation']['valid'] else 'FAIL'}")
    print(f"Generated {len(result['outputs'])} outputs in {args.output_dir}")
    if not result["validation"]["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
