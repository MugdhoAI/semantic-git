"""Tests for the semantic-git check command."""

import subprocess
import sys

import pytest

from semantic_git.cli import main


def test_valid_message_passes_with_exit_zero(capsys):
    assert main(["check", "feat(parser): add the parser"]) == 0
    assert capsys.readouterr().out == "PASS: feat(parser): add the parser\n"


def test_invalid_message_fails_with_exit_one_and_reasons(capsys):
    assert main(["check", "random words"]) == 1
    assert capsys.readouterr().out == (
        "FAIL: random words\n"
        "  - header must look like '<type>(<scope>): <description>'\n"
    )


def test_unknown_type_is_reported(capsys):
    assert main(["check", "wip: something"]) == 1
    assert capsys.readouterr().out == (
        "FAIL: wip: something\n  - unknown type 'wip'\n"
    )


def test_config_flag_changes_the_rules(tmp_path, capsys):
    config = tmp_path / "semantic-git.toml"
    config.write_text('allowed_types = ["feat"]\n')
    assert main(["check", "fix: correct a bug", "--config", str(config)]) == 1
    assert "unknown type 'fix'" in capsys.readouterr().out
    assert main(["check", "feat: add a feature", "--config", str(config)]) == 0


def test_missing_config_file_is_a_usage_error(capsys):
    assert main(["check", "feat: add it", "--config", "no-such.toml"]) == 2
    assert "error:" in capsys.readouterr().err


def test_bad_config_is_a_usage_error(tmp_path, capsys):
    config = tmp_path / "semantic-git.toml"
    config.write_text("surprise = true\n")
    assert main(["check", "feat: add it", "--config", str(config)]) == 2
    assert "unknown config key 'surprise'" in capsys.readouterr().err


def test_missing_message_is_a_usage_error():
    with pytest.raises(SystemExit) as excinfo:
        main(["check"])
    assert excinfo.value.code == 2


def test_module_entry_point_reports_a_pass():
    result = subprocess.run(
        [sys.executable, "-m", "semantic_git", "check", "fix: correct a bug"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert result.stdout == "PASS: fix: correct a bug\n"
