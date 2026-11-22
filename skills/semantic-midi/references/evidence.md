# Semantic MIDI evidence boundary

The included original `hopeful-hook.json` contains 13 monophonic notes in 4 bars of 4/4 at 104 BPM, D natural minor. It deliberately has a half-beat gap. Expected tonic pitch D4 = MIDI 62, peak D5 = MIDI 74.

**Observed on GitHub Actions (2026-11-22):** On commit `cf4048e6e52845351f6158d43f423327e6000d92`, the `semantic-midi` job completed successfully with 10 standard-library/Mido tests, including exact MIDI readback. [Workflow run](https://github.com/PaulTiffany/SunOmega/actions/runs/45062200467). This is implementation evidence only, and the branch may receive further commits.

**CI checks:** standard-library validator tests and a job with installed Mido loaded the resulting MIDI and checked note count, pitch/tick schedule, tempo and hash repeatability. Receipt: input SHA-256 `864dccc8f7a6976c8d45eb8c1aa7440b5195f6be43866cd1dd96481507ab0154`; output MIDI SHA-256 `57921156c44fbf0bdd3e8e0157b45020ed08a0515d33e4357881e603ab601f9d`; 13 notes, 7680 ticks, 240 silent ticks, pitch 62–74. This supports exact source-to-MIDI compilation only.

**Not yet established:** any generated Suno audio, official MCP MIDI upload success, preservation of melody in an arrangement, perceived emotional arc, DJ mix suitability, user preference or broader Omega reliability. These require separately authorized, dated evidence.

Source rationale: https://help.suno.com/en/articles/14594177 (Suno MIDI conditioning, edited 2026-11-04); https://mido.readthedocs.io/en/stable/api.html (Mido serialization).
