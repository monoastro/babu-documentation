"""
Run every suite in this directory.

The project has no pytest dependency, and adding one for four files that need
nothing beyond ``assert`` would not earn its place in requirements.txt. Each
suite is an ordinary script; this runner is the ``&&`` chain, written once.

    .venv/bin/python tests/run_all.py

Exit status is 0 only if every suite passed, so it works as a CI gate.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent


def main() -> int:
    suites = sorted(p for p in TESTS_DIR.glob("test_*.py"))
    if not suites:
        print("no suites found", file=sys.stderr)
        return 1

    failed: list[str] = []
    for suite in suites:
        # Same interpreter as this runner. A bare "python" would resolve
        # through PATH to a shim without this project's dependencies.
        completed = subprocess.run(
            [sys.executable, str(suite)],
            cwd=TESTS_DIR.parent,
            capture_output=True,
            text=True,
        )
        summary = [
            line
            for line in completed.stdout.splitlines()
            if line.startswith("FAIL") or "passed" in line
        ]
        status = "PASS" if completed.returncode == 0 else "FAIL"
        print(f"{status}  {suite.name}: {'; '.join(summary) or 'no output'}")
        if completed.returncode != 0:
            failed.append(suite.name)
            # Only failures get their detail printed — a passing run should be
            # four lines, not four screens.
            for line in completed.stdout.splitlines():
                if line.startswith("FAIL"):
                    print(f"      {line}")
            if completed.stderr.strip():
                print(f"      stderr: {completed.stderr.strip()[-500:]}")

    print(f"\n{len(suites) - len(failed)}/{len(suites)} suites passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
