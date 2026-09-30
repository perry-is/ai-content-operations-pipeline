import json
import tempfile
import unittest
from pathlib import Path

from content_operations.demo import ROOT, SYNTHETIC_SOURCE
from content_operations.identity import draft_id, finalize_id, validate_content_id
from content_operations.metadata import build_metadata
from content_operations.reference_library import load_library, recommend
from content_operations.source import resolve_fact
from content_operations.taxonomy import MODALITIES, PATHWAYS, classify_source
from content_operations.validation import validate_metadata
from content_operations.workflow import run_workflow


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.library = load_library(ROOT / "examples" / "synthetic_reference_library.json")

    def metadata(self):
        refs = recommend(SYNTHETIC_SOURCE, self.library)
        return build_metadata(SYNTHETIC_SOURCE, refs)

    def test_final_content_id_is_stable(self):
        self.assertEqual(finalize_id("podcast_s01e001_learning_to_rest", "podcast_s01e001_learning_to_rest"), "podcast_s01e001_learning_to_rest")
        with self.assertRaises(ValueError):
            finalize_id("podcast_s01e001_learning_to_rest", "podcast_s01e001_resting")

    def test_draft_id_can_be_finalized_but_is_temporary(self):
        temporary = draft_id("New topic!")
        self.assertEqual(temporary, "draft_new_topic")
        self.assertTrue(validate_content_id(temporary))
        self.assertEqual(finalize_id(temporary, "guide_new_topic"), "guide_new_topic")

    def test_source_hierarchy_prefers_primary_fact(self):
        value, source = resolve_fact({"practice": "journaling"}, {"practice": "body scan"}, "practice")
        self.assertEqual((value, source), ("journaling", "primary_source"))

    def test_source_notes_fill_missing_primary_fact(self):
        self.assertEqual(resolve_fact({}, {"duration": "short"}, "duration"), ("short", "supporting_notes"))

    def test_controlled_vocabulary_is_available(self):
        self.assertIn("nervous_system", PATHWAYS)
        self.assertIn("needs_review", MODALITIES)

    def test_invalid_taxonomy_triggers_review(self):
        result = classify_source({"transcript": "A fictional unrelated topic."})
        self.assertEqual(result["primary_pathway"], "needs_review")
        self.assertIn("confident", result["review_reason"])

    def test_unknown_urls_remain_blank(self):
        urls = self.metadata()["urls"]
        self.assertEqual(urls["spotify"], "")
        self.assertEqual(urls["youtube"], "")
        self.assertEqual(urls["blog"], "")

    def test_relationships_use_content_ids(self):
        record = self.metadata()
        self.assertIn("blog_small_transitions", record["related_content"]["related_blogs"])
        self.assertNotIn("A Small Pause Between Tasks", record["related_content"]["related_blogs"])

    def test_malformed_related_title_is_rejected(self):
        record = self.metadata()
        record["related_content"]["related_blogs"] = ["A Small Pause Between Tasks"]
        result = validate_metadata(record)
        self.assertFalse(result["valid"])
        self.assertTrue(any("stable content IDs" in error for error in result["errors"]))

    def test_valid_metadata_passes(self):
        known = {item["content_id"] for item in self.library} | {SYNTHETIC_SOURCE["content_id"]}
        self.assertTrue(validate_metadata(self.metadata(), known)["valid"])

    def test_invalid_metadata_has_useful_errors(self):
        record = self.metadata()
        record["source_type"] = "video"
        record["created_date"] = "yesterday"
        errors = validate_metadata(record)["errors"]
        self.assertTrue(any("source_type" in error for error in errors))
        self.assertTrue(any("ISO" in error for error in errors))

    def test_uncertain_classification_sets_review_flag(self):
        record = self.metadata()
        self.assertTrue(record["review"]["needs_review"])
        self.assertTrue(record["review"]["review_reason"])
        self.assertIn("needs_review", record["taxonomy"]["secondary_modalities"])

    def test_dynamic_tags_are_separate_from_taxonomy(self):
        record = self.metadata()
        self.assertIn("peace feels unfamiliar", record["tags"]["dynamic_search_tags"])
        self.assertNotIn("dynamic_search_tags", record["taxonomy"])

    def test_generated_outputs_share_content_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_workflow(SYNTHETIC_SOURCE, ROOT / "examples" / "synthetic_reference_library.json", Path(tmp))
            for filename in ("public_companion.md", "deep_guide.md", "publishing_sheet.md", "future_optimization.md"):
                self.assertIn(SYNTHETIC_SOURCE["content_id"], (Path(tmp) / filename).read_text(encoding="utf-8"))
            self.assertEqual(json.loads((Path(tmp) / "metadata.json").read_text(encoding="utf-8"))["content_id"], SYNTHETIC_SOURCE["content_id"])

    def test_metadata_remains_internally_consistent(self):
        record = self.metadata()
        self.assertEqual(record["content_id"], SYNTHETIC_SOURCE["content_id"])
        self.assertEqual(record["source_type"], "podcast_episode")
        self.assertTrue(record["review"]["needs_review"])

    def test_reference_library_recommends_relevant_items(self):
        ids = {item["content_id"] for item in recommend(SYNTHETIC_SOURCE, self.library)}
        self.assertIn("blog_small_transitions", ids)
        self.assertIn("guide_noticing_pressure", ids)

    def test_demo_generates_all_expected_files(self):
        expected = {"public_companion.md", "deep_guide.md", "publishing_sheet.md", "future_optimization.md", "metadata.json", "validation_report.txt"}
        with tempfile.TemporaryDirectory() as tmp:
            result = run_workflow(SYNTHETIC_SOURCE, ROOT / "examples" / "synthetic_reference_library.json", Path(tmp))
            self.assertEqual(set(result["outputs"]), expected)
            self.assertEqual({p.name for p in Path(tmp).iterdir()}, expected)
            self.assertTrue(result["validation"]["valid"])

    def test_validator_requires_single_metadata_record(self):
        result = validate_metadata(self.metadata(), record_count=2)
        self.assertFalse(result["valid"])
        self.assertTrue(any("Exactly one" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
