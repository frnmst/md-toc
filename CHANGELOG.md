<!--
SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--TOC-->

- [Changelog](#changelog)
  - [\[Unreleased\]](#unreleased)
  - [\[9.0.1\] Unreleased](#901-unreleased)
    - [Fixed](#fixed)
    - [Added](#added)
    - [Changed](#changed)
  - [\[9.0.0\] 2024-04-10](#900-2024-04-10)
    - [Fixed](#fixed-1)
    - [Fixed](#fixed-2)
    - [Removed](#removed)
  - [\[8.2.2\] 2023-11-09](#822-2023-11-09)
    - [Changed](#changed-1)
    - [Fixed](#fixed-3)
  - [\[8.2.1\] 2023-11-07](#821-2023-11-07)
    - [Changed](#changed-2)
    - [Added](#added-1)
  - [\[8.2.0\] 2023-08-08](#820-2023-08-08)
    - [Fixed](#fixed-4)
    - [Added](#added-2)
  - [\[8.1.9\] 2023-02-10](#819-2023-02-10)
    - [Changed](#changed-3)
    - [Fixed](#fixed-5)
  - [\[8.1.8\] 2023-01-06](#818-2023-01-06)
    - [Changed](#changed-4)
    - [Removed](#removed-1)
    - [Fixed](#fixed-6)
  - [\[8.1.7\] 2022-12-29](#817-2022-12-29)
    - [Added](#added-3)
    - [Fixed](#fixed-7)
    - [Changed](#changed-5)
  - [\[8.1.6\] 2022-12-08](#816-2022-12-08)
    - [Fixed](#fixed-8)
  - [\[8.1.5\] 2022-10-28](#815-2022-10-28)
    - [Added](#added-4)
    - [Fixed](#fixed-9)
  - [\[8.1.4\] 2022-06-15](#814-2022-06-15)
    - [Changed](#changed-6)
    - [Fixed](#fixed-10)
  - [\[8.1.3\] 2022-04-20](#813-2022-04-20)
    - [Deprecated](#deprecated)
    - [Fixed](#fixed-11)
  - [\[8.1.2\] 2022-04-03](#812-2022-04-03)
    - [Fixed](#fixed-12)
    - [Changed](#changed-7)
  - [\[8.1.1\] 2022-01-27](#811-2022-01-27)
    - [Fixed](#fixed-13)
  - [\[8.1.0\] 2021-11-29](#810-2021-11-29)
    - [Fixed](#fixed-14)
  - [\[8.0.1\] 2021-08-20](#801-2021-08-20)
    - [Fixed](#fixed-15)
    - [Changed](#changed-8)
    - [Added](#added-5)
  - [\[8.0.0\] 2021-05-28](#800-2021-05-28)
    - [Changed](#changed-9)
    - [Added](#added-6)
    - [Removed](#removed-2)

<!--TOC-->

## [Unreleased]

- Update existing cmark code from version 0.30.0 to version
  [0.31.2](https://spec.commonmark.org/0.31.2/changes.html).
- An `md_toc.exceptions.TocDoesNotRenderAsCoherentList` exception is raised for
  big inputs (>= 50M characters) when using the benchmark script.
  There is a jump in the detected header level, 1 then 3, not 2. This always
  happens with the last line of the dummy input file.
- Add code fence detection before writing TOC in place.
  Until version 9.0.0, given for example a file like this

  ````markdown
  ```

  <!--TOC_MARKER-->

  ```

  # ONE

  ## TWO

  # ONE

  ## TWO

  ### THREE
  ````

  running

  ```shell
  md_toc --toc-marker '<!--TOC_MARKER-->' -p github file.md
  ```

  results in

  ````markdown
  ```

  <!--TOC_MARKER-->

  - [ONE](#one)
    - [TWO](#two)
  - [ONE](#one-1)
    - [TWO](#two-1)
      - [THREE](#three)

  <!--TOC_MARKER-->

  ```

  # ONE

  ## TWO

  # ONE

  ## TWO

  ### THREE
  ````

  instead of

  ````markdown
  ```

  <!--TOC_MARKER-->

  ```

  # ONE

  ## TWO

  # ONE

  ## TWO

  ### THREE
  ````

  This means that if a TOC marker is detected within fenced code block it must
  be ignored. A similar problem happens if there are two TOC markers, one of
  them being inside a fenced code block:

  ````markdown
  ```

  <!--TOC_MARKER-->

  ```

  <!--TOC_MARKER-->

  # ONE

  ## TWO

  # ONE

  ## TWO

  ### THREE
  ````

  using the previous command results in

  ````markdown
  ```

  <!--TOC_MARKER-->

  - [ONE](#one)
    - [TWO](#two)
  - [ONE](#one-1)
    - [TWO](#two-1)
      - [THREE](#three)

  <!--TOC_MARKER-->
  <!--TOC_MARKER-->

  ```

  <!--TOC_MARKER-->

  # ONE

  ## TWO

  # ONE

  ## TWO

  ### THREE
  ````

## [9.0.1] Unreleased

### Fixed

- [__✓__ 5c7ddab](https://github.com/frnmst/md-toc/commit/5c7ddab)

  Add missing binary file detections in `md_toc.api.build_toc`.
- [__✓__ 89e2d60](https://github.com/frnmst/md-toc/commit/89e2d60)

  Fix references to `md_toc.api.build_toc` from `md_toc.build_toc`.
- [__✓__ 5c7ddab](https://github.com/frnmst/md-toc/commit/5c7ddab)

  Improve test coverage
- [__✓__ 5c7ddab](https://github.com/frnmst/md-toc/commit/5c7ddab)

  Reduce some code for function input validation.
- Cleanup ./README.md.

### Added

- Add changelog in repository.
- Add community URLs in CLI help.
- [__✓__ 276acd6](https://github.com/frnmst/md-toc/commit/276acd6)

  Add GitHub unit test action (draft).

### Changed

- Use modern packaging via pyproject.toml and drop setup{py,cfg}.
- Change and update pre-commit hooks.
- Drop support for Python <= 3.10 and add 3.14 to unit test validations.

## [9.0.0] 2024-04-10

### Fixed

- [__✓__ f3398b6](https://github.com/frnmst/md-toc/commit/f3398b6)

  `setup.cfg` now reads `options.install_requires` from the `./requirements.txt`
  file instead from a hard-coded list.
- [__✓__ f3398b6](https://github.com/frnmst/md-toc/commit/f3398b6)

  Add `--require-virtualenv` pip option in Makefile where necessary.
- [__✓__ f154114](https://github.com/frnmst/md-toc/commit/f154114)
  [__✓__ 31e703b](https://github.com/frnmst/md-toc/commit/31e703b)
  [__✓__ f357165](https://github.com/frnmst/md-toc/commit/f357165)

  Add use of SHA512 and SHA256 hashes for the `./.requirements-freeze-hashes.txt`
  file. The Makefile now downloads packages locally, computes their checksums,
  and updates the `./requirements-freeze.txt` and `./requirements-freeze-hashes.txt`  files.
- [__✓__ f154114](https://github.com/frnmst/md-toc/commit/f154114)

  Fix `.github/FUNDING.yml`
- [__✓__ 42d3086](https://github.com/frnmst/md-toc/commit/42d3086)

  Read tox test requirements (`testenv` in setup.cfg) from requirement files
  instead of hard-coded packages.

- [__✓__ #42: *IndexError: list index out of range*](https://github.com/frnmst/md-toc/issues/42)

  This issue is related to GitHub only: it seems they fixed their backend code.
  Will close once md-toc 9.x is out.
- [__✓__ c8a6402](https://github.com/frnmst/md-toc/commit/c8a6402)

  Improve documentation for the API so it is more readable: use `autosummary`
  and `automodule`.
- [__✓__ 40f9231](https://github.com/frnmst/md-toc/commit/40f9231)

  Remove NULL bytes before passing the anchor link to the `remove_emphasis`
  cmark function. Without this change, md-toc fails with this and other similar
  inputs. More tests are needed to determine if the generated TOCs still work.

  This is the output of `hexyl a.md`:

  ```
  ┌────────┬─────────────────────────┬─────────────────────────┬────────┬────────┐
  │00000000│ 23 20 61 62 63 64 65 66 ┊ 67 68 69 6a 6b 6c 6d 6e │# abcdef┊ghijklmn│
  │00000010│ 6f 70 71 72 73 74 75 76 ┊ 77 78 79 7a 41 42 43 44 │opqrstuv┊wxyzABCD│
  │00000020│ 45 46 47 48 49 4a 4b 4c ┊ 4d 4e 4f 50 51 52 53 54 │EFGHIJKL┊MNOPQRST│
  │00000030│ 55 56 57 58 59 5a 60 00 ┊ 00 00 0a                │UVWXYZ`0┊00_     │
  └────────┴─────────────────────────┴─────────────────────────┴────────┴────────┘
  ```

  ```shell
  cat -e a.md
  # abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`^@^@^@$
  ```

  Result:

  ```shell
  python3 -m md_toc github a.md

    Traceback (most recent call last):
      File "./md-toc/md_toc/__main__.py", line 36, in main
        result = args.func(args)
                 ^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cli.py", line 79, in write_toc
        toc_struct = build_multiple_tocs(
                     ^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/api.py", line 483, in build_multiple_tocs
        return [
               ^
      File "./md-toc/md_toc/api.py", line 484, in <listcomp>
        build_toc(
      File "./md-toc/md_toc/api.py", line 325, in build_toc
        headers: list[types.Header] = get_md_header(
                                      ^^^^^^^^^^^^^^
      File "./md-toc/md_toc/api.py", line 1320, in get_md_header
        return [
               ^
      File "./md-toc/md_toc/api.py", line 1328, in <listcomp>
        build_anchor_link(
      File "./md-toc/md_toc/api.py", line 906, in build_anchor_link
        header_text_trimmed = remove_emphasis(header_text_trimmed, parser)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/api.py", line 836, in remove_emphasis
        ignore: list[range] = inlines_c._cmark_cmark_parse_inlines(
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cmark/inlines_c.py", line 2184, in _cmark_cmark_parse_inlines
        while not _cmark_is_eof(subj) and _cmark_parse_inline(
                                          ^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cmark/inlines_c.py", line 2117, in _cmark_parse_inline
        new_inl = _cmark_handle_backticks(subj, options)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cmark/inlines_c.py", line 639, in _cmark_handle_backticks
        openticks: _cmarkCmarkChunk = _cmark_take_while(subj, '_cmark_isbacktick')
                                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cmark/inlines_c.py", line 497, in _cmark_take_while
        while _cmark_take_while_loop_condition(subj, '_cmark_isbacktick'):
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cmark/inlines_c.py", line 482, in _cmark_take_while_loop_condition
        c = _cmark_peek_char(subj)
            ^^^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cmark/inlines_c.py", line 430, in _cmark_peek_char
        raise ValueError
    ValueError
  ```

- [__✓__ 40f9231](https://github.com/frnmst/md-toc/commit/40f9231)

  Add more checks in the `md_toc.cmark.inlines_c._cmark_subject_find_special_char`
  function to avoid overflows. More tests are needed to determine if the
  generated TOCs still work.

  This is the output of `hexyl a.md`:

  ```
  ┌────────┬─────────────────────────┬─────────────────────────┬────────┬────────┐
  │00000000│ 23 20 61 62 63 64 65 66 ┊ 67 68 69 6a 6b 6c 6d 6e │# abcdef┊ghijklmn│
  │00000010│ 6f 70 71 72 73 74 75 76 ┊ 77 78 79 7a 41 42 43 44 │opqrstuv┊wxyzABCD│
  │00000020│ 45 46 47 48 49 4a 4b 4c ┊ 4d 4e 4f 50 51 52 53 54 │EFGHIJKL┊MNOPQRST│
  │00000030│ 55 56 57 58 59 5a c5 8c ┊ 61 62 63 64 65 66 67 68 │UVWXYZ××┊abcdefgh│
  │00000040│ 69 6a 6b 6c 6d 6e 6f 70 ┊ 71 72 73 74 75 76 77 78 │ijklmnop┊qrstuvwx│
  │00000050│ 79 7a 41 42 43 44 45 46 ┊ 47 48 49 4a 4b 4c 4d 4e │yzABCDEF┊GHIJKLMN│
  │00000060│ 4f 50 51 52 53 54 55 56 ┊ 57 58 59 5a 0a          │OPQRSTUV┊WXYZ_   │
  └────────┴─────────────────────────┴─────────────────────────┴────────┴────────┘
  ```

  ```shell
  cat -e a.md
  # abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZM-EM-^LabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$
  ```

  Result:

  ```shell
  python3 -m md_toc github a.md

     Traceback (most recent call last):
       File "./md-toc/md_toc/__main__.py", line 36, in main
        result = args.func(args)
                 ^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cli.py", line 79, in write_toc
        toc_struct = build_multiple_tocs(
                     ^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/api.py", line 483, in build_multiple_tocs
        return [
               ^
      File "./md-toc/md_toc/api.py", line 484, in <listcomp>
        build_toc(
      File "./md-toc/md_toc/api.py", line 325, in build_toc
        headers: list[types.Header] = get_md_header(
                                      ^^^^^^^^^^^^^^
      File "./md-toc/md_toc/api.py", line 1324, in get_md_header
        return [
               ^
      File "./md-toc/md_toc/api.py", line 1332, in <listcomp>
        build_anchor_link(
      File "./md-toc/md_toc/api.py", line 910, in build_anchor_link
        header_text_trimmed = remove_emphasis(header_text_trimmed, parser)
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/api.py", line 840, in remove_emphasis
        ignore: list[range] = inlines_c._cmark_cmark_parse_inlines(
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cmark/inlines_c.py", line 2187, in _cmark_cmark_parse_inlines
        while not _cmark_is_eof(subj) and _cmark_parse_inline(
                                          ^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cmark/inlines_c.py", line 2152, in _cmark_parse_inline
        endpos = _cmark_subject_find_special_char(subj, options)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "./md-toc/md_toc/cmark/inlines_c.py", line 2090, in _cmark_subject_find_special_char
        if SPECIAL_CHARS[ord(subj.input.data[n])] == 1:
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
    IndexError: list index out of range
    ```

- [__✓__ 40f9231](https://github.com/frnmst/md-toc/commit/40f9231)

  Improve benchmark script.

- [__✓__ 1a40e9b](https://github.com/frnmst/md-toc/commit/1a40e9b)

  Use Python [dataclass](https://docs.python.org/3.11/library/dataclasses.html)
  in cmark code where appropriate.

- [__✓__ 1a40e9b](https://github.com/frnmst/md-toc/commit/1a40e9b)

  Remove debug code in cmark code classes.

- [__✓__ 0904177](https://github.com/frnmst/md-toc/commit/0904177)

  Fix the anchor link punctuation filter regex for cmark-like markdown parsers.
  This reflects the existing
  [Ruby code](https://github.com/gjtorikian/html-pipeline/blob/7c7fad1f82f81ebf15dd81d59eed28d979b8e441/lib/html/pipeline/toc_filter.rb#L30).
  See also
  [#42: *IndexError: list index out of range*](https://github.com/frnmst/md-toc/issues/42).

- [__✓__ 9659e9d](https://github.com/frnmst/md-toc/commit/9659e9d)

  Simplify fuzzer script

- [__✓__ 970b5a9](https://github.com/frnmst/md-toc/commit/970b5a9)

  Fix benchmark script: improve random file generation speed

### Added

- [__✓__ f3398b6](https://github.com/frnmst/md-toc/commit/f3398b6)

  Add Flatpak manifest file.
- [__✓__ 31e703b](https://github.com/frnmst/md-toc/commit/31e703b)

  Add pip-audit pre-commit hook.
- [__✓__ 31e703b](https://github.com/frnmst/md-toc/commit/31e703b)

  Move Makefile to a separate project.
- [__✓__ 8b2f1da](https://github.com/frnmst/md-toc/commit/8b2f1da)

  Start adding examples in docstrings.
- [__✓__ 40f9231](https://github.com/frnmst/md-toc/commit/40f9231)

  Add use of fuzzer to detect bugs.

- [__✓__ 0904177](https://github.com/frnmst/md-toc/commit/0904177)

  Add the `md_toc.api.anchor_link_punctuation_filter` function and related
  unit tests. See also
  [#42: *IndexError: list index out of range*](https://github.com/frnmst/md-toc/issues/42).

### Changed

- [__✓__ c8a6402](https://github.com/frnmst/md-toc/commit/c8a6402)

  Change the module imports. To import functions or exceptions from the API
  you now need the full path. For example `md_toc.build_toc` becomes
  `md_toc.api.build_toc`. To do this:
  - the `md_toc/__init__` file needs to have the bare minimum data
  - the API section of the developer interface documentation points to elements
    via their full name
  The purpose of this is to have a cleaner project structure.
- [__✓__ ab64da0](https://github.com/frnmst/md-toc/commit/ab64da0)
  [__✓__ ba25606](https://github.com/frnmst/md-toc/commit/ba25606)
  [__✓__ 9b92f17](https://github.com/frnmst/md-toc/commit/9b92f17)

  Snake case for all variables.
- [__✓__ ab64da0](https://github.com/frnmst/md-toc/commit/ab64da0)
  [__✓__ 3dcbc6d](https://github.com/frnmst/md-toc/commit/3dcbc6d)
  [__✓__ 456343f](https://github.com/frnmst/md-toc/commit/456343f)

  Fix and cleanup `md_toc/constants.py`.
- [__✓__ 9b92f17](https://github.com/frnmst/md-toc/commit/9b92f17)

  Fix and cleanup `md_toc/types.py`:
  - `class IndentationLogElement`
    - `list marker` -> `list_marker`
    - `indentation_space` -> `indentation_spaces`
  - `class Header`
    - `type` -> `header_type`
  - `class HeaderTypeCounter`
    - `1` ... `6` -> `h1` ... `h6`
  - `class AtxHeadingStructElement`
    - `header type` -> `header_type`
    - `header text trimmed` -> `header_text_trimmed`
- [__✓__ ba25606](https://github.com/frnmst/md-toc/commit/ba25606)

  Change default maximum header level to the maximum supported for each parser.
- [__✓__ 40f9231](https://github.com/frnmst/md-toc/commit/40f9231)

  Catch `UnicodeDecodeError` exceptions in the
  `md_toc.api.build_toc` function: stop reading the file and print an HTML
  comment.

### Removed

- [__✓__ 88f66bc](https://github.com/frnmst/md-toc/commit/88f66bc)

  Remove the deprecated `md_toc.exceptions.CannotTreatUnicodeString` exception.
- [__✓__ 7bbbccc](https://github.com/frnmst/md-toc/commit/7bbbccc)

  Remove the `md_toc.api.toc_renders_as_coherent_list` and
  `md_toc.api.init_indentation_status_list` functions and replace them with
  a much simpler check.

> [!NOTE]
> GitHub Flavored Markdown is still at version 0.29. md-toc does its best
> to support both GFM 0.29 and cmark 0.30.

## [8.2.3] 2024-02-15

### Added

- [__✓__ fbf9359](https://github.com/frnmst/md-toc/commit/fbf9359)

  Add `./SECURITY.md` file.
- [__✓__ fbf9359](https://github.com/frnmst/md-toc/commit/fbf9359)

  Add [pyupgrade](https://github.com/asottile/pyupgrade) to pre-commit.
- [__✓__ 696d334](https://github.com/frnmst/md-toc/commit/696d334)

  Add more project metadata and funding info.

- [__✓__ 9edbafc](https://github.com/frnmst/md-toc/commit/9edbafc)

  Cleanup pre-commit hooks: remove unused ones and add some from the default
  pre-commit repository.

- [__✓__ 7c6fb22](https://github.com/frnmst/md-toc/commit/7c6fb22)

  Add more classifiers in `./setup.cfg`.

### Changed

- [__✓__ 2bf06bb](https://github.com/frnmst/md-toc/commit/2bf06bb)

  Remove the `md_toc.generic._utf8_array_to_string` function. Replace
  this with a single Python line in the
  `md_toc.cmark.buffer_c._cmark_cmark_strbuf_put`
  function:

  ```python
  dt = bytearray(data).decode('UTF-8')
  ```

### Fixed

- [__✓__ 2bf06bb](https://github.com/frnmst/md-toc/commit/2bf06bb)

  Replace variable correctly in the
  `md_toc.cmark.buffer_c._cmark_cmark_strbuf_put` function.
- [__✓__ fbf9359](https://github.com/frnmst/md-toc/commit/fbf9359)

  Fix `/.pre-commit-config.yaml` file indentations.
- [__✓__ fbf9359](https://github.com/frnmst/md-toc/commit/fbf9359)

  Cleanup *Pre-commit hook* documentation page.

- [__✓__ 9edbafc](https://github.com/frnmst/md-toc/commit/9edbafc)

  Fix some cmark code translated from C: `memmove` functions should now be
  implemented correctly.

- [__✓__ 7c6fb22](https://github.com/frnmst/md-toc/commit/7c6fb22)

  Move [Bandit](https://github.com/PyCQA/bandit) configuration from
  `/.pre-commit-config.yaml` to `./pyproject.toml`.

- [__✓__ 7c6fb22](https://github.com/frnmst/md-toc/commit/7c6fb22)

  Disable upper pinning Python version, as suggested by
  [this](https://iscinumpy.dev/post/bound-version-constraints/#pinning-the-python-version-is-special)
  document.

> [!NOTE]
> GitHub Flavored Markdown is still at version 0.29. md-toc does its best
> to support both GFM 0.29 and cmark 0.30.

### Removed

- [__✓__ 9edbafc](https://github.com/frnmst/md-toc/commit/9edbafc)

  Remove an `import` case for Python < 3.8: recent versions of md-toc support
  Python >= 3.8.

## [8.2.2] 2023-11-09

### Changed

- Add unit test support for multiple Python versions using
  [tox](https://tox.wiki) and [asdf](https://asdf-vm.com/)
- Bump fpyutils to 4.0.1. See `Fixed` section below.

### Fixed

- This unit test for md-toc version 8.2.1 failed when the new version of
  [fpyutils](https://blog.franco.net.eu.org/software/#fpyutils) was used in the
  `/requirements.txt` file:

  ```diff
  - fpyutils>=3.0.1,<4
  + fpyutils==4.0.0
  ```

  ```
  $ python -m unittest discover

  .ssss......s......sFs.......
  ======================================================================
  FAIL: test_write_string_on_file_between_markers (md_toc.tests.tests.TestApi.test_write_string_on_file_between_markers)
  Test that the TOC is written correctly on the file.
  ----------------------------------------------------------------------
  Traceback (most recent call last):
    File "/dev/shm/md-toc/md_toc/tests/tests.py", line 529, in test_write_string_on_file_between_markers
      self.assertEqual(
  AssertionError: 'hello\n' != 'hello\n<!--TOC-->\n\nThis is a static line\n\n<!--TOC-->\n'
    hello
  + <!--TOC-->
  +
  + This is a static line
  +
  + <!--TOC-->


    ----------------------------------------------------------------------
  Ran 28 tests in 0.090s

  FAILED (failures=1, skipped=7)
  ```

  This new bug was caused by
  [the new changes in fpyuils 4.0.0](https://blog.franco.net.eu.org/software/CHANGELOG-fpyutils.html#400---2023-11-06)
- Support older Python versions >= 3.8, using `__future__` imports. See also
  fpyutils 4.0.1

> [!NOTE]
> GitHub Flavored Markdown is still at version 0.29. md-toc does its best
> to support both GFM 0.29 and cmark 0.30.

## [8.2.1] 2023-11-07

### Changed

- Clean up code:
  - use more list comprehensions
  - use less variables in general
  - remove some typing checks for the arguments passed to functions
    and replace them with improved typing notation in the function
    prototype
- Use stronger typing thanks to the [`typing`](https://docs.python.org/3.11/library/typing.html) module.
- Replace duplicated code in the `md_toc.api.remove_html_tags` function with a
  for loop.
- Use of the SHA1 checksum for the keys of the `header_duplicate_counter`
  dict. This lowers memory usage at the cost of time. The most effective
  application of this is when you have very long headings: previously the keys
  of this dict would take lots of space. By using a checksum, the space used
  is constant. See the `md_toc.api.build_anchor_link` function.
- Update documentation:
  - Add API change notices to the documentation. These changes will take place
    from version 9
  - Update Sphinx version and its theme
- Minimum supported Python version is now `3.8`.

### Added

- Create the `md_toc/types.py` files that holds the structure for some complex
  objects

> [!NOTE]
> GitHub Flavored Markdown is still at version 0.29. md-toc does its best
> to support both GFM 0.29 and cmark 0.30.

## [8.2.0] 2023-08-08

### Fixed

- Definetly closed
  [issue #36: *Consider Mentioning Existence of GitHub's Built-In Markdown Table of Contents*](https://github.com/frnmst/md-toc/issues/36).
  Added more projects for feature comparisons.
- [Issue #38: *Invalid Cross-device Link*](https://github.com/frnmst/md-toc/issues/38)
  declared officially closed for inactivity (no recent reports).

### Added

- Using the new `--diff` option enables md-toc to return `128` if the existing
  TOC in a file is different from the newly generated one, instead of a normal
  `0` value. Some CI systems don't allow modifying files in-place when running
  pre-commit.

  By returning something different than 0, the pre-commit pipeline fails so the
  user gets notified that the TOC needs to be changed.
  See [issue #40: *There are no diff unless we specify `-p`*](https://github.com/frnmst/md-toc/issues/40).

> [!NOTE]
> GitHub Flavored Markdown is still at version 0.29. md-toc does its best
> to support both GFM 0.29 and cmark 0.30.

## [8.1.9] 2023-02-10

### Changed

- Moved some cmark constants to their appropriate files so as to mirror the
  upstream C code.

### Fixed

- Added an API example in the README file to write the TOC in place.
- Improve and update md-toc's pre-commit hook documentation.
- Continuing to fix [issue #25](https://github.com/frnmst/md-toc/issues/25).
- Improved md-toc version history table: split versions to improve
  readability.

> [!NOTE]
> GitHub Flavored Markdown is still at version 0.29. md-toc does its best
> to support both GFM 0.29 and cmark 0.30.

## [8.1.8] 2023-01-06

### Changed

- Improved TOC list detection: allow up to 3 leading spaces instead of 0
  for first line of lists inside TOC markers (`<!--TOC-->`) to be detected
  as real TOC content that needs to be replaced.
- Use of a `requirements-freeze.txt` file with pinned dependencies for the
  development environment, computed from the `requirements.txt` and
  `requirements-dev` files.
- Pinned [fpyutils](https://blog.franco.net.eu.org/software/#fpyutils)
  dependency at least to version 3.0.1.
- Use of modern tools to install the package from the PKGBUILD file.
  See
  [Standards based (PEP 517)](https://wiki.archlinux.org/title/Python_package_guidelines#Standards_based_(PEP_517))
  vs
  [setuptools or distutils](https://wiki.archlinux.org/title/Python_package_guidelines#setuptools_or_distutils)

### Removed

- Removed use of `pkg_resources` because they are deprecated.

### Fixed

- Improvements for [issue #38](https://github.com/frnmst/md-toc/issues/38).
- Continue fixing
  [issue #36](https://github.com/frnmst/md-toc/issues/36)
  and split feature table by subject.

> [!NOTE]
> GitHub Flavored Markdown is still at version 0.29. md-toc does its best
> to support both GFM 0.29 and cmark 0.30.

## [8.1.7] 2022-12-29

### Added

- Add comparison table for the various tools similar to md-toc. This closes
  [issue #36](https://github.com/frnmst/md-toc/issues/36) although there is
  still room for improvement.

### Fixed

- Use of list comprehensions instead of for loops to possibly improve speed.
- Pinned YAPF and flake8 versions through the pre-commit update command
  in the Makefile.
- Improved benchmark script
  - Improved random string generation speed using `ctypes`.
  - Bug fixes.
- Continuing to fix [issue #25](https://github.com/frnmst/md-toc/issues/25).
- Fixed pre-commit hooks.

### Changed

- Implement use of `setup.cfg` and `pyproject.toml`.
  `setup.py` is now a dummy file.
- Moved some pre-commit options to `setup.cfg`.
- Replaced Pipenv environment with `venv` and `pip` commands.
- Replaced distribution commands (`setup.py sdist`, `setup.py bdist_wheel`)
  with the [`build`](https://pypa-build.readthedocs.io/en/stable/) module.
- Pinned [fpyutils](https://blog.franco.net.eu.org/software/#fpyutils)
  dependency at least to version 3.0.0.

> [!NOTE]
> GitHub Flavored Markdown is still at version 0.29. md-toc does its best
> to support both GFM 0.29 and cmark 0.30.

## [8.1.6] 2022-12-08

### Fixed

- Until version 8.1.5, given for example a file like this

  ```markdown
  # ONE

  ## TWO

  ### THREE

  ### THREE

  ### THREE

  ## THREE

  # ONE
  ```

  running

  ```shell
  md_toc github -l2 file.md
  ```

  results in

  ```markdown
  - [ONE](#one)
    - [TWO](#two)
    - [THREE](#three)
  - [ONE](#one-1)
  ```

  instead of

  ```markdown
  - [ONE](#one)
    - [TWO](#two)
    - [THREE](#three-3)
  - [ONE](#one-1)
  ```

  Note the `-l2` option.

  md-toc works fine if you use the maximum header level (typically 6).
  Add a `visible` key in the returned `struct` of the
  `md_toc.api.get_atx_heading` function so that correct duplicate header counts
  can be performed. This means that in cases of non
  maximum header level selection (typically < 6) using the
  `-l [{1,2,3,4,5,6}], --header-levels [{1,2,3,4,5,6}]` option, all headers
  must be parsed even if they are not visible in the end.
- Update documentation.
- Change Sphinx theme.

> [!NOTE]
> GitHub Flavored Markdown is still at version 0.29. md-toc does its best to support both GFM 0.29 and cmark 0.30.

## [8.1.5] 2022-10-28

### Added

- Added support for ignoring emphasis in HTML point braces (`< ... >`).
  See [issue #25](https://github.com/frnmst/md-toc/issues/25).
- Added some benchmarks and a benchmark script. These benchmarks are not
  reproducible: random strings are generated each run. There are two purposes
  for these benchmarks:
  - see how md-toc performance changes with each release
  - detect bugs (runtime errors, exceptions especially)
    that are not addressed by the tests file

### Fixed

- Fixed some docstring documentation. See [issue #39](https://github.com/frnmst/md-toc/issues/39).
- Fixed variable typing using mypy git hook.

Note: GitHub Flavored Markdown is still at version 0.29. md-toc does its best to
      support both GFM 0.29 and cmark 0.30.

## [8.1.4] 2022-06-15

### Changed

- Readme is now in markdown instead of rst.

### Fixed

- Improved readme according to [issue #36](https://github.com/frnmst/md-toc/issues/36): better description of md-toc features
  compared to similar solutions.
- Improved TOC marker detection and TOC substitution in place: replace an existing TOC only if
  - the TOC is a list
  - or there is no content between the TOC markers

Note: GitHub Flavored Markdown is still at version 0.29. md-toc does its best to
      support both GFM 0.29 and cmark 0.30.

## [8.1.3] 2022-04-20

### Deprecated

- Deprecation of `md_toc.exceptions.CannotTreatUnicodeString` exception.
  This exception will be removed in version 9 of md-toc.

### Fixed

- Memory improvements for operations on class instances.
- Speed improvements for concatenation operations on strings.
- Improved constants file.
- Added square bracket support detection in emphasis for cmark.
  See [issue 25](https://github.com/frnmst/md-toc/issues/25)

Note: GitHub Flavored Markdown is still at version 0.29. md-toc does its best to
      support both GFM 0.29 and cmark 0.30.

## [8.1.2] 2022-04-03

### Fixed

- Added code span support detection in emphasis for cmark.
  See [issue 25](https://github.com/frnmst/md-toc/issues/25)
- Ported missing code changes from cmark 0.29 to 0.30.

  Note: GitHub Flavored Markdown is still at version 0.29. md-toc does its best to
        support both GFM 0.29 and cmark 0.30.

### Changed

- All cmark code has been split in separate Python modules:
  each module represents a C source file.
- Documentation about markdown specification has been split in various files
  to improve readability.
- Updated copyright headers.

## [8.1.1] 2022-01-27

### Fixed

- Fixed [issue 30](https://github.com/frnmst/md-toc/issues/30): added full support for
  CommonMark 0.30.

  Note:

  - GitHub Flavored Markdown is still at version 0.29. md-toc does its best to
    support both GFM 0.29 and cmark 0.30.
  - Previously missing implementations for the markdown emphasis removal have not
    been added with this release.

- Improved adherence to upstream cmark code.
- Added missing values in constants.
- Imported fixes from [fpydocs](https://blog.franco.net.eu.org/software/#fpydocs).
- Updated copyright headers.

## [8.1.0] 2021-11-29

### Fixed

- New line output is now handled correctly.
  See [issue 33](https://github.com/frnmst/md-toc/issues/33).
- Updated copyright headers.
- Imported fixes from [fpydocs](https://blog.franco.net.eu.org/software/#fpydocs).
- Metadata fixes in the setup.py file.

## [8.0.1] 2021-08-20

### Fixed

- Cmark-specific code is now more adherent to the original.
- License references are now more accurate.
- The PyPI wheel is now made reproducible.
- Updated email.

### Changed

- Cmark-specific code has been moved to a separate Python module: `cmark.py`.

### Added

- New git hooks have been added in the pre-commit file.
- Examples for unit tests of Cmark 0.30 have been checked with the existing examples.

## [8.0.0] 2021-05-28

### Changed

- Translated functions directly from cmark to treat emphasis.
- `md_toc.api.get_md_header` and `md_toc.api.get_atx_heading` now support
  multiple lines.
- Updated documentation.
- Updated tests.
- Updated package dependencies.

### Added

- Newline string argument choice from the CLI.
- Added these exceptions:
  - `md_toc.exceptions.StringCannotContainNewlines`
  - `md_toc.exceptions.CannotTreatUnicodeString`

### Removed

- Removal of these functions:
  - `md_toc.api.get_generic_fdr_indices`
  - `md_toc.api.get_fdr_indices`
  - `md_toc.api.can_open_emphasis`
  - `md_toc.api.can_close_emphasis`
  - `md_toc.api.get_nearest_list_id`
