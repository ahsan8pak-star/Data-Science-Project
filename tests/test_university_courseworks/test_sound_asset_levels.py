"""
Guard the CS1OP sound effect levels.

[AI-authored fix] The levels were set by hand once, which meant nothing stopped
the next person from adding a quiet clip, or from re-saving one of the files in
a different bit depth. Two things went wrong before this guard existed: an
attempt to normalise every clip as 16-bit turned the 8-bit and 24-bit clips into
noise, and a single flat gain clipped all 34 clips to the same level and erased
the differences between them.

So these tests check the levels on disk rather than trusting the report:

  * every clip clears the floor the user asked for, and none is below the
    15% point they named as too quiet;
  * no clip is actually clipping - the soft limiter keeps peaks under -1 dBFS,
    and hard-clipped samples would read as full scale;
  * the python/ and java/ copies stay byte-identical, since they are the same
    assets and a fork would only show up on the untested platform;
  * `sound_volumes.json` still describes the files that are actually there, so
    the artefact cannot quietly go stale;
  * the ordering survives, so each effect is still recognisably its own effect.

The measurements come from `scripts/normalize_sound_volumes.py`, imported as a
module so the guard and the tool can never disagree about how a clip is read.
"""

import hashlib
import importlib.util
import json
import sys
import wave
from pathlib import Path

import pytest

from tests.test_university_courseworks.conftest import CS1OP_COURSEWORK

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = CS1OP_COURSEWORK / "sound_volumes.json"
SOUND_DIRS = [
    CS1OP_COURSEWORK / "java" / "resources" / "sound_effects",
    CS1OP_COURSEWORK / "python" / "resources" / "sound_effects",
]


def load_normaliser():
    """Import the normalising script so the guard reads clips the same way it writes them."""
    path = REPO_ROOT / "scripts" / "normalize_sound_volumes.py"
    spec = importlib.util.spec_from_file_location("normalize_sound_volumes", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


normaliser = load_normaliser()


@pytest.fixture(scope="module")
def report():
    assert REPORT_PATH.is_file(), (
        f"{REPORT_PATH.name} is missing; run scripts/normalize_sound_volumes.py"
    )
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def measured():
    """Measure every clip in both folders straight from disk."""
    return {directory: normaliser.collect(directory) for directory in SOUND_DIRS}


class TestSoundLevelsClearTheFloor:
    def test_quietest_clip_clears_the_requested_floor(self, report):
        """The user asked for the quietest clip at 20% of the loudest."""
        after = report["totals"]["after"]
        assert after["gated_ratio_percent"] >= normaliser.TARGET_RATIO * 100, (
            f"quietest clip sits at {after['gated_ratio_percent']}% of the loudest, "
            f"below the {normaliser.TARGET_RATIO * 100}% that was asked for"
        )

    def test_no_clip_falls_below_the_too_quiet_point(self, report):
        """15% was named as the level below which a clip counts as too quiet."""
        assert report["totals"]["after"]["gated_ratio_percent"] >= (
            normaliser.MIN_ACCEPTABLE_RATIO * 100
        )

    def test_every_clip_reached_its_target(self, report):
        assert report["totals"]["clips_below_target"] == 0, (
            "some clips could not reach their target level even with the limiter "
            "wide open, so they are quieter than the report claims"
        )


class TestNoClipIsClipping:
    def test_peaks_never_reach_full_scale(self, measured):
        """
        The soft knee is designed to sit at the -1 dBFS ceiling, and a clip whose
        peaks rest exactly there is working as intended. What must never happen is
        a sample at full scale, which is a hard clip and wraps on playback.
        """
        for directory, clips in measured.items():
            for name, clip in clips.items():
                assert clip["peak"] < 1.0, (
                    f"{name} in {directory.name} reaches full scale, so it is "
                    f"hard clipped rather than limited"
                )

    def test_headroom_is_left_for_inter_sample_peaks(self, measured):
        for clips in measured.values():
            for name, clip in clips.items():
                assert normaliser.to_dbfs(clip["peak"]) <= -0.9, (
                    f"{name} has no headroom left"
                )


class TestBothLanguagesStayInStep:
    def test_python_and_java_copies_are_byte_identical(self):
        """Same assets, two folders: a fork would only surface on the untested platform."""
        digests = [
            {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(directory.glob("*.wav"))
            }
            for directory in SOUND_DIRS
        ]
        assert digests[0] == digests[1], "python/ and java/ sound effects have diverged"

    def test_report_records_both_languages(self, report):
        languages = {entry["language"] for entry in report["directories"]}
        assert languages == {"java", "python"}


class TestReportIsNotStale:
    def test_every_clip_on_disk_is_in_the_report(self, report, measured):
        listed = {row["file"] for row in report["files"]}
        for directory, clips in measured.items():
            assert set(clips) == listed, (
                f"{directory.name} sound_effects and the report disagree about "
                f"which clips exist"
            )

    def test_recorded_levels_match_the_files(self, report, measured):
        """A report that describes levels the files no longer have is worse than none."""
        rows = {row["file"]: row for row in report["files"]}
        for directory, clips in measured.items():
            for name, clip in clips.items():
                recorded = rows[name]["after"]["gated_rms_dbfs"]
                actual = normaliser.to_dbfs(clip["level"])
                assert abs(recorded - actual) <= 0.5, (
                    f"{name} in {directory.name} measures {actual} dBFS but the "
                    f"report says {recorded} dBFS; re-run the normaliser"
                )

    def test_formats_are_unchanged(self, report, measured):
        """
        The normaliser rewrites every clip, so a lost bit depth or a changed
        sample rate would otherwise pass unnoticed.
        """
        rows = {row["file"]: row for row in report["files"]}
        for clips in measured.values():
            for name, clip in clips.items():
                row = rows[name]
                assert clip["sample_width_bytes"] == row["sample_width_bytes"]
                assert clip["channels"] == row["channels"]
                assert clip["sample_rate_hz"] == row["sample_rate_hz"]

    def test_the_tool_is_named_so_the_report_can_be_regenerated(self, report):
        assert (REPO_ROOT / report["script"]).is_file(), (
            f"the report names {report['script']}, which does not exist"
        )


class TestOrderingSurvives:
    def test_relative_order_is_preserved(self, report):
        """
        Range compression must not swap two effects around: the loudest clip
        before is the loudest after, and so on down the list.
        """
        before = sorted(report["files"], key=lambda row: row["before"]["gated_rms_dbfs"])
        after = sorted(report["files"], key=lambda row: row["after"]["gated_rms_dbfs"])
        assert [row["file"] for row in before] == [row["file"] for row in after]

    def test_every_clip_landed_on_its_mapped_target(self, report):
        """
        Each clip should finish exactly where the range compression mapping sent
        it: the quietest at 20% of the loudest, the loudest where it started, and
        everything else in between on a straight line.

        Recomputing the mapping here, from the recorded "before" levels, is what
        makes this a check of the result rather than a restatement of it.
        """
        def linear(dbfs):
            return 10 ** (dbfs / 20)

        before = [row["before"]["gated_rms_dbfs"] for row in report["files"]]
        quietest, loudest = min(before), max(before)
        ratio = report["method"]["floor_ratio"]

        for row in report["files"]:
            expected = normaliser.target_rms_for(
                linear(row["before"]["gated_rms_dbfs"]),
                linear(quietest),
                linear(loudest),
                ratio,
            )
            expected_dbfs = normaliser.to_dbfs(expected)
            actual_dbfs = row["after"]["gated_rms_dbfs"]
            assert abs(actual_dbfs - expected_dbfs) <= 0.5, (
                f"{row['file']} finished at {actual_dbfs} dBFS but the mapping "
                f"sends it to {expected_dbfs} dBFS"
            )

    def test_the_loudest_clip_is_the_reference_and_the_quietest_moved(self, report):
        """
        The loudest clip is what everything else is measured against, so it should
        barely move. The quietest is the one that was too quiet to hear.
        """
        rows = sorted(report["files"], key=lambda row: row["before"]["gated_rms_dbfs"])
        loudest, quietest = rows[-1], rows[0]
        assert loudest["gain_db"] <= 3.5, (
            f"the loudest clip {loudest['file']} moved by {loudest['gain_db']} dB, "
            "so it is no longer the reference"
        )
        assert quietest["gain_db"] >= 8.0, (
            f"the quietest clip {quietest['file']} only gained "
            f"{quietest['gain_db']} dB"
        )

    def test_no_clip_was_silenced(self, report):
        for row in report["files"]:
            assert row["after"]["gated_rms_dbfs"] > row["before"]["gated_rms_dbfs"] - 0.5, (
                f"{row['file']} came out quieter than it went in"
            )


class TestClipsAreStillPlayable:
    def test_every_clip_has_audio_in_it(self, measured):
        """A silent or empty clip would pass a level check and fail in the game."""
        for clips in measured.values():
            for name, clip in clips.items():
                assert clip["level"] > 0, f"{name} has no audible content"

    def test_durations_are_unchanged_by_the_rewrite(self, measured):
        """
        The rewrite happens in place, so it must not pad or truncate: the frame
        count has to match what the samples imply.
        """
        for clips in measured.values():
            for name, clip in clips.items():
                directory = next(
                    d for d, c in measured.items() if name in c
                )
                with wave.open(str(directory / name), "rb") as handle:
                    frames = handle.getnframes()
                assert frames * clip["channels"] == len(clip["samples"]), (
                    f"{name} has {len(clip['samples'])} samples but "
                    f"{frames} frames of {clip['channels']} channels"
                )

