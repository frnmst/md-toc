# Copyright (C) 2017-2022 Franco Masotti (see /README.md)
# SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
