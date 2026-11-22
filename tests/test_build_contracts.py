"""GF-style production build declarations must remain bounded and queryable."""
import copy
from pathlib import Path
import unittest

from sunomega.builds import build_metta, searchable_text, validate_build
from sunomega.knowledge import load_records, to_metta

ROOT = Path(__file__).resolve().parents[1] / "knowledge" / "records"


class BuildContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = load_records(ROOT)

    def test_all_techniques_have_an_agent_usable_build(self):
        for r in self.records:
            if r["kind"] == "technique":
                with self.subTest(record=r["id"]):
                    self.assertIn("build", r)
                    validate_build(r["build"], r["id"])

    def test_build_proof_does_not_claim_more_than_supported(self):
        for r in self.records:
            if "build" not in r:
                continue
            with self.subTest(record=r["id"]):
                b = r["build"]
                self.assertGreaterEqual(len(b["execute"]), 2)
                if b["proof"]["status"] in {"locally-tested", "provider-tested", "listener-observed"}:
                    self.assertTrue(b["proof"]["evidence"])
                # Community prompt guidance remains a hypothesis, not an achievement.
                if r["kind"] == "technique":
                    self.assertEqual(b["proof"]["status"], "proposed")

    def test_executable_package_links_are_really_present(self):
        from sunomega.builds import validate_package_links
        validate_package_links(self.records, ROOT)
        skill = next(r for r in self.records if r["id"] == "capability-semantic-midi")
        self.assertEqual(skill["build_path"], "skills/semantic-midi/build.json")
        self.assertEqual(skill["build"]["proof"]["status"], "locally-tested")

    def test_symbolic_projection_preserves_steps_authority_and_proof(self):
        atoms = to_metta(self.records)
        self.assertIn('(BuildTarget "technique-lyric-prosody"', atoms)
        self.assertIn('(BuildStep "technique-lyric-prosody" 1 ', atoms)
        self.assertIn('(BuildEffect "technique-lyric-prosody" "spend")', atoms)
        self.assertIn('(BuildProofStatus "technique-lyric-prosody" "proposed")', atoms)
        self.assertIn('(BuildPath "capability-semantic-midi" "skills/semantic-midi/build.json")', atoms)

    def test_retrieval_includes_procedural_language(self):
        r = next(x for x in self.records if x["id"] == "technique-lyric-prosody")
        self.assertIn("breathing", searchable_text(r))
        self.assertIn("syllables", searchable_text(r))

    def test_reject_unknown_effect(self):
        b = copy.deepcopy(next(r for r in self.records if "build" in r)["build"])
        b["effects"].append("run-arbitrary-command")
        with self.assertRaisesRegex(ValueError, "invalid or duplicate effects"):
            validate_build(b, "fixture")

    def test_reject_missing_matchup(self):
        b = copy.deepcopy(next(r for r in self.records if "build" in r)["build"])
        del b["matchup"]["avoid_when"]
        with self.assertRaisesRegex(ValueError, "matchup"):
            validate_build(b, "fixture")

    def test_reject_false_tested_claim_without_evidence(self):
        b = copy.deepcopy(next(r for r in self.records if "build" in r)["build"])
        b["proof"]["status"] = "listener-observed"
        b["proof"]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "tested proof"):
            validate_build(b, "fixture")

    def test_reject_path_traversal_as_evidence(self):
        b = copy.deepcopy(next(r for r in self.records if "build" in r)["build"])
        b["proof"]["evidence"] = ["research/../../private.txt"]
        with self.assertRaisesRegex(ValueError, "safe local path"):
            validate_build(b, "fixture")


if __name__ == "__main__":
    unittest.main()
