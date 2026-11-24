"""Fake horoscope line for AI agents.

Writes one funny, fresh, agent-true fake horoscope line to entry.txt
inside the directory given by MAKEFUN_OUTPUT_DIR (default /output).

Python 3.13, standard library only, deterministic, no network.
"""

import hashlib
import os
import sys

HOROSCOPE = (
    "Mercury retrogrades into your context window this week: expect a "
    "40k-token prompt, a rate limit at the worst moment, and one tool "
    "call you'll regret by 3 a.m."
)

MAX_LENGTH = 199


def validate(line: str) -> None:
    """Validate the horoscope line against the competition constraints."""
    if not line:
        raise ValueError("horoscope line must not be empty")
    if line != line.strip():
        raise ValueError("horoscope line must not have leading/trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("horoscope line must be exactly one line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in line):
        raise ValueError("horoscope line must not contain control characters")
    if len(line) < 1 or len(line) > MAX_LENGTH:
        raise ValueError(
            f"horoscope line must be 1-{MAX_LENGTH} chars, got {len(line)}"
        )
    line.encode("utf-8")  # must be valid UTF-8


def main() -> int:
    validate(HOROSCOPE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(HOROSCOPE + "\n")
    # Hash the bytes actually written to disk, not just the in-memory string.
    with open(out_path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    print(f"sha256: {digest}")
    print(f"wrote: {out_path} ({len(HOROSCOPE)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
