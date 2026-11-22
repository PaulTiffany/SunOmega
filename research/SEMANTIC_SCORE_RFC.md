# RFC: Semantic melody dictation, v0

## Problem

Human language describes **intent** (“a rising question, answered softly”), but Standard MIDI Files encode **events** (pitch/onset/duration/velocity). ABC and MusicXML carry notation but not always machine-actionable human intent. Preserve both instead of asking an LLM to write raw MIDI events or promising that vague adjectives deterministically compile.

Sources: [S5](sources.json) Suno MIDI conditioning; [S10](sources.json) notation study; [S13](sources.json) CMU representation comparison; [S14](sources.json) music21; [S15](sources.json) Mido.

## Proposed v0 authoring contract

`schema: sunomega.semantic-melody.v0` represents a **single monophonic pitched melody** on a 480-PPQN grid, limited to 1–16 bars. It carries `intent` as explanatory, unexecuted text; `tonic` and `mode` (major or natural minor), `meter`, `tempo_bpm`, exact `notes` with start/duration fractions of a quarter note, and **verifiable** constraints.

Example: [original four-bar D-minor hook](../skills/semantic-midi/examples/hopeful-hook.json).

An LLM may choose durations, degrees and octave. The compiler *must not* convert “hopeful” to notes on its own. That musical judgment belongs to the composing agent, is recorded explicitly, and is reviewable.

Pitch resolution: scale degree 1–7 is relative to a tonic register, `octave` defined as the MIDI octave of degree 1; degree 7 may therefore be heard in the next chromatic octave. C4 = MIDI note 60. Supported tonal systems are intentionally limited; chromatic alterations and modulations require a later schema revision.

`notes[].start` and `duration` are exact rational *quarter-note beats*, e.g. `"3/2"`, `"4"`; gaps are rests. The compiler rejects notes overlapping, outside the declared measure span, unrepresentable tick fractions, invalid register or missing required constraints. No auto-quantization or hidden accompaniment is allowed.

`constraints` currently cover first/last scale degree, minimum total silence, and maximum leap size. These are testable specifications. The aesthetic intent is not.

## Why not start with MusicXML, ABC, or direct MIDI?

- **Direct MIDI** is the correct transport into Suno but too low level for natural composition dialogue.
- **ABC** is a useful human-readable export for simple folk/monophonic melodies; less expressive for tracked intention and evidence.
- **MusicXML** is a strong future interchange for scores/parts/articulations. Its richer data model is promising, but generating giant XML structures directly in chat is avoidable.
- **A small typed JSON score** is easy for an LLM to produce and for a deterministic validator to reject when ambiguous. Its score can later be serialized into ABC or MusicXML without replacing either standard.

## Decomposition that preserves evidence

`human brief -> LLM-authored semantic score -> validated exact events -> MIDI bytes -> Suno conditioned generation -> observed audio transcription/analysis -> human evaluation`.

Every boundary has an independent witness. A valid MIDI file does not prove Suno adhered to it. Suno audio metadata or pitch extraction is uncertain on polyphonic production; transcribed notes are not automatically ground truth. A listening panel remains necessary for identity/expressiveness.

## Next version candidates (not implemented)

Named motifs and explicit variation operations (repeat, transpose, invert, rhythmic augmentation), polyphonic accompaniment, articulation, chord-aware degree spelling, stronger cadence/contour checks, optional lyrics-to-onset alignment, MusicXML output, and robust matching of rendered Suno audio to source score.

**Avoid** teaching an LLM a custom text syntax that silently invents musical data. Keep intermediate objects explicit, finite, and independently inspected.
