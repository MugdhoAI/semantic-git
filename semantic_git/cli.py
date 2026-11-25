"""Command line entry point: ``semantic-git check <message>``."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .config import load_rules
from .parser import parse_message
from .validator import validate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="semantic-git",
        description="Validate commit messages against the semantic format.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser(
        "check", help="validate one commit message"
    )
    check.add_argument("message", help="the commit message to validate")
    check.add_argument(
        "--config",
        type=Path,
        default=None,
        help="path to a semantic-git.toml config file",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI. Returns 0 for a pass, 1 for a fail, 2 for a usage error."""
    args = build_parser().parse_args(argv)
    if args.command == "check":
        try:
            rules = load_rules(args.config)
        except (OSError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        result = validate(parse_message(args.message), rules)
        if result.passed:
            print(f"PASS: {args.message}")
            return 0
        print(f"FAIL: {args.message}")
        for reason in result.reasons:
            print(f"  - {reason}")
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
