#
# cmark.py
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
"""The cmark implementation file."""

import copy
import sys

from ..constants import parser as md_parser
from ..exceptions import CannotTreatUnicodeString
from ..generic import _noop, _replace_substring


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


class _cmarkCmarkNode:
    # license C applies here. See docs/copyright_license.rst
    def __init__(self):
        # cmark_strbuf

        # /** Defines the memory allocation functions to be used by CMark
        # * when parsing and allocating a document tree
        # */
        # typedef struct cmark_mem {
        #   void *(*calloc)(size_t, size_t);
        #   void *(*realloc)(void *, size_t);
        #   void (*free)(void *);
        # } cmark_mem;
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


class _cmarkCmarkChunk:
    r"""See chunk.h file."""

    # license E applies here. See docs/copyright_license.rst

    def __init__(self, data: str = None, length: int = 0, alloc: int = 0):
        self.data: str = data
        self.length: int = length

        # also implies a NULL-terminated string
        self.alloc: int = alloc


class _cmarkDelimiter:
    r"""A list node with attributes useful for processing emphasis."""

    # license C applies here. See docs/copyright_license.rst

    def __init__(self, delim_char: str, length: int):
        self.previous = None
        self.next = None

        # _cmarkCmarkNode
        self.inl_text = None

        self.literal = None

        self.delim_char = delim_char
        self.length = length
        self.offset = 0
        self.original_length = length
        self.active = True
        self.can_open = False
        self.can_close = False

    def __str__(self):
        if self.delim_char is not None:
            if self.previous is None:
                previous = 'None'
            else:
                previous = hex(id(self.previous))
            if self.next is None:
                next = 'None'
            else:
                next = hex(id(self.next))

            el = '== element ' + hex(id(self)) + " =="
            it = 'inl_text = ' + str(self.inl_text)
            li = 'literal = ' + str(self.literal)
            de = 'delim_char = ' + self.delim_char
            le = 'length = ' + str(self.length)
            of = 'offset = ' + str(self.offset)
            oi = 'original_length = ' + str(self.original_length)
            ac = 'active = ' + str(self.active)
            pr = 'previous = ' + previous
            ne = 'next = ' + next
            co = 'can_open = ' + str(self.can_open)
            cc = 'can_close = ' + str(self.can_close)

            return (el + '\n' + it + '\n' + li + '\n' + de + '\n' + le + '\n' + of + '\n' + oi + '\n'
                    + ac + '\n' + pr + '\n' + ne + '\n' + co + '\n'
                    + cc + '\n')


class _cmarkSubject:
    r"""A double linked list useful for processing emphasis."""

    # license C applies here. See docs/copyright_license.rst

    def __init__(self):
        r"""Define the memory allocation functions to be used by CMark when parsing and allocating a document tree.

        typedef struct cmark_mem {
          void *(*calloc)(size_t, size_t);
          void *(*realloc)(void *, size_t);
          void (*free)(void *);
        } cmark_mem;
        """
        self.mem = None

        self.line = 0
        self.pos = 0
        self.block_offset = 0
        self.column_offset = 0
        self.start = None
        self.last_delim = None
        self.last_bracket = None

        # This corresponds to the line.
        # cmark_chunk input
        self.input: _cmarkCmarkChunk = None

        self.refmap: _cmarkCmarkReferenceMap = None
        self.backticks: list = list(range(0, md_parser['cmark']['generic']['MAXBACKTICKS']))
        self.scanned_for_backticks: bool = False

    def push(self, node: _cmarkDelimiter):
        r"""Add a new node."""
        if self.start is None and self.last_delim is None:
            # Empty list.
            self.start = self.last_delim = node
        else:
            self.last_delim.next = node
            node.previous = self.last_delim

            if node.previous is not None:
                # Connect last exising node to new node.
                node.previous.next = node

            self.last_delim = self.last_delim.next
            node.next = None

    def pop(self) -> _cmarkDelimiter:
        r"""Remove the last node."""
        node = None
        if self.start is None and self.last_delim is None:
            pass
        else:
            node = self.last_delim
            self.last_delim = node.previous

            if self.last_delim is None:
                self.start = None

        return node

    def extract(self, delim: _cmarkDelimiter):
        r"""Remove a specific node.

        This method is equivalent to the remove_delimiter
        function in inlines.c
        """
        if delim is None:
            return

        if delim.next is None:
            # end of list:
            if delim != self.last_delim:
                raise ValueError

            self.last_delim = delim.previous
        else:
            delim.next.previous = delim.previous

        if delim.previous is not None:
            delim.previous.next = delim.next
        # subj.mem.free(delim)

    def scroll(self):
        r"""Print the list."""
        print(self.start)
        print("===")
        x = self.start
        while x is not None:
            print(x)
            x = x.next


class _cmarkBracket:
    # license C applies here. See docs/copyright_license.rst
    def __init__(self):
        self.previous = None
        self.previous_delimiter = None

        # _cmarkCmarkNode
        self.inl_text = None

        self.position = 0
        self.image = False
        self.active = True
        self.bracket_after = False


# /** Defines the memory allocation functions to be used by CMark
#  * when parsing and allocating a document tree
#  */
# typedef struct cmark_mem {
#   void *(*calloc)(size_t, size_t);
#   void *(*realloc)(void *, size_t);
#   void (*free)(void *);
# } cmark_mem;
class _cmarkCmarkMem:
    pass


class _cmarkCmarkStrbuf:
    def __init__(self):
        self.mem: _cmarkCmarkMem = None
        self.ptr: str = str()
        self.asize: int = 0
        self.size: int = 0


# Should be equivalent to
#     #define CMARK_BUF_INIT(mem) \
#       { mem, cmark_strbuf__initbuf, 0, 0 }
# 0.29, 0.30
def _cmark_CMARK_BUF_INIT(mem):
    b = _cmarkCmarkStrbuf()
    b.mem = mem

    return b


# 0.29, 0.30
def _cmark_advance(subj: _cmarkSubject):
    # license C applies here. See docs/copyright_license.rst.
    # Advance the subject.  Doesn't check for eof.
    subj.pos += 1


# 0.29, 0.30
def _cmark_cmark_utf8proc_is_space(char: int, parser: str = 'github') -> bool:
    r"""Match anything in the Zs class, plus LF, CR, TAB, FF."""
    # license D applies here. See docs/copyright_license.rst.
    value = False
    if chr(char) in md_parser[parser]['pseudo-re']['UWC']:
        value = True

    return value


# 0.29, 0.30
def _cmark_cmark_ispunct(char: int, parser: str = 'github') -> bool:
    r"""Return True if c is an ascii punctuation character."""
    # license C applies here. See docs/copyright_license.rst.
    value = False
    if chr(char) in md_parser[parser]['pseudo-re']['APC']:
        value = True

    return value


# 0.29, 0.30
def _cmark_cmark_utf8proc_is_punctuation(char: int, parser: str = 'github') -> bool:
    r"""Match anything in the P[cdefios] classes."""
    # license C applies here. See docs/copyright_license.rst.
    value = False
    if (char < 128 and _cmark_cmark_ispunct(char)) or chr(char) in md_parser[parser]['pseudo-re']['UPC']:
        value = True

    return value


# 0.29, 0.30
def _cmark_cmark_utf8proc_charlen(line: str, line_length: int) -> int:
    # license D applies here. See docs/copyright_license.rst
    length: int
    i: int

    if not line_length:
        return 0

    # Use length = 1 instead of the utf8proc_utf8class[256]
    # list.
    # For example:
    # len('ł') == 2 # in Python 2
    # len('ł') == 1 # in Python 3
    # See the documentation.
    # In Python 3 since all strings are unicode by default
    # they all have length of 1.
    length = 1
    if len(line) > 1:
        # See
        # https://docs.python.org/3/howto/unicode.html#comparing-strings
        raise CannotTreatUnicodeString

    if not length:
        return -1

    if line_length >= 0 and length > line_length:
        return -line_length

    for i in range(1, length):
        if (ord(line[i]) & 0xC0) != 0x80:
            return -i

    return length


# 0.29, 0.30
def _cmark_cmark_utf8proc_iterate(line: str, line_len: int) -> tuple:
    # license D applies here. See docs/copyright_license.rst
    length: int = 0
    uc: int = -1
    dst: int = -1

    length = _cmark_cmark_utf8proc_charlen(line, line_len)
    if length < 0:
        return -1, dst

    if length == 1:
        uc = ord(line[0])
    elif length == 2:
        uc = ((ord(line[0]) & 0x1F) << 6) + (ord(line[1]) & 0x3F)
        if uc < 0x80:
            uc = -1
    elif length == 3:
        uc = ((ord(line[0]) & 0x0F) << 12) + ((ord(line[1]) & 0x3F) << 6) + (ord(line[2]) & 0x3F)
        if uc < 0x800 or (uc >= 0xD800 and uc < 0xE000):
            uc = -1
    elif length == 4:
        uc = (((ord(line[0]) & 0x07) << 18) + ((ord(line[1]) & 0x3F) << 12) +
              ((ord(line[2]) & 0x3F) << 6) + (ord(line[3]) & 0x3F))
        if uc < 0x10000 or uc >= 0x110000:
            uc = -1

    if uc < 0:
        return -1, dst

    dst = uc

    return length, dst


# 0.29, 0.30
def _cmark_peek_at(subj: _cmarkSubject, pos: int) -> int:
    # license C applies here. See docs/copyright_license.rst
    return ord(subj.input.data[pos])


# 0.29, 0.30
def _cmark_scan_delims(subj: _cmarkSubject, c: str) -> tuple:
    # license C applies here. See docs/copyright_license.rst
    numdelims: int = 0
    before_char_pos: int = 0
    after_char: int = 0
    before_char: int = 0
    length: int = 0
    left_flanking: bool = False
    right_flanking: bool = False
    can_open: bool = False
    can_close: bool = False

    if subj.pos == 0:
        before_char = 10
    else:
        before_char_pos = subj.pos - 1
        # walk back to the beginning of the UTF_8 sequence
        while _cmark_peek_at(subj, before_char_pos) >> 6 == 2 and before_char_pos > 0:
            before_char_pos -= 1

        length, before_char = _cmark_cmark_utf8proc_iterate(subj.input.data[before_char_pos:before_char_pos + 1],
                                                            subj.pos - before_char_pos)

        if length == -1:
            before_char = 10

    if c == '\'' or c == '"':
        numdelims += 1
        _cmark_advance(subj)
    else:
        while chr(_cmark_peek_char(subj)) == c:
            numdelims += 1
            _cmark_advance(subj)

    length, after_char = _cmark_cmark_utf8proc_iterate(subj.input.data[subj.pos:subj.pos + 1], subj.input.length - subj.pos)

    if length == -1:
        after_char = 10

    if (numdelims > 0
       and (not _cmark_cmark_utf8proc_is_space(after_char))
       and (not _cmark_cmark_utf8proc_is_punctuation(after_char)
            or _cmark_cmark_utf8proc_is_space(before_char)
            or _cmark_cmark_utf8proc_is_punctuation(before_char))):
        left_flanking = True

    if (numdelims > 0
       and (not _cmark_cmark_utf8proc_is_space(before_char))
       and (not _cmark_cmark_utf8proc_is_punctuation(before_char)
            or _cmark_cmark_utf8proc_is_space(after_char)
            or _cmark_cmark_utf8proc_is_punctuation(after_char))):
        right_flanking = True

    if c == '_':
        if (left_flanking
           and (not right_flanking or _cmark_cmark_utf8proc_is_punctuation(before_char))):
            can_open = True
        if (right_flanking
           and (not left_flanking or _cmark_cmark_utf8proc_is_punctuation(after_char))):
            can_close = True
    elif c == '\'' or c == '"':
        if (left_flanking and not right_flanking and
           before_char != ']' and before_char != ')'):
            can_open = True
        can_close = right_flanking
    else:
        can_open = left_flanking
        can_close = right_flanking

    return numdelims, can_open, can_close


# 0.29, 0.30
def _cmark_push_delimiter(subj: _cmarkSubject, c: str, can_open: bool,
                          can_close: bool, inl_text: _cmarkCmarkNode):
    # license C applies here. See docs/copyright_license.rst
    delim = _cmarkDelimiter(c, inl_text.length)
    delim.can_open = can_open
    delim.can_close = can_close
    delim.inl_text = inl_text
    subj.push(delim)
    # List operations are handled in the class definition.


# 0.29, 0.30
def _cmark_cmark_chunk_dup(ch: _cmarkCmarkChunk, pos: int, length: int) -> str:
    # license E applies here. See docs/copyright_license.rst
    c = _cmarkCmarkChunk(copy.deepcopy(ch.data[pos: pos + length]), length)
    return c


# 0.30
def _cmark_cmark_chunk_literal(data: str) -> _cmarkCmarkChunk:
    # license E applies here. See docs/copyright_license.rst
    length: int
    c: _cmarkCmarkChunk

    if data is not None:
        length = len(data)
    else:
        length = 0

    c = _cmarkCmarkChunk(data, length)
    return c


# 0.29, 0.30
def _cmark_handle_delim(subj: _cmarkSubject, c: str, smart: bool = False) -> _cmarkCmarkNode:
    # license C applies here. See docs/copyright_license.rst
    numdelims: int
    can_open: bool
    can_close: bool
    inl_text: _cmarkCmarkNode
    contents: str

    numdelims, can_open, can_close = _cmark_scan_delims(subj, c)

    if c == '\'' and smart:
        contents = _cmark_cmark_chunk_literal(md_parser['cmark']['generic']['RIGHTSINGLEQUOTE'])
    elif c == '"' and smart:
        if can_close:
            contents = _cmark_cmark_chunk_literal(md_parser['cmark']['generic']['RIGHTDOUBLEQUOTE'])
        else:
            contents = _cmark_cmark_chunk_literal(md_parser['cmark']['generic']['LEFTDOUBLEQUOTE'])
    else:
        contents = _cmark_cmark_chunk_dup(subj.input, subj.pos - numdelims, numdelims)

    inl_text = _cmark_make_str(subj, subj.pos - numdelims, subj.pos - 1, contents)

    if (can_open or can_close) and (not (c == '\'' or c == '"')):
        _cmark_push_delimiter(subj, c, can_open, can_close, inl_text)

    return inl_text


# 0.29, 0.30
def _cmark_peek_char(subj: _cmarkSubject) -> int:
    # license C applies here. See docs/copyright_license.rst
    # Instead of using assert just raise a ValueError
    if subj.pos < subj.input.length and ord(subj.input.data[subj.pos]) == 0:
        raise ValueError

    if subj.pos < subj.input.length:
        return ord(subj.input.data[subj.pos])
    else:
        return 0


# 0.30
# Unlink a node without adjusting its next, prev, and parent pointers.
def _cmark_S_node_unlink(node: _cmarkCmarkNode):
    # license C applies here. See docs/copyright_license.rst
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
def _cmark_S_free_nodes(e: _cmarkCmarkNode):
    # license C applies here. See docs/copyright_license.rst
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
    # license C applies here. See docs/copyright_license.rst
    _cmark_S_node_unlink(node)
    node.next = None
    _cmark_S_free_nodes(node)


# 0.29, 0.30
def _cmark_remove_emph(subj: _cmarkSubject, opener: _cmarkDelimiter, closer: _cmarkDelimiter, ignore: list):
    # license C applies here. See docs/copyright_license.rst
    # This function refers to S_insert_emph()
    delim: _cmarkDelimiter
    tmp_delim: _cmarkDelimiter
    use_delims: int
    opener_inl: _cmarkCmarkNode = opener.inl_text
    closer_inl: _cmarkCmarkNode = closer.inl_text
    opener_num_chars: int = opener_inl.length
    closer_num_chars: int = closer_inl.length
    tmp: _cmarkCmarkNode
    tmpnext: _cmarkCmarkNode
    emph: _cmarkCmarkNode

    # calculate the actual number of characters used from this closer
    if closer_num_chars >= 2 and opener_num_chars >= 2:
        use_delims = 2
    else:
        use_delims = 1

    # remove used characters from associated inlines.
    opener_num_chars -= use_delims
    closer_num_chars -= use_delims
    opener_inl.length = opener_num_chars
    closer_inl.length = closer_num_chars
    # No need to add string terminators.
    # opener_inl->data[opener_num_chars] = 0;
    # closer_inl->data[closer_num_chars] = 0;

    # free delimiters between opener and closer
    delim = closer.previous
    while delim is not None and delim != opener:
        tmp_delim = delim.previous
        subj.extract(delim)
        delim = tmp_delim

    # IGNORE
    #
    # create new emph or strong, and splice it in to our inlines
    # between the opener and closer
    # emph = use_delims == 1 ? make_emph(subj->mem) : make_strong(subj->mem);
    # tmp = opener_inl->next;
    # while (tmp && tmp != closer_inl) {
    #   tmpnext = tmp->next;
    #   cmark_node_unlink(tmp);
    #   append_child(emph, tmp);
    #   tmp = tmpnext;
    # }
    # cmark_node_insert_after(opener_inl, emph);
    #

    # Custom variables and computations.
    opener_relative_start = opener_inl.end_column - use_delims + 1 - opener.offset
    opener_relative_end = opener_inl.end_column + 1 - opener.offset
    closer_relative_start = closer_inl.start_column + closer.offset
    closer_relative_end = closer_inl.start_column + use_delims + closer.offset

    ignore.append(range(opener_relative_start, opener_relative_end))
    ignore.append(range(closer_relative_start, closer_relative_end))

    opener.offset += use_delims
    closer.offset += use_delims

    # if opener has 0 characters, remove it and its associated inline
    if opener_num_chars == 0:
        _cmark_cmark_node_free(opener_inl)
        subj.extract(opener)

    # if closer has 0 characters, remove it and its associated inline
    if closer_num_chars == 0:
        # remove empty closer inline
        _cmark_cmark_node_free(closer_inl)
        # remove closer from list
        tmp_delim = closer.next
        subj.extract(closer)
        closer = tmp_delim

    return closer


# 0.30
def _cmark_cmark_set_cstr(mem, dst: str, src: str) -> int:
    # license C applies here. See docs/copyright_license.rst
    old: str = dst
    length: int

    _noop(old)

    if src and src[0]:
        length = len(src)
        dst = copy.deepcopy(src)
    else:
        length = 0
        dst = None

    # No need to free in Python.

    return length


# 0.30
def _cmark_cmark_node_set_literal(node: _cmarkCmarkNode, content: str) -> int:
    # license C applies here. See docs/copyright_license.rst
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


# 0.29, 0.30
def _cmark_process_emphasis(subj: _cmarkSubject, stack_bottom: _cmarkDelimiter, ignore: list) -> list:
    # license C applies here. See docs/copyright_license.rst
    closer: _cmarkDelimiter = subj.last_delim
    opener: _cmarkDelimiter
    openers_bottom_index: int = 0
    opener_found: bool
    openers_bottom_index: int = 0
    openers_bottom: list = [stack_bottom, stack_bottom, stack_bottom, stack_bottom, stack_bottom, stack_bottom]

    # move back to first relevant delim.
    while closer is not None and closer.previous is not stack_bottom:
        closer = closer.previous

    # now move forward, looking for closers, and handling each
    while closer is not None:
        if closer.can_close:
            if closer.delim_char == '"':
                openers_bottom_index = 0
            elif closer.delim_char == '\'':
                openers_bottom_index = 1
            elif closer.delim_char == '_':
                openers_bottom_index = 2
            elif closer.delim_char == '*':
                openers_bottom_index = 3 + (closer.length % 3)
            else:
                raise ValueError

            # Now look backwards for first matching opener:
            opener = closer.previous
            opener_found = False
            while opener is not None and opener != openers_bottom[openers_bottom_index]:
                if opener.can_open and opener.delim_char == closer.delim_char:
                    # interior closer of size 2 can't match opener of size 1
                    # or of size 1 can't match 2
                    if (not (closer.can_open or opener.can_close)
                       or closer.length % 3 == 0
                       or (opener.length + closer.length) % 3 != 0):
                        opener_found = True
                        break
                opener = opener.previous

            old_closer = closer
            if closer.delim_char == '*' or closer.delim_char == '_':
                if opener_found:
                    closer = _cmark_remove_emph(subj, opener, closer, ignore)
                else:
                    closer = closer.next

            elif closer.delim_char == '\'':
                _cmark_cmark_node_set_literal(closer.inl_text, md_parser['cmark']['generic']['RIGHTSINGLEQUOTE'])
                if opener_found:
                    _cmark_cmark_node_set_literal(opener.inl_text, md_parser['cmark']['generic']['LEFTSINGLEQUOTE'])
                closer = closer.next
            elif closer.delim_char == '"':
                _cmark_cmark_node_set_literal(closer.inl_text, md_parser['cmark']['generic']['RIGHTDOUBLEQUOTE'])
                if opener_found:
                    _cmark_cmark_node_set_literal(opener.inl_text, md_parser['cmark']['generic']['LEFTDOUBLEQUOTE'])
                closer = closer.next

            if not opener_found:
                # set lower bound for future searches for openers
                openers_bottom[openers_bottom_index] = old_closer.previous
                if not old_closer.can_open:
                    # we can remove a closer that can't be an
                    # opener, once we've seen there's no
                    # matching opener:
                    subj.extract(old_closer)
        else:
            closer = closer.next

    # free all delimiters in list until stack_bottom:
    while subj.last_delim is not None and subj.last_delim != stack_bottom:
        subj.extract(subj.last_delim)


# 0.29, 0.30
def _cmark_skip_line_end(subj: _cmarkSubject) -> bool:
    # license C applies here. See docs/copyright_license.rst
    seen_line_end_char: bool = False

    if _cmark_peek_char(subj) == '\r':
        _cmark_advance(subj)
        seen_line_end_char = True
    if _cmark_peek_char(subj) == '\n':
        _cmark_advance(subj)
        seen_line_end_char = True
    return seen_line_end_char or _cmark_is_eof(subj)


# 0.29, 0.30
def _cmark_make_simple(mem, t: int) -> _cmarkCmarkNode:
    # license C applies here. See docs/copyright_license.rst
    e = _cmarkCmarkNode()
    e.mem = copy.deepcopy(mem)
    e.type = t
    return e


# 0.29, 0.30
def _cmark_make_linebreak(mem):
    # license C applies here. See docs/copyright_license.rst
    _cmark_make_simple(mem, md_parser['cmark']['cmark_node_type']['CMARK_NODE_LINEBREAK'])


# 0.29, 0.30
def _cmark_handle_backslash(subj: _cmarkSubject):
    r"""Parse backslash-escape or just a backslash, returning an inline."""
    # license C applies here. See docs/copyright_license.rst
    _cmark_advance(subj)
    nextchar: str = _cmark_peek_char(subj)

    # only ascii symbols and newline can be escaped
    if _cmark_cmark_ispunct(nextchar):
        _cmark_advance(subj)
        return _cmark_make_str(subj, subj.pos - 2, subj.pos - 1, _cmark_cmark_chunk_dup(subj.input, subj.pos - 1, 1))
    elif (not _cmark_is_eof(subj)) and _cmark_skip_line_end(subj):
        return _cmark_make_linebreak(subj.mem)
    else:
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1, _cmark_cmark_chunk_literal('\\'))


# 0.29, 0.30
def _cmark_make_literal(subj: _cmarkSubject, t: int, start_column: int, end_column: int) -> _cmarkCmarkNode:
    # license C applies here. See docs/copyright_license.rst
    r"""Create an inline with a literal string value."""
    e = _cmarkCmarkNode()

    # cmark_strbuf_init(subj->mem, &e->content, 0)
    e.mem = copy.deepcopy(subj.mem)
    e.type = t
    e.start_line = e.end_line = subj.line
    # columns are NOT 1 based.
    e.start_column: int = start_column + subj.column_offset + subj.block_offset
    e.end_column: int = end_column + subj.column_offset + subj.block_offset
    return e


# 0.29, 0.30
def _cmark_make_str(subj: _cmarkSubject, sc: int, ec: int, s: _cmarkCmarkChunk) -> _cmarkCmarkNode:
    # license C applies here. See docs/copyright_license.rst
    # s = char
    # sc = start column
    # ec = end cloumn
    e = _cmark_make_literal(subj, md_parser['cmark']['cmark_node_type']['CMARK_NODE_TEXT'], sc, ec)

    # Realloc with NULL ptr is equal to malloc, so no need to translate
    # this operation:
    # e->data = (unsigned char *)subj->mem->realloc(NULL, s.len + 1);

    if s.data is not None:
        e.data = copy.deepcopy(s.data)

    # No need to add line terminator (\0).
    e.length = s.length

    return e


# 0.29, 0.30
def _cmark_push_bracket(subj: _cmarkSubject, image: bool, inl_text: _cmarkCmarkNode):
    # license C applies here. See docs/copyright_license.rst
    b = _cmarkBracket()
    if subj.last_bracket is not None:
        subj.last_bracket.bracket_after = True
    b.image = image
    b.active = True
    b.inl_text = inl_text
    b.previous = subj.last_bracket
    b.previous_delimiter = subj.last_delim
    b.position = subj.pos
    b.bracket_after = False
    subj.last_bracket = b


# 0.29, 0.30
def _cmark_subject_find_special_char(subj: _cmarkSubject, options: int) -> int:
    # license C applies here. See docs/copyright_license.rst
    # "\r\n\\`&_*[]<!"
    SPECIAL_CHARS: list = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1,
        1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]

    # " ' . -
    SMART_PUNCT_CHARS: list = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]

    n: int = subj.pos + 1

    # Patch to avoid overflow problems.
    if n > subj.input.length - 1:
        return subj.input.length
    if ord(subj.input.data[n]) > len(SPECIAL_CHARS) - 1 or ord(subj.input.data[n]) > len(SMART_PUNCT_CHARS) - 1:
        return n
    # End patch.

    while n < subj.input.length:
        if SPECIAL_CHARS[ord(subj.input.data[n])] == 1:
            return n
        if options & md_parser['cmark']['generic']['CMARK_OPT_SMART'] and SMART_PUNCT_CHARS[ord(subj.input.data[n])]:
            return n
        n += 1

    return subj.input.length


# 0.29, 0.30
def _cmark_subject_from_buf(mem, line_number: int,
                            block_offset: int, e: _cmarkSubject, chunk: _cmarkCmarkChunk,
                            refmap: _cmarkCmarkReferenceMap):
    # license C applies here. See docs/copyright_license.rst
    i: int
    e.mem = mem
    e.input = chunk
    e.line = line_number
    e.pos = 0
    e.block_offset = block_offset
    e.column_offset = 0
    e.refmap = refmap
    e.last_delim = None
    e.last_bracket = None

    for i in range(0, md_parser['cmark']['generic']['MAXBACKTICKS']):
        e.backticks[i] = 0

    e.scanned_for_backticks = False


# 0.30
def _cmark_S_is_line_end_char(c: str) -> bool:
    # license C applies here. See docs/copyright_license.rst
    return c == '\n' or c == '\r'


# 0.30
# /**
#  * Returns 1 if c is a "whitespace" character as defined by the spec.
#  */
# int cmark_isspace(char c) { return cmark_ctype_class[(uint8_t)c] == 1; }
# The only defined whitespaces in the spec are Unicode whitespaces.
def _cmark_cmark_chunk_rtrim(c: _cmarkCmarkChunk):
    # license E applies here. See docs/copyright_license.rst
    while c.length > 0:
        # if (!cmark_isspace(c->data[c->len - 1]))
        if not c.data[c.length - 1] in md_parser['cmark']['pseudo-re']['UWC']:
            break

        c.length -= 1


# 0.30
def _cmark_isbacktick(c: int) -> int:
    backtick: int = 0
    if chr(c) == '`':
        backtick = 1

    return backtick


# Try to process a backtick code span that began with a
# span of ticks of length openticklength length (already
# parsed).  Return 0 if you don't find matching closing
# backticks, otherwise return the position in the subject
# after the closing backticks.
# 0.29, 0.30
def _cmark_scan_to_closing_backticks(subj: _cmarkSubject, openticklength: int) -> int:
    found: bool = False

    if openticklength > md_parser['cmark']['generic']['MAXBACKTICKS']:
        # we limit backtick string length because of the array subj->backticks:
        return 0

    if (subj.scanned_for_backticks and
       subj.backticks[openticklength] <= subj.pos):
        # return if we already know there's no closer
        return 0

    while not found:
        # read non backticks
        c: int

        c = _cmark_peek_char(subj)
        while not _cmark_isbacktick(c):
            _cmark_advance(subj)
            c = _cmark_peek_char(subj)
        if _cmark_is_eof(subj):
            break

        numticks: int = 0
        while _cmark_isbacktick(_cmark_peek_char(subj)):
            _cmark_advance(subj)
            numticks += 1

        # store position of ender
        # Ender starting point.
        if numticks <= md_parser['cmark']['generic']['MAXBACKTICKS']:
            subj.backticks[numticks] = subj.pos - numticks

        if numticks == openticklength:
            return subj.pos

    # got through whole input without finding closer
    subj.scanned_for_backticks = True
    return 0


# Take characters while a predicate holds, and return a string.
# 0.29, 0.30
def _cmark_take_while(subj: _cmarkSubject) -> _cmarkCmarkChunk:
    r"""Get backtick spanning."""
    c: int
    startpos: int = subj.pos
    len: int = 0

    c = _cmark_peek_char(subj)
    while _cmark_isbacktick(c):
        _cmark_advance(subj)
        len += 1
        c = _cmark_peek_char(subj)

    return _cmark_cmark_chunk_dup(subj.input, startpos, len)


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


# Destructively modify string, converting newlines to
# spaces, then removing a single leading + trailing space,
# unless the code span consists entirely of space characters.
# 0.29, 0.30
def _cmark_S_normalize_code(s: _cmarkCmarkStrbuf):
    r: int = 0
    w: int = 0
    contains_nonspace: bool = False

    while r < s.size:
        if s.ptr[r] == '\r':
            if (s.ptr[r + 1] != '\n'):
                s.ptr = _replace_substring(s.ptr, ' ', w, w)
                w += 1
        elif s.ptr[r] == '\n':
            s.ptr = _replace_substring(s.ptr, ' ', w, w)
            w += 1
        else:
            s.ptr = _replace_substring(s.ptr, s.ptr[r], w, w)
            w += 1

        if s.ptr[r] != ' ':
            contains_nonspace = True

        r += 1

    # begins and ends with space?
    if (contains_nonspace
       and s.ptr[0] == ' '
       and s.ptr[w - 1] == ' '):
        _cmark_cmark_strbuf_drop(s, 1)
        _cmark_cmark_strbuf_truncate(s, w - 2)
    else:
        _cmark_cmark_strbuf_truncate(s, w)


# 0.29, 0.30
def _cmark_cmark_strbuf_init(mem: _cmarkCmarkMem, buf: _cmarkCmarkStrbuf, initial_size: int):
    buf.mem = mem
    buf.asize = 0
    buf.size = 0
    buf.ptr = str()

    if initial_size > 0:
        _cmark_cmark_strbuf_grow(buf, initial_size)


# 0.29, 0.30
def _cmark_cmark_strbuf_detach(buf: _cmarkCmarkStrbuf) -> str:
    data: str = buf.ptr

    if buf.asize == 0:
        # return an empty string
        #     return (unsigned char *)buf->mem->calloc(1, 1);
        return str()

    _cmark_cmark_strbuf_init(buf.mem, buf, 0)
    return data


# Return the number of newlines in a given span of text in a subject.  If
# the number is greater than zero, also return the number of characters
# between the last newline and the end of the span in `since_newline`.
# 0.29, 0.30
def _cmark_count_newlines(subj: _cmarkSubject, start: int, length: int) -> tuple:
    nls: int = 0
    since_nl: int = 0

    while length > 0:
        if subj.input.data[start] == '\n':
            nls += 1
            since_nl = 0
        else:
            since_nl += 1

        start += 1
        length -= 1

    if not nls:
        return 0

    since_newline = since_nl
    return nls, since_newline


# Adjust `node`'s `end_line`, `end_column`, and `subj`'s `line` and
# `column_offset` according to the number of newlines in a just-matched span
# of text in `subj`.
# 0.29, 0.30
def _cmark_adjust_subj_node_newlines(subj: _cmarkSubject, node: _cmarkCmarkNode, matchlen: int, extra: int, options: int):
    if not options & md_parser['cmark']['generic']['CMARK_OPT_SOURCEPOS']:
        return

    newlines: int
    since_newline: int

    newlines, since_newline = _cmark_count_newlines(subj, subj.pos - matchlen - extra, matchlen)
    if newlines:
        subj.line += newlines
        node.end_line += newlines
        node.end_column = since_newline
        subj.column_offset = - subj.pos + since_newline + extra


# 0.29, 0.30
def _cmark_handle_backticks(subj: _cmarkSubject, options: int) -> _cmarkCmarkNode:
    openticks: _cmarkCmarkChunk = _cmark_take_while(subj)
    startpos: int = subj.pos
    endpos: int = _cmark_scan_to_closing_backticks(subj, openticks.length)

    # not found
    if endpos == 0:
        # rewind
        subj.pos = startpos
        return _cmark_make_str(subj, subj.pos, subj.pos, openticks)
    else:
        buf = _cmark_CMARK_BUF_INIT(subj.mem)
        _cmark_cmark_strbuf_set(buf, subj.input.data[startpos:], endpos - startpos - openticks.length)
        _cmark_S_normalize_code(buf)

        node: _cmarkCmarkNode = _cmark_make_literal(subj, md_parser['cmark']['cmark_node_type']['CMARK_NODE_CODE'], startpos, endpos - openticks.length - 1)
        node.len = buf.size
        node.data = _cmark_cmark_strbuf_detach(buf)
        _cmark_adjust_subj_node_newlines(subj, node, endpos - startpos, openticks.length, options)
        return node


# 0.29, 0.30
def _cmark_parse_inline(subj: _cmarkSubject, parent: _cmarkCmarkNode, options: int = 0) -> int:
    r"""Handle all the different elements of a string."""
    # license C applies here. See docs/copyright_license.rst
    new_inl: _cmarkCmarkNode = None
    contents: str
    c: int
    startpos: int
    endpos: int

    c = _cmark_peek_char(subj)
    if c == 0:
        return 0
    elif chr(c) == '\r' or chr(c) == '\n':
        _cmark_advance(subj)
        # TODO
    elif chr(c) == '`':
        new_inl = _cmark_handle_backticks(subj, options)
    elif chr(c) == '\\':
        new_inl = _cmark_handle_backslash(subj)
    elif chr(c) == '*' or chr(c) == '_' or chr(c) == '\'' or chr(c) == '"':
        new_inl = _cmark_handle_delim(subj, chr(c), (options & md_parser['cmark']['generic']['CMARK_OPT_SMART']) != 0)
    elif chr(c) == '[':
        _cmark_advance(subj)
        new_inl = _cmark_make_str(subj, subj.pos - 1, subj.pos - 1, _cmark_cmark_chunk_literal('['))
        _cmark_push_bracket(subj, False, new_inl)
    elif chr(c) == ']':
        # TODO
        _cmark_advance(subj)

    # TODO: images, HTML tags detection.

    else:
        endpos = _cmark_subject_find_special_char(subj, options)
        contents = _cmark_cmark_chunk_dup(subj.input, subj.pos, endpos - subj.pos)
        startpos = subj.pos
        subj.pos = endpos

        # if we're at a newline, strip trailing spaces.
        if _cmark_S_is_line_end_char(_cmark_peek_char(subj)):
            _cmark_cmark_chunk_rtrim(contents)

        new_inl = _cmark_make_str(subj, startpos, endpos - 1, contents)

    if new_inl is not None:
        parent.append_child_lite(new_inl)

    return 1


# 0.30
def _cmark_pop_bracket(subj: _cmarkSubject):
    # license C applies here. See docs/copyright_license.rst
    b: _cmarkBracket
    if subj.last_bracket is None:
        return
    b = subj.last_bracket
    subj.last_bracket = subj.last_bracket.previous
    # No need to free.
    # subj->mem->free(b);
    _noop(b)


# 0.30
def _cmark_cmark_parse_inlines(mem, parent: _cmarkCmarkNode,
                               refmap: _cmarkCmarkReferenceMap, options: int) -> list:
    r"""Get the ignore list."""
    # license C applies here. See docs/copyright_license.rst
    subj: _cmarkSubject
    content: _cmarkCmarkChunk = _cmarkCmarkChunk(parent.data, parent.length)
    subj = _cmarkSubject()
    _cmark_subject_from_buf(mem, parent.start_line, parent.start_column - 1 + parent.internal_offset, subj, content, refmap)
    _cmark_cmark_chunk_rtrim(subj.input)

    while not _cmark_is_eof(subj):
        _cmark_parse_inline(subj, parent, options)

    ignore = list()
    # When we hit the end of the input, we call the process emphasis procedure (see below), with stack_bottom = NULL.
    _cmark_process_emphasis(subj, None, ignore)

    # free bracket and delim stack
    while subj.last_delim:
        subj.extract(subj.last_delim)
    while subj.last_bracket:
        _cmark_pop_bracket(subj)

    return ignore


# 0.30
def _cmark_is_eof(subj: _cmarkSubject):
    r"""Return true if there are more characters in the subject."""
    # license C applies here. See docs/copyright_license.rst.
    return subj.pos >= subj.input.length


if __name__ == '__main__':
    pass
