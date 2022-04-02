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

from .buffer_h import _cmark_CMARK_BUF_INIT, _cmarkCmarkStrbuf
from .cmark_h import _cmarkCmarkMem

# License E applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# 0.29, 0.30
def _cmark_cmark_strbuf_init(mem: _cmarkCmarkMem, buf: _cmarkCmarkStrbuf, initial_size: int):
    buf.mem = mem
    buf.asize = 0
    buf.size = 0
    buf.ptr = str()

    if initial_size > 0:
        _cmark_cmark_strbuf_grow(buf, initial_size)


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

    if target_size > INT32_MAX / 2:
        print("[cmark] _cmark_cmark_strbuf_grow requests buffer with size > " + str(INT32_MAX / 2) + ", aborting")
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
            buf.ptr = copy.deepcopy(data[0:length])
        buf.size = length

        # No need to set termination character
        #     buf.ptr[buf.size] = '\0'


# 0.29, 0.30
def _cmark_cmark_strbuf_detach(buf: _cmarkCmarkStrbuf) -> str:
    data: str = buf.ptr

    if buf.asize == 0:
        # return an empty string
        #     return (unsigned char *)buf->mem->calloc(1, 1);
        return str()

    _cmark_cmark_strbuf_init(buf.mem, buf, 0)
    return data


# 0.29, 0.30
def _cmark_cmark_strbuf_truncate(buf: _cmarkCmarkStrbuf, len: int):
    if len < 0:
        len = 0

    if len < buf.size:
        buf.size = len

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
            buf.ptr = copy.deepcopy(buf.ptr[n:buf.size])

    # No need for the terminator character.
    # buf->ptr[buf->size] = '\0';


if __name__ == '__main__':
    pass
