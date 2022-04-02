#
# node_c.py
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

from ..constants import parser as md_parser
from ..generic import _noop
from .node_h import _cmarkCmarkNode

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# 0.30
def _cmark_S_free_nodes(e: _cmarkCmarkNode):
    mem = e.mem
    next: _cmarkCmarkNode
    _noop(mem)

    while e is not None:
        # No need to run free operations.

        if e.last_child:
            # Splice children into list
            e.last_child.next = e.next
            e.next = e.first_child

        next = e.next

        # mem->free(e);

        e = next


# 0.30
def _cmark_cmark_node_free(node: _cmarkCmarkNode):
    _cmark_S_node_unlink(node)
    node.next = None
    _cmark_S_free_nodes(node)


# 0.30
def _cmark_cmark_set_cstr(mem, dst: str, src: str) -> int:
    old: str = dst
    length: int

    _noop(old)

    if src and src[0]:
        length = len(src)

        # Alternative to:
        #     *dst = (unsigned char *)mem->realloc(NULL, len + 1);
        #     memcpy(*dst, src, len + 1);
        dst = copy.deepcopy(src)
    else:
        length = 0
        dst = None

    # No need to free in Python.

    return length


# 0.30
def _cmark_cmark_node_set_literal(node: _cmarkCmarkNode, content: str) -> int:
    if node is None:
        return 0

    if (node.type == md_parser['cmark']['cmark_node_type']['CMARK_NODE_HTML_BLOCK']
       or node.type == md_parser['cmark']['cmark_node_type']['CMARK_NODE_TEXT']
       or node.type == md_parser['cmark']['cmark_node_type']['CMARK_NODE_HTML_INLINE']
       or node.type == md_parser['cmark']['cmark_node_type']['CMARK_NODE_CODE']
       or node.type == md_parser['cmark']['cmark_node_type']['CMARK_NODE_CODE_BLOCK']):
        length, data = _cmark_cmark_set_cstr(node.mem, content)
        node.length = length
        node.data = data
        return 1

    return 0


# 0.30
# Unlink a node without adjusting its next, prev, and parent pointers.
def _cmark_S_node_unlink(node: _cmarkCmarkNode):
    if node is None:
        return

    if node.prev:
        node.prev.next = node.next
    if node.next:
        node.next.prev = node.prev

    # Adjust first_child and last_child of parent.
    # Start and end pointers.
    parent: _cmarkCmarkNode = node.parent
    if parent:
        if parent.first_child == node:
            parent.first_child = node.next
        if parent.last_child == node:
            parent.last_child = node.prev


if __name__ == '__main__':
    pass
