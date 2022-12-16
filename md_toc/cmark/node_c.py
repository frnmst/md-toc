# -*- coding: utf-8 -*-
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
from .cmark_h import _cmarkCmarkMem
from .node_h import _cmarkCmarkNode

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# 0.30
def _cmark_S_is_block(node: _cmarkCmarkNode) -> bool:
    if node is None:
        return False
    return (node.type >=
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_FIRST_BLOCK']
            and node.type <=
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_LAST_BLOCK'])


# 0.30
def _cmark_S_is_inline(node: _cmarkCmarkNode) -> bool:
    if node is None:
        return False
    return (node.type >=
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_FIRST_INLINE']
            and node.type <=
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_LAST_INLINE'])


# 0.30
def _cmark_S_can_contain(node: _cmarkCmarkNode,
                         child: _cmarkCmarkNode) -> bool:
    if (node is None or child is None or node == child):
        return False

    # Verify that child is not an ancestor of node.
    if child.first_child is not None:
        cur: _cmarkCmarkNode = node.parent

        while cur is not None:
            if cur == child:
                return False
            cur = cur.parent

    if child.type == md_parser['cmark']['cmark_node_type'][
            'CMARK_NODE_DOCUMENT']:
        return False

    if node.type in [
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_DOCUMENT'],
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_BLOCK_QUOTE'],
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_ITEM'],
    ]:
        return _cmark_S_is_block(child) and child.type != md_parser['cmark'][
            'cmark_node_type']['CMARK_NODE_ITEM']

    elif node.type in [
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_LIST']
    ]:
        return child.type == md_parser['cmark']['cmark_node_type'][
            'CMARK_NODE_ITEM']

    elif node.type in [
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_CUSTOM_BLOCK']
    ]:
        return True

    elif node.type in [
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_PARAGRAPH'],
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_HEADING'],
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_EMPH'],
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_STRONG'],
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_LINK'],
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_IMAGE'],
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_CUSTOM_INLINE'],
    ]:
        return _cmark_S_is_inline(child)

    return False


# Free a cmark_node list and any children.
# 0.30
def _cmark_S_free_nodes(e: _cmarkCmarkNode):
    # mem: _cmarkCmarkMem = e.mem
    next: _cmarkCmarkNode

    while e is not None:
        if e.type in [
                md_parser['cmark']['cmark_node_type']['CMARK_NODE_CODE_BLOCK']
        ]:
            del e.data
            del e.as_code.info
            e.data = str()
            e.as_code.info = str()
        elif e.type in [
                md_parser['cmark']['cmark_node_type']['CMARK_NODE_TEXT'],
                md_parser['cmark']['cmark_node_type']
            ['CMARK_NODE_HTML_INLINE'],
                md_parser['cmark']['cmark_node_type']['CMARK_NODE_CODE'],
                md_parser['cmark']['cmark_node_type']['CMARK_NODE_HTML_BLOCK'],
        ]:
            del e.data
            e.data = str()
        elif e.type in [
                md_parser['cmark']['cmark_node_type']['CMARK_NODE_LINK'],
                md_parser['cmark']['cmark_node_type']['CMARK_NODE_IMAGE'],
        ]:
            del e.as_link.url
            del e.as_link.title
            e.as_link.url = str()
            e.as_link.title = str()
        elif e.type in [
                md_parser['cmark']['cmark_node_type']
            ['CMARK_NODE_CUSTOM_BLOCK'],
                md_parser['cmark']['cmark_node_type']
            ['CMARK_NODE_CUSTOM_INLINE'],
        ]:
            del e.as_custom.on_enter
            del e.as_custom.on_exit
            e.as_custom.on_enter = str()
            e.as_custom.on_exit = str()

        if e.last_child:
            # Splice children into list
            e.last_child.next = e.next
            e.next = e.first_child

        next = e.next
        #     mem->free(e);
        del e
        e = next


# 0.30
def _cmark_cmark_node_free(node: _cmarkCmarkNode):
    _cmark_S_node_unlink(node)
    node.next = None
    _cmark_S_free_nodes(node)


# 0.30
def _cmark_cmark_set_cstr(mem: _cmarkCmarkMem, dst: str, src: str) -> tuple:
    old: str = dst
    length: int

    if src and src[0]:
        length = len(src)

        # Alternative to:
        #     *dst = (unsigned char *)mem->realloc(NULL, len + 1);
        #     memcpy(*dst, src, len + 1);
        dst = copy.deepcopy(src[:length + 1])
    else:
        length = 0
        dst = str()

    if old:
        # Alternative to:
        #     mem->free(old);
        del old
        del dst
        dst = str()

    return length, dst


# 0.30
def _cmark_cmark_node_set_literal(node: _cmarkCmarkNode, content: str) -> int:
    length: int
    data: str

    if node is None:
        return 0

    if (node.type
            == md_parser['cmark']['cmark_node_type']['CMARK_NODE_HTML_BLOCK']
            or node.type
            == md_parser['cmark']['cmark_node_type']['CMARK_NODE_TEXT']
            or node.type
            == md_parser['cmark']['cmark_node_type']['CMARK_NODE_HTML_INLINE']
            or node.type
            == md_parser['cmark']['cmark_node_type']['CMARK_NODE_CODE']
            or node.type
            == md_parser['cmark']['cmark_node_type']['CMARK_NODE_CODE_BLOCK']):
        length, data = _cmark_cmark_set_cstr(node.mem, node.data, content)
        node.length = length
        node.data = data
        return 1

    return 0


# 0.29, 0.30
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


# 0.30
def _cmark_cmark_node_unlink(node: _cmarkCmarkNode):
    _cmark_S_node_unlink(node)

    node.next = None
    node.prev = None
    node.parent = None


# Inserts 'sibling' before 'node'.  Returns 1 on success, 0 on failure.
# 0.30
def _cmark_cmark_node_insert_before(node: _cmarkCmarkNode,
                                    sibling: _cmarkCmarkNode) -> int:
    if node is None or sibling is None:
        return 0

    if not node.parent or not _cmark_S_can_contain(node.parent, sibling):
        return 0

    _cmark_S_node_unlink(sibling)

    old_prev: _cmarkCmarkNode = node.prev

    # Insert 'sibling' between 'old_prev' and 'node'.
    if old_prev:
        old_prev.next = sibling
    sibling.prev = old_prev
    sibling.next = node
    node.prev = sibling

    # Set new parent.
    parent: _cmarkCmarkNode = node.parent
    sibling.parent = parent

    # Adjust first_child of parent if inserted as first child.
    if parent and not old_prev:
        parent.first_child = sibling

    return 1


def _cmark_cmark_node_insert_after(node: _cmarkCmarkNode,
                                   sibling: _cmarkCmarkNode) -> int:
    if node is None or sibling is None:
        return 0

    if not node.parent or not _cmark_S_can_contain(node.parent, sibling):
        return 0

    _cmark_S_node_unlink(sibling)

    old_next = node.next

    # Insert 'sibling' between 'node' and 'old_next'.
    if old_next:
        old_next.prev = sibling

    sibling.next = old_next
    sibling.prev = node
    node.next = sibling

    # Set new parent.
    parent: _cmarkCmarkNode = node.parent
    sibling.parent = parent

    # Adjust last_child of parent if inserted as last child.
    if parent and not old_next:
        parent.last_child = sibling

    return 1


if __name__ == '__main__':
    pass
