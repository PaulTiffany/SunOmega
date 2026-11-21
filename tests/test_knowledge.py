"""Standard library tests for the knowledge graph."""
import unittest
from pathlib import Path
from sunomega.knowledge import load_records, validate_records, to_metta

ROOT = Path(__file__).resolve().parents[1] / "knowledge" / "records"


class KnowledgeTests(unittest.TestCase):
    def test_records_valid(self):
        self.assertGreaterEqual(len(load_records(ROOT)), 7)

    def test_projection_deterministic(self):
        records = load_records(ROOT)
        self.assertEqual(to_metta(records), to_metta(list(reversed(records))))
        self.assertIn('(Record "capability-official-mcp" "capability")', to_metta(records))

    def test_broken_source_rejected(self):
        records = [dict(r) for r in load_records(ROOT)]
        target = next(r for r in records if r["kind"] == "technique")
        target["sources"] = ["missing-id"]
        with self.assertRaisesRegex(ValueError, "missing source"):
            validate_records(records)

    def test_duplicate_rejected(self):
        records = load_records(ROOT)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate_records(records + [dict(records[0])])


if __name__ == "__main__":
    unittest.main()
