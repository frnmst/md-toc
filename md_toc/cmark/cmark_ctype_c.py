#
# cmark_ctype_c.py
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
r"""The cmark implementation file."""

import string
import unicodedata

from ..constants import parser as md_parser

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# Return True if c is a "whitespace" character as defined by the spec.
# 0.30
def _cmark_cmark_isspace(char: int) -> bool:
    # A Unicode whitespace character is any code point in the Unicode Zs
    # general category, or a tab (U+0009), line feed (U+000A), form feed
    # (U+000C), or carriage return (U+000D).
    return (unicodedata.category(chr(char)) == 'Zs'
            or chr(char) in ['\u0009', '\u000A', '\u000C', '\u000D'])


# Return True if c is an ascii punctuation character.
# 0.29, 0.30
def _cmark_cmark_ispunct(char: int) -> bool:
    return chr(char) in string.punctuation


if __name__ == '__main__':
    pass
