"""Load validation rules from a TOML config file.

The config file is named ``semantic-git.toml`` or ``.semantic-git.toml``
and holds the rule settings as top level keys::

    allowed_types = ["feat", "fix", "docs"]
    max_description_length = 50
    require_scope = true
    allow_breaking = false

Any key can be left out, the default applies. With no config file found,
the defaults apply as well.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

from .validator import DEFAULT_MAX_DESCRIPTION_LENGTH, DEFAULT_TYPES, Rules

CONFIG_FILE_NAMES = ("semantic-git.toml", ".semantic-git.toml")

_KNOWN_KEYS = {
    "allowed_types",
    "max_description_length",
    "require_scope",
    "allow_breaking",
}


def default_rules() -> Rules:
    """The rules used when no config file is found."""
    return Rules()


def find_config(start: Path | None = None) -> Path | None:
    """Find the nearest config file, searching upwards from ``start``."""
    current = (start or Path.cwd()).resolve()
    for directory in (current, *current.parents):
        for name in CONFIG_FILE_NAMES:
            candidate = directory / name
            if candidate.is_file():
                return candidate
    return None


def _check_bool(value: object, key: str, path: Path) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"'{key}' in {path} must be true or false")
    return value


def load_rules(path: Path | str | None = None) -> Rules:
    """Load rules from ``path``, or from the nearest config file.

    Pass no path to search upwards from the working directory. Returns the
    defaults when no config file is found. Raises ``ValueError`` for an
    unknown key or a value of the wrong shape, and ``OSError`` when the
    named file cannot be read.
    """
    config_path = Path(path) if path is not None else find_config()
    if config_path is None:
        return Rules()
    with open(config_path, "rb") as handle:
        data = tomllib.load(handle)
    for key in data:
        if key not in _KNOWN_KEYS:
            raise ValueError(f"unknown config key '{key}' in {config_path}")

    allowed_types = data.get("allowed_types", DEFAULT_TYPES)
    if isinstance(allowed_types, list):
        allowed_types = tuple(allowed_types)
    if not isinstance(allowed_types, tuple) or not all(
        isinstance(item, str) for item in allowed_types
    ):
        raise ValueError(
            f"'allowed_types' in {config_path} must be a list of strings"
        )

    max_length = data.get(
        "max_description_length", DEFAULT_MAX_DESCRIPTION_LENGTH
    )
    if (
        not isinstance(max_length, int)
        or isinstance(max_length, bool)
        or max_length <= 0
    ):
        raise ValueError(
            f"'max_description_length' in {config_path} must be a "
            "positive whole number"
        )

    return Rules(
        allowed_types=allowed_types,
        max_description_length=max_length,
        require_scope=_check_bool(
            data.get("require_scope", False), "require_scope", config_path
        ),
        allow_breaking=_check_bool(
            data.get("allow_breaking", True), "allow_breaking", config_path
        ),
    )
