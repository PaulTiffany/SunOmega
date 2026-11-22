# Observed Suno MCP tool contracts (ChatGPT environment)

**Observed:** 2026-11-22 by inspecting this session's connected Suno tool descriptors, without invoking paid operations. These are **host-specific interface observations**, not a public stable API specification and **not proof that Omega exposes the same tool names or grants**.

Public provider baseline: https://help.suno.com/en/articles/14551425 (official endpoint and authorization, updated 2026-11-18), https://help.suno.com/en/articles/14486145 (plans, credit use, account library). Actual tool discovery and account entitlements must be performed in each agent host.

## GF-style operation selection (read the contract before acting)

| Agent task | Observed connector operation | Requirements / effects / stop condition |
|---|---|---|
| Inspect quota and eligible models | `account_usage` | Read-only; check `allowed_models` and plan. Do not infer grants from global vendor documentation. |
| Generate from a musical brief | `audio_create` | Simple `description` **or** custom `lyrics + style`; incompatible combinations fail. Credit-consuming; Suno sign-in makes two song candidates per call. Explicit authorization first. |
| Create from an original MIDI score | `midi_upload_create`, optionally `midi_upload_complete`, then `audio_create(midi_upload_id)` | Upload must be .mid/.midi <=256 KB containing notes; upload path may require host file transfer. The observed `audio_create` contract uses **Simple Mode and v6-wild** for MIDI, rejects other models, and performs a copyright check before streaming. Do not assume desktop UI's broader model selection applies to this MCP tool. |
| Inspect whether melody survived | `audio_analysis`, `audio_listen`, manual listening | Read-only analysis outputs beat/meter/sections/key/descriptors with asynchronous status; **not** an exact MIDI note-by-note proof. Strong fidelity tests require audio transcription and human review. |
| Transcribe a finished Suno song into MIDI | `audio_midi` | Opposite direction from MIDI input! Observed contract: user-owned finished song, Studio/Premier grant and 10 song credits unless already transcribed; must authorize. |
| Isolate drums or vocals | `audio_stems_create` then `audio_stems_retrieve` | Completed owned clip, `generate.stems` grant. Modes `two` or `twelve`, asynchronous; observed connector charges 10 or 50 credits respectively and returns two takes. Do not pay for 12-part separation if a cheaper method suffices. |
| Generate short rhythmic bridges | `sounds_create` | Short one-shot or loop with key/tempo; paid-eligible signed-in users; two clips per call. Useful candidate but not an instantaneous performance process. |
| Continue an existing musical phrase | `audio_extensions_create` | `continue_at` seconds; extension contains **only the new section**. After completion, use `audio_full_song` for the chain; do not mistake an extension clip for the full song. |
| Recombine two complete takes | `audio_mashups_create` | Two complete accessible parent clips, existing rights/permission and credits. A mashup is not itself a beat-aligned DJ crossfade. |
| Download a file for local mixing | `audio_download` | Returns a user-owned MP3/WAV URL. Probe without `confirm`; if it reports `requires_credit`, require explicit approval before repeating with `confirm: true`. |
| Analyze reusable structure and transitions | `audio_analysis` | Beat positions, meter, BPM, key and sections can guide local transitions; confidence/availability vary. The local mixer owns deterministic beat-accurate execution. |

## Additional observed constraints for an agent

- `audio_create` custom mode does not mix unrestricted `description` with `lyrics/style`. Pass controls only if available; `variety` is integer 0–4, not fractional, while `weirdness` and `style_influence` use 0–1 scales.
- `duration` in `audio_create` targets 15–360 seconds in this interface. Generation/analysis are asynchronous; `streaming`, `complete`, `processing`, `queued`, `error`, `partial` have operation-specific meanings.
- `Max Mode` incurs extra credits; never enable it reflexively. Creator/retry calls may provide idempotency keys; use the same key only for the same immutable request.
- MIDI-upload `upload_url`/fields are temporary credentials. Never log or commit them. Successful score compilation does not establish that the host can upload local bytes through its own tool binding.
- Different authenticated principals expose different grants (suno.com sign-in vs API-key principals). Handle `401/403/402/429` explicitly rather than trying undocumented bypasses.
- Suno `audio_analysis` may return incomplete sections, beat tracks or null key and is not a substitute for a listener's musical evaluation.
- Do not hardcode connector-normalized names as external MCP protocol method names. The real Omega runtime must perform discovery.

## Narrow next experiment

Once M0 authentication has passed, use the original local MIDI fixture from `skills/semantic-midi/`, discover the actual Omega-visible upload/generation operations, compare matched v6-wild MIDI/text conditions **only if that model is actually granted**, retain input/output receipts and listener assessment. No automatic credit spending.

**Status: researched tool interface, not live integration evidence.**
