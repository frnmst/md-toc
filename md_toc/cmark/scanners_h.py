# -*- coding: utf-8 -*-
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

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


def _cmark_scan_spacechars(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_spacechars', c, n)


def _cmark_scan_link_title(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_link_title', c, n)


def _cmark_scan_autolink_uri(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_autolink_uri', c, n)


def _cmark_scan_autolink_email(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_autolink_email', c, n)


def _cmark_scan_html_comment(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_html_comment', c, n)


def _cmark_scan_html_cdata(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_cdata', c, n)


def _cmark_scan_html_tag(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_html_tag', c, n)


def _cmark_scan_html_declaration(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_html_declaration', c, n)


def _cmark_scan_html_pi(c: _cmarkCmarkChunk, n: int) -> int:
    return _cmark__scan_at('_cmark__scan_html_pi', c, n)
