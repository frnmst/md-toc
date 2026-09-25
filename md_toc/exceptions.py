# Copyright (C) 2017-2020 Franco Masotti (see /README.md)
# SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Exceptions file."""


class GithubOverflowCharsLinkLabel(Exception):
    """Cannot parse link label."""


class GithubEmptyLinkLabel(Exception):
    """The link lables contains only whitespace characters or is empty."""


class GithubOverflowOrderedListMarker(Exception):
    """The ordered list marker number is too big."""


class StdinIsNotAFileToBeWritten(Exception):
    """stdin cannot be written onto."""


class TocDoesNotRenderAsCoherentList(Exception):
    """TOC list indentations are either wrong or not what the user intended."""


class StringCannotContainNewlines(Exception):
    """The specified string cannot contain newlines."""
