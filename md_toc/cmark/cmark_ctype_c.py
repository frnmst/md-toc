# -*- coding: utf-8 -*-
#
# cmark_ctype_c.py
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

from ..constants import parser as md_parser

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# Return True if c is a "whitespace" character as defined by the spec.
# 0.30
def _cmark_cmark_isspace(char: int) -> bool:
    value = False
    if chr(char) in md_parser['cmark']['pseudo-re']['UWC']:
        value = True

    return value


# Return True if c is an ascii punctuation character.
# 0.29, 0.30
def _cmark_cmark_ispunct(char: int) -> bool:
    value = False
    if chr(char) in md_parser['cmark']['pseudo-re']['APC']:
        value = True

    return value


if __name__ == '__main__':
    pass
