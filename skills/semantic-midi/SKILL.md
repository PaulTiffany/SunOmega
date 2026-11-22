---
name: semantic-midi
description: Compile an explicitly authored semantic melody with verifiable note events into a MIDI file; suitable for experimenting with official Suno MIDI conditioning.
---

# Semantic melody → MIDI

**Target:** an original, exactly specified monophonic MIDI score plus a checkable receipt.

**Equip:** Python 3.11+, the bundled `compile_melody.py`, and `mido` to export MIDI. Standard library suffices for `--validate-only`. Install from repository root: `pip install -e ".[midi]"`.

**Input:** [an original 4-bar melody](examples/hopeful-hook.json), with `intent` as explanatory metadata and exact degree/onset/duration/velocity. No free-form mood adjective is silently compiled into pitches. See [semantic score RFC](../../research/SEMANTIC_SCORE_RFC.md).

**Execute** from repository root:

```bash
python skills/semantic-midi/scripts/compile_melody.py skills/semantic-midi/examples/hopeful-hook.json --validate-only
python skills/semantic-midi/scripts/compile_melody.py skills/semantic-midi/examples/hopeful-hook.json --output /tmp/hopeful-hook.mid
```

Use a writable local output path appropriate for the host. The script prints a JSON receipt with score/MIDI SHA-256, note count, durations, pitch range and silence. It refuses to replace different existing output bytes.

**Matchup:** v0 deliberately supports one melodic line in major/natural minor, <=16 bars. It cannot implement arbitrary harmony, tuplets with nonrepresentable timing, invented instrument effects, free-form emotion commands, or Suno uploads. Encoding is exact; composition is an external LLM/human activity.

**Proof:** run `python -m unittest discover -s tests -v` and, with mido, the MIDI round-trip test. Existing test fixtures establish only compiler behavior. For Suno, a separate authenticated, credit-authorized test must compare generated audio to the notes, then collect listener judgment. See [evidence](references/evidence.md).

**Stopping conditions:** validation failure; reproducible MIDI receipt; or missing dependency. Do not retry generation, spend credits, or claim audio playback without an independent client and user request.

MIT: [LICENSE](LICENSE). Copyright (c) 2026 Paul Carver Tiffany III.
