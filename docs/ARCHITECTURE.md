# Technical architecture

**One knowledge base, multiple consumers.** Git-versioned JSON is the durable source of truth. A deterministic exporter loads the same records as MeTTa atoms in an in-process Hyperon AtomSpace; no separate hand-maintained graph. ChatGPT can read through GitHub. A future MCP knowledge service can expose provenance-aware queries and reviewed contributions.

**Layers:** evidence/sources -> typed records -> MeTTa/AtomSpace -> read-only knowledge interface -> existing Omega inference and execution -> official Suno MCP. Music generation is asynchronous. Local playback/mixing must remain continuous independently of provider latency.

**Stack:** Python 3.11; Hyperon 0.2.10 as optional adapter (experimental); JSON + Git for provenance/versioning; built-in validation and unittest; GitHub Actions; optional mido / pretty_midi, FFmpeg, librosa, soundfile for MIDI/audio. Do not deploy Redis, graph DB, vector DB, distributed AtomSpace or custom agent runtime at this scale.

**Boundaries:** the remote Suno MCP is https://api.suno.com/mcp; authentication is per agent/client, and ChatGPT credentials cannot be inherited by Omega. User explicitly authorizes credit-consuming actions. Public knowledge and private individual musical taste must be separated. Do not infer emotions from noisy physiological measures without consent and validation. Keep unpublished origination/continual-learning details out of this public repository.

**Phasing:** prove Omega<->Suno MCP first; validate KB and AtomSpace queries second; next experiment with MIDI composition/conditioning, prompt practices and stem-aware DJ transitions. Avoid hard dependencies on inaccessible OmegaHive.
