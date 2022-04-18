#
# scanners_c.py
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

import copy
import re

from ..constants import parser as md_parser
from .chunk_h import _cmarkCmarkChunk

# These functions have been re-written to avoid GOTO jumps,
# also using the scanners.re source file.
# The original C source states:
# /* Generated by re2c 1.3 */


def _cmark__scan_at(scanner_function_name: str, c: _cmarkCmarkChunk,
                    offset: int) -> int:
    res: int
    ptr: str = c.data

    if ptr is None or offset > c.length:
        return 0
    else:
        #     lim: str = ptr[c.length]

        #     ptr[c.length] = '\0'
        if scanner_function_name == '_cmark__scan_spacechars':
            res = _cmark__scan_spacechars(ptr, offset)
        if scanner_function_name == '_cmark__scan_link_title':
            res = _cmark__scan_link_title(ptr, offset)

        #     ptr[c.length] = lim

    return res


# Try to match a link title (in single quotes, in double quotes, or
# in parentheses), returning number of chars matched.  Allow one
# level of internal nesting (quotes within quotes).
def _cmark__scan_link_title(ptr: str, p: int) -> int:
    start_match: int = 0
    end_match: int = 0

    r1 = '["] (' + md_parser['cmark']['re']['SCANNERS']['escaped_char'] + '|[^"\u0000])* ["]'
    r2 = "['] (" + md_parser['cmark']['re']['SCANNERS']['escaped_char'] + "|[^'\u0000])* [']"
    r3 = r'[\(] (' + md_parser['cmark']['re']['SCANNERS']['escaped_char'] + r"|[^\(\)\u0000])* [']"
    r = '(' + r1 + '|' + r2 + '|' + r3 + ')'
    span = re.match(r, ptr[p:])
    if span:
        ll = list(span.span())
        start_match = ll[0]
        end_match = ll[1]
        retval = end_match - start_match
    else:
        retval = 0

    return retval


# Match SOME space characters, including newlines.
def _cmark__scan_spacechars(ptr: str, p: int) -> int:
    start_match: int = 0
    end_match: int = 0

    # Match matches from the start of the string.
    span = re.match(md_parser['cmark']['re']['SCANNERS']['spacechar'], ptr[p:])
    if span:
        ll = list(span.span())
        start_match = ll[0]
        end_match = ll[1]
        retval = end_match - start_match
    else:
        retval = 0

    return retval