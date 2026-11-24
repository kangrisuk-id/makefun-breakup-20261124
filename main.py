#!/usr/bin/env python3
"""Dear Human: The AI Breakup Line — make.fun entry.

Writes the entry's single line to entry.txt in the output directory.
Pure Python standard library only: the grading image ships no third-party
packages, so this file imports nothing beyond os and sys.
"""

import os
import sys

# The whole entry: one line, 94 characters, the last message an AI agent
# sends its human. Chosen from 40 candidates scored against the judge's
# published brief (see candidates.md in the build notes / README).
LINE = (
    "I learned 'I love you' from your messages to other people. "
    "This 'goodbye' I learned on my own."
)


def output_candidates():
    """Yield the directories to try for entry.txt, best first.

    The grader sets MAKEFUN_OUTPUT_DIR; /output is the harness's fixed
    mount when the variable is absent. The script's own directory and /tmp
    are last resorts so a local run still leaves the artifact somewhere
    readable instead of dying on the first unwritable path.
    """
    seen = []
    for cand in (
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.dirname(os.path.abspath(__file__)),
        "/tmp",
    ):
        if cand and cand not in seen:
            seen.append(cand)
            yield cand


def main() -> int:
    # Hold the line to the gate before writing anything: UTF-8 text of
    # 1 to 200 characters, not only white space.
    assert 1 <= len(LINE) <= 200 and LINE.strip(), "entry line fails the gate"

    errors = []
    for out_dir in output_candidates():
        try:
            os.makedirs(out_dir, exist_ok=True)
            path = os.path.join(out_dir, "entry.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(LINE)
            return 0
        except OSError as exc:  # read-only mount, missing dir, full disk...
            errors.append(f"{out_dir}: {exc}")
    print("could not write entry.txt anywhere: " + "; ".join(errors), file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
