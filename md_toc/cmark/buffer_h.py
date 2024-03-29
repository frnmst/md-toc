#
# buffer_h.py
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
r"""A cmark implementation file."""

from dataclasses import dataclass
from typing import Optional

from .cmark_h import _cmarkCmarkMem

# License E applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# 0.29, 0.30
@dataclass
class _cmarkCmarkStrbuf:
    mem: Optional[_cmarkCmarkMem] = None
    ptr: str = ''
    asize: int = 0
    size: int = 0


# Should be equivalent to
#     #define CMARK_BUF_INIT(mem) \
#       { mem, cmark_strbuf__initbuf, 0, 0 }
# 0.29, 0.30
def _cmark_CMARK_BUF_INIT(mem: _cmarkCmarkMem):
    b = _cmarkCmarkStrbuf()
    b.mem = mem

    return b


if __name__ == '__main__':
    pass
