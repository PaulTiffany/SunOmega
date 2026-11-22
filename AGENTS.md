# Instructions for SunOmega agents and contributors

**Purpose:** make Suno production knowledge reusable by ChatGPT and authorized Omegas. The repository is not an implementation of Omega or a place to publish unrelated research.

## Required workflow

1. **Read docs/ARCHITECTURE.md, docs/KNOWLEDGE_POLICY.md, and knowledge/records before suggesting a best practice.**
2. Distinguish official Suno features from user/community claims; cite record IDs and source URLs. Never upgrade a hypothesis to "tested" based solely on prose.
3. Prefer one small, explicit, sourced record per technique over large copied guides. Run `sunomega validate`, `sunomega smoke-metta` (with optional Hyperon installed) and unit tests after knowledge changes.
4. Retain failed/negative experiments and model/version scope. Do not erase disagreements; add relations and evidence.
5. Never claim Omega↔Suno MCP works until M0 proof has been recorded. Use only https://api.suno.com/mcp for official Suno integration.
6. Never expose credentials, assume ChatGPT's Suno authorization can be delegated, spend credits without operator approval, or store personal preference/biofeedback in this public repository.
7. Do not add novel origination, continual-learning mechanisms, private OmegaHive code, or other independent research to this project.
8. Keep tooling simple: core Python stdlib, optional Hyperon/MIDI/audio dependencies; no backend or database unless measured requirements justify one.

## Query

To search by keyword from repository root: `sunomega search "prosody"`.
For complete inspectable facts: `sunomega export-metta`.
For source provenance: open linked record IDs, and then original publication URLs. Explain uncertainty.

## GF-style production builds and research

When a musical request can be served by an existing build, query its capability record in the AtomSpace (e.g. `capability-semantic-midi`), follow the `BuildPath` atom to a `skills/<id>/build.json`, then read the package's `SKILL.md` and evidence. Treat build inspection as read-only; tool execution is a separate user-authorized operation.

Consult `research/SUNO_EVIDENCE.md` and the dated `research/sources.json` for production facts and research provenance, and `research/SUNO_MCP_TOOL_SURFACE.md` for **observed ChatGPT-specific** connector contracts. These cannot establish actual Omega tool grants.

A musical instruction is not an exact MIDI event stream. Let the composing model author explicit score events; deterministic helpers only validate and compile them. Keep spec correctness, exported bytes, Suno result, measured audio fidelity and human listening judgments separate.

## Changes

Use small commits/PRs. Update tests/docs for schema changes. Prefer a working, narrow capability over a speculative multi-agent platform.
