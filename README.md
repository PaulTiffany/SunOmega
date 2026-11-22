# SunOmega

**Shared, agent-first Suno production knowledge and orchestration.**

SunOmega is an MIT-licensed project by **Paul Carver Tiffany III**. It gives ChatGPT and authorized Omegas one inspectable source of evidence about musical production. An eventual OmegaDJ can use it for continuous music with voluntary game/participant feedback.

**Milestone 0 remains open:** an Omega has not yet been proven to connect to the official Suno MCP (https://api.suno.com/mcp), discover its tools, and generate a song through its own authenticated session. ChatGPT's connection does not prove that integration.

## Architecture — GF-style builds indexed by AtomSpace

- **Git + JSON records:** source-linked musical knowledge, prompt guidance, tool capabilities, and controlled experiment claims.
- **GF production contracts:** every technique declares Target / Equip / Execute / Matchup / Proof, effects, bounds and stopping conditions. A recipe is advisory; only an explicitly linked `skills/<id>/build.json` package provides a runnable helper.
- **MeTTa / Hyperon AtomSpace:** deterministic, queryable projection of those records, their sources, their relationships and their build contracts. Git JSON remains authoritative.
- **Agent/host boundary:** a retrieved recipe never grants authority to authenticate, spend, upload, or publish. Tool grants and budgets are handled independently.
- **Later music pipeline:** official Suno MCP; optional Mido/pretty_midi for score/MIDI, FFmpeg/librosa/soundfile for audio, and local playback/mixing independent of asynchronous generation.

See [knowledge format and examples](knowledge/README.md), [architecture](docs/ARCHITECTURE.md), [MCP proof gate](docs/OMEGA_SUNO_MCP.md), [knowledge policy](docs/KNOWLEDGE_POLICY.md) and [roadmap](docs/ROADMAP.md).

## Try the knowledge base

From a Python 3.11-compatible checkout:

```bash
python -m pip install -e ".[atomspace,midi]"
sunomega validate
sunomega builds
sunomega search "breathing"
sunomega show technique-lyric-prosody
sunomega export-metta
sunomega smoke-metta
```

The semantic-score-to-MIDI GF package lives in [skills/semantic-midi](skills/semantic-midi/). The research [draft PR](https://github.com/PaulTiffany/SunOmega/pull/4) introduces that package and the GF contracts; do not treat it as merged into `main` until reviewed.

## Project milestones

M0 prove Omega → official Suno MCP with independent authorization and explicit approval for paid test generation. M1 make the shared AtomSpace-based Suno knowledge usable by both human/ChatGPT and Omega. M2 explore exact symbolic melody control and Suno MIDI adherence. Later: controlled prompt tests, stems, continuous mixing and private opt-in taste preferences.

## Licensing and boundaries

Original code and docs are under [MIT](LICENSE), copyright (c) 2026 Paul Carver Tiffany III. Suno/Reddit publications retain their own copyrights; we link and summarize them. Do not commit credentials, private taste or biometric data, unlicensed audio, or unpublished origination/continual-learning research. Not affiliated with Suno or OmegaHive.
