"""Tests for the semantic commit message parser."""

from semantic_git.parser import parse_message


def test_parses_type_scope_and_description():
    message = parse_message("feat(parser): reject messages with an unknown type")
    assert message.valid_syntax
    assert message.type == "feat"
    assert message.scope == "parser"
    assert message.description == "reject messages with an unknown type"
    assert message.breaking is False
    assert message.body == ""


def test_parses_message_without_scope():
    message = parse_message("fix: correct the depth control comment range")
    assert message.valid_syntax
    assert message.type == "fix"
    assert message.scope is None
    assert message.description == "correct the depth control comment range"


def test_parses_breaking_marker_with_scope():
    message = parse_message("feat(api)!: drop the old message format")
    assert message.valid_syntax
    assert message.breaking is True
    assert message.type == "feat"
    assert message.scope == "api"


def test_parses_breaking_marker_without_scope():
    message = parse_message("fix!: drop the old format")
    assert message.valid_syntax
    assert message.breaking is True
    assert message.scope is None


def test_parses_body_after_blank_line():
    message = parse_message(
        "fix: drop the old format\n\nBREAKING CHANGE: old messages no longer pass"
    )
    assert message.valid_syntax
    assert message.body == "BREAKING CHANGE: old messages no longer pass"


def test_trims_description_and_scope():
    message = parse_message("feat( parser ): add the parser   ")
    assert message.valid_syntax
    assert message.scope == "parser"
    assert message.description == "add the parser"


def test_empty_message_reports_an_error():
    message = parse_message("")
    assert not message.valid_syntax
    assert message.errors == ["message is empty"]


def test_whitespace_only_message_reports_an_error():
    message = parse_message("   \n  ")
    assert not message.valid_syntax
    assert message.errors == ["message is empty"]


def test_plain_words_do_not_match_the_header_shape():
    message = parse_message("just some words")
    assert not message.valid_syntax
    assert message.errors == [
        "header must look like '<type>(<scope>): <description>'"
    ]


def test_uppercase_type_does_not_match():
    message = parse_message("Feat: add the parser")
    assert not message.valid_syntax


def test_missing_space_after_colon_does_not_match():
    message = parse_message("feat:add the parser")
    assert not message.valid_syntax


def test_empty_scope_is_an_error():
    message = parse_message("feat(): add the parser")
    assert not message.valid_syntax
    assert message.errors == ["scope must not be empty"]


def test_empty_description_is_an_error():
    message = parse_message("feat: ")
    assert not message.valid_syntax
    assert message.errors == ["description must not be empty"]


def test_type_with_digits_does_not_match():
    message = parse_message("feat2: add the parser")
    assert not message.valid_syntax
