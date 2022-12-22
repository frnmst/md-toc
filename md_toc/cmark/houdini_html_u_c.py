# -*- coding: utf-8 -*-
#
# houdini_html_u_c.py
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

import re

from ..constants import parser as md_parser
from ..generic import _strncmp
from .buffer_c import (
    _cmark_cmark_strbuf_grow,
    _cmark_cmark_strbuf_put,
    _cmark_cmark_strbuf_putc,
    _cmark_cmark_strbuf_puts,
)
from .buffer_h import _cmarkCmarkStrbuf
from .houdini_h import _cmark_HOUDINI_UNESCAPED_SIZE
from .utf8_c import _cmark_cmark_utf8proc_encode_char

# License F applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# Recursive function of a binary search.
# 0.30.
def _cmark_S_lookup(i: int, low: int, hi: int, s: str, length: int) -> str:
    j: int
    cmp: int = _strncmp(
        s, md_parser['cmark']['re']['ENTITIES']['entities'][i]['entity'],
        length)
    #  if (cmp == 0 && cmark_entities[i].entity[len] == 0) {
    if cmp == 0 and length == len(
            md_parser['cmark']['re']['ENTITIES']['entities'][i]['entity']):
        return md_parser['cmark']['re']['ENTITIES']['entities'][i]['bytes']
    elif cmp == -1 and i > low:
        j = i - int((i - low) / 2)
        if j == i:
            j -= 1
        return _cmark_S_lookup(j, low, i - 1, s, length)
    elif cmp == 1 and i < hi:
        j = i + int((hi - i) / 2)
        if j == i:
            j += 1
        return _cmark_S_lookup(j, i + 1, hi, s, length)
    else:
        return None


# 0.30.
def _cmark_S_lookup_entity(s: str, length: int):
    return _cmark_S_lookup(
        int(md_parser['cmark']['re']['ENTITIES']['CMARK_NUM_ENTITIES'] / 2), 0,
        md_parser['cmark']['re']['ENTITIES']['CMARK_NUM_ENTITIES'] - 1, s,
        length)


# 0.30.
def _cmark_houdini_unescape_ent(ob: _cmarkCmarkStrbuf, src: str,
                                size: int) -> int:
    i: int = 0

    if size >= 3 and src[0] == '#':
        codepoint: int = 0
        num_digits: int = 0
        max_digits: int = 7

        if re.match(r'\d', src[1]):

            i = 1
            while i < size and re.match(r'\d', src[i]):
                codepoint = (codepoint * 10) + (ord(src[i]) - ord('0'))

                if codepoint >= 0x110000:
                    # Keep counting digits but
                    # avoid integer overflow.
                    codepoint = 0x110000

                i += 1

            num_digits = i - 1
            max_digits = 7

        elif src[1] == 'x' or src[1] == 'X':
            i = 2
            while i < size and re.match(r'[\dA-Fa-f]', src[i]):
                codepoint = (codepoint * 16) + ((ord(src[i]) | 32) % 39 - 9)

                if codepoint >= 0x110000:
                    # Keep counting digits but
                    # avoid integer overflow.
                    codepoint = 0x110000

                i += 1

            num_digits = i - 2
            max_digits = 6

        if (num_digits >= 1 and num_digits <= max_digits and i < size
                and src[i] == ';'):
            if (codepoint == 0 or (codepoint >= 0xD800 and codepoint < 0xE000)
                    or codepoint >= 0x110000):
                codepoint = 0xFFFD

            _cmark_cmark_utf8proc_encode_char(codepoint, ob)
            return i + 1

    else:
        if size > md_parser['cmark']['re']['ENTITIES'][
                'CMARK_ENTITY_MAX_LENGTH']:
            size = md_parser['cmark']['re']['ENTITIES'][
                'CMARK_ENTITY_MAX_LENGTH']

        for i in range(
                md_parser['cmark']['re']['ENTITIES']
            ['CMARK_ENTITY_MIN_LENGTH'], size):
            if src[i] == ' ':
                break

            if src[i] == ';':
                entity: str = _cmark_S_lookup_entity(src, i)

                if entity is not None:
                    _cmark_cmark_strbuf_puts(ob, entity)
                    return i + 1

                break

    return 0


# 0.30.
def _cmark_houdini_unescape_html(
    ob: _cmarkCmarkStrbuf,
    src: str,
    size: int,
) -> int:
    i: int = 0
    org: int
    ent: int

    while i < size:
        org = i
        while i < size and src[i] != '&':
            i += 1

        if i > org:
            if org == 0:
                if i >= size:
                    return 0

                _cmark_cmark_strbuf_grow(ob,
                                         _cmark_HOUDINI_UNESCAPED_SIZE(size))

            _cmark_cmark_strbuf_put(ob, src[org:], i - org)

        # escaping
        if i >= size:
            break

        i += 1

        ent = _cmark_houdini_unescape_ent(ob, src[i:], size - i)
        i += ent

        # not really an entity
        if ent == 0:
            _cmark_cmark_strbuf_putc(ob, ord('&'))

    return 1


def _cmark_houdini_unescape_html_f(
    ob: _cmarkCmarkStrbuf,
    src: str,
    size: int,
):
    if not _cmark_houdini_unescape_html(ob, src, size):
        _cmark_cmark_strbuf_put(ob, src, size)
