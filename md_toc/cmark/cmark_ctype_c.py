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


# 0.29, 0.30
def _cmark_cmark_ispunct(char: int, parser: str = 'github') -> bool:
    r"""Return True if c is an ascii punctuation character."""
    # license C applies here. See docs/copyright_license.rst.
    value = False
    if chr(char) in md_parser[parser]['pseudo-re']['APC']:
        value = True

    return value
