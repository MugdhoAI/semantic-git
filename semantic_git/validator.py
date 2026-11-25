"""Validate a parsed commit message against a set of rules."""

from __future__ import annotations

from dataclasses import dataclass

from .parser import ParsedMessage

DEFAULT_TYPES = (
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
)
DEFAULT_MAX_DESCRIPTION_LENGTH = 72


@dataclass(frozen=True)
class Rules:
    """The rules a commit message must follow."""

    allowed_types: tuple[str, ...] = DEFAULT_TYPES
    max_description_length: int = DEFAULT_MAX_DESCRIPTION_LENGTH
    require_scope: bool = False
    allow_breaking: bool = True


@dataclass
class ValidationResult:
    """The outcome of validating one message."""

    passed: bool
    reasons: list[str]


def validate(
    message: ParsedMessage, rules: Rules | None = None
) -> ValidationResult:
    """Check a parsed message against the rules.

    Every failure adds one plain reason, so the caller can print exactly
    what is wrong instead of a bare pass or fail.
    """
    rules = rules or Rules()
    reasons = list(message.errors)
    if message.type is not None and message.type not in rules.allowed_types:
        reasons.append(f"unknown type '{message.type}'")
    if (
        message.description is not None
        and len(message.description) > rules.max_description_length
    ):
        reasons.append(
            f"description is {len(message.description)} characters, "
            f"over the limit of {rules.max_description_length}"
        )
    if rules.require_scope and message.scope is None:
        reasons.append("a scope is required")
    if message.breaking and not rules.allow_breaking:
        reasons.append("breaking change marker '!' is not allowed")
    return ValidationResult(passed=not reasons, reasons=reasons)
