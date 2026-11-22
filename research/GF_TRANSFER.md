# GF lessons for SunOmega

Grounding: [GF README](https://github.com/PaulTiffany/GF/blob/main/README.md), [architecture](https://github.com/PaulTiffany/GF/blob/main/ARCHITECTURE.md), [agent contribution rules](https://github.com/PaulTiffany/GF/blob/main/AGENTS.md), and [declaration template](https://github.com/PaulTiffany/GF/blob/main/templates/build.json), inspected 2026-11-22.

## The right abstraction: a reproducible *move*

GF is an executable build wiki for a tool-equipped assistant. It combines **Target -> Equip -> Execute -> Matchup -> Proof** and an independent host authority boundary, not an omnipotent agent platform.

SunOmega should support GF-like **production builds**. A knowledge statement such as “lyric prosody may affect phrasing” is not itself a build. An executable build adds:
- **Target**: clearly stated musical outcome; observable criterion.
- **Equip**: runtime, user-granted Suno features, inputs and rights.
- **Execute**: constrained steps, explicit adapter/tool names, reproducible helper.
- **Matchup**: supported environment/models/genre, assumptions and failure modes.
- **Proof**: request/source digest, tool receipt, output artifact analysis, and human listening judgment distinguished.

## Evidence tiers, never conflated

1. **Specification:** the semantic score is well-formed and constraints are satisfied.
2. **Artifact:** MIDI/audio bytes exist, verify checksums and expected events.
3. **Provider result:** Suno accepted a request and produced an actual finished clip.
4. **Audio adherence:** independent listening or analysis finds the requested notes, rhythm, structure, dynamics, etc.
5. **Experience:** an actual listener judges the musical outcome as intended.

Level 1/2 success must not masquerade as level 3/4/5. CI is not listener testimony. Official documentation is not evidence that an untested Omega has authenticated.

## Build contract requirements

Every shipped capability declares `requires`, `inputs`, `outputs`, `effects` (local-read, local-write, network-read, network-write, account-write, spend), enforced and operator bounds, `stop_when`, and evidence. The static catalogue/search path is read-only; running tools is a separate authority decision.

A procedure can have source/technique nodes in the AtomSpace, but should remain a portable, self-contained package with its own test fixture. The AtomSpace indexes what it **can** do, including prerequisites, source status, applicability and contrary evidence. It does not acquire permissions, spend credits or improvise unspecified notes.

## Transfer from the GF failure history

GF learned to distinguish a verified artifact, an attachment actually delivered, and playback observed on the client; earlier successes inferred from URLs were corrected by a genuine client probe. This maps directly to MIDI correctness, Suno generation completion, measured musical fidelity and actual listener preference.

GF also used finite counterexample searches with explicit model scope and `inconclusive` budgets; for SunOmega, a perfect local score compilation proves nothing about Suno's stochastic audio output. Keep failure and uncertainty records.

## Recommendation

Prioritize one narrow build: **semantic-score-to-MIDI** with deterministic note timing/pitch receipts, bounded inputs and a deliberately unimplemented Suno upload step. Then prove Omega->official Suno MCP in its own separate integration gate. Do not add a general agent runtime, separate graph database or novel research algorithms.
