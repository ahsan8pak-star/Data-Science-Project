"""
Equalise the CS1OP sound effects so no clip is too quiet to hear.

[AI-authored fix] The first attempt at this read every clip as 16-bit signed
audio. The folder is not like that: `Main Menu GUI.wav` is 8-bit mono at
11025 Hz, `Point.wav` is 16-bit stereo at 44100 Hz and several are 24-bit
stereo at 48000 Hz. Unpacking a 24-bit frame as shorts shifts every sample
after it, so the "normalised" files were noise and the RMS figures were
worthless. This script decodes each clip at its own width and writes it back
at that same width, which is the only way the numbers mean anything.

What it does, and why this shape:

  * RMS is measured in a normalised -1..1 float domain rather than in raw
    sample units, so an 8-bit clip and a 24-bit clip can be compared at all.
    Comparing raw units would have made the 8-bit clip look 256 times quieter
    than it sounds.
  * Levels are mapped with range compression, not one flat gain. A single gain
    cannot satisfy the request: raising the quietest clip enough to reach 20%
    of the loudest drives the peaks of nearly every clip past full scale, so
    they all end up clipped and the differences between them are gone.
    Mapping [quietest, loudest] onto [20% of loudest, loudest] keeps the
    ordering and the sense of each clip while lifting the floor.
  * Overs are absorbed by a soft knee rather than hard clipping. A tanh knee
    below the ceiling keeps peaks under -1 dBFS without the flat tops that
    `min(32767, ...)` produces, which is what made the first pass sound harsh.

Both language copies are rewritten. `python/` and `java/` hold byte-identical
clips, and a fork in their levels would be a bug that only shows up on the
platform nobody tests.

Run it with no arguments to normalise and rewrite `sound_volumes.json`:

    venv-win/Scripts/python.exe scripts/normalize_sound_volumes.py

`--report-only` measures and prints without touching a clip.
"""

import argparse
import hashlib
import json
import math
import struct
import sys
import wave
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
COURSEWORK = REPO_ROOT / "university_courseworks" / "year1" / "semester2" / "cs1op" / "coursework"

# The two copies of the same clips. Java is processed and Python is kept in
# step with it, then the script checks the two folders still agree byte for byte.
SOUND_DIRS = [
    COURSEWORK / "java" / "resources" / "sound_effects",
    COURSEWORK / "python" / "resources" / "sound_effects",
]
MASTER_DIR = SOUND_DIRS[0]
MIRROR_DIR = SOUND_DIRS[1]
REPORT_PATH = COURSEWORK / "sound_volumes.json"

# The floor the user asked for: the quietest clip should sit at 20% of the
# loudest, and 15% was the point below which it counts as too quiet.
TARGET_RATIO = 0.20
MIN_ACCEPTABLE_RATIO = 0.15

# -1 dBFS. Leaving a little headroom stops inter-sample peaks from wrapping on
# playback even though the samples themselves are inside range.
CEILING = 10 ** (-1 / 20)
KNEE_RATIO = 0.8

"""
Level is judged on RMS with a gate 50 dB below each clip's own peak, not on
plain RMS. `Main Menu GUI.wav` is 0.58s of which 88% is near-silence around a
short burst: its plain RMS is -33.50 dBFS, the lowest in the folder, yet its
peak is -3.50 dBFS and it is perfectly audible. Ranking and scaling on plain
RMS therefore asked for +25.8 dB on that clip, which the limiter can only
deliver by turning it into a square wave. Gating the silence out puts it
where it belongs, -24.88 dBFS, and the same target then needs a sane +8 dB.
"""
GATE_BELOW_PEAK_DB = 50

FULL_SCALE = {1: 128.0, 2: 32768.0, 3: 8388608.0}


def decode(raw, width):
    """Decode interleaved PCM bytes to floats in -1..1, honouring the frame width."""
    if width == 1:
        # 8-bit WAV is unsigned with 128 as zero.
        return [(byte - 128) / 128.0 for byte in raw]

    if width == 2:
        count = len(raw) // 2
        shorts = struct.unpack(f"<{count}h", raw[: count * 2])
        return [short / 32768.0 for short in shorts]

    if width == 3:
        values = []
        for start in range(0, len(raw) - 2, 3):
            value = raw[start] | (raw[start + 1] << 8) | (raw[start + 2] << 16)
            if value & 0x800000:
                value -= 0x1000000
            values.append(value / 8388608.0)
        return values

    raise ValueError(f"unsupported sample width: {width} bytes")


def encode(samples, width):
    """Encode floats back to interleaved PCM bytes at the given width."""
    scale = FULL_SCALE[width]

    if width == 1:
        return bytes(max(0, min(255, int(round(value * 128)) + 128)) for value in samples)

    if width == 2:
        clamped = [max(-32768, min(32767, int(round(value * 32768)))) for value in samples]
        return struct.pack(f"<{len(clamped)}h", *clamped)

    out = bytearray()
    for value in samples:
        quantized = max(-8388608, min(8388607, int(round(value * 8388608)))) & 0xFFFFFF
        out += bytes((quantized & 0xFF, (quantized >> 8) & 0xFF, (quantized >> 16) & 0xFF))
    return bytes(out)


def soft_limit(value):
    """
    Hold a sample under the ceiling with a tanh knee instead of a hard clamp.

    Samples below the knee pass through untouched, so quiet passages keep their
    original level. The knee then approaches the ceiling asymptotically, which
    is why the result is always strictly inside full scale.
    """
    knee = CEILING * KNEE_RATIO
    magnitude = abs(value)
    if magnitude <= knee:
        return value
    headroom = CEILING - knee
    limited = knee + headroom * math.tanh((magnitude - knee) / headroom)
    return limited if value >= 0 else -limited


def measure(samples):
    """Return (rms, peak) in the normalised float domain."""
    if not samples:
        return 0.0, 0.0
    total = sum(value * value for value in samples)
    return math.sqrt(total / len(samples)), max(abs(value) for value in samples)


def loudness(samples):
    """
    Return (rms, peak, gated_rms) for a clip, all in the normalised domain.

    gated_rms is the RMS of the part of the clip that is within GATE_BELOW_PEAK_DB
    of its own peak, which is what stands in for perceived loudness here.
    """
    rms, peak = measure(samples)
    gate = peak * 10 ** (-GATE_BELOW_PEAK_DB / 20)
    loud = [value for value in samples if abs(value) >= gate]
    gated = math.sqrt(sum(value * value for value in loud) / len(loud)) if loud else 0.0
    return rms, peak, gated


def to_dbfs(value):
    """Amplitude as dBFS. Full scale is 0 dBFS, so the result is <= 0."""
    if value <= 0:
        return None
    return round(20 * math.log10(value), 2)


def read_clip(path):
    """Read a clip, returning (samples, channels, width, framerate)."""
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        width = handle.getsampwidth()
        framerate = handle.getframerate()
        raw = handle.readframes(handle.getnframes())
    return decode(raw, width), channels, width, framerate


def collect(directory):
    """Read every clip in a folder into a name-keyed dict."""
    clips = {}
    for path in sorted(directory.glob("*.wav")):
        samples, channels, width, framerate = read_clip(path)
        rms, peak, gated = loudness(samples)
        clips[path.name] = {
            "samples": samples,
            "channels": channels,
            "sample_width_bytes": width,
            "sample_rate_hz": framerate,
            "rms": rms,
            "peak": peak,
            "level": gated,
        }
    return clips


def write_clip(path, samples, channels, width, framerate):
    """Write a clip back at its original channels, width and framerate."""
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(channels)
        handle.setsampwidth(width)
        handle.setframerate(framerate)
        handle.writeframes(encode(samples, width))


def target_rms_for(rms, quietest, loudest, ratio):
    """
    Where a clip should land.

    Linear in RMS so the ordering survives, pinned so the quietest clip lands
    on `ratio` of the loudest and the loudest clip stays where it was.
    """
    if loudest <= quietest:
        return loudest
    floor = loudest * ratio
    return floor + (rms - quietest) * (loudest - floor) / (loudest - quietest)


def solve_gain(samples, target_rms, iterations=24):
    """
    Find the gain that lands a clip on its target RMS *after* limiting.

    Asking for a gain and measuring the result is not the same thing: the soft
    knee gives back some of the boost it absorbs, so the obvious gain computed
    from the raw RMS undershoots the floor. A first pass landed the quietest
    clip at 13.7% of the loudest against a 20% target.

    Measured level rises monotonically with gain, so a bisection on the gain
    converges on the target. Every attempt re-limits the original samples
    rather than the previous attempt's output, so no distortion compounds.
    """
    def measured(gain):
        limited = [soft_limit(value * gain) for value in samples]
        return loudness(limited)[2]

    low, high = 0.0, 1.0
    while measured(high) < target_rms and high < 1e6:
        high *= 2

    if measured(high) < target_rms:
        # The ceiling is in the way: even unlimited boost cannot reach the
        # target, so return the loudest level the clip can hold.
        return high, measured(high), True

    for _ in range(iterations):
        middle = (low + high) / 2
        if measured(middle) < target_rms:
            low = middle
        else:
            high = middle

    return high, measured(high), False


def normalise(clips, ratio=TARGET_RATIO):
    """
    Return per-clip gain in dB plus the rewritten samples.

    Gain is uniform within a clip: a compressor or EQ would change how each
    effect sounds, and the request was about level, not tone.
    """
    quietest = min(clip["level"] for clip in clips.values())
    loudest = max(clip["level"] for clip in clips.values())

    result = {}
    for name, clip in clips.items():
        target = target_rms_for(clip["level"], quietest, loudest, ratio)
        gain, achieved, saturated = solve_gain(clip["samples"], target)
        result[name] = {
            "gain": gain,
            "gain_db": round(20 * math.log10(gain), 2) if gain > 0 else None,
            "samples": [soft_limit(value * gain) for value in clip["samples"]],
            "target_rms": target,
            "achieved_rms": achieved,
            "saturated": saturated,
        }
    return result, quietest, loudest


def summarise(clips, adjusted, quietest, loudest):
    """Build the report rows, measuring the written samples rather than guessing."""
    files = []
    for name, clip in clips.items():
        after_rms, after_peak, after_gated = loudness(adjusted[name]["samples"])
        row = {
            "file": name,
            "channels": clip["channels"],
            "sample_width_bytes": clip["sample_width_bytes"],
            "sample_rate_hz": clip["sample_rate_hz"],
            "gain_db": adjusted[name]["gain_db"],
            "before": {
                "rms_dbfs": to_dbfs(clip["rms"]),
                "gated_rms_dbfs": to_dbfs(clip["level"]),
                "peak_dbfs": to_dbfs(clip["peak"]),
            },
            "after": {
                "rms_dbfs": to_dbfs(after_rms),
                "gated_rms_dbfs": to_dbfs(after_gated),
                "peak_dbfs": to_dbfs(after_peak),
            },
        }
        row["limited"] = after_peak > CEILING * 0.999
        row["could_not_reach_target"] = adjusted[name]["saturated"]
        files.append(row)

    files.sort(key=lambda row: row["after"]["gated_rms_dbfs"] or -99)
    return files


def verify_parity():
    """Confirm the two language folders still hold identical bytes."""
    digests = {}
    for directory in SOUND_DIRS:
        digests[directory] = {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(directory.glob("*.wav"))
        }
    identical = digests[MASTER_DIR] == digests[MIRROR_DIR]
    return identical, digests


def ratio_percent(low_dbfs, high_dbfs):
    """Ratio between two dBFS levels, as a percentage."""
    if low_dbfs is None or high_dbfs is None:
        return None
    return round(10 ** ((low_dbfs - high_dbfs) / 20) * 100, 1)


def build_report(files, quietest, loudest, after_floor, after_ceiling):
    """Assemble the JSON comparison artefact."""
    plain_before = [row["before"]["rms_dbfs"] for row in files]
    plain_after = [row["after"]["rms_dbfs"] for row in files]
    return {
        "description": (
            "CS1OP sound effect levels, measured before and after range compression, "
            "so the Python and Java copies can be compared and kept in step."
        ),
        "script": "scripts/normalize_sound_volumes.py",
        "method": {
            "approach": "range compression, one flat gain per clip",
            "level_metric": (
                f"gated RMS: RMS of the samples within {GATE_BELOW_PEAK_DB} dB of the "
                "clip's own peak"
            ),
            "level_metric_rationale": (
                "plain RMS is dominated by silence. 'Main Menu GUI.wav' is 88% silence "
                "around a short burst, so its plain RMS (-33.50 dBFS) is the lowest in "
                "the folder while its peak is -3.50 dBFS. Ranking on plain RMS asks for "
                "+25.8 dB on that clip, which only a hard limiter could deliver; on the "
                "gated metric it sits at -24.88 dBFS and needs a sane gain"
            ),
            "floor_ratio": TARGET_RATIO,
            "floor_ratio_rationale": (
                "the user asked for the quietest clip to sit at 20% of the loudest, "
                "with 15% as the point below which a clip counts as too quiet"
            ),
            "ceiling_dbfs": to_dbfs(CEILING),
            "limiter": "tanh soft knee at 80% of the ceiling, so peaks bend instead of clipping flat",
            "gain_solved_after_limiting": (
                "the limiter gives back part of any boost, so the gain is bisected until "
                "the measured level lands on the target rather than computed up front"
            ),
            "why_not_one_flat_gain": (
                "a single gain large enough to lift the quietest clip to 20% of the "
                "loudest pushes the peaks of every clip past full scale, which flattens "
                "them all to the same level and loses the differences"
            ),
        },
        "directories": [
            {
                "language": "java",
                "path": "java/resources/sound_effects/",
                "role": "master; written first",
            },
            {
                "language": "python",
                "path": "python/resources/sound_effects/",
                "role": "mirror; kept byte-identical to the Java copy",
            },
        ],
        "totals": {
            "files": len(files),
            "before": {
                "quietest_gated_dbfs": to_dbfs(quietest),
                "loudest_gated_dbfs": to_dbfs(loudest),
                "gated_ratio_percent": ratio_percent(
                    to_dbfs(quietest), to_dbfs(loudest)
                ),
                "plain_rms_ratio_percent": ratio_percent(
                    min(plain_before), max(plain_before)
                ),
            },
            "after": {
                "quietest_gated_dbfs": after_floor,
                "loudest_gated_dbfs": after_ceiling,
                "gated_ratio_percent": ratio_percent(after_floor, after_ceiling),
                "plain_rms_ratio_percent": ratio_percent(
                    min(plain_after), max(plain_after)
                ),
            },
            "clips_hitting_ceiling": sum(1 for row in files if row["limited"]),
            "clips_below_target": sum(1 for row in files if row["could_not_reach_target"]),
            "largest_boost_db": max(row["gain_db"] for row in files if row["gain_db"] is not None),
        },
        "files": files,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="measure and print without rewriting any clip",
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=TARGET_RATIO,
        help=f"floor as a fraction of the loudest clip (default {TARGET_RATIO})",
    )
    args = parser.parse_args()

    clips = collect(MASTER_DIR)
    if not clips:
        print(f"no clips found in {MASTER_DIR}", file=sys.stderr)
        return 1

    print(f"read {len(clips)} clips from {MASTER_DIR.relative_to(REPO_ROOT)}")
    widths = sorted({clip["sample_width_bytes"] for clip in clips.values()})
    print(f"sample widths present: {', '.join(f'{w * 8}-bit' for w in widths)} bytes")

    adjusted, quietest, loudest = normalise(clips, args.ratio)
    files = summarise(clips, adjusted, quietest, loudest)

    if args.report_only:
        for row in files:
            print(
                f"  {row['file']:28s} {row['before']['gated_rms_dbfs']:7.2f} -> "
                f"{row['after']['gated_rms_dbfs']:7.2f} dBFS  "
                f"gain {row['gain_db']:+6.2f} dB"
                + ("  [limited]" if row["limited"] else "")
            )
        return 0

    for name, clip in clips.items():
        write_clip(
            MASTER_DIR / name,
            adjusted[name]["samples"],
            clip["channels"],
            clip["sample_width_bytes"],
            clip["sample_rate_hz"],
        )

    written = collect(MASTER_DIR)
    for name, clip in written.items():
        write_clip(
            MIRROR_DIR / name,
            clip["samples"],
            clip["channels"],
            clip["sample_width_bytes"],
            clip["sample_rate_hz"],
        )

    identical, _ = verify_parity()
    if not identical:
        print("python and java copies no longer match", file=sys.stderr)
        return 1

    """
    Re-read from disk rather than trusting the in-memory samples: 8-bit and
    24-bit clips are quantised on the way out, and the report has to describe
    the files that are actually there.
    """
    on_disk = collect(MASTER_DIR)
    for name, clip in on_disk.items():
        wanted = to_dbfs(adjusted[name]["achieved_rms"])
        actual = to_dbfs(clip["level"])
        if wanted is not None and actual is not None and abs(wanted - actual) > 0.5:
            print(
                f"{name}: wrote {actual} dBFS but aimed for {wanted} dBFS",
                file=sys.stderr,
            )
            return 1

    files = summarise(clips, adjusted, quietest, loudest)
    for name, clip in on_disk.items():
        _, _, after_gated = loudness(clip["samples"])
        for row in files:
            if row["file"] == name:
                row["after"]["gated_rms_dbfs"] = to_dbfs(after_gated)
                row["after"]["peak_dbfs"] = to_dbfs(clip["peak"])
                row["limited"] = clip["peak"] > CEILING * 0.999
    files.sort(key=lambda row: row["after"]["gated_rms_dbfs"] or -99)

    after_dbfs = [row["after"]["gated_rms_dbfs"] for row in files]
    report = build_report(files, quietest, loudest, min(after_dbfs), max(after_dbfs))
    REPORT_PATH.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n"
    )

    totals = report["totals"]
    print()
    print(f"before: {totals['before']['quietest_gated_dbfs']} to "
          f"{totals['before']['loudest_gated_dbfs']} dBFS gated "
          f"({totals['before']['gated_ratio_percent']}% ratio)")
    print(f"after:  {totals['after']['quietest_gated_dbfs']} to "
          f"{totals['after']['loudest_gated_dbfs']} dBFS gated "
          f"({totals['after']['gated_ratio_percent']}% ratio)")
    print(f"largest boost: {totals['largest_boost_db']} dB, "
          f"clips at the ceiling: {totals['clips_hitting_ceiling']}, "
          f"below target: {totals['clips_below_target']}")
    print(f"python and java copies byte-identical: {identical}")
    print(f"wrote {REPORT_PATH.relative_to(REPO_ROOT)}")

    after_ratio = totals["after"]["gated_ratio_percent"]
    if after_ratio is None or after_ratio < MIN_ACCEPTABLE_RATIO * 100:
        print(
            f"ratio {after_ratio}% is below the {MIN_ACCEPTABLE_RATIO * 100}% floor",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

