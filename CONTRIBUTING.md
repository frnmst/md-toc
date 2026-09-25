<!--
SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Contributing

<!--TOC-->

- [Contributing](#contributing)
  - [Git branches](#git-branches)
  - [Pull requests](#pull-requests)
    - [Unit tests](#unit-tests)
  - [Variable naming](#variable-naming)
    - [Data type annotations](#data-type-annotations)
  - [AI Policy](#ai-policy)
    - [Commits](#commits)
    - [Models](#models)
    - [LLM codebase input](#llm-codebase-input)
  - [Note](#note)

<!--TOC-->

If you want to contribute, please follow these simple policies.

## Git branches

- `master`: this branch is protected and only updated when a new release is
   ready
- `dev`: this is the main working branch, recent changes can be merged here

## Pull requests

1. add a new endpoint or fix
2. add unit tests by mocking the files if necessary
  - valid cases
  - edge cases
  - invalid cases
3. run the [unit tests](#unit-tests)
3. create a pull request on the `dev` branch

### Unit tests

1. install the Python versions listed in the
   [pyproject.toml](pyproject.toml) `tool.tox.env_list` entry: use
   [ASDF](https://asdf-vm.com/guide/getting-started.html)
2. install the development environment as shown in the python-makefile[^1]
   repository (see footnotes)
3. run the tests with TOX:

   ```shell
   make tox
   ```

4. all tests must pass

## Variable naming

To keep things very uniform and simple please use snake\_case for all
variables. In case of cmark code directly translated from C to Python, use
these prefixes:

- `_cmark_` for function names
- `_cmark` for structs

### Data type annotations

When using type annotations with `Annotated`, follow
[FastAPI's standard](https://fastapi.tiangolo.com/tutorial/dependencies/#share-annotated-dependencies)
which uses Capitalized CamelCase.

## AI Policy

> [!NOTE]
> md-toc was born in 2017 before LLMs were a thing, so most of the code is
> human-only authored.

md-toc is human-authored, and (now) AI-assisted code for some brainstorming and
debugging: LLM use is not blanket-banned, but all its outputs must be
thoroughly checked. LLMs can be used for ideas and specific domain problem
solving, but its outputs must always be challenged to provide better quality
code and compared with the official documentation and best practices. In this
project an LLM should be used as a more powerful search engine: that's it.

Remember that LLMs have varying degrees of sycophancy so prompts must be
adapted to mitigate that.

This policy is similar to
[Proposal E - Choice 5: Responsible Use of Generative AI](https://www.debian.org/vote/2026/vote_002#texte)
voted by Debian in 2026.

### Commits

No kind of automated AI agent can be involved, and all commits must be signed
by real humans.

### Models

All the LLMs used by the authors must be lighter, accountless, free-to-use,
cloud models, even better if free (libre) and self-hosted.

### LLM codebase input

Please do not input this whole repository into an LLM and ask it to find
vulnerabilities or to "improve the code". You may prompt specific code snippets
if you are unsure about what they do.

## Note

If these indications are not followed, your contribution cannot be merged in
the codebase.

[^1]: [Codeberg](https://codeberg.org/frnmst/python-makefile),
      [Framagit](https://framagit.org/frnmst/python-makefile),
      [Self-hosted Forgejo](https://repos.franco.net.eu.org/frnmst/python-makefile)
