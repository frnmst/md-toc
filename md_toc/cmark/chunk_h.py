# -*- coding: utf-8 -*-
#
# chunk_h.py
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
r"""The cmark implementation file."""

import copy

from ..constants import parser as md_parser
from .cmark_ctype_c import _cmark_cmark_isspace

# License E applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst

# Returns 1 if c is a "whitespace" character as defined by the spec.
#   int cmark_isspace(char c) { return cmark_ctype_class[(uint8_t)c] == 1; }
# The only defined whitespaces in the spec are Unicode whitespaces.


# 0.30
class _cmarkCmarkChunk:
    __slots__ = [
        'data',
        'length',
    ]

    def __init__(self, data: str = None, length: int = 0):
        self.data: str = data
        self.length: int = length


# 0.30
def _cmark_cmark_chunk_free(c: _cmarkCmarkChunk):
    c.data = None
    c.length = 0


# 0.30
def _cmark_cmark_chunk_ltrim(c: _cmarkCmarkChunk):
    while c.length > 0 and _cmark_cmark_isspace(ord(c.data[0])):
        c.data = c.data[1:]
        c.length -= 1


# 0.30
def _cmark_cmark_chunk_rtrim(c: _cmarkCmarkChunk):
    while c.length > 0:
        if not _cmark_cmark_isspace(ord(c.data[c.length - 1])):
            break

        c.length -= 1


# 0.30
def _cmark_cmark_chunk_trim(c: _cmarkCmarkChunk):
    _cmark_cmark_chunk_ltrim(c)
    _cmark_cmark_chunk_rtrim(c)


# 0.30
def _cmark_cmark_chunk_literal(data: str) -> _cmarkCmarkChunk:
    length: int
    c: _cmarkCmarkChunk

    if data is not None:
        length = len(data)
    else:
        length = 0

    c = _cmarkCmarkChunk(data, length)
    return c


# 0.29, 0.30
def _cmark_cmark_chunk_dup(ch: _cmarkCmarkChunk, pos: int,
                           length: int) -> _cmarkCmarkChunk:
    c = _cmarkCmarkChunk(copy.deepcopy(ch.data[pos:]), length)
    return c


if __name__ == '__main__':
    pass
