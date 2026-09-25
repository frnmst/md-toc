# Copyright (C) 2017-2022 Franco Masotti (see /README.md)
# SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)
#
# SPDX-License-Identifier: GPL-3.0-or-later
r"""A cmark implementation file."""

from .cmark_h import _cmarkCmarkMem

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# 0.30
class _cmarkCmarkReference:
    __slots__ = [
        'next',
        'label',
        'url',
        'title',
        'age',
        'size',
    ]

    def __init__(self):
        self.next: _cmarkCmarkReference = None
        self.label: str = None
        self.url: str = None
        self.title: str = None
        self.age: int = 0
        self.size: int = 0


# 0.30
class _cmarkCmarkReferenceMap:
    __slots__ = [
        'mem',
        'refs',
        'sorted',
        'size',
        'ref_size',
        'max_ref_size',
    ]

    def __init__(self):
        self.mem: _cmarkCmarkMem = None
        self.refs: _cmarkCmarkReference = None
        # A list of _cmarkCmarkReference
        self.sorted: list = None
        self.size: int = 0
        self.ref_size: int = 0
        self.max_ref_size: int = 0


if __name__ == '__main__':
    pass
