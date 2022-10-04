# -*- coding: utf-8 -*-
#
# cmark_h.py
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

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# Defines the memory allocation functions to be used by CMark
# when parsing and allocating a document tree
#     typedef struct cmark_mem {
#       void *(*calloc)(size_t, size_t);
#       void *(*realloc)(void *, size_t);
#       void (*free)(void *);
#     } cmark_mem;
class _cmarkCmarkMem:
    pass


if __name__ == '__main__':
    pass
