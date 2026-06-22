#!/usr/bin/env python3
"""Cursor stop hook — disabled.

Automation no longer auto-chains milestones. Build one milestone per Agent
session, then stop and review before starting the next.

To build the next milestone manually, say in Agent mode:

  Build Milestone N from BUILD_PROMPT.md

To open a PR when all milestones are done:

  Commit my changes, push to a new branch, and open a PR
"""

from __future__ import annotations

import sys


def main() -> int:
    if not sys.stdin.isatty():
        sys.stdin.read()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
