# -*- coding: utf-8 -*-
#
# cmark_h.py
#
# Copyright (C) 2017-2022 Franco Masotti (see /README.md)
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

from enum import Enum

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# Defines the memory allocation functions to be used by CMark
# when parsing and allocating a document tree
#     typedef struct cmark_mem {
#       void *(*calloc)(size_t, size_t);
#       void *(*realloc)(void *, size_t);
#       void (*free)(void *);
#     } cmark_mem;
class _cmarkCmarkMem:
    pass


# C enum
# typedef enum { ... } cmark_node_type;
# Undefined value in the C source code get their value
# accoring to their position in the sequence, like an array.
class _cmarkCmarkNodeType(Enum):
    # Error status.
    CMARK_NODE_NONE = 0

    # Block.
    CMARK_NODE_DOCUMENT = 1
    CMARK_NODE_BLOCK_QUOTE = 2
    CMARK_NODE_LIST = 3
    CMARK_NODE_ITEM = 4
    CMARK_NODE_CODE_BLOCK = 5
    CMARK_NODE_HTML_BLOCK = 6
    CMARK_NODE_CUSTOM_BLOCK = 7
    CMARK_NODE_PARAGRAPH = 8
    CMARK_NODE_HEADING = 9
    CMARK_NODE_THEMATIC_BREAK = 10

    CMARK_NODE_FIRST_BLOCK = CMARK_NODE_DOCUMENT
    CMARK_NODE_LAST_BLOCK = CMARK_NODE_THEMATIC_BREAK

    # Inline
    CMARK_NODE_TEXT = 11
    CMARK_NODE_SOFTBREAK = 12
    CMARK_NODE_LINEBREAK = 13
    CMARK_NODE_CODE = 14
    CMARK_NODE_HTML_INLINE = 15
    CMARK_NODE_CUSTOM_INLINE = 16
    CMARK_NODE_EMPH = 17
    CMARK_NODE_STRONG = 18
    CMARK_NODE_LINK = 19
    CMARK_NODE_IMAGE = 20

    CMARK_NODE_FIRST_INLINE = CMARK_NODE_TEXT
    CMARK_NODE_LAST_INLINE = CMARK_NODE_IMAGE

    # For backwards compatibility:
    CMARK_NODE_HEADER = CMARK_NODE_HEADING
    CMARK_NODE_HRULE = CMARK_NODE_THEMATIC_BREAK
    CMARK_NODE_HTML = CMARK_NODE_HTML_BLOCK
    CMARK_NODE_INLINE_HTML = CMARK_NODE_HTML_INLINE


CMARK_OPT_SOURCEPOS = 1 << 1
CMARK_OPT_SMART = 1 << 10

if __name__ == '__main__':
    pass
