#
# cmark_reference_h.py
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
r"""The cmark implementation file."""

from ..generic import _noop

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


class _cmarkCmarkReference:
    def __init__(self):
        next = None
        label: str = None
        url: str = None
        title: str = None
        age: int = 0
        size: int = 0

        _noop(next)
        _noop(label)
        _noop(url)
        _noop(title)
        _noop(age)
        _noop(size)


class _cmarkCmarkReferenceMap:
    def __init__(self):
        mem = None
        refs: _cmarkCmarkReference
        sorted: _cmarkCmarkReference
        size: int = 0
        ref_size: int = 0
        max_ref_size: int = 0

        _noop(mem)
        _noop(size)
        _noop(ref_size)
        _noop(max_ref_size)


if __name__ == '__main__':
    pass
