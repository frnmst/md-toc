#
# api.py
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
"""The main file."""

import re
import sys

import fpyutils

from .constants import common_defaults
from .constants import parser as md_parser
from .exceptions import (CannotTreatUnicodeString, GithubEmptyLinkLabel,
                         GithubOverflowCharsLinkLabel,
                         GithubOverflowOrderedListMarker,
                         StdinIsNotAFileToBeWritten,
                         StringCannotContainNewlines,
                         TocDoesNotRenderAsCoherentList)


##########################
# cmark specific Classes #
##########################
class _cmarkCmarkNode:
    def __init__(self):
        prev = None
        parent = None
        first_child = None
        last_child = None

        user_data = None

        start_line = 0
        start_column = 0
        end_line = 0
        end_column = 0
        internal_offset = 0


class _cmarkDelimiterDLLNode:
    r"""A list node with attributes useful for processing emphasis."""

    def __init__(self, delim_char: str, length: int, start_index: int):
        self.previous = None
        self.next = None

        # _cmarkCmarkNode
        inl_text = None

        self.delim_char = delim_char
        self.length = length
        self.offset = 0
        self.original_length = length
        self.active = True
        self.start_index = start_index
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
            de = 'delim_char = ' + self.delim_char
            le = 'length = ' + str(self.length)
            of = 'offset = ' + str(self.offset)
            oi = 'original_length = ' + str(self.original_length)
            ac = 'active = ' + str(self.active)
            st = 'start_index = ' + str(self.start_index)
            pr = 'previous = ' + previous
            ne = 'next = ' + next
            co = 'can_open = ' + str(self.can_open)
            cc = 'can_close = ' + str(self.can_close)

            return (el + '\n' + de + '\n' + le + '\n' + of + '\n' + oi + '\n'
                    + ac + '\n' + st + '\n' + pr + '\n' + ne + '\n' + co + '\n'
                    + cc + '\n')


class _cmark_DLL:
    r"""A double linked list useful for processing emphasis."""

    def __init__(self):
        self.pos = 0
        self.start = None
        self.last_delim = None
        self.last_bracket = None

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
        print('last_bracket: ' + str(self.last_backet))
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

#####################
# Generic functions #
#####################
# _ctoi and _isascii taken from cpython source Lib/curses/ascii.py
# See:
# https://github.com/python/cpython/blob/283de2b9c18e38c9a573526d6c398ade7dd6f8e9/Lib/curses/ascii.py#L48
# https://github.com/python/cpython/blob/283de2b9c18e38c9a573526d6c398ade7dd6f8e9/Lib/curses/ascii.py#L56
#
# These 2 functions are released under the
# PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
# See https://directory.fsf.org/wiki/License:Python-2.0.1
def _ctoi(c: str):
    if not len(c) == 1:
        raise ValueError

    retval = c
    if isinstance(c, str):
        retval = ord(c)

    return retval


def _isascii(c):
    return 0 <= _ctoi(c) <= 127


############################
# cmark specific functions #
############################
def _cmark_advance(subj: _cmark_DLL):
    # Advance the subject.  Doesn't check for eof.
    subj.pos += 1

def _cmark_is_space(char: int, parser: str = 'github') -> bool:
    # license D applies here. See docs/markdown_specification.rst
    value = False
    if chr(char) in md_parser[parser]['pseudo-re']['UWC']:
        value = True

    return value


def _cmark_is_punctuation(char: int, parser: str = 'github') -> bool:
    # license D applies here. See docs/markdown_specification.rst
    value = False
    if chr(char) in md_parser[parser]['pseudo-re']['PC']:
        value = True

    return value


def _cmark_ispunct(char: int, parser: str = 'github') -> bool:
    # license D applies here. See docs/markdown_specification.rst

    value = False
    if chr(char) in md_parser[parser]['pseudo-re']['APC']:
        value = True

    return value


def _cmark_utf8proc_charlen(line: str, line_length: int) -> int:
    # license E applies here. See docs/markdown_specification.rst

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


def _cmark_utf8proc_iterate(line: str, line_len: int) -> tuple:
    # license E applies here. See docs/markdown_specification.rst

    length = 0
    uc = -1
    dst = -1

    length = _cmark_utf8proc_charlen(line, line_len)
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


def _cmark_scan_delims(subj: _cmark_DLL, line: str, c: str) -> tuple:
    # license D applies here. See docs/markdown_specification.rst

    left_flanking = False
    right_flanking = False
    can_open = False
    can_close = False
    numdelims = 0
    before_char_pos = 0
    before_char = 0
    after_char = 0

    if subj.pos == 0:
        before_char = 10
    else:
        before_char_pos = subj.pos - 1
        # walk back to the beginning of the UTF_8 sequence
        while _cmark_peek_char(line, before_char_pos) >> 6 == 2 and before_char_pos > 0:
            before_char_pos -= 1

        length, before_char = _cmark_utf8proc_iterate(line[before_char_pos:before_char_pos + 1],
                                                      subj.pos - before_char_pos)

        if length == -1:
            before_char = 10

    if c == '\'' or c == '"':
        numdelims += 1
        _cmark_advance(subj)
    else:
        while chr(_cmark_peek_char(line, subj.pos)) == c:
            numdelims += 1
            _cmark_advance(subj)

    length, after_char = _cmark_utf8proc_iterate(line[subj.pos:subj.pos + 1], len(line) - subj.pos)

    if length == -1:
        after_char = 10

    if (numdelims > 0
       and (not _cmark_is_space(after_char))
       and (not _cmark_is_punctuation(after_char)
            or _cmark_is_space(before_char)
            or _cmark_is_punctuation(before_char))):
        left_flanking = True

    if (numdelims > 0
       and (not _cmark_is_space(before_char))
       and (not _cmark_is_punctuation(before_char)
            or _cmark_is_space(after_char)
            or _cmark_is_punctuation(after_char))):
        right_flanking = True

    if c == '_':
        if (left_flanking
           and (not right_flanking or _cmark_is_punctuation(before_char))):
            can_open = True
        if (right_flanking
           and (not left_flanking or _cmark_is_punctuation(after_char))):
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


def _cmark_handle_delim(subj: _cmark_DLL, line: str, c: str) -> int:
    # license D applies here. See docs/markdown_specification.rst

    numdelims, can_open, can_close = _cmark_scan_delims(subj, line, c)

    # make_str(subj, subj->pos - numdelims, subj->pos - 1, contents);
    # start_column = subj->pos - numdelims
    # static CMARK_INLINE cmark_node *make_literal(subject *subj, cmark_node_type t,
    #                                         int start_column, int end_column,
    #                                         cmark_chunk s)
    #  // columns are 1 based.
    # e->start_column = start_column + 1 + subj->column_offset + subj->block_offset;
    start_index = subj.pos - numdelims

    if (can_open or can_close) and (not (c == '\'' or c == '"')):
        current = _cmarkDelimiterDLLNode(c, numdelims, start_index)
        current.can_open = can_open
        current.can_close = can_close
        subj.push(current)

    return numdelims


def _cmark_peek_char(line: str, pos: int) -> int:
    # license D applies here. See docs/markdown_specification.rst

    if pos < len(line):
        return ord(line[pos])
    else:
        return 0


def _cmark_remove_emph(delimiter_stack: _cmark_DLL, opener: _cmarkDelimiterDLLNode, closer: _cmarkDelimiterDLLNode, ignore: list):
    # license D applies here. See docs/markdown_specification.rst

    opener_num_chars = opener.length
    closer_num_chars = closer.length

    # calculate the actual number of characters used from this closer
    if closer_num_chars >= 2 and opener_num_chars >= 2:
        use_delims = 2
    else:
        use_delims = 1

    # remove used characters from associated inlines.
    opener_num_chars -= use_delims
    closer_num_chars -= use_delims
    opener.length = opener_num_chars
    closer.length = closer_num_chars

    # free delimiters between opener and closer
    delim = closer.previous
    while delim is not None and delim != opener:
        tmp_delim = delim.previous
        delimiter_stack.extract(delim)
        delim = tmp_delim

    opener_relative_start = opener.start_index + opener.original_length - opener.offset - use_delims
    opener_relative_end = opener.start_index + opener.original_length - opener.offset

    closer_relative_start = closer.start_index + closer.original_length - closer.offset - use_delims
    closer_relative_end = closer.start_index + closer.original_length - closer.offset

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


def _cmark_process_emphasis(delimiter_stack: _cmark_DLL, ignore: list) -> list:
    # license D applies here. See docs/markdown_specification.rst

    # Store indices.
    openers_bottom = [None, None, None, None, None, None]

    stack_bottom = None

    # delimiter *closer = subj->last_delim;
    closer = delimiter_stack.last_delim

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
                    closer = _cmark_remove_emph(delimiter_stack, opener, closer, ignore)
                else:
                    closer = closer.next
            elif closer.delim_char == '\'' or closer.delim_char == '"':
                closer = closer.next
            if not opener_found:
                # set lower bound for future searches for openers
                openers_bottom[openers_bottom_index] = old_closer.previous
                if not old_closer.can_open:
                    # we can remove a closer that can't be an
                    # opener, once we've seen there's no
                    # matching opener:
                    delimiter_stack.extract(old_closer)
        else:
            closer = closer.next

    # free all delimiters in list until stack_bottom:
    while delimiter_stack.last_delim is not None and delimiter_stack.last_delim != stack_bottom:
        delimiter_stack.extract(delimiter_stack.last_delim)


def _cmark_handle_backslash(subj: _cmark_DLL, line: str, char: str):
    r"""Parse backslash-escape or just a backslash, returning an inline.

    .. note: license D applies here. See docs/markdown_specification.rst
    """
    _cmark_advance(subj)
    nextchar = _cmark_peek_char(line, subj.pos)

    # only ascii symbols and newline can be escaped
    if _cmark_ispunct(nextchar):
        _cmark_advance(subj)

def _cmark_make_literal(subj: _cmark_DLL, start_column: int, end_column: int, char: str):
    e = _cmarkCmarkNode()
    # FIXME.
    e.start_line = e.end_line = line;
    # columns are 1 based.
    e.start_column = start_column + 1
    e.end_column = end_column + 1

    return e

def _cmark_make_str(subj: _cmark_DLL, start_column: int, end_column: int, char: str):
    return _cmark_make_literal(subj, start_column, end_column, char)

def _cmark_push_bracket(subj: _cmark_DLL, image: bool, inl_text: str):
    b = Bracket()
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

def _cmark_handle_close_bracket(subj: _cmark_DLL):
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



def _cmark_parse_inline(subj: _cmark_DLL, line: str) -> tuple:
    r"""Handle all the different elements of a string.

    ..note: license D applies here. See docs/markdown_specification.rst
    """
    numdelim = 0

    c = _cmark_peek_char(line, subj.pos)
    if c == 0:
        return 0
    elif chr(c) == '\\':
        numdelim = _cmark_handle_backslash(subj, line, chr(c))
    elif chr(c) == '*' or chr(c) == '_' or chr(c) == '\'' or chr(c) == '"':
        numdelim = _cmark_handle_delim(subj, line, chr(c))
    elif chr(c) == '[':
        pass
#        _cmark_advance(subj)
#       new_inl = _cmark_make_str(subj, subj.pos - 1, subj.pos - 1, '[')
#        new_inl = line[subj.pos - 1]
#       _cmark_push_bracket(subj, False, new_inl)
    elif chr(c) == ']':
        pass

    # TODO: images, code, HTML tags detection.

    return numdelim


#######
# API #
#######
def write_string_on_file_between_markers(filename: str, string: str,
                                         marker: str):
    r"""Write the table of contents on a single file.

    :parameter filename: the file that needs to be read or modified.
    :parameter string: the string that will be written on the file.
    :parameter marker: a marker that will identify the start
         and the end of the string.
    :type filenames: str
    :type string: str
    :type marker: str
    :returns: None
    :rtype: None
    :raises: StdinIsNotAFileToBeWritten or an fpyutils exception
         or a built-in exception.
    """
    if filename == '-':
        raise StdinIsNotAFileToBeWritten

    final_string = marker + '\n\n' + string.rstrip() + '\n\n' + marker + '\n'
    marker_line_positions = fpyutils.filelines.get_line_matches(
        filename, marker, 2, loose_matching=True)

    if 1 in marker_line_positions:
        if 2 in marker_line_positions:
            fpyutils.filelines.remove_line_interval(
                filename, marker_line_positions[1], marker_line_positions[2],
                filename)
        else:
            fpyutils.filelines.remove_line_interval(
                filename, marker_line_positions[1], marker_line_positions[1],
                filename)
        fpyutils.filelines.insert_string_at_line(
            filename,
            final_string,
            marker_line_positions[1],
            filename,
            append=False)


def write_strings_on_files_between_markers(filenames: list, strings: list,
                                           marker: str):
    r"""Write the table of contents on multiple files.

    :parameter filenames: the files that needs to be read or modified.
    :parameter strings: the strings that will be written on the file. Each
         string is associated with one file.
    :parameter marker: a marker that will identify the start
         and the end of the string.
    :type filenames: list
    :type string: list
    :type marker: str
    :returns: None
    :rtype: None
    :raises: an fpyutils exception or a built-in exception.
    """
    if not len(filenames) == len(strings):
        raise ValueError
    if len(filenames) > 0:
        for f in filenames:
            if not isinstance(f, str):
                raise TypeError
    if len(strings) > 0:
        for s in strings:
            if not isinstance(s, str):
                raise TypeError

    file_id = 0
    for f in filenames:
        write_string_on_file_between_markers(f, strings[file_id], marker)
        file_id += 1


def build_toc(filename: str,
              ordered: bool = False,
              no_links: bool = False,
              no_indentation: bool = False,
              no_list_coherence: bool = False,
              keep_header_levels: int = 3,
              parser: str = 'github',
              list_marker: str = '-',
              skip_lines: int = 0,
              constant_ordered_list: bool = False,
              newline_string: str = common_defaults['newline string']) -> str:
    r"""Build the table of contents of a single file.

    :parameter filename: the file that needs to be read.
    :parameter ordered: decides whether to build an ordered list or not.
         Defaults to ``False``.
    :parameter no_links: disables the use of links.
         Defaults to ``False``.
    :parameter no_indentation: disables indentation in the list.
         Defaults to ``False``.
    :parameter keep_header_levels: the maximum level of headers to be
         considered as such when building the table of contents.
         Defaults to ``3``.
    :parameter parser: decides rules on how to generate anchor links.
         Defaults to ``github``.
    :parameter list_marker: a string that contains some of the first
         characters of the list element.
         Defaults to ``-``.
    :parameter skip_lines: the number of lines to be skipped from
         the start of file before parsing for table of contents.
         Defaults to ``0```.
    :parameter constant_ordered_list: use a single integer
        as list marker. This sets ordered to ``True``.
    :parameter newline_string: the set of characters used to
        go to a new line.
    :type filename: str
    :type ordered: bool
    :type no_links: bool
    :type no_indentation: bool
    :type keep_header_levels: int
    :type parser: str
    :type list_marker: str
    :type skip_lines: int
    :type constant_ordered_list: bool
    :type newline_string: str
    :returns: toc, the corresponding table of contents of the file.
    :rtype: str
    :raises: a built-in exception.
    """
    if not skip_lines >= 0:
        raise ValueError

    toc = str()
    header_type_counter = dict()
    header_type_curr = 0
    header_type_prev = 0
    header_type_first = 0
    header_duplicate_counter = dict()

    if filename == '-':
        f = sys.stdin
    else:
        # When reading input from the stream,
        # if newline is None, universal newlines mode is enabled.
        # Lines in the input can end in '\n', '\r', or '\r\n',
        # and these are translated into '\n' before being returned to the caller.
        # See
        # https://docs.python.org/3/library/functions.html#open-newline-parameter
        f = open(filename, 'r', newline=None)

    # Help the developers: override the list_marker in case
    # this function is called with the default unordered list marker,
    # for example like this:
    # print(md_toc.build_toc('test.md', ordered=True))
    # This avoids an AssertionError later on.
    if (ordered and list_marker == md_parser[parser]['list']['unordered']['default marker']):
        list_marker = md_parser[parser]['list']['ordered'][
            'default closing marker']
    if constant_ordered_list:
        ordered = True
    if ordered and (list_marker is None or list_marker not in md_parser[parser]['list']['ordered']['closing markers']):
        list_marker = md_parser[parser]['list']['ordered']['default closing marker']

    if skip_lines > 0:
        loop = True
        line_counter = 1
        while loop:
            if line_counter > skip_lines or f.readline() == str():
                loop = False
            line_counter += 1

    line = f.readline()
    indentation_log = init_indentation_log(parser, list_marker)
    if not no_indentation and not no_list_coherence:
        indentation_list = init_indentation_status_list(parser)
    is_within_code_fence = False
    code_fence = None
    is_document_end = False
    while line:
        # Document ending detection.
        #
        # This changes the state of is_within_code_fence if the
        # file has no closing fence markers. This serves no practial
        # purpose since the code would run correctly anyway. It is
        # however more sematically correct.
        #
        # See the unit tests (examples 95 and 96 of the github parser)
        # and the is_closing_code_fence function.
        if filename != '-':
            # stdin is not seekable.
            file_pointer_pos = f.tell()
            if f.readline() == str():
                is_document_end = True
            f.seek(file_pointer_pos)

        # Code fence detection.
        if is_within_code_fence:
            is_within_code_fence = not is_closing_code_fence(
                line, code_fence, is_document_end, parser)
        else:
            code_fence = is_opening_code_fence(line, parser)
            if code_fence is not None:
                # Update the status of the next line.
                is_within_code_fence = True

        if not is_within_code_fence or code_fence is None:

            # Header detection and gathering.
            headers = get_md_header(line, header_duplicate_counter,
                                    keep_header_levels, parser, no_links)

            # We only need to get the first element since all the lines
            # have been already separated here.
            header = headers[0]

            if header is not None:
                header_type_curr = header['type']

                # Take care of the ordered TOC.
                if ordered and not constant_ordered_list:
                    increase_index_ordered_list(header_type_counter,
                                                header_type_prev,
                                                header_type_curr, parser)
                    index = header_type_counter[header_type_curr]
                elif constant_ordered_list:
                    # This value should work on most parsers.
                    index = 1
                else:
                    index = 1

                # Take care of list indentations.
                if no_indentation:
                    no_of_indentation_spaces_curr = 0
                    # TOC list coherence checks are not necessary
                    # without indentation.
                else:
                    if not no_list_coherence:
                        if header_type_first == 0:
                            header_type_first = header_type_curr
                        if not toc_renders_as_coherent_list(
                                header_type_curr, header_type_first,
                                indentation_list, parser):
                            raise TocDoesNotRenderAsCoherentList

                    compute_toc_line_indentation_spaces(
                        header_type_curr, header_type_prev, parser, ordered,
                        list_marker, indentation_log, index)
                    no_of_indentation_spaces_curr = indentation_log[
                        header_type_curr]['indentation spaces']

                # Build a single TOC line.
                toc_line_no_indent = build_toc_line_without_indentation(
                    header, ordered, no_links, index, parser, list_marker)

                # Save the TOC line with the indentation.
                toc += build_toc_line(toc_line_no_indent,
                                      no_of_indentation_spaces_curr) + newline_string

                header_type_prev = header_type_curr

            # endif

        # endif

        line = f.readline()

    # endwhile

    f.close()

    return toc


def build_multiple_tocs(filenames: list,
                        ordered: bool = False,
                        no_links: bool = False,
                        no_indentation: bool = False,
                        no_list_coherence: bool = False,
                        keep_header_levels: int = 3,
                        parser: str = 'github',
                        list_marker: str = '-',
                        skip_lines: int = 0,
                        constant_ordered_list: bool = False,
                        newline_string: str = common_defaults['newline string']) -> list:
    r"""Parse files by line and build the table of contents of each file.

    :parameter filenames: the files that needs to be read.
    :parameter ordered: decides whether to build an ordered list or not.
         Defaults to ``False``.
    :parameter no_links: disables the use of links.
         Defaults to ``False``.
    :parameter no_indentation: disables indentation in the list.
         Defaults to ``False``.
    :parameter keep_header_levels: the maximum level of headers to be
         considered as such when building the table of contents.
         Defaults to ``3``.
    :parameter parser: decides rules on how to generate anchor links.
         Defaults to ``github``.
    :parameter skip_lines: the number of lines to be skipped from
         the start of file before parsing for table of contents.
         Defaults to ``0```.
    :parameter list_marker: a string that contains some of the first
         characters of the list element.
         Defaults to ``-``.
    :parameter constant_ordered_list: use a single integer
        as list marker. This sets ordered to ``True``.
    :type filenames: list
    :type ordered: bool
    :type no_links: bool
    :type no_indentation: bool
    :type keep_header_levels: int
    :type parser: str
    :type list_marker: str
    :type skip_lines: int
    :type constant_ordered_list: bool
    :returns: toc_struct, the corresponding table of contents for each input
         file.
    :rtype: list
    :raises: a built-in exception.

    .. warning:: In case of ordered TOCs you must explicitly pass one of the
        supported ordered list markers.
    """
    if len(filenames) > 0:
        for f in filenames:
            if not isinstance(f, str):
                raise TypeError

    if len(filenames) == 0:
        filenames.append('-')
    file_id = 0
    toc_struct = list()
    while file_id < len(filenames):
        toc_struct.append(
            build_toc(filenames[file_id], ordered, no_links, no_indentation,
                      no_list_coherence, keep_header_levels, parser,
                      list_marker, skip_lines, constant_ordered_list, newline_string))
        file_id += 1

    return toc_struct


def increase_index_ordered_list(header_type_count: dict,
                                header_type_prev: int,
                                header_type_curr: int,
                                parser: str = 'github'):
    r"""Compute the current index for ordered list table of contents.

    :parameter header_type_count: the count of each header type.
    :parameter header_type_prev: the previous type of header (h[1,...,Inf]).
    :parameter header_type_curr: the current type of header (h[1,...,Inf]).
    :parameter parser: decides rules on how to generate ordered list markers.
         Defaults to ``github``.
    :type header_type_count: dict
    :type header_type_prev: int
    :type header_type_curr: int
    :type parser: str
    :returns: None
    :rtype: None
    :raises: GithubOverflowOrderedListMarker or a built-in exception.
    """
    # header_type_prev might be 0 while header_type_curr can't.
    if not header_type_prev >= 0:
        raise ValueError
    if not header_type_curr >= 1:
        raise ValueError

    # Base cases for a new table of contents or a new index type.
    if header_type_prev == 0:
        header_type_prev = header_type_curr
    if (header_type_curr not in header_type_count
            or header_type_prev < header_type_curr):
        header_type_count[header_type_curr] = 0

    header_type_count[header_type_curr] += 1

    if (parser == 'github' or parser == 'cmark' or parser == 'gitlab'
            or parser == 'commonmarker'):
        if header_type_count[header_type_curr] > md_parser['github']['list'][
                'ordered']['max marker number']:
            raise GithubOverflowOrderedListMarker


def init_indentation_log(parser: str = 'github',
                         list_marker: str = '-') -> dict:
    r"""Create a data structure that holds list marker information.

    :parameter parser: decides rules on how compute indentations.
         Defaults to ``github``.
    :parameter list_marker: a string that contains some of the first
         characters of the list element. Defaults to ``-``.
    :type parser: str
    :type list_marker: str
    :returns: indentation_log, the data structure.
    :rtype: dict
    :raises: a built-in exception.

    .. warning: this function does not make distinctions between ordered and unordered
         TOCs.
    """
    if parser not in md_parser:
        raise ValueError

    indentation_log = dict()
    for i in range(1, md_parser[parser]['header']['max levels'] + 1):
        indentation_log[i] = {
            'index': md_parser[parser]['list']['ordered']['min marker number'],
            'list marker': list_marker,
            'indentation spaces': 0
        }

    return indentation_log


def compute_toc_line_indentation_spaces(
        header_type_curr: int = 1,
        header_type_prev: int = 0,
        parser: str = 'github',
        ordered: bool = False,
        list_marker: str = '-',
        indentation_log: dict = init_indentation_log('github', '-'),
        index: int = 1):
    r"""Compute the number of indentation spaces for the TOC list element.

    :parameter header_type_curr: the current type of header (h[1,...,Inf]).
         Defaults to ``1``.
    :parameter header_type_prev: the previous type of header (h[1,...,Inf]).
         Defaults to ``0``.
    :parameter parser: decides rules on how compute indentations.
         Defaults to ``github``.
    :parameter ordered: if set to ``True``, numbers will be used
         as list ids instead of dash characters.
         Defaults to ``False``.
    :parameter list_marker: a string that contains some of the first
         characters of the list element.
         Defaults to ``-``.
    :parameter indentation_log: a data structure that holds list marker
         information for ordered lists.
         Defaults to ``init_indentation_log('github', '.')``.
    :parameter index: a number that will be used as list id in case of an
         ordered table of contents. Defaults to ``1``.
    :type header_type_curr: int
    :type header_type_prev: int
    :type parser: str
    :type ordered: bool
    :type list_marker: str
    :type indentation_log: dict
    :type index: int
    :returns: None
    :rtype: None
    :raises: a built-in exception.

    .. warning:: In case of ordered TOCs you must explicitly pass one of the
        supported ordered list markers.
    """
    if not header_type_curr >= 1:
        raise ValueError
    if not header_type_prev >= 0:
        raise ValueError
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark', 'redcarpet']:
        if ordered:
            if list_marker not in md_parser[parser]['list']['ordered']['closing markers']:
                raise ValueError
        else:
            if list_marker not in md_parser[parser]['list']['unordered']['bullet markers']:
                raise ValueError
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:
        if not len(indentation_log) == md_parser['github']['header']['max levels']:
            raise ValueError
        for i in range(1, md_parser['github']['header']['max levels'] + 1):
            if 'index' not in indentation_log[i]:
                raise ValueError
            if 'list marker' not in indentation_log[i]:
                raise ValueError
            if 'indentation spaces' not in indentation_log[i]:
                raise ValueError
            if not isinstance(indentation_log[i]['list marker'], str):
                raise TypeError
            if not isinstance(indentation_log[i]['index'], int):
                raise TypeError
            if not isinstance(indentation_log[i]['indentation spaces'], int):
                raise TypeError
    if not index >= 1:
        raise TypeError

    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:
        if ordered:
            if header_type_prev == 0:
                index_length = 0
            else:
                index_length = len(
                    str(indentation_log[header_type_prev]['index']))
        else:
            index_length = 0

        if header_type_prev == 0:
            # Base case for the first toc line.
            indentation_log[header_type_curr]['indentation spaces'] = 0
        elif header_type_curr > header_type_prev:
            # More indentation.
            indentation_log[header_type_curr]['indentation spaces'] = (
                indentation_log[header_type_prev]['indentation spaces'] + len(
                    indentation_log[header_type_prev]['list marker']) +
                index_length + len(' '))
        elif header_type_curr < header_type_prev:
            # Less indentation. Since we went "back" we must reset
            # all the sublists in the data structure. The indentation spaces are the ones
            # computed before.
            for i in range(header_type_curr + 1,
                           md_parser['github']['header']['max levels'] + 1):
                indentation_log[i]['index'] = md_parser['github']['list'][
                    'ordered']['min marker number']
                indentation_log[i]['indentation spaces'] = 0
                indentation_log[i]['list marker'] = list_marker
        # And finally, in case of same indentation we have: header_type_curr = header_type_prev
        # so indentation_log[header_type_curr]['indentation spaces'] = indentation_log[header_type_prev]['indentation spaces']
        # which is an identity.

        if ordered:
            indentation_log[header_type_curr]['index'] = index
        indentation_log[header_type_curr]['list marker'] = list_marker

    elif parser in ['redcarpet']:
        indentation_log[header_type_curr]['indentation spaces'] = 4 * (
            header_type_curr - 1)


def build_toc_line_without_indentation(header: dict,
                                       ordered: bool = False,
                                       no_links: bool = False,
                                       index: int = 1,
                                       parser: str = 'github',
                                       list_marker: str = '-') -> str:
    r"""Return a list element of the table of contents.

    :parameter header: a data structure that contains the original
         text, the trimmed text and the type of header.
    :parameter ordered: if set to ``True``, numbers will be used
         as list ids, otherwise a dash character. Defaults
         to ``False``.
    :parameter no_links: disables the use of links. Defaults to ``False``.
    :parameter index: a number that will be used as list id in case of an
         ordered table of contents. Defaults to ``1``.
    :parameter parser: decides rules on how compute indentations.
         Defaults to ``github``.
    :parameter list_marker: a string that contains some of the first
         characters of the list element. Defaults to ``-``.
    :type header: dict
    :type ordered: bool
    :type no_links: bool
    :type index: int
    :type parser: str
    :type list_marker: str
    :returns: toc_line_no_indent, a single line of the table of contents
         without indentation.
    :rtype: str
    :raises: a built-in exception.

    .. warning:: In case of ordered TOCs you must explicitly pass one of the
        supported ordered list markers.
    """
    if 'type' not in header:
        raise ValueError
    if 'text_original' not in header:
        raise ValueError
    if 'text_anchor_link' not in header:
        raise ValueError
    if not isinstance(header['type'], int):
        raise TypeError
    if not isinstance(header['text_original'], str):
        raise TypeError
    if not isinstance(header['text_anchor_link'], str):
        raise TypeError
    if not header['type'] >= 1:
        raise ValueError
    if not index >= 1:
        raise ValueError
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark', 'redcarpet']:
        if ordered:
            if list_marker not in md_parser[parser]['list']['ordered']['closing markers']:
                raise ValueError
        else:
            if list_marker not in md_parser[parser]['list']['unordered']['bullet markers']:
                raise ValueError

    toc_line_no_indent = str()

    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark', 'redcarpet']:
        if ordered:
            list_marker = str(index) + list_marker

        # See
        # https://spec.commonmark.org/0.28/#example-472
        # and
        # https://github.com/vmg/redcarpet/blob/e3a1d0b00a77fa4e2d3c37322bea66b82085486f/ext/redcarpet/markdown.c#L998
        if no_links:
            line = header['text_original']
        else:
            line = '[' + header['text_original'] + ']' + '(#' + header[
                'text_anchor_link'] + ')'
        toc_line_no_indent = list_marker + ' ' + line

    return toc_line_no_indent


def build_toc_line(toc_line_no_indent: str,
                   no_of_indentation_spaces: int = 0) -> str:
    r"""Build the TOC line.

    :parameter toc_line_no_indent: the TOC line without indentation.
    :parameter no_of_indentation_spaces: the number of indentation spaces.
         Defaults to ``0``.
    :type toc_line_no_indent: str
    :type no_of_indentation_spaces: int
    :returns: toc_line, a single line of the table of contents.
    :rtype: str
    :raises: a built-in exception.
    """
    if not no_of_indentation_spaces >= 0:
        raise ValueError

    indentation = no_of_indentation_spaces * ' '
    toc_line = indentation + toc_line_no_indent

    return toc_line


def remove_html_tags(line: str, parser: str = 'github') -> str:
    r"""Remove HTML tags.

    :parameter line: a string.
    :parameter parser: decides rules on how to remove HTML tags.
         Defaults to ``github``.
    :type line: str
    :type parser: str
    :returns: the input string without HTML tags.
    :rtype: str
    :raises: a built-in exception.
    """
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:
        # We need to match newline as well because it is a WS, so we
        # must use re.DOTALL.
        line = re.sub(md_parser[parser]['re']['OT'], str(), line, flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['CT'], str(), line, flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['CO'], str(), line, flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['PI'], str(), line, flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['DE'], str(), line, flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['CD'], str(), line, flags=re.DOTALL)

    return line


def remove_emphasis(line: str, parser: str = 'github') -> list:
    r"""Remove emphasis.

    :parameter line: a string.
    :parameter parser: decides rules on how to find delimiters.
        Defaults to ``github``.
    :type line: str
    :type parser: str
    :returns: the input line without emphasis.
    :rtype: str
    :raises: a built-in exception.
    """
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark', 'redcarpet']:

        delimiter_stack = _cmark_DLL()
        i = 0
        while i < len(line):
            delimiter_stack.pos = i
            numdelims = _cmark_parse_inline(delimiter_stack, line)

            advance = False
            if delimiter_stack.pos > i:
                i = delimiter_stack.pos
                advance = True

            if not advance:
                i += 1

        ignore = list()

        # When we hit the end of the input, we call the process emphasis procedure (see below), with stack_bottom = NULL.
        _cmark_process_emphasis(delimiter_stack, ignore)
        line = filter_indices_from_line(line, ignore)
    elif parser in ['redcarpet']:
        # TODO
        pass

    return line


def filter_indices_from_line(line: str, ranges: list) -> str:
    r"""Given a line and a Python ranges, remove the characters in the ranges.

    :parameter line: a string.
    :parameter ranges: a list of Python ranges.
    :type line: str
    :type ranges: list
    :returns: the line without the specified indices.
    :rtype: str
    :raises: a built-in exception.
    """
    # Transform ranges into lists.
    rng = list()
    for r in ranges:
        rng.append(list(r))

    # Flatten list.
    ll = [item for e in rng for item in e]

    s = sorted(ll)
    final = str()
    i = 0
    while i < len(line):
        if i not in s:
            final += line[i]
        i += 1

    return final


def build_anchor_link(header_text_trimmed: str,
                      header_duplicate_counter: str,
                      parser: str = 'github') -> str:
    r"""Apply the specified slug rule to build the anchor link.

    :parameter header_text_trimmed: the text that needs to be transformed
        in a link.
    :parameter header_duplicate_counter: a data structure that keeps track of
        possible duplicate header links in order to avoid them. This is
        meaningful only for certain values of parser.
    :parameter parser: decides rules on how to generate anchor links.
        Defaults to ``github``.
    :type header_text_trimmed: str
    :type header_duplicate_counter: dict
    :type parser: str
    :returns: None if the specified parser is not recognized, or the anchor
        link, otherwise.
    :rtype: str
    :raises: a built-in exception.

    .. note: license A applies for the redcarpet part.
        See docs/markdown_specification.rst
    """
    # Check for newlines.
    if len(replace_and_split_newlines(header_text_trimmed)) > 1:
        raise StringCannotContainNewlines

    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:
        header_text_trimmed = header_text_trimmed.lower()

        # Filter HTML tags.
        header_text_trimmed = remove_html_tags(header_text_trimmed, parser)

        # Filter "emphasis and strong emphasis".
        header_text_trimmed = remove_emphasis(header_text_trimmed, parser)

        # Remove punctuation: Keep spaces, hypens and "word characters"
        # only.
        header_text_trimmed = re.sub(r'[^\w\s\- ]', '', header_text_trimmed)
        # Replace spaces with dash.
        header_text_trimmed = header_text_trimmed.replace(' ', '-')

        if parser in ['gitlab']:
            # See https://docs.gitlab.com/ee/user/markdown.html#header-ids-and-links
            # Two or more hyphens in a row are converted to one.
            header_text_trimmed = re.sub('-+', '-', header_text_trimmed)

        # Check for duplicates.
        ht = header_text_trimmed
        # Set the initial value if we are examining the first occurrency.
        # The state of header_duplicate_counter is available to the caller
        # functions.
        if header_text_trimmed not in header_duplicate_counter:
            header_duplicate_counter[header_text_trimmed] = 0
        if header_duplicate_counter[header_text_trimmed] > 0:
            header_text_trimmed = header_text_trimmed + '-' + str(
                header_duplicate_counter[header_text_trimmed])
        header_duplicate_counter[ht] += 1
        return header_text_trimmed
    elif parser in ['redcarpet']:
        # To ensure full compatibility what follows is a direct translation
        # of the rndr_header_anchor C function used in redcarpet.
        STRIPPED = " -&+$,/:;=?@\"#{}|^~[]`\\*()%.!'"
        header_text_trimmed_len = len(header_text_trimmed)
        inserted = 0
        stripped = 0
        header_text_trimmed_middle_stage = ''
        for i in range(0, header_text_trimmed_len):
            if header_text_trimmed[i] == '<':
                while i < header_text_trimmed_len and header_text_trimmed[
                        i] != '>':
                    i += 1
            elif header_text_trimmed[i] == '&':
                while i < header_text_trimmed_len and header_text_trimmed[
                        i] != ';':
                    i += 1
            # str.find() == -1 if character is not found in str.
            # https://docs.python.org/3.6/library/stdtypes.html?highlight=find#str.find
            elif not _isascii(header_text_trimmed[i]) or STRIPPED.find(
                    header_text_trimmed[i]) != -1:
                if inserted and not stripped:
                    header_text_trimmed_middle_stage += '-'
                stripped = 1
            else:
                header_text_trimmed_middle_stage += header_text_trimmed[
                    i].lower()
                stripped = 0
                inserted += 1

        if stripped > 0 and inserted > 0:
            header_text_trimmed_middle_stage = header_text_trimmed_middle_stage[
                0:-1]

        if inserted == 0 and header_text_trimmed_len > 0:
            hash = 5381
            for i in range(0, header_text_trimmed_len):
                # Get the unicode representation with ord.
                # Unicode should be equal to ASCII in ASCII's range of
                # characters.
                hash = ((hash << 5) + hash) + ord(header_text_trimmed[i])

            # This is equivalent to %x in C. In Python we don't have
            # the length problem so %x is equal to %lx in this case.
            # Apparently there is no %l in Python...
            header_text_trimmed_middle_stage = 'part-' + '{0:x}'.format(hash)

        return header_text_trimmed_middle_stage


def replace_and_split_newlines(line: str) -> list:
    r"""Replace all the newline characters with line feeds and separate the components.

    :parameter line: a string.
    :type line: str
    :returns: a list of newline separated strings.
    :rtype: list
    :raises: a built-in exception.
    """
    line = line.replace('\r\n', '\n')
    line = line.replace('\r', '\n')

    # Ignore the sequences of consecutive first and last newline characters.
    # Since there is no need to process the last
    # empty line.
    line = line.lstrip('\n')
    line = line.rstrip('\n')

    line = line.split('\n')

    return line


def get_atx_heading(line: str,
                    keep_header_levels: int = 3,
                    parser: str = 'github',
                    no_links: bool = False) -> list:
    r"""Given a line extract the link label and its type.

    :parameter line: the line to be examined. This string may include newline
        characters in between.
    :parameter keep_header_levels: the maximum level of headers to be
         considered as such when building the table of contents.
         Defaults to ``3``.
    :parameter parser: decides rules on how to generate the anchor text.
         Defaults to ``github``.
    :parameter no_links: disables the use of links.
    :type line: str
    :type keep_header_levels: int
    :type parser: str
    :type no_links: bool
    :returns: struct, a list of dictionaries with ``header type`` (int)
        and ``header text trimmed`` (str) keys. Both values are
        set to ``None`` if the line does not contain header elements according to
        the rules of the selected markdown parser.
    :rtype: list
    :raises: GithubEmptyLinkLabel or GithubOverflowCharsLinkLabel or a
         built-in exception.

    .. note:: license B applies for the github part and license A for redcarpet part.
         See docs/markdown_specification.rst
    """
    if not keep_header_levels >= 1:
        raise ValueError

    struct = list()

    if len(line) == 0:
        return [{'header type': None, 'header text trimmed': None}]

    for subl in replace_and_split_newlines(line):
        current_headers = None
        final_line = None

        if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:

            struct.append({'header type': None, 'header text trimmed': None})

            # Empty substring or backslash.
            if len(subl) == 0 or subl[0] == '\u005c':
                continue

            i = 0
            while i < len(subl) and subl[i] == ' ' and i <= md_parser['github'][
                    'header']['max space indentation']:
                i += 1
            if i > md_parser['github']['header']['max space indentation']:
                continue

            offset = i
            while i < len(subl) and subl[i] == '#' and i <= md_parser['github'][
                    'header']['max levels'] + offset:
                i += 1
            if i - offset > md_parser['github']['header'][
                    'max levels'] or i - offset > keep_header_levels or i - offset == 0:
                continue

            current_headers = i - offset

            # Include special cases for l endings which should not be
            # discarded as non-ATX headers.
            if i < len(subl) and (subl[i] != ' ' and subl[i] != '\u000a'
                                  and subl[i] != '\u000d'):
                continue

            i += 1
            # Exclude leading whitespaces after the ATX header identifier.
            while i < len(subl) and subl[i] == ' ':
                i += 1

            # An algorithm to find the start and the end of the closing sequence (cs).
            # The closing sequence includes all the significant part of the
            # string. This algorithm has a complexity of O(n) with n being the
            # length of the l.
            cs_start = i
            cs_end = cs_start
            # subl_prime =~ subl'.
            subl_prime = subl[::-1]
            len_subl = len(subl)
            hash_char_rounds = 0
            go = True
            i = 0
            hash_round_start = i

            # Ignore all characters after newlines and carrage returns which
            # are not at the end of the l.
            # See the two CRLF marker tests.
            crlf_marker = 0
            stripped_crlf = False
            while i < len_subl - cs_start:
                if subl_prime[i] in ['\u000a', '\u000d']:
                    crlf_marker = i
                    stripped_crlf = True
                i += 1

            # crlf_marker is the first CR LF character in the string.
            i = crlf_marker
            if stripped_crlf:
                # Skip last character only if is '\u000a', '\u000d'.
                i += 1

            # We know for sure that from now '\u000a', '\u000d' will not be
            # considered.
            cs_end = i

            # Cut spaces and hashes.
            while go and i < len_subl - cs_start:
                if (subl_prime[i] not in [' ', '#']
                        or hash_char_rounds > 1):
                    if i > hash_round_start and hash_char_rounds > 0:
                        cs_end = len_subl - hash_round_start
                    else:
                        cs_end = len_subl - i
                    go = False
                if go:
                    while subl_prime[i] == ' ':
                        i += 1
                    hash_round_start = i
                    while subl_prime[i] == '#':
                        i += 1
                    if i > hash_round_start:
                        hash_char_rounds += 1

            final_line = subl[cs_start:cs_end]

            # Add escaping.
            if not no_links:
                if len(final_line) > 0 and final_line[-1] == '\u005c':
                    final_line += ' '
                if len(
                        final_line.strip('\u0020').strip('\u0009').strip('\u000a').
                        strip('\u000b').strip('\u000c').strip('\u000d')) == 0:
                    raise GithubEmptyLinkLabel
                if len(final_line
                       ) > md_parser['github']['link']['max chars label']:
                    raise GithubOverflowCharsLinkLabel

                i = 0
                while i < len(final_line):
                    # Escape square brackets if not already escaped.
                    if (final_line[i] == '[' or final_line[i] == ']'):
                        j = i - 1
                        consecutive_escape_characters = 0
                        while j >= 0 and final_line[j] == '\u005c':
                            consecutive_escape_characters += 1
                            j -= 1
                        if ((consecutive_escape_characters > 0
                             and consecutive_escape_characters % 2 == 0)
                                or consecutive_escape_characters == 0):
                            tmp = '\u005c'
                        else:
                            tmp = str()
                        final_line = final_line[0:i] + tmp + final_line[i:len(
                            final_line)]
                        i += 1 + len(tmp)
                    else:
                        i += 1

            # Overwrite the element with None as values.
            struct[-1] = {'header type': current_headers, 'header text trimmed': final_line}

        elif parser in ['redcarpet']:

            struct.append({'header type': None, 'header text trimmed': None})

            if len(subl) == 0 or subl[0] != '#':
                continue

            i = 0
            while (i < len(subl)
                   and i < md_parser['redcarpet']['header']['max levels']
                   and subl[i] == '#'):
                i += 1
            current_headers = i

            if i < len(subl) and subl[i] != ' ':
                continue

            while i < len(subl) and subl[i] == ' ':
                i += 1

            end = i
            while end < len(subl) and subl[end] != '\n':
                end += 1

            while end > 0 and subl[end - 1] == '#':
                end -= 1

            while end > 0 and subl[end - 1] == ' ':
                end -= 1

            if end > i:
                final_line = subl
                if not no_links and len(final_line) > 0 and final_line[-1] == '\\':
                    final_line += ' '
                    end += 1
                final_line = final_line[i:end]

            if final_line is None:
                current_headers = None

            struct[-1] = {'header type': current_headers, 'header text trimmed': final_line}

        # TODO: escape or remove '[', ']', '(', ')' in inline links for redcarpet,
        # TODO: check link label rules for redcarpet.

    # endfor

    return struct


def get_md_header(header_text_line: str,
                  header_duplicate_counter: dict,
                  keep_header_levels: int = 3,
                  parser: str = 'github',
                  no_links: bool = False) -> dict:
    r"""Build a data structure with the elements needed to create a TOC line.

    :parameter header_text_line: a single markdown line that needs to be
        transformed into a TOC line. This line may include nmultiple newline
        characters in between.
    :parameter header_duplicate_counter: a data structure that contains the
         number of occurrencies of each header anchor link. This is used to
         avoid duplicate anchor links and it is meaningful only for certain
         values of parser.
    :parameter keep_header_levels: the maximum level of headers to be
         considered as such when building the table of contents.
         Defaults to ``3``.
    :parameter parser: decides rules on how to generate anchor links.
         Defaults to ``github``.
    :type header_text_line: str
    :type header_duplicate_counter: dict
    :type keep_header_levels: int
    :type parser: str
    :returns: a list with elements ``None`` if the input line does not correspond
        to one of the designated cases or a list of data structures containing
        the necessary components to create a table of contents.
    :rtype: list
    :raises: a built-in exception.

    .. note::
         This works like a wrapper to other functions.
    """
    result = get_atx_heading(header_text_line, keep_header_levels, parser,
                             no_links)

    headers = list()
    for r in result:
        if r == {'header type': None, 'header text trimmed': None}:
            headers.append(None)
        else:
            header_type, header_text_trimmed = r['header type'], r['header text trimmed']
            headers.append({
                'type':
                header_type,
                'text_original':
                header_text_trimmed,
                'text_anchor_link':
                build_anchor_link(header_text_trimmed, header_duplicate_counter,
                                  parser)
            })

    return headers


def is_valid_code_fence_indent(line: str, parser: str = 'github') -> bool:
    r"""Determine if the given line has valid indentation for a code block fence.

    :parameter line: a single markdown line to evaluate.
    :parameter parser: decides rules on how to generate the anchor text.
         Defaults to ``github``.
    :type line: str
    :type parser: str
    :returns: True if the given line has valid indentation or False
         otherwise.
    :rtype: bool
    :raises: a built-in exception.
    """
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:
        return len(line) - len(line.lstrip(
            ' ')) <= md_parser['github']['code fence']['min marker characters']
    elif parser in ['redcarpet']:
        # TODO.
        return False


def is_opening_code_fence(line: str, parser: str = 'github'):
    r"""Determine if the given line is possibly the opening of a fenced code block.

    :parameter line: a single markdown line to evaluate.
    :parameter parser: decides rules on how to generate the anchor text.
         Defaults to ``github``.
    :type line: str
    :type parser: str
    :returns: None if the input line is not an opening code fence. Otherwise,
         returns the string which will identify the closing code fence
         according to the input parsers' rules.
    :rtype: typing.Optional[str]
    :raises: a built-in exception.
    """
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:
        markers = md_parser['github']['code fence']['marker']
        marker_min_length = md_parser['github']['code fence'][
            'min marker characters']

        if not is_valid_code_fence_indent(line):
            return None

        line = line.lstrip(' ').rstrip('\n')
        if not line.startswith((markers['backtick'] * marker_min_length, markers['tilde'] * marker_min_length)):
            return None

        # The info string is the whole line except the first opening code
        # fence markers.
        if line == len(line) * line[0]:
            info_string = str()
            info_string_start = len(line)
        else:
            # Get the index where the info string starts.
            i = 0
            done = False
            while not done and i < len(line):
                if line[i] != line[0]:
                    info_string_start = i
                    done = True
                i += 1

            info_string = line[info_string_start:len(line)]

        # Backticks or tildes in info string are explicitly forbidden
        # in a backtick-opened code fence, for Commonmark 0.29.
        # This also solves example 107 [Commonmark 0.28]. See:
        # https://github.github.com/gfm/#example-107
        if markers['backtick'] in info_string and line[0] != markers['tilde']:
            return None

        return line[0:info_string_start]
    elif parser in ['redcarpet']:
        # TODO.
        return None


def is_closing_code_fence(line: str,
                          fence: str,
                          is_document_end: bool = False,
                          parser: str = 'github') -> bool:
    r"""Determine if the given line is the end of a fenced code block.

    :parameter line: a single markdown line to evaluate.
    :paramter fence: a sequence of backticks or tildes marking the start of
         the current code block. This is usually the return value of the
         is_opening_code_fence function.
    :parameter is_document_end: This variable tells the function that the
         end of the file is reached.
         Defaults to ``False``.
    :parameter parser: decides rules on how to generate the anchor text.
         Defaults to ``github``.
    :type line: str
    :type fence: str
    :type is_document_end: bool
    :type parser: str
    :returns: True if the line ends the current code block. False otherwise.
    :rtype: bool
    :raises: a built-in exception.
    """
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:
        markers = md_parser['github']['code fence']['marker']
        marker_min_length = md_parser['github']['code fence'][
            'min marker characters']

        if not is_valid_code_fence_indent(line):
            return False

        # Remove opening fence indentation after it is known to be valid.
        fence = fence.lstrip(' ')
        # Check if fence uses valid characters.
        if not fence.startswith((markers['backtick'], markers['tilde'])):
            return False

        if len(fence) < marker_min_length:
            return False

        # Additional security.
        fence = fence.rstrip('\n').rstrip(' ')
        # Check that all fence characters are equal.
        if fence != len(fence) * fence[0]:
            return False

        # We might be inside a code block if this is not closed
        # by the end of the document, according to example 96 and 97.
        # This means that the end of the document corresponds to
        # a closing code fence.
        # Of course we first have to check that fence is a valid opening
        # code fence marker.
        # See:
        # example 96 [Commonmark 0.29]
        # example 97 [Commonmark 0.29]
        if is_document_end:
            return True

        # Check if line uses the same character as fence.
        line = line.lstrip(' ')
        if not line.startswith(fence):
            return False

        line = line.rstrip('\n').rstrip(' ')
        # Solves:
        # example 93 -> 94 [Commonmark 0.28]
        # example 94 -> 95 [Commonmark 0.29]
        if len(line) < len(fence):
            return False

        # Closing fence must not have alien characters.
        if line != len(line) * line[0]:
            return False

        return True
    elif parser in ['redcarpet']:
        # TODO.
        return False


def init_indentation_status_list(parser: str = 'github'):
    r"""Create a data structure that holds the state of indentations.

    :parameter parser: decides the length of the list.
         Defaults to ``github``.
    :type parser: str
    :returns: indentation_list, a list that contains the state of
         indentations given a header type.
    :rtype: list
    :raises: a built-in exception.
    """
    indentation_list = list()

    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark', 'redcarpet']:
        for i in range(0, md_parser[parser]['header']['max levels']):
            indentation_list.append(False)

    return indentation_list


def toc_renders_as_coherent_list(
        header_type_curr: int = 1,
        header_type_first: int = 1,
        indentation_list: list = init_indentation_status_list('github'),
        parser: str = 'github') -> bool:
    r"""Check if the TOC will render as a working list.

    :parameter header_type_curr: the current type of header (h[1,...,Inf]).
    :parameter header_type_first: the type of header first encountered (h[1,...,Inf]).
         This must correspond to the one with the least indentation.
    :parameter parser: decides rules on how to generate ordered list markers.
    :type header_type_curr: int
    :type header_type_first: int
    :type indentation_list: list
    :type parser: str
    :returns: renders_as_list
    :rtype: bool
    :raises: a built-in exception.

    .. note: this function modifies the input list.
    """
    if not header_type_curr >= 1:
        raise ValueError
    if not header_type_first >= 1:
        raise ValueError
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark', 'redcarpet']:
        if not len(indentation_list) == md_parser[parser]['header']['max levels']:
            raise ValueError
    for e in indentation_list:
        if not isinstance(e, bool):
            raise TypeError

    renders_as_list = True
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark', 'redcarpet']:
        # Update with current information.
        indentation_list[header_type_curr - 1] = True

        # Reset next cells to False, as a detection mechanism.
        for i in range(header_type_curr,
                       md_parser['github']['header']['max levels']):
            indentation_list[i] = False

        # Check for previous False cells. If there is a "hole" in the list
        # it means that the TOC will have "wrong" indentation spaces, thus
        # either not rendering as an HTML list or not as the user intended.
        i = header_type_curr - 1
        while i >= header_type_first - 1 and indentation_list[i]:
            i -= 1
        if i >= header_type_first - 1:
            renders_as_list = False
        if header_type_curr < header_type_first:
            renders_as_list = False

    return renders_as_list


if __name__ == '__main__':
    pass
