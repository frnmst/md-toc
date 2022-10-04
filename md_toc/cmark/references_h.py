# -*- coding: utf-8 -*-
#
# reference_h.py
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
