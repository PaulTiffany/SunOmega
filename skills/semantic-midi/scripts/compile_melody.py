"""Compile an explicitly authored, monophonic semantic score into Standard MIDI.

This is a GF-style narrow helper, not a generative composition model.
Aesthetic intent is human/LLM-authored metadata, NOT secretly interpreted.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from io import BytesIO
import json
from pathlib import Path

PPQN = 480
TONICS = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
          "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
          "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11}
MODES = {"major": (0, 2, 4, 5, 7, 9, 11),
         "natural_minor": (0, 2, 3, 5, 7, 8, 10)}
ROOT_FIELDS = {"schema", "title", "intent", "tonic", "mode", "tempo_bpm",
               "meter", "bars", "phrases", "notes", "constraints"}
NOTE_FIELDS = {"start", "duration", "degree", "octave", "velocity"}
CONSTRAINT_FIELDS = {"first_degree", "last_degree", "max_leap_semitones",
                     "min_total_rest_beats"}


def _fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, str) or len(value) > 15:
        raise ValueError(f"{label} must be a short rational string")
    try:
        val = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{label}: invalid rational number") from exc
    if val.denominator > 96 or val.numerator > 10_000:
        raise ValueError(f"{label}: value outside bounds")
    return val


def _exact_ticks(value: Fraction, label: str) -> int:
    ticks = value * PPQN
    if ticks.denominator != 1:
        raise ValueError(f"{label} is not representable at {PPQN} ticks/quarter")
    return ticks.numerator


def validate_score(score: dict) -> dict:
    """Return exact normalized MIDI events, and reject unsupported/ambiguous input."""
    if not isinstance(score, dict) or set(score) != ROOT_FIELDS:
        raise ValueError("Unsupported or missing top-level fields")
    if score["schema"] != "sunomega.semantic-melody.v0":
        raise ValueError("Unsupported semantic score schema")
    if not isinstance(score["title"], str) or not 1 <= len(score["title"]) <= 100:
        raise ValueError("title must have 1..100 characters")
    if not isinstance(score["intent"], str) or not 1 <= len(score["intent"]) <= 500:
        raise ValueError("intent must be concise human-authored context")
    tonic, mode = score["tonic"], score["mode"]
    if not isinstance(tonic, str) or not isinstance(mode, str) or tonic not in TONICS or mode not in MODES:
        raise ValueError("Unsupported tonic or mode")
    bpm, bars = score["tempo_bpm"], score["bars"]
    if type(bpm) is not int or not 40 <= bpm <= 240:
        raise ValueError("tempo_bpm must be integer 40..240")
    if type(bars) is not int or not 1 <= bars <= 16:
        raise ValueError("bars must be integer 1..16")
    meter = score["meter"]
    if not isinstance(meter, dict) or set(meter) != {"numerator", "denominator"}:
        raise ValueError("meter requires numerator and denominator")
    num, den = meter["numerator"], meter["denominator"]
    if type(num) is not int or not 1 <= num <= 12 or type(den) is not int or den not in (2, 4, 8, 16):
        raise ValueError("Unsupported meter")
    total = Fraction(bars * num * 4, den)
    _exact_ticks(total, "total measure length")
    phrases = score["phrases"]
    if not isinstance(phrases, list) or len(phrases) > 16:
        raise ValueError("phrases must be a bounded list")
    for item in phrases:
        if not isinstance(item, dict) or set(item) != {"name", "start", "end", "intent"}:
            raise ValueError("phrase needs name, start, end, intent")
        if any(not isinstance(item[k], str) or not 1 <= len(item[k]) <= 200 for k in ("name", "intent")):
            raise ValueError("phrase needs short text")
        start, end = _fraction(item["start"], "phrase start"), _fraction(item["end"], "phrase end")
        if not (0 <= start < end <= total):
            raise ValueError("phrase must be contained in score")
        _exact_ticks(start, "phrase start")
        _exact_ticks(end, "phrase end")
    notes = score["notes"]
    if not isinstance(notes, list) or not 1 <= len(notes) <= 128:
        raise ValueError("notes must contain 1..128 events")
    events = []
    for i, note in enumerate(notes):
        if not isinstance(note, dict) or set(note) != NOTE_FIELDS:
            raise ValueError(f"note {i}: unsupported/missing note fields")
        degree, octave, velocity = note["degree"], note["octave"], note["velocity"]
        if type(degree) is not int or not 1 <= degree <= 7:
            raise ValueError(f"note {i}: degree must be 1..7")
        if type(octave) is not int or not 0 <= octave <= 8:
            raise ValueError(f"note {i}: octave must be 0..8")
        if type(velocity) is not int or not 1 <= velocity <= 127:
            raise ValueError(f"note {i}: velocity must be 1..127")
        start = _fraction(note["start"], f"note {i} start")
        duration = _fraction(note["duration"], f"note {i} duration")
        if not (start >= 0 and duration > 0 and start + duration <= total):
            raise ValueError(f"note {i}: time outside score")
        pitch = 12 * (octave + 1) + TONICS[tonic] + MODES[mode][degree - 1]
        if not 0 <= pitch <= 127:
            raise ValueError(f"note {i}: pitch outside MIDI range")
        events.append({"start": _exact_ticks(start, "start"),
                       "end": _exact_ticks(start + duration, "end"),
                       "pitch": pitch, "degree": degree, "velocity": velocity})
    events.sort(key=lambda e: (e["start"], e["end"], e["pitch"]))
    prev_end = 0
    for event in events:
        if event["start"] < prev_end:
            raise ValueError("Monophonic v0 forbids overlapping notes")
        prev_end = event["end"]
    constraints = score["constraints"]
    if not isinstance(constraints, dict) or not set(constraints) <= CONSTRAINT_FIELDS:
        raise ValueError("Unsupported constraints")
    for key in ("first_degree", "last_degree"):
        if key in constraints:
            val = constraints[key]
            if type(val) is not int or not 1 <= val <= 7:
                raise ValueError(f"{key}: expected degree 1..7")
    if events[0]["degree"] != constraints.get("first_degree", events[0]["degree"]):
        raise ValueError("First degree constraint failed")
    if events[-1]["degree"] != constraints.get("last_degree", events[-1]["degree"]):
        raise ValueError("Last degree constraint failed")
    if "max_leap_semitones" in constraints:
        jump = constraints["max_leap_semitones"]
        if type(jump) is not int or not 0 <= jump <= 24:
            raise ValueError("max_leap_semitones must be 0..24")
        if any(abs(a["pitch"] - b["pitch"]) > jump for a, b in zip(events, events[1:])):
            raise ValueError("Maximum leap constraint failed")
    rest = _exact_ticks(total, "total") - sum(e["end"] - e["start"] for e in events)
    if "min_total_rest_beats" in constraints:
        target = _fraction(constraints["min_total_rest_beats"], "min_total_rest_beats")
        if target < 0 or rest < _exact_ticks(target, "min_total_rest_beats"):
            raise ValueError("Minimum total rest constraint failed")
    return {"title": score["title"], "bpm": bpm, "meter": (num, den),
            "bars": bars, "notes": events, "total_ticks": _exact_ticks(total, "total"),
            "silent_ticks": rest}


def make_midi_bytes(normalized: dict) -> bytes:
    """Render validated exact events, using Mido only for MIDI serialization."""
    try:
        from mido import Message, MetaMessage, MidiFile, MidiTrack, bpm2tempo
    except ImportError as exc:
        raise RuntimeError("Install optional MIDI dependency: pip install -e '.[midi]'") from exc
    mid = MidiFile(type=0, ticks_per_beat=PPQN)
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("track_name", name=normalized["title"], time=0))
    track.append(MetaMessage("set_tempo", tempo=bpm2tempo(normalized["bpm"]), time=0))
    num, den = normalized["meter"]
    track.append(MetaMessage("time_signature", numerator=num, denominator=den, time=0))
    scheduled = []
    for event in normalized["notes"]:
        scheduled.append((event["start"], 1, event["pitch"], event["velocity"]))
        scheduled.append((event["end"], 0, event["pitch"], 0))
    prev = 0
    for tick, is_on, pitch, velocity in sorted(scheduled):
        track.append(Message("note_on" if is_on else "note_off",
                             note=pitch, velocity=velocity, time=tick-prev))
        prev = tick
    track.append(MetaMessage("end_of_track", time=normalized["total_ticks"]-prev))
    target = BytesIO()
    mid.save(file=target)
    return target.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an authored semantic melody and optionally export MIDI")
    parser.add_argument("score", type=Path)
    parser.add_argument("--output", type=Path, help="Destination .mid; will not overwrite different bytes")
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        raw = args.score.read_bytes()
        if len(raw) > 64 * 1024:
            raise ValueError("Score exceeds 64 KiB")
        normalized = validate_score(json.loads(raw.decode("utf-8")))
        receipt = {"score_sha256": hashlib.sha256(raw).hexdigest(),
                   "note_count": len(normalized["notes"]),
                   "total_ticks": normalized["total_ticks"],
                   "silent_ticks": normalized["silent_ticks"],
                   "min_pitch": min(x["pitch"] for x in normalized["notes"]),
                   "max_pitch": max(x["pitch"] for x in normalized["notes"])}
        if not args.validate_only:
            if args.output is None or args.output.suffix.lower() != ".mid":
                raise ValueError("Provide --output with a .mid destination or --validate-only")
            payload = make_midi_bytes(normalized)
            if args.output.exists():
                if args.output.read_bytes() != payload:
                    raise ValueError("Output exists with different bytes; refusing overwrite")
            else:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_bytes(payload)
            receipt["midi_sha256"] = hashlib.sha256(payload).hexdigest()
            receipt["midi_path"] = str(args.output)
        print(json.dumps(receipt, indent=2, sort_keys=True))
    except (OSError, ValueError, RuntimeError, UnicodeError, json.JSONDecodeError) as exc:
        parser.exit(1, f"semantic-midi: {exc}\n")


if __name__ == "__main__":
    main()
