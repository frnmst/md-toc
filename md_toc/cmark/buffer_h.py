# Copyright (C) 2017-2022 Franco Masotti (see /README.md)
# SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)
#
# SPDX-License-Identifier: GPL-3.0-or-later
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
