# SunOmega

**Agent-first Suno music production knowledge and orchestration.**

SunOmega is an MIT-licensed project by **Paul Carver Tiffany III**. Its purpose is to build a shared, structured, inspectable body of Suno production knowledge that ChatGPT and authorized Omegas can both access. OmegaDJ, continuous music driven by voluntary audience/game feedback, is a later application.

**Status: foundation only.** Omega-to-Suno MCP connectivity has not yet been proven. No generation or DJ system is claimed to work.

## Priorities

1. **M0: prove an existing Omega can use the official Suno MCP** (https://api.suno.com/mcp) with a separately authorized account, discover tools, perform read-only calls, then create a test track with explicit approval.
2. **M1: shared knowledge base.** Source-attributed, Git-versioned JSON records; deterministic MeTTa/Hyperon AtomSpace projection; CLI and later shared MCP knowledge queries.
3. **M2+: production tooling.** MIDI generation, audio analysis, stems, reliable transitions, prompt experiments, opt-in musical tastes, and OmegaDJ.

## Technology

Python 3.11, optional Hyperon 0.2.10 / MeTTa, Git + JSON records, official remote Suno MCP. Later: mido / pretty_midi, FFmpeg, librosa, soundfile and a separate live mixer. We deliberately avoid a server database or custom learning algorithms until needed.

See [architecture](docs/ARCHITECTURE.md), [MCP proof](docs/OMEGA_SUNO_MCP.md), [knowledge policy](docs/KNOWLEDGE_POLICY.md), and [roadmap](docs/ROADMAP.md).

## Start (after Python package is added)

    python -m pip install -e .
    sunomega validate
    sunomega search "midi"
    sunomega export-metta

For real Hyperon AtomSpace queries, install the optional atomspace extra and use smoke-metta. The repository is useful to ChatGPT immediately through GitHub; a dedicated SunOmega MCP is a later interface.

## Safety, ownership and rights

Original code and original documentation: MIT; [LICENSE](LICENSE), Copyright (c) 2026 Paul Carver Tiffany III. Linked Reddit and Suno works remain subject to their own rights, and we cite/summarize instead of republishing. Do not commit access tokens, personal biofeedback, third-party audio or unpublished origination/continual-learning research. Not affiliated with Suno or OmegaHive.
