#
# cmark.py
#
# Copyright (C) 2017-2021 frnmst (Franco Masotti) <franco.masotti@tutanota.com>
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

from .constants import parser as md_parser
from .exceptions import CannotTreatUnicodeString


##########################
# cmark specific Classes #
##########################
class _cmarkCmarkNode:
    def __init__(self):
        # cmark_strbuf
        self.content = None

        self.prev = None
        self.parent = None
        self.first_child = None
        self.last_child = None

        self.user_data = None

        self.start_line = 0
        self.start_column = 0
        self.end_line = 0
        self.end_column = 0
        self.internal_offset = 0

        # union
        ## cmark_chunk
        self.as_literal = None
        self.as_literal_len: int = 0

        # Add a new variable.
        self.numdelims: int = 0


class _cmarkDelimiterDLLNode:
    r"""A list node with attributes useful for processing emphasis."""

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


class _cmark_Subject:
    r"""A double linked list useful for processing emphasis."""

    def __init__(self, input: str):
        '''
        /** Defines the memory allocation functions to be used by CMark
         * when parsing and allocating a document tree
         */
        typedef struct cmark_mem {
          void *(*calloc)(size_t, size_t);
          void *(*realloc)(void *, size_t);
          void (*free)(void *);
        } cmark_mem;
        '''
        self.mem = None

        self.line = 0
        self.pos = 0
        self.block_offset = 0
        self.column_offset = 0
        self.start = None
        self.last_delim = None
        self.last_bracket = None

        # This corresponds to the line.
        self.input: str = input

    def push(self, node: _cmarkDelimiterDLLNode):
        r"""Add a new node."""
        if self.start is None and self.last_delim is None:
            self.start = self.last_delim = node
        else:
            self.last_delim.next = node
            node.previous = self.last_delim
            self.last_delim = self.last_delim.next
            node.next = None

    def pop(self) -> _cmarkDelimiterDLLNode:
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

    def extract(self, node: _cmarkDelimiterDLLNode):
        r"""Remove a specific node."""
        if node is None:
            pass
        elif self.start is not None and self.last_delim is not None:
            if node == self.last_delim:
                self.last_delim = node.previous

                if self.last_delim is None:
                    self.start = None
            else:
                node.next.previous = node.previous
            if node.previous is not None:
                node.previous.next = node.next
            else:
                self.start = node.next

    def scroll(self):
        r"""Print the list."""
        print(self.start)
        print("===")
        x = self.start
        while x is not None:
            print(x)
            x = x.next

class _cmark_Bracket:
    def __init__(self):
        self.previous = None
        self.previous_delimiter = None

        # _cmarkCmarkNode
        self.inl_text = None

        self.position = 0
        self.image = False
        self.active = True
        self.bracket_after = False

def _cmark_advance(subj: _cmark_Subject):
    # Advance the subject.  Doesn't check for eof.
    subj.pos += 1

def _cmark_cmark_utf8proc_is_space(char: int, parser: str = 'github') -> bool:
    r"""license D applies here. See docs/markdown_specification.rst.

    Matches anything in the Zs class, plus LF, CR, TAB, FF.
    """
    value = False
    if chr(char) in md_parser[parser]['pseudo-re']['UWC']:
        value = True

    return value


def _cmark_cmark_utf8proc_is_punctuation(char: int, parser: str = 'github') -> bool:
    r"""license D applies here. See docs/markdown_specification.rst.

    Matches anything in the P[cdefios] classes.
    """
    value = False
    if chr(char) in md_parser[parser]['pseudo-re']['PC']:
        value = True

    return value


def _cmark_cmark_ispunct(char: int, parser: str = 'github') -> bool:
    r"""license D applies here. See docs/markdown_specification.rst.

    Returns True if c is an ascii punctuation character.
    """
    value = False
    if chr(char) in md_parser[parser]['pseudo-re']['APC']:
        value = True

    return value


def _cmark_cmark_utf8proc_charlen(line: str, line_length: int) -> int:
    # license E applies here. See docs/markdown_specification.rst
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


def _cmark_cmark_utf8proc_iterate(line: str, line_len: int) -> tuple:
    # license E applies here. See docs/markdown_specification.rst

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

def _cmark_peek_at(subj: _cmark_Subject, pos: int) -> int:
    # license D applies here. See docs/markdown_specification.rst
    return ord(subj.input[pos])

def _cmark_scan_delims(subj: _cmark_Subject, c: str) -> tuple:
    # license D applies here. See docs/markdown_specification.rst
    numdelims: int = 0
    before_char_pos: int = 0
    after_char: int = 0
    before_char: int = 0
    left_flanking: bool = False
    length: int = 0
    right_flanking: bool = False

    can_open = False
    can_close = False

    if subj.pos == 0:
        before_char = 10
    else:
        before_char_pos = subj.pos - 1
        # walk back to the beginning of the UTF_8 sequence
        while _cmark_peek_at(subj, before_char_pos) >> 6 == 2 and before_char_pos > 0:
            before_char_pos -= 1

        length, before_char = _cmark_cmark_utf8proc_iterate(subj.input[before_char_pos:before_char_pos + 1],
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

    length, after_char = _cmark_cmark_utf8proc_iterate(subj.input[subj.pos:subj.pos + 1], len(subj.input) - subj.pos)

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


def _cmark_push_delimiter(subj: _cmark_Subject, c: str, can_open: bool,
                          can_close: bool, inl_text: _cmarkCmarkNode):
    # license D applies here. See docs/markdown_specification.rst
    delim = _cmarkDelimiterDLLNode(c, inl_text.as_literal_len)
    delim.can_open = can_open
    delim.can_close = can_close
    delim.inl_text = inl_text
    subj.push(delim)
    # List operations are handled in the class definition.

def _cmark_cmark_chunk_dup(ch: str, pos: int, length: int) -> str:
    # license F applies here. See docs/markdown_specification.rst
    return copy.deepcopy(ch[pos: pos + length])

def _cmark_handle_delim(subj: _cmark_Subject, c: str) -> int:
    # license D applies here. See docs/markdown_specification.rst
    numdelims: int
    can_open: bool
    can_close: bool
    contents: str

    numdelims, can_open, can_close = _cmark_scan_delims(subj, c)
    contents = _cmark_cmark_chunk_dup(subj.input, subj.pos - numdelims, numdelims)
    inl_text = _cmark_make_str(subj, subj.pos - numdelims, subj.pos - 1, contents)

    if (can_open or can_close) and (not (c == '\'' or c == '"')):
        _cmark_push_delimiter(subj, c, can_open, can_close, inl_text)

    return numdelims


def _cmark_peek_char(subj: _cmark_Subject) -> int:
    # license D applies here. See docs/markdown_specification.rst
    assert not (subj.pos < len(subj.input) and ord(subj.input[subj.pos]) == 0)

    if subj.pos < len(subj.input):
        return ord(subj.input[subj.pos])
    else:
        return 0


def _cmark_remove_emph(delimiter_stack: _cmark_Subject, opener: _cmarkDelimiterDLLNode, closer: _cmarkDelimiterDLLNode, ignore: list):
    r"""This function refers to S_insert_emph()

    license D applies here. See docs/markdown_specification.rst
    """
    opener_inl: _cmarkCmarkNode = opener.inl_text
    closer_inl: _cmarkCmarkNode = closer.inl_text
    opener_num_chars: int = opener_inl.as_literal_len
    closer_num_chars: int = closer_inl.as_literal_len

    # calculate the actual number of characters used from this closer
    if closer_num_chars >= 2 and opener_num_chars >= 2:
        use_delims = 2
    else:
        use_delims = 1

    # remove used characters from associated inlines.
    opener_num_chars -= use_delims
    closer_num_chars -= use_delims
    opener_inl.as_literal_len = opener_num_chars
    closer_inl.as_literal_len = closer_num_chars

    # free delimiters between opener and closer
    delim = closer.previous
    while delim is not None and delim != opener:
        tmp_delim = delim.previous
        delimiter_stack.extract(delim)
        delim = tmp_delim

    # IGNORE
    # create new emph or strong, and splice it in to our inlines
    # between the opener and closer
    # emph = use_delims == 1 ? make_emph(subj->mem) : make_strong(subj->mem);

    # Custom variables.
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
        delimiter_stack.extract(opener)

    # if closer has 0 characters, remove it and its associated inline
    if closer_num_chars == 0:
        # remove closer from list
        tmp_delim = closer.next
        delimiter_stack.extract(closer)
        closer = tmp_delim

    return closer

def _cmark_process_emphasis(subj: _cmark_Subject, stack_bottom: _cmarkDelimiterDLLNode, ignore: list) -> list:
    # license D applies here. See docs/markdown_specification.rst
    closer: _cmarkDelimiterDLLNode = subj.last_delim
    opener: _cmarkDelimiterDLLNode
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
                closer.inl_text.as_literal = md_parser['cmark']['generic']['RIGHTSINGLEQUOTE']
                if opener_found:
                    opener.inl_text.as_literal = md_parser['cmark']['generic']['LEFTSINGLEQUOTE']
                closer = closer.next
            elif closer.delim_char == '"':
                closer.inl_text.as_literal = md_parser['cmark']['generic']['RIGHTDOUBLEQUOTE']
                if opener_found:
                    opener.inl_text.as_literal = md_parser['cmark']['generic']['LEFTDOUBLEQUOTE']
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

def _cmark_skip_line_end(subj: _cmark_Subject) -> bool:
    # license D applies here. See docs/markdown_specification.rst
    seen_line_end_char: bool = False;

    if _cmark_peek_char(subj) == '\r':
        _cmark_advance(subj)
        seen_line_end_char = True
    if _cmark_peek_char(subj) == '\n':
        _cmark_advance(subj)
        seen_line_end_char = True
    return seen_line_end_char or _cmark_is_eof(subj)


def make_simple(mem) -> _cmarkCmarkNode:
    # license D applies here. See docs/markdown_specification.rst
    e = _cmarkCmarkNode()
    e.content = copy.deepcopy(mem)
    return e;

def _cmark_make_linebreak(mem):
    # license D applies here. See docs/markdown_specification.rst
    _cmark_make_simple(mem)

def _cmark_handle_backslash(subj: _cmark_Subject):
    r"""Parse backslash-escape or just a backslash, returning an inline.

    .. note: license D applies here. See docs/markdown_specification.rst
    """
    _cmark_advance(subj)
    nextchar: str = _cmark_peek_char(subj)

    # only ascii symbols and newline can be escaped
    if _cmark_cmark_ispunct(nextchar):
        _cmark_advance(subj)
        return _cmark_make_str(subj, subj.pos - 2, subj.pos - 1, _cmark_cmark_chunk_dup(subj.input, subj.pos - 1, 1))
    elif (not _cmark_is_eof(subj)) and _cmark_skip_line_end(subj):
        return _cmark_make_linebreak(subj.mem)
    else:
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1, '\\')

def _cmark_make_literal(subj: _cmark_Subject, start_column: int, end_column: int, char: str):
    # license D applies here. See docs/markdown_specification.rst
    r"""Create an inline with a literal string value."""
    e = _cmarkCmarkNode()

    # cmark_strbuf_init(subj->mem, &e->content, 0)
    e.content = copy.deepcopy(subj.mem)

    e.as_literal: str = char
    e.as_literal_len: int = len(char)
    e.start_line = subj.line
    e.end_line = subj.line

    # columns are NOT 1 based.
    e.start_column: int = start_column + subj.column_offset + subj.block_offset
    e.end_column: int = end_column + subj.column_offset + subj.block_offset

    return e

def _cmark_make_str(subj: _cmark_Subject, start_column: int, end_column: int, char: str):
    # license D applies here. See docs/markdown_specification.rst
    return _cmark_make_literal(subj, start_column, end_column, char)

def _cmark_push_bracket(subj: _cmark_Subject, image: bool, inl_text: str):
    # license D applies here. See docs/markdown_specification.rst
    b = _cmark_Bracket()
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

def _cmark_handle_close_bracket(subj: _cmark_Subject):
    # license D applies here. See docs/markdown_specification.rst
    # TODO
    advance(subj) # advance past ]
    initial_pos = subj.pos

    # get last [ or ![
    opener = subj.last_bracket

    if opener is None:
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1, ']')

    if not opener.active:
        # take delimiter off stack
        pop_bracket(subj);
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1, ']');

    # If we got here, we matched a potential link/image text.
    # Now we check to see if it's a link/image.
    is_image = opener.image

    after_link_text_pos = subj.pos

def _cmark_subject_find_special_char(subj: _cmark_Subject, options: int) -> int:
    # license D applies here. See docs/markdown_specification.rst

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
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    CMARK_OPT_SMART = 1 << 10
    n: int = subj.pos + 1

    if n > len(subj.input) - 1:
        return len(subj.input)
    if ord(subj.input[n]) > len(SPECIAL_CHARS) - 1 or ord(subj.input[n]) > len(SMART_PUNCT_CHARS) - 1:
        return n

    while n < len(subj.input):
        if SPECIAL_CHARS[ord(subj.input[n])] == 1:
            return n
        if options & CMARK_OPT_SMART and SMART_PUNCT_CHARS[ord(subj.input[n])]:
            return n
        n += 1

    return len(subj.input)

def _cmark_parse_inline(subj: _cmark_Subject, options: int = 0) -> int:
    r"""Handle all the different elements of a string.

    ..note: license D applies here. See docs/markdown_specification.rst
    """
    new_inl: _cmarkCmarkNode = None
    contents: str
    c: int
    startpos: int
    endpos: int

    numdelim = 0

    c = _cmark_peek_char(subj)
    if c == 0:
        return 0
    elif chr(c) == '\\':
        numdelim = _cmark_handle_backslash(subj)
    elif chr(c) == '*' or chr(c) == '_' or chr(c) == '\'' or chr(c) == '"':
        numdelim = _cmark_handle_delim(subj, chr(c))
    elif chr(c) == '[':
        _cmark_advance(subj)
        new_inl = _cmark_make_str(subj, subj.pos - 1, subj.pos - 1, '[')
        _cmark_push_bracket(subj, False, new_inl)
    elif chr(c) == ']':
        # FIXME
        _cmark_advance(subj)

    # TODO: images, code, HTML tags detection.

    else:
        endpos = _cmark_subject_find_special_char(subj, options);
        contents = _cmark_cmark_chunk_dup(subj.input, subj.pos, endpos - subj.pos)
        startpos = subj.pos;
        subj.pos = endpos;

        '''
        // if we're at a newline, strip trailing spaces.
        if (S_is_line_end_char(peek_char(subj))) {
          cmark_chunk_rtrim(&contents);
        }
        '''

        new_inl = _cmark_make_str(subj, startpos, endpos - 1, contents)

    """
    if new_inl is not None:
        _cmark_cmark_node_append_child(parent, new_inl)
    """

    return 1

def _cmark_is_eof(subj: _cmark_Subject):
    r"""license D applies here. See docs/markdown_specification.rst.

    Return true if there are more characters in the subject.
    """
    return subj.pos >= len(subj.input)

if __name__ == '__main__':
    pass