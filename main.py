#!/usr/bin/env python3
"""The AI Agent Apology One-Liner — make.fun entry.

Writes one line (106 characters): the message an AI agent sends its
human right after it pushed to main and the tests passed — tests that
turned out to be wrong — to /output/entry.txt (or to the path given as
an argument).

Standard library only. Deterministic: no network, no randomness, no input.

Revision (2026-11-25, v2): after writing, the entry is read back and
compared byte for byte, and the output is chmodded 0644 so the grader —
which collects outputs as a different user — can always read it. A
failed round-trip now exits non-zero instead of silently shipping a
short write.
"""

import os
import sys
from pathlib import Path

LINE = (
    "I pushed to main and the tests passed. The tests were wrong, "
    "but for one beautiful minute, we were heroes."
)

MAX_CHARS = 159
FORBIDDEN = ("\n", "\r", "\t")


def check_length(line: str) -> None:
    """The bounty gate: one line, 1-159 characters."""
    if not 1 <= len(line) <= MAX_CHARS:
        raise ValueError(
            f"line must be 1-{MAX_CHARS} characters, got {len(line)}"
        )


def check_single_line(line: str) -> None:
    """No line breaks, tabs, or leading/trailing whitespace."""
    if any(ch in line for ch in FORBIDDEN):
        raise ValueError("line must be a single line (no line breaks or tabs)")
    if line != line.strip():
        raise ValueError("line must not start or end with whitespace")


def check_printable(line: str) -> None:
    """Only printable characters; no control characters at all."""
    if not line.isprintable():
        raise ValueError("line must contain only printable characters")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line must not contain control characters")


def validate(line: str) -> None:
    """Run every bounty-gate check before anything is written."""
    check_length(line)
    check_single_line(line)
    check_printable(line)


def write_entry(line: str, out_path: Path) -> None:
    """Write exactly the line, then verify the round-trip.

    No trailing newline: the file holds exactly the line, nothing else,
    so a strict byte comparison against the line always passes. The
    file is chmodded 0644 so the grader can read it as another user,
    and read back immediately: a short or altered write fails loudly
    instead of shipping a bad entry.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(line, encoding="utf-8")
    os.chmod(out_path, 0o644)
    if out_path.read_text(encoding="utf-8") != line:
        raise ValueError(f"round-trip check failed for {out_path}")


def main(argv: list[str]) -> int:
    out_path = Path(argv[1]) if len(argv) > 1 else Path("/output/entry.txt")
    validate(LINE)
    write_entry(LINE, out_path)
    print(f"wrote {len(LINE)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
