# -*- coding: utf-8 -*-
#
# reference_c.py
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

import functools

from ..constants import parser as md_parser
from .buffer_c import (
    _cmark_cmark_strbuf_detach,
    _cmark_cmark_strbuf_normalize_whitespace,
    _cmark_cmark_strbuf_trim,
)
from .buffer_h import _cmark_CMARK_BUF_INIT, _cmarkCmarkStrbuf
from .chunk_h import _cmarkCmarkChunk
from .cmark_h import _cmarkCmarkMem
from .references_h import _cmarkCmarkReference, _cmarkCmarkReferenceMap
from .utf8_c import _cmark_cmark_utf8proc_case_fold

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# normalize reference:  collapse internal whitespace to single space,
# remove leading/trailing whitespace, case fold
# Return NULL if the reference name is actually empty (i.e. composed
# solely from whitespace)
# 0.30
def _cmark_normalize_reference(mem: _cmarkCmarkMem,
                               ref: _cmarkCmarkChunk) -> str:
    normalized: _cmarkCmarkStrbuf = _cmark_CMARK_BUF_INIT(mem)
    result: str

    if ref is None:
        return None

    if ref.length == 0:
        return None

    _cmark_cmark_utf8proc_case_fold(normalized, ref.data, ref.length)
    _cmark_cmark_strbuf_trim(normalized)
    _cmark_cmark_strbuf_normalize_whitespace(normalized)

    result = _cmark_cmark_strbuf_detach(normalized)
    if not result:
        raise ValueError

    #     if result[0] == '\0':
    if result == str():
        #     mem.free(result)
        del result
        return None

    return result


def _cmark_labelcmp(a: str, b: str) -> bool:
    return a == b


def _cmark_refcmp(p1: _cmarkCmarkReference, p2: _cmarkCmarkReference) -> int:
    res: bool = _cmark_labelcmp(p1.label, p2.label)

    if res:
        return res
    else:
        return p1.age - p2.age


def _cmark_sort_references(maps: _cmarkCmarkReferenceMap):
    i: int
    last: int = 0
    size: int = maps.size
    r: _cmarkCmarkReference = maps.refs

    #     **sorted = NULL;
    # A list of _cmarkCmarkReference
    srt: list = list()

    #     sorted = (cmark_reference **)maps->mem->calloc(size, sizeof(cmark_reference *));
    while (r):
        srt.append(r)
        r = r.next

    #     qsort(sorted, size, sizeof(cmark_reference *), refcmp);
    srt = sorted(srt, key=functools.cmp_to_key(_cmark_refcmp))

    for i in range(1, size):
        if _cmark_labelcmp(srt[i].label, srt[last].label) != 0:
            last += 1
            srt[last] = srt[i]

    maps.sorted = srt
    maps.size = last + 1


# Returns reference if refmaps contains a reference with matching
# label, otherwise NULL.
# 0.30
def _cmark_cmark_reference_lookup(
    maps: _cmarkCmarkReferenceMap,
    label: _cmarkCmarkChunk,
) -> _cmarkCmarkReference:
    # A list of _cmarkCmarkReference
    ref: list = None
    r: _cmarkCmarkReference = None
    norm: str

    #     MAX_LINK_LABEL_LENGTH
    if label.length < 1 or label.length > md_parser['cmark']['link'][
            'max chars label'] + 1:
        return None

    if maps is None or not maps.size:
        return None

    norm = _cmark_normalize_reference(maps.mem, label)
    if norm is None:
        return None

    if not maps.sorted:
        _cmark_sort_references(maps)

    # TODO
    #      ref = (cmark_reference **)bsearch(norm, maps->sorted, maps->size, sizeof(cmark_reference *),
    #                    refsearch);
    # FIXME

    #     maps->mem->free(norm);
    del norm

    if ref is not None:
        r = ref[0]
        # Check for expansion limit
        if maps.max_ref_size and r.size > maps.max_ref_size - maps.ref_size:
            return None
        maps.ref_size += r.size

    return r
