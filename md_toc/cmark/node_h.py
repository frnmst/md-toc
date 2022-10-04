# -*- coding: utf-8 -*-
#
# node_h.py
#
# Copyright (C) 2017-2022 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
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
r"""A cmark implementation file."""

from .cmark_h import _cmarkCmarkMem

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


class _cmarkCmarkList:
    __slots__ = [
        'marker_offset',
        'padding',
        'start',
        'list_type',
        'delimiter',
        'bullet_char',
        'tight',
    ]

    def __init__(self):
        self.marker_offset: int
        self.padding: int
        self.start: int
        self.list_type: int
        self.delimiter: int
        self.bullet_char: int
        self.tight: bool


class _cmarkCmarkCode:
    __slots__ = [
        'info',
        'fence_length',
        'fence_offset',
        'fence_offset',
        'fence_char',
        'fenced',
    ]

    def __init__(self):
        self.info: str
        self.fence_length: int
        self.fence_offset: int
        self.fence_char: int
        self.fenced: int


class _cmarkCmarkHeading:
    __slots__ = [
        'level',
        'setext',
    ]

    def __init__(self):
        self.level: int
        self.setext: bool


class _cmarkCmarkLink:
    __slots__ = [
        'url',
        'title',
    ]

    def __init__(self):
        self.url: str
        self.title: str


class _cmarkCmarkCustom:
    __slots__ = [
        'on_enter',
        'on_exit',
    ]

    def __init__(self):
        self.on_enter: str
        self.on_exit: str


class _cmarkCmarkNode:
    __slots__ = [
        'mem',
        'next',
        'prev',
        'parent',
        'first_child',
        'last_child',
        'user_data',
        'data',
        'length',
        'start_line',
        'start_column',
        'end_line',
        'end_column',
        'internal_offset',
        'type',
        'flags',
        'as_list',
        'as_code',
        'as_heading',
        'as_link',
        'as_custom',
        'as_html_block_type',
        'numdelims',
    ]

    def __init__(self):
        self.mem: _cmarkCmarkMem = None

        self.next: _cmarkCmarkNode = None
        self.prev: _cmarkCmarkNode = None
        self.parent: _cmarkCmarkNode = None
        self.first_child: _cmarkCmarkNode = None
        self.last_child: _cmarkCmarkNode = None

        self.user_data = None

        self.data: str = None
        self.length: int = 0

        self.start_line: int = 0
        self.start_column: int = 0
        self.end_line: int = 0
        self.end_column: int = 0
        self.internal_offset: int = 0
        self.type: int = 0
        self.flags: int = 0

        # "as" union.
        self.as_list: _cmarkCmarkList = _cmarkCmarkList()
        self.as_code: _cmarkCmarkCode = _cmarkCmarkCode()
        self.as_heading: _cmarkCmarkHeading = _cmarkCmarkHeading()
        self.as_link: _cmarkCmarkLink = _cmarkCmarkLink()
        self.as_custom: _cmarkCmarkCustom = _cmarkCmarkCustom()
        self.as_html_block_type: int = 0

        # Add a new variable.
        self.numdelims: int = 0


if __name__ == '__main__':
    pass
