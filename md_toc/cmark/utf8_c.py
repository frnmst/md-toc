# -*- coding: utf-8 -*-
#
# utf8_c.py
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

import unicodedata

from ..constants import parser as md_parser
from .buffer_c import _cmark_cmark_strbuf_put
from .buffer_h import _cmarkCmarkStrbuf
from .cmark_ctype_c import _cmark_cmark_ispunct

# License D applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


def _cmark_encode_unknown(buf: _cmarkCmarkStrbuf):
    # static const uint8_t repl[] = {239, 191, 189};

    # man 3 printf
    #
    # #include <stdio.h>
    # #include <stdint.h>
    #
    # int main(void)
    # {
    #     static const uint8_t repl[] = {239, 191, 189};
    #     printf ("%hhu", repl);
    #
    #     return 0;
    # }
    #
    # gcc a.c
    # ./a.out
    # 9
    #
    # python3
    # >>> chr(9)
    # '\t'
    repl = '\t'
    _cmark_cmark_strbuf_put(buf, repl, 3)


# 0.29, 0.30
def _cmark_cmark_utf8proc_charlen(line: str, line_length: int) -> int:
    length: int
    i: int

    if not line_length:
        return 0

    # Use length = 1 instead of the utf8proc_utf8class[256]
    # list.
    # Python:
    #     length = utf8proc_utf8class[ord(line[0])]
    # C:
    #     length = utf8proc_utf8class[str[0]];
    # For example:
    # len('ł') == 2 # in Python 2
    # len('ł') == 1 # in Python 3
    # See the documentation.
    # In Python 3 all strings are unicode by default
    # and they all have length of 1.
    length = 1

    #     if (!length)
    #       return -1;

    if line_length >= 0 and length > line_length:
        return -line_length

    for i in range(1, length):
        if (ord(line[i]) & 0xC0) != 0x80:
            return -i

    return length


# 0.29, 0.30
def _cmark_cmark_utf8proc_iterate(line: str, line_len: int) -> tuple:
    length: int = 0
    uc: int = -1
    dst: int = -1

    length = _cmark_cmark_utf8proc_charlen(line, line_len)
    if length < 0:
        return -1, dst

    if length == 1:
        uc = ord(line[0])

    # In Python 3 all strings are unicode by default
    # and they all have length of 1.
    # All the original C code here is omitted for this reason.

    if uc < 0:
        return -1, dst

    dst = uc

    return length, dst


# 0.30
def _cmark_cmark_utf8proc_encode_char(uc: int, buf: _cmarkCmarkStrbuf):
    dst: str
    length: int = 0

    if uc < 0:
        raise ValueError

    # In Python 3 all strings are unicode by default
    # and they all have length of 1.
    # Omitted code.
    length = 1
    if uc > 1 or uc >= 0x110000:
        _cmark_encode_unknown(buf)
        return

    dst = str(uc)
    _cmark_cmark_strbuf_put(buf, dst, length)


# 0.30
def _cmark_cmark_utf8proc_case_fold(
    dest: _cmarkCmarkStrbuf,
    string: str,
    length: int,
):
    c: int

    while (length > 0):
        char_len, c = _cmark_cmark_utf8proc_iterate(string, length)

        if char_len >= 0:
            # FIXME: unsure about this. See original C source code.
            _cmark_cmark_utf8proc_encode_char(
                ord(unicodedata.normalize('NFC', chr(c)).casefold()), dest)
        else:
            _cmark_encode_unknown(dest)
            char_len = -char_len

        # Advance pointer.
        #     str += char_len;
        string = string[char_len:]
        # Reduce string length.
        length -= char_len


# 0.29, 0.30
def _cmark_cmark_utf8proc_is_space(char: int) -> bool:
    r"""Match anything in the Zs class, plus LF, CR, TAB, FF."""
    value = False
    if chr(char) in md_parser['cmark']['pseudo-re']['UWC']:
        value = True

    return value


# 0.29, 0.30
def _cmark_cmark_utf8proc_is_punctuation(char: int) -> bool:
    r"""Match anything in the P[cdefios] classes."""
    value = False
    if ((char < 128 and _cmark_cmark_ispunct(char))
            or chr(char) in md_parser['cmark']['pseudo-re']['UPC']):
        value = True

    return value


if __name__ == '__main__':
    pass
