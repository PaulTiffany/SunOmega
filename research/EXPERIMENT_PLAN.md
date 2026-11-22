# SunOmega experiments — bounded, falsifiable, source-linked

These are **proposals**, not completed Suno experiments. Do not spend credits, upload an audio file, or save private preferences without permission. Baseline feature availability and user grants first.

## M0 — integration gate (existing Issue #1)

Use the official endpoint and existing Omega runtime. Record MCP transport/auth support, tool discovery, read-only usage/library response, and an explicitly authorized short generation. No assumption that the ChatGPT Suno connector's tool names/plan are available in Omega. **PASS** is observed Omega-originated action and finished original clip; an unsupported client is a documented blocker.

## E1 — semantic composition fidelity (local; zero Suno credits)

**Question:** can an LLM translate a musical brief into a valid, verifiable semantic score and produce an exact MIDI file without notes drifting from its own score?

Inputs: bounded original four-bar fixture, exact tempo/meter/key, one or more authored alternatives. Outcomes: compile/no-compile, actual note count, starts, degrees, rests, pitches, dynamics, hash. Negative fixture: overlapping notes/invalid fractions/constraint violations rejected. The helper's success is not evidence of musical beauty.

## E2 — MIDI vs text conditioning (Suno, operator-approved)

Hypothesis: an original MIDI condition improves preservation of specified *melodic contour, timing and cadence* compared with a text-only description of the same material.

Controls: same musical identity, instrument brief, target duration and model; only the provision of MIDI differs. Before testing, probe which Suno model supports MIDI over the available MCP path; do **not** mix a v6-wild MIDI condition with an unrelated v6 text-only baseline and call it controlled. Use at least two independent original melodies, matched candidate counts, and predeclared inclusion/exclusion criteria; separate technical score fidelity from human appeal. Budget: define number of provider calls and credits **before** execution.

Measurements: melodic onset alignment after estimated beat map, interval/contour preservation in adequately isolated lead regions, phrase/cadence recognition by blind listeners, bad output count, actual credit and latency receipt. If an audio transcription tool confuses polyphony, mark that metric inconclusive.

## E3 — prompt build composition (Suno, operator-approved)

Hypothesis: an explicit “musicians' actions and arrangement arc” brief reduces generic/flat results compared with tag-cloud prompting. Fixed model/controls/lyrics/candidate count, randomize evaluation order, compare listener assessments of coherence, vocal pacing and intended buildup. Do not declare one favorable pair universal.

## E4 — prosody and breathing (Suno, operator-approved)

Question: under fixed style/tempo/model, does changing line lengths, repetition and deliberate rests reduce rushed vocals? First test clear natural punctuation/shorter lines; treat community bracket commands like `[Silence]` as experimental, not officially supported syntax. Measure estimated syllables per second, actual sung pauses and listener judgments. Multiple songs / conditions to avoid a single-genre artifact.

## E5 — stem continuity (Suno + local audio; operator-approved)

Generate or reuse an authorized instrumental, isolate drums if account grants and credits allow, obtain timing/key/sections, align a loop across the outgoing and incoming tracks, audition the transition. Report beat drift, clipping, stem artifacts, out-of-phase percussion, perceived continuity and whether a prepared fallback prevents dead air when generation takes too long. Local real-time playback remains independent of Suno job duration.

## Evidence receipt fields

`experiment_id`, `hypothesis`, `source_ids`, `repo_commit`, `agent_host`, `tool_names`, `model`, `controls`, `full_requests`, `source_score_sha256`, `midi_sha256`, `clip_ids`, `job_status`, `credit_cost`, `timestamps`, `audio_analysis`, `listener_preference`, `negative_results`, `limitations`.

Never substitute LLM self-grading for listener feedback or audio analysis. Cite [S11](sources.json) for limits of common automatic metrics.
