# -*- coding: utf-8 -*-
#
# exceptions.py
#
# Copyright (C) 2017-2020 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
#
# This file is part of md-toc.
#
# md-toc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# md-toc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with md-toc.  If not, see <http://www.gnu.org/licenses/>.
#
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


class CannotTreatUnicodeString(Exception):
    """Cannot treat unicode string.

    .. note:: This exception is deprecated and will be removed in the next major release.
    """
