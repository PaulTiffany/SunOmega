# Semantic MIDI evidence boundary

The included original `hopeful-hook.json` contains 13 monophonic notes in 4 bars of 4/4 at 104 BPM, D natural minor. It deliberately has a half-beat gap. Expected tonic pitch D4 = MIDI 62, peak D5 = MIDI 74.

**Before CI:** this package is an implementation proposal. Do not mark tests as observed until a workflow passes on the PR head.

**CI checks:** standard-library validator tests; an additional job with installed Mido loads the resulting MIDI and checks note count, pitch/tick schedule, tempo and hash repeatability. A passing job will support exact source-to-MIDI compilation only.

**Not yet established:** any generated Suno audio, official MCP MIDI upload success, preservation of melody in an arrangement, perceived emotional arc, DJ mix suitability, user preference or broader Omega reliability. These require separately authorized, dated evidence.

Source rationale: https://help.suno.com/en/articles/14594177 (Suno MIDI conditioning, edited 2026-11-04); https://mido.readthedocs.io/en/stable/api.html (Mido serialization).
