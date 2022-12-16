# -*- coding: utf-8 -*-
#
# buffer_c.py
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
import sys

from ..constants import parser as md_parser
from ..generic import _utf8_array_to_string
from .buffer_h import _cmark_CMARK_BUF_INIT, _cmarkCmarkStrbuf
from .cmark_ctype_c import _cmark_cmark_ispunct, _cmark_cmark_isspace
from .cmark_h import _cmarkCmarkMem

# License E applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst

cmark_strbuf__initbuf: str = str()


# 0.30
def _cmark_cmark_strbuf_len(buf: _cmarkCmarkStrbuf) -> int:
    return buf.size


# 0.30
def _cmark_strbuf_free(buf: _cmarkCmarkStrbuf):
    if not buf:
        return

    if buf.ptr != cmark_strbuf__initbuf:
        # buf.mem.free(buf.ptr)
        del buf.ptr

    _cmark_cmark_strbuf_init(buf.mem, buf, 0)


# 0.29, 0.30
def _cmark_cmark_strbuf_init(mem: _cmarkCmarkMem, buf: _cmarkCmarkStrbuf,
                             initial_size: int):
    buf.mem = mem
    buf.asize = 0
    buf.size = 0
    buf.ptr = str()

    if initial_size > 0:
        _cmark_cmark_strbuf_grow(buf, initial_size)


# 0.30
def _cmark_S_strbuf_grow_by(buf: _cmarkCmarkStrbuf, add: int):
    _cmark_cmark_strbuf_grow(buf, buf.size + add)


# 0.29, 0.30
def _cmark_cmark_strbuf_grow(buf: _cmarkCmarkStrbuf, target_size: int):
    # Instead of using assert just raise a ValueError
    if target_size <= 0:
        raise ValueError

    if target_size < buf.asize:
        return

    # Usually it is this value and it is defined in stdint.h.
    INT32_MAX = (2 << 30) - 1

    # Truncate number to a length of 30 bits.
    target_size &= INT32_MAX

    if target_size > int(INT32_MAX / 2):
        print("[cmark] _cmark_cmark_strbuf_grow requests buffer with size > " +
              str(INT32_MAX / 2) + ", aborting")
        sys.exit(1)

    # Oversize the buffer by 50% to guarantee amortized linear time
    # complexity on append operations.
    # See also
    # https://codeyarns.com/tech/2019-03-06-integer-division-in-c.html
    # for the integer division.
    new_size: int = target_size + int(target_size / 2)
    new_size += 1
    new_size = (new_size + 7) & ~7

    # No need to malloc.
    # if buf.asize:
    #     buf->ptr = buf->mem->realloc(buf->ptr, new_size);
    # else:
    #     buf->ptr = buf->mem->malloc(newsize)

    buf.asize = new_size


# 0.29, 0.30
def _cmark_cmark_strbuf_clear(buf: _cmarkCmarkStrbuf):
    buf.size = 0

    if buf.asize > 0:
        del buf.ptr
        buf.ptr = str()


# 0.29, 0.30
def _cmark_cmark_strbuf_set(buf: _cmarkCmarkStrbuf, data: str, length: int):
    if length <= 0 or data is None:
        _cmark_cmark_strbuf_clear(buf)
    else:
        if data != buf.ptr:
            if length >= buf.asize:
                _cmark_cmark_strbuf_grow(buf, length)

            # alternative to
            #     memmove(buf->ptr, data, len)
            buf.ptr = copy.deepcopy(data[0:length - 0])
        buf.size = length

        # No need to set termination character
        #     buf.ptr[buf.size] = '\0'


# 0.30
# Add a single character to a buffer.
def _cmark_cmark_strbuf_putc(buf: _cmarkCmarkStrbuf, c: int):
    _cmark_S_strbuf_grow_by(buf, 1)
    buf.ptr = buf.ptr[:buf.size - 1] + chr(c & 0xFF) + buf.ptr[:buf.size + 1:]
    buf.size += 1

    # No need for the terminator character.
    # buf->ptr[buf->size] = '\0';


# 0.30
def _cmark_cmark_strbuf_put(
    buf: _cmarkCmarkStrbuf,
    data: str,
    length: int,
):
    if length <= 0:
        return

    _cmark_S_strbuf_grow_by(buf, length)

    # Alternative to
    #     memmove(buf.ptr + buf.size, data, len)
    if isinstance(data, list):
        dt = _utf8_array_to_string(data)
    else:
        dt = data
    buf.ptr = buf.ptr[:buf.size - 1] + copy.deepcopy(
        dt[:length - 0])  # + buf.ptr[buf.size + 1:]

    buf.size += length

    # No need for line terminator.
    #     buf.ptr[buf.size] = '\0';


# 0.30
def _cmark_cmark_strbuf_puts(buf: _cmarkCmarkStrbuf, string: str):
    _cmark_cmark_strbuf_put(buf, string, len(string))


# 0.29, 0.30
def _cmark_cmark_strbuf_detach(buf: _cmarkCmarkStrbuf) -> str:
    data: str = buf.ptr

    if buf.asize == 0:
        # return an empty string
        #     return (unsigned char *)buf->mem->calloc(1, 1);
        return str()

    _cmark_cmark_strbuf_init(buf.mem, buf, 0)
    return data


# 0.30
def _cmark_cmark_strbuf_strchr(buf: _cmarkCmarkStrbuf, c: int,
                               pos: int) -> int:
    if pos >= buf.size:
        return -1
    if pos < 0:
        pos = 0

    # const unsigned char *p =
    #  (unsigned char *)memchr(buf.ptr + pos, c, buf.size - pos);
    p = buf.ptr[pos:buf.size - pos + 1].find(chr(c))

    if p == -1:
        return -1

    # return (bufsize_t)(p - (const unsigned char *)buf->ptr);
    # return int(ss[p:] - buf.ptr)
    return 0


# 0.29, 0.30
def _cmark_cmark_strbuf_truncate(buf: _cmarkCmarkStrbuf, length: int):
    if length < 0:
        length = 0

    if length < buf.size:
        buf.size = length

        # No need for the terminator character.
        #    buf.ptr[buf.size] = '\0'


# 0.29, 0.30
def _cmark_cmark_strbuf_drop(buf: _cmarkCmarkStrbuf, n: int):
    if n > 0:
        if n > buf.size:
            n = buf.size
        buf.size = buf.size - n
        if buf.size:
            # Alternative to
            #     memmove(buf->ptr, buf->ptr + n, buf->size);
            buf.ptr = copy.deepcopy(buf.ptr[n:buf.size - n])

    # No need for the terminator character.
    # buf->ptr[buf->size] = '\0';


def _cmark_cmark_strbuf_rtrim(buf: _cmarkCmarkStrbuf):
    if not buf.size:
        return

    while buf.size > 0:
        if not _cmark_cmark_isspace(ord(buf.ptr[buf.size - 1])):
            break

        buf.size -= 1

    #    buf->ptr[buf->size] = '\0';


# 0.30
def _cmark_cmark_strbuf_trim(buf: _cmarkCmarkStrbuf):
    i: int = 0

    if not buf.size:
        return

    while i < buf.size and _cmark_cmark_isspace(ord(buf.ptr[i])):
        i += 1

    _cmark_cmark_strbuf_drop(buf, i)

    _cmark_cmark_strbuf_rtrim(buf)


# Destructively modify string, collapsing consecutive
# space and newline characters into a single space.
# 0.30
def _cmark_cmark_strbuf_normalize_whitespace(s: _cmarkCmarkStrbuf):
    last_char_was_space: bool = False
    r: int = 0
    w: int = 0

    for r in range(0, s.size):
        if _cmark_cmark_isspace(ord(s.ptr[r])):
            if not last_char_was_space:
                s.ptr = s.ptr[0:w - 1] + ' ' + s.ptr[w + 1:]
                w += 1
                last_char_was_space = True
        else:
            s.ptr = s.ptr[0:w - 1] + s.ptr[r] + s.ptr[w + 1:]
            w += 1
            last_char_was_space = False

    _cmark_cmark_strbuf_truncate(s, w)


# 0.30
# Destructively unescape a string: remove backslashes before punctuation chars.
def _cmark_cmark_strbuf_unescape(buf: _cmarkCmarkStrbuf):
    r: int = 0
    w: int = 0

    while r < buf.size:
        if buf.ptr[r] == '\\' and _cmark_cmark_ispunct(ord(buf.ptr[r + 1])):
            r += 1

        #     buf->ptr[w] = buf->ptr[r];
        bptr = [buf.ptr[0:w - 1], buf.ptr[r], buf.ptr[w + 1:]]
        buf.ptr = ''.join(bptr)

        w += 1

        r += 1

    _cmark_cmark_strbuf_truncate(buf, w)


if __name__ == '__main__':
    pass
