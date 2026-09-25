# Copyright (C) 2017-2022 Franco Masotti (see /README.md)
# SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)
#
# SPDX-License-Identifier: GPL-3.0-or-later
r"""The cmark implementation file."""

import copy
from dataclasses import dataclass

from ..constants import parser as md_parser
from .cmark_ctype_c import _cmark_cmark_isspace

# License E applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst

# Returns 1 if c is a "whitespace" character as defined by the spec.
#   int cmark_isspace(char c) { return cmark_ctype_class[(uint8_t)c] == 1; }
# The only defined whitespaces in the spec are Unicode whitespaces.


# 0.30
@dataclass
class _cmarkCmarkChunk:
    data: str = None
    length: int = 0


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
