# semantic-git

semantic-git is a planned command line tool that helps developers write and validate commit messages that follow semantic commit structure, often called conventional commits.

## The problem

Commit messages are the permanent record of why a change was made, but they are often written in a hurry. Inconsistent messages make a repository history hard to scan, hard to search, and hard to reuse for release notes or changelogs. A small amount of structure, applied consistently, makes that history far easier to read and to automate around.

## What semantic structure means here

A semantic commit message has a type, an optional scope, and a short description:

```
<type>(<scope>): <description>
```

Common types include feat, fix, docs, refactor, test, and chore. The scope names the part of the project the change touches. The description is a short summary of the change.

Example:

```
feat(parser): reject messages with an unknown type
```

## Usage

The first working version is implemented. Install it in editable mode,
then validate one commit message at a time:

```
pip install -e .
semantic-git check "feat(parser): reject messages with an unknown type"
```

A message that follows the rules prints `PASS` and exits with status 0.
A message that breaks the rules prints `FAIL`, one reason per problem,
and exits with status 1. You can also run it without installing:

```
python -m semantic_git check "fix: correct the comment range"
```

These commands are still planned, not built yet:

- `semantic-git check --range <range>`: validate every commit message in a range of git history.
- `semantic-git init`: write a starter configuration file that sets the allowed types, scopes, and description length limits for a repository.
- A git hook mode, where validation runs automatically when a commit is created and blocks messages that do not follow the configured rules.

## Configuration

Rules live in `semantic-git.toml` (or `.semantic-git.toml`) in the
repository root or any parent directory. Every key is optional:

```toml
allowed_types = ["feat", "fix", "docs"]
max_description_length = 50
require_scope = true
allow_breaking = false
```

The defaults are the eleven common types (feat, fix, docs, style,
refactor, perf, test, build, ci, chore, revert), a description limit of
72 characters, no required scope, and breaking changes allowed. Pass a
different file with `semantic-git check --config path/to/config.toml`.

## First scope

The first working version now:

- Validates one commit message at a time against the semantic format.
- Checks the type against a configurable list of allowed types.
- Checks that a description is present and within a configurable length limit.
- Prints a clear pass or fail result, with a specific reason for each failure.
- Reads its rules from a simple configuration file.

The first working version does not:

- Rewrite or fix commit messages automatically.
- Generate changelogs or release notes.
- Integrate with hosting platforms or CI services.
- Support plugins or custom validation rules written as code.

## Development

Run the test suite with pytest:

```
pytest
```

## Status

The first working version is done: `semantic-git check` validates one
message against configurable rules, and the rules load from a TOML config
file. The remaining planned work is range checking, the `init` command,
and the git hook mode.
