#
# node_h.py
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


class _cmarkCmarkNode:
    def __init__(self):
        # cmark_strbuf

        # _cmarkCmarkMem
        self.mem = None
        self.type = None

        # Main.
        self.data = None
        self.length = 0

        self.prev = None
        self.next = None
        self.parent = None
        self.first_child = None
        self.last_child = None

        self.user_data = None

        self.start_line = 0
        self.start_column = 0
        self.end_line = 0
        self.end_column = 0
        self.internal_offset = 0

        # Add a new variable.
        self.numdelims: int = 0

    def append_child(self):
        pass

    def append_child_lite(self, child):
        old_last_child: _cmarkCmarkNode = self.last_child

        child.next = None
        child.prev = old_last_child
        child.parent = self
        self.last_child = child

        if old_last_child:
            old_last_child.next = child
        else:
            # Also set first_child if node previously had no children.
            self.first_child = child


if __name__ == '__main__':
    pass
