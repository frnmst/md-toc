#
# scanners_h.py
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

from .chunk_h import _cmarkCmarkChunk
from .scanners_c import _cmark__scan_at


def _cmark_scan_spacechars(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_spacechars', c, n)


def _cmark_scan_link_title(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_link_title', c, n)