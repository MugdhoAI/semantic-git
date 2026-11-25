"""Parse a commit message into its semantic parts.

A semantic commit message has a header shaped like::

    <type>(<scope>): <description>

The scope is optional. A ``!`` before the colon marks a breaking change.
Anything after a blank line following the header is the body.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_HEADER_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)"
    r"(?:\((?P<scope>[^()\n]*)\))?"
    r"(?P<breaking>!)?"
    r": (?P<description>.*)$"
)


@dataclass
class ParsedMessage:
    """The parts of one commit message, plus any syntax problems found."""

    raw: str
    type: str | None = None
    scope: str | None = None
    breaking: bool = False
    description: str | None = None
    body: str = ""
    errors: list[str] = field(default_factory=list)

    @property
    def valid_syntax(self) -> bool:
        """True when the header matched the semantic shape with no problems."""
        return not self.errors


def parse_message(text: str) -> ParsedMessage:
    """Parse one commit message.

    Bad input never raises here. Problems are recorded on the result in
    ``errors`` so the caller can report them.
    """
    message = ParsedMessage(raw=text)
    if not text.strip():
        message.errors.append("message is empty")
        return message

    lines = text.strip("\n").splitlines()
    match = _HEADER_PATTERN.match(lines[0])
    if match is None:
        message.errors.append(
            "header must look like '<type>(<scope>): <description>'"
        )
        return message

    message.type = match.group("type")
    scope = match.group("scope")
    if scope is not None:
        if not scope.strip():
            message.errors.append("scope must not be empty")
        else:
            message.scope = scope.strip()
    message.breaking = match.group("breaking") == "!"

    description = match.group("description")
    if not description.strip():
        message.errors.append("description must not be empty")
    else:
        message.description = description.strip()

    rest = lines[1:]
    while rest and not rest[0].strip():
        rest = rest[1:]
    message.body = "\n".join(rest).strip()
    return message
