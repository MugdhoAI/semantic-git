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

## Planned usage

Nothing in this section exists yet. These commands describe the intended workflow for the first working version. They are a plan, not instructions for a tool you can run today.

- `semantic-git check <message>`: validate a single commit message and report what is wrong with it, if anything.
- `semantic-git check --range <range>`: validate every commit message in a range of git history.
- `semantic-git init`: write a starter configuration file that sets the allowed types, scopes, and description length limits for a repository.
- A git hook mode, where validation runs automatically when a commit is created and blocks messages that do not follow the configured rules.

## First scope

The first working version will:

- Validate one commit message at a time against the semantic format.
- Check the type against a configurable list of allowed types.
- Check that a description is present and within a configurable length limit.
- Print a clear pass or fail result, with a specific reason for each failure.
- Read its rules from a simple configuration file.

The first working version will not:

- Rewrite or fix commit messages automatically.
- Generate changelogs or release notes.
- Integrate with hosting platforms or CI services.
- Support plugins or custom validation rules written as code.

## Status

This repository is at the planning stage. There is no code, no installer, and nothing to run yet. This README defines the project so the first implementation has a clear target to build against.
