# Copyright (C) 2017-2022 Franco Masotti (see /README.md)
# SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
