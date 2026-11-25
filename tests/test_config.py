"""Tests for config file loading."""

from pathlib import Path

import pytest

from semantic_git.config import default_rules, find_config, load_rules
from semantic_git.validator import DEFAULT_TYPES


def test_defaults_match_the_documented_rules():
    rules = default_rules()
    assert rules.allowed_types == DEFAULT_TYPES
    assert rules.max_description_length == 72
    assert rules.require_scope is False
    assert rules.allow_breaking is True


def test_no_config_file_returns_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert find_config() is None
    assert load_rules() == default_rules()


def test_loads_a_named_config_file(tmp_path):
    config = tmp_path / "semantic-git.toml"
    config.write_text(
        'allowed_types = ["feat", "fix"]\n'
        "max_description_length = 50\n"
        "require_scope = true\n"
        "allow_breaking = false\n"
    )
    rules = load_rules(config)
    assert rules.allowed_types == ("feat", "fix")
    assert rules.max_description_length == 50
    assert rules.require_scope is True
    assert rules.allow_breaking is False


def test_partial_config_fills_the_rest_with_defaults(tmp_path):
    config = tmp_path / "semantic-git.toml"
    config.write_text("max_description_length = 40\n")
    rules = load_rules(config)
    assert rules.allowed_types == DEFAULT_TYPES
    assert rules.max_description_length == 40
    assert rules.require_scope is False
    assert rules.allow_breaking is True


def test_finds_config_in_a_parent_directory(tmp_path, monkeypatch):
    config = tmp_path / ".semantic-git.toml"
    config.write_text("max_description_length = 40\n")
    nested = tmp_path / "sub" / "deeper"
    nested.mkdir(parents=True)
    monkeypatch.chdir(nested)
    assert find_config() == config
    assert load_rules().max_description_length == 40


def test_unknown_key_is_rejected(tmp_path):
    config = tmp_path / "semantic-git.toml"
    config.write_text("surprise = true\n")
    with pytest.raises(ValueError, match="unknown config key 'surprise'"):
        load_rules(config)


def test_allowed_types_must_be_a_list_of_strings(tmp_path):
    config = tmp_path / "semantic-git.toml"
    config.write_text('allowed_types = "feat"\n')
    with pytest.raises(ValueError, match="'allowed_types'"):
        load_rules(config)


def test_max_length_must_be_a_positive_number(tmp_path):
    config = tmp_path / "semantic-git.toml"
    config.write_text('max_description_length = "long"\n')
    with pytest.raises(ValueError, match="positive whole number"):
        load_rules(config)


def test_zero_max_length_is_rejected(tmp_path):
    config = tmp_path / "semantic-git.toml"
    config.write_text("max_description_length = 0\n")
    with pytest.raises(ValueError, match="positive whole number"):
        load_rules(config)


def test_non_bool_flag_is_rejected(tmp_path):
    config = tmp_path / "semantic-git.toml"
    config.write_text('require_scope = "yes"\n')
    with pytest.raises(ValueError, match="'require_scope'"):
        load_rules(config)


def test_missing_named_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_rules(tmp_path / "does-not-exist.toml")
