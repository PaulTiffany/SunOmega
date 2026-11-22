"""Semantic score contract tests — musical intent is NOT an executed instruction."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "skills" / "semantic-midi" / "scripts" / "compile_melody.py"
FIXTURE = REPO / "skills" / "semantic-midi" / "examples" / "hopeful-hook.json"
spec = importlib.util.spec_from_file_location("semantic_midi", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class SemanticMIDITests(unittest.TestCase):
    def setUp(self):
        self.score = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_original_fixture_pitch_time_and_rest(self):
        result = module.validate_score(self.score)
        self.assertEqual(result["total_ticks"], 16 * 480)
        self.assertEqual(len(result["notes"]), 13)
        self.assertEqual(result["silent_ticks"], 240)
        self.assertEqual(result["notes"][0]["pitch"], 62)  # D4
        self.assertEqual(max(x["pitch"] for x in result["notes"]), 74)  # D5
        self.assertEqual(result["notes"][-1]["pitch"], 62)

    def test_overlap_is_rejected(self):
        self.score["notes"][1]["start"] = "1/2"
        with self.assertRaisesRegex(ValueError, "overlapping"):
            module.validate_score(self.score)

    def test_constraint_failure_is_rejected(self):
        self.score["constraints"]["min_total_rest_beats"] = "1"
        with self.assertRaisesRegex(ValueError, "Minimum total rest"):
            module.validate_score(self.score)

    def test_fraction_beyond_ppqn_is_rejected(self):
        self.score["notes"][0]["duration"] = "1/7"
        with self.assertRaises(ValueError):
            module.validate_score(self.score)

    def test_unsupported_semantics_are_not_silently_ignored(self):
        self.score["notes"][0]["emotional_color"] = "joy"
        with self.assertRaisesRegex(ValueError, "unsupported"):
            module.validate_score(self.score)

    @unittest.skipUnless(importlib.util.find_spec("mido"), "mido extra not installed")
    def test_midi_determinism_and_round_trip(self):
        from mido import MidiFile
        from io import BytesIO

        normalized = module.validate_score(self.score)
        one = module.make_midi_bytes(normalized)
        two = module.make_midi_bytes(normalized)
        self.assertEqual(one, two)
        self.assertTrue(one.startswith(b"MThd"))
        midi = MidiFile(file=BytesIO(one))
        notes_on = [m for tr in midi.tracks for m in tr
                    if m.type == "note_on" and m.velocity > 0]
        self.assertEqual(len(notes_on), 13)
        self.assertEqual(notes_on[0].note, 62)
        self.assertIn(74, [n.note for n in notes_on])
        self.assertTrue(any(m.type == "set_tempo" for tr in midi.tracks for m in tr))
        self.assertEqual(sum(m.time for m in midi.tracks[0]), 7680)


if __name__ == "__main__":
    unittest.main()
