"""Tests for the commit message validator."""

from semantic_git.parser import parse_message
from semantic_git.validator import Rules, validate


def test_valid_message_passes_with_default_rules():
    result = validate(parse_message("feat(parser): add the parser"))
    assert result.passed
    assert result.reasons == []


def test_message_without_scope_passes_by_default():
    result = validate(parse_message("fix: correct the comment range"))
    assert result.passed


def test_unknown_type_fails_and_names_the_type():
    result = validate(parse_message("wip: something in progress"))
    assert not result.passed
    assert result.reasons == ["unknown type 'wip'"]


def test_custom_allowed_types_accept_a_new_type():
    rules = Rules(allowed_types=("feat", "fix", "wip"))
    result = validate(parse_message("wip: something in progress"), rules)
    assert result.passed


def test_description_over_the_limit_fails():
    result = validate(parse_message("feat: " + "x" * 73))
    assert not result.passed
    assert result.reasons == ["description is 73 characters, over the limit of 72"]


def test_description_exactly_at_the_limit_passes():
    result = validate(parse_message("feat: " + "x" * 72))
    assert result.passed


def test_custom_description_limit_is_honoured():
    rules = Rules(max_description_length=10)
    result = validate(parse_message("feat: a longer description"), rules)
    assert not result.passed
    assert result.reasons == ["description is 20 characters, over the limit of 10"]


def test_required_scope_fails_when_missing():
    rules = Rules(require_scope=True)
    result = validate(parse_message("feat: add the parser"), rules)
    assert not result.passed
    assert result.reasons == ["a scope is required"]


def test_required_scope_passes_when_present():
    rules = Rules(require_scope=True)
    result = validate(parse_message("feat(parser): add the parser"), rules)
    assert result.passed


def test_breaking_marker_fails_when_not_allowed():
    rules = Rules(allow_breaking=False)
    result = validate(parse_message("feat!: drop the old format"), rules)
    assert not result.passed
    assert result.reasons == ["breaking change marker '!' is not allowed"]


def test_breaking_marker_passes_by_default():
    result = validate(parse_message("feat!: drop the old format"))
    assert result.passed


def test_syntax_errors_carry_through_as_reasons():
    result = validate(parse_message("just some words"))
    assert not result.passed
    assert result.reasons == [
        "header must look like '<type>(<scope>): <description>'"
    ]


def test_several_failures_are_all_reported():
    rules = Rules(require_scope=True)
    result = validate(parse_message("wip: " + "x" * 73), rules)
    assert not result.passed
    assert result.reasons == [
        "unknown type 'wip'",
        "description is 73 characters, over the limit of 72",
        "a scope is required",
    ]
