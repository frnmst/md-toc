# -*- coding: utf-8 -*-
#
# types.py
#
# Copyright (C) 2023 Franco Masotti (see /README.md)
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
r"""Complex dict type definitions."""
from typing import TypedDict


class IndentationLogElement(TypedDict, total=False):
    r"""An ``indentation_log_element`` object.

    :parameter index: values: 1 -> md_parser['github']['header']['max levels'] + 1.
    :parameter list marker: ordered or undordered list marker.
    :parameter indentation spaces: number of indentation spaces.
    :type index: int
    :type list marker: str
    :type indentation spaces: int
    """

    # index: 1 -> md_parser['github']['header']['max levels'] + 1
    index: int
    # FIXME
    # Spaces are not allowed.


#    list marker: str
#    indentation spaces: int


class Header(TypedDict):
    r"""A ``header`` object.

    :parameter type: h1 to h6 (``1`` -> ``6``).
    :parameter text_original: Raw text.
    :parameter text_anchor_link: Transformed text so it works as an anchor
       link.
    :parameter visible: if ``True`` the header needs to be visible, if
       ``False`` it will not.
    :type type: int
    :type text_original: str
    :type text_anchor_link: str
    :type visible: bool
    """

    type: int
    text_original: str
    text_anchor_link: str
    visible: bool


class HeaderTypeCounter(TypedDict, total=False):
    r"""The number of headers for each type, from ``h1`` to ``h6``."""

    # Should be something like:
    # '1': int
    # '2': int
    # '3': int
    # '4': int
    # '5': int
    # '6': int
    pass


class HeaderDuplicateCounter(TypedDict, total=False):
    r"""A ``header_duplicate_counter`` object.

    :parameter ``key``: a generic string corresponding to header links. Its
       value is the number of times ``key`` appears during the execution of
       md-toc.

    .. note:: This dict can be empty.
    """

    key: int


class AtxHeadingStructElement(TypedDict, total=False):
    """A single element of the list returned by the ``get_atx_heading`` function.

    :parameter header type: h1 to h6 (``1`` -> ``6``).
    :parameter header text trimmed: the link label.
    :parameter visible: if the line has a smaller header that
       ``keep_header_levels``, then ``visible`` is set to ``False``.
    :type header type: int
    :type header text trimmed: str
    :type visible: bool

    .. note:: ``header type`` and ``header text trimmed`` are
       set to ``None`` if the line does not contain header elements according
       to the rules of the selected markdown parser.
       ``visible`` is set to ``True`` if the line needs to be saved, ``False``
       if it just needed for duplicate counting.
    """

    # header type: int
    # header text trimmed: str
    visible: bool
