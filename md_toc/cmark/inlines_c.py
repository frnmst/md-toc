# -*- coding: utf-8 -*-
#
# inlines_c.py
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
from ..generic import _replace_substring
from .buffer_c import (
    _cmark_cmark_strbuf_detach,
    _cmark_cmark_strbuf_drop,
    _cmark_cmark_strbuf_puts,
    _cmark_cmark_strbuf_set,
    _cmark_cmark_strbuf_truncate,
    _cmark_cmark_strbuf_unescape,
)
from .buffer_h import _cmark_CMARK_BUF_INIT, _cmarkCmarkStrbuf
from .chunk_h import (
    _cmark_cmark_chunk_dup,
    _cmark_cmark_chunk_free,
    _cmark_cmark_chunk_literal,
    _cmark_cmark_chunk_rtrim,
    _cmark_cmark_chunk_trim,
    _cmarkCmarkChunk,
)
from .cmark_ctype_c import _cmark_cmark_ispunct, _cmark_cmark_isspace
from .cmark_h import _cmarkCmarkMem
from .houdini_html_u_c import (
    _cmark_houdini_unescape_html,
    _cmark_houdini_unescape_html_f,
)
from .node_c import (
    _cmark_cmark_node_free,
    _cmark_cmark_node_insert_after,
    _cmark_cmark_node_insert_before,
    _cmark_cmark_node_set_literal,
    _cmark_cmark_node_unlink,
)
from .node_h import _cmarkCmarkNode
from .references_c import _cmark_cmark_reference_lookup
from .references_h import _cmarkCmarkReference, _cmarkCmarkReferenceMap
from .scanners_h import (
    _cmark_scan_autolink_email,
    _cmark_scan_autolink_uri,
    _cmark_scan_html_cdata,
    _cmark_scan_html_comment,
    _cmark_scan_html_declaration,
    _cmark_scan_html_pi,
    _cmark_scan_html_tag,
    _cmark_scan_link_title,
    _cmark_scan_spacechars,
)
from .utf8_c import (
    _cmark_cmark_utf8proc_is_punctuation,
    _cmark_cmark_utf8proc_is_space,
    _cmark_cmark_utf8proc_iterate,
)

# License C applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


# 0.29, 0.30
def _cmark_make_linebreak(mem: _cmarkCmarkMem):
    return _cmark_make_simple(
        mem, md_parser['cmark']['cmark_node_type']['CMARK_NODE_LINEBREAK'])


def _cmark_make_softbreak(mem: _cmarkCmarkMem):
    return _cmark_make_simple(
        mem, md_parser['cmark']['cmark_node_type']['CMARK_NODE_SOFTBREAK'])


def _cmark_make_emph(mem: _cmarkCmarkMem):
    return _cmark_make_simple(
        mem, md_parser['cmark']['cmark_node_type']['CMARK_NODE_EMPH'])


def _cmark_make_strong(mem: _cmarkCmarkMem):
    return _cmark_make_simple(
        mem, md_parser['cmark']['cmark_node_type']['CMARK_NODE_STRONG'])


class _cmarkDelimiter:
    r"""A list node with attributes useful for processing emphasis."""

    __slots__ = [
        'previous',
        'next',
        'inl_text',
        'length',
        'delim_char',
        'can_open',
        'can_close',
        'offset',
    ]

    def __init__(self):
        self.previous: _cmarkDelimiter = None
        self.next: _cmarkDelimiter = None
        self.inl_text: _cmarkCmarkNode = None
        self.length: int = 0
        self.delim_char = str()
        self.can_open: bool = False
        self.can_close: bool = False

        # Extra attribute.
        self.offset: int = 0

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
            de = 'delim_char = ' + self.delim_char
            le = 'length = ' + str(self.length)
            of = 'offset = ' + str(self.offset)
            ac = 'active = ' + str(self.active)
            pr = 'previous = ' + previous
            ne = 'next = ' + next
            co = 'can_open = ' + str(self.can_open)
            cc = 'can_close = ' + str(self.can_close)

            return (el + '\n' + it + '\n' + '\n' + de + '\n' + le + '\n' + of +
                    '\n' + ac + '\n' + pr + '\n' + ne + '\n' + co + '\n' + cc +
                    '\n')


class _cmarkBracket:
    __slots__ = [
        'previous',
        'previous_delimiter',
        'inl_text',
        'position',
        'image',
        'active',
        'bracket_after',
    ]

    def __init__(self):
        self.previous: _cmarkBracket = None
        self.previous_delimiter: _cmarkDelimiter = None
        self.inl_text: _cmarkCmarkNode = None
        self.position: bool = 0
        self.image: bool = False
        self.active: bool = True
        self.bracket_after: bool = False


class _cmarkSubject:
    r"""A double linked list useful for processing emphasis."""

    __slots__ = [
        'mem',
        'input',
        'flags',
        'line',
        'pos',
        'block_offset',
        'column_offset',
        'refmap',
        'last_delim',
        'last_bracket',
        'backticks',
        'scanned_for_backticks',
    ]

    def __init__(self):
        self.mem: _cmarkCmarkMem = None
        self.input: _cmarkCmarkChunk = None
        self.flags: int = 0
        self.line: int = 0
        self.pos: int = 0
        self.block_offset: int = 0
        self.column_offset: int = 0
        self.refmap: _cmarkCmarkReferenceMap = None
        self.last_delim: _cmarkDelimiter = None
        self.last_bracket: _cmarkBracket = None

        # An integer list.
        self.backticks: list = list(
            range(0, md_parser['cmark']['generic']['MAXBACKTICKS'] + 1))

        self.scanned_for_backticks: bool = False

    def scroll(self):
        r"""Print the list."""
        print(self.start)
        print('===')
        x = self.start
        while x is not None:
            print(x)
            x = x.next


# 0.30
def _cmark_S_is_line_end_char(c: str) -> bool:
    return c == '\n' or c == '\r'


# 0.30
def _cmark_make_literal(subj: _cmarkSubject, t: int, start_column: int,
                        end_column: int) -> _cmarkCmarkNode:
    r"""Create an inline with a literal string value."""
    e = _cmarkCmarkNode()

    e.mem = copy.deepcopy(subj.mem)
    e.type = t
    e.start_line = e.end_line = subj.line
    # columns are 1 based.
    e.start_column: int = start_column + 1 + subj.column_offset + subj.block_offset
    e.end_column: int = end_column + 1 + subj.column_offset + subj.block_offset
    return e


# 0.30
def _cmark_make_simple(mem: _cmarkCmarkMem, t: int) -> _cmarkCmarkNode:
    e = _cmarkCmarkNode()
    e.mem = copy.deepcopy(mem)
    e.type = t
    return e


# 0.30
def _cmark_make_str(subj: _cmarkSubject, sc: int, ec: int,
                    s: _cmarkCmarkChunk) -> _cmarkCmarkNode:
    # s = char
    # sc = start column
    # ec = end cloumn
    e = _cmark_make_literal(
        subj, md_parser['cmark']['cmark_node_type']['CMARK_NODE_TEXT'], sc, ec)

    # e->data = (unsigned char *)subj->mem->realloc(NULL, s.len + 1);

    # if (s.data != NULL) {
    #   memcpy(e->data, s.data, s.len);
    # }
    if s.data is not None:
        e.data = copy.deepcopy(s.data[:s.length])

    # No need to add line terminator (\0).
    #     e->data[s.len] = 0;
    e.length = s.length
    return e


def _cmark_make_str_from_buf(
    subj: _cmarkSubject,
    sc: int,
    ec: int,
    buf: _cmarkCmarkStrbuf,
) -> _cmarkCmarkNode:
    e: _cmarkCmarkNode = _cmark_make_literal(
        subj, md_parser['cmark']['cmark_node_type']['CMARK_NODE_TEXT'], sc, ec)
    e.length = buf.size
    e.data = _cmark_cmark_strbuf_detach(buf)
    return e


# Like make_str, but parses entities.
def _cmark_make_str_with_entities(
    subj: _cmarkSubject,
    start_column: int,
    end_column: int,
    content: _cmarkCmarkChunk,
) -> _cmarkCmarkNode:
    unescaped: _cmarkCmarkStrbuf = _cmark_CMARK_BUF_INIT(subj.mem)

    if _cmark_houdini_unescape_html(unescaped, content.data, content.length):
        return _cmark_make_str_from_buf(subj, start_column, end_column,
                                        unescaped)
    else:
        return _cmark_make_str(subj, start_column, end_column, content)


# Like cmark_node_append_child but without costly sanity checks.
# Assumes that child was newly created.
def _cmark_append_child(node: _cmarkCmarkNode, child: _cmarkCmarkNode):
    old_last_child: _cmarkCmarkNode = node.last_child

    child.next = None
    child.prev = old_last_child
    child.parent = node
    node.last_child = child

    if old_last_child:
        old_last_child.next = child
    else:
        # Also set first_child if node previously had no children.
        node.first_child = child


# Duplicate a chunk by creating a copy of the buffer not by reusing the
# buffer like cmark_chunk_dup does.
# 0.30
def _cmark_cmark_strdup(mem: _cmarkCmarkMem, src: str) -> str:
    if src is None:
        return None

    length: int = len(src)
    data: str = copy.deepcopy(src[:length + 1])

    return data


def _cmark_cmark_clean_autolink(mem: _cmarkCmarkMem, url: _cmarkCmarkChunk,
                                is_email: int):
    buf: _cmarkCmarkStrbuf = _cmark_CMARK_BUF_INIT(mem)

    _cmark_cmark_chunk_trim(url)

    if is_email:
        _cmark_cmark_strbuf_puts(buf, "mailto:")

    _cmark_houdini_unescape_html_f(buf, url.data, url.length)
    return _cmark_cmark_strbuf_detach(buf)


# 0.30
def _cmark_make_autolink(
    subj: _cmarkSubject,
    start_column: int,
    end_column: int,
    url: _cmarkCmarkChunk,
    is_email: int,
) -> _cmarkCmarkNode:
    link: _cmarkCmarkNode = _cmark_make_simple(
        subj.mem, md_parser['cmark']['cmark_node_type']['CMARK_NODE_LINK'])
    link.as_link.url = _cmark_cmark_clean_autolink(subj.mem, url, is_email)
    link.as_link.title = None
    link.start_line = link.end_line = subj.line
    link.start_column = start_column + 1
    link.end_column = end_column + 1
    _cmark_append_child(
        link,
        _cmark_make_str_with_entities(subj, start_column + 1, end_column - 1,
                                      url))
    return link


# 0.30
def _cmark_subject_from_buf(
    mem: _cmarkCmarkMem,
    line_number: int,
    block_offset: int,
    e: _cmarkSubject,
    chunk: _cmarkCmarkChunk,
    refmap: _cmarkCmarkReferenceMap,
):
    i: int
    e.mem = mem
    e.input = chunk
    e.flags = 0
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
def _cmark_isbacktick(c: int) -> bool:
    backtick: bool = False
    if chr(c) == '`':
        backtick = True

    return backtick


# 0.29, 0.30
def _cmark_peek_char(subj: _cmarkSubject) -> int:
    # Instead of using assert just raise a ValueError
    if subj.pos < subj.input.length and ord(subj.input.data[subj.pos]) == 0:
        raise ValueError

    if subj.pos < subj.input.length:
        return ord(subj.input.data[subj.pos])
    else:
        return 0


# 0.29, 0.30
def _cmark_peek_at(subj: _cmarkSubject, pos: int) -> int:
    return ord(subj.input.data[pos])


# Return true if there are more characters in the subject.
# 0.30
def _cmark_is_eof(subj: _cmarkSubject) -> bool:
    return subj.pos >= subj.input.length


# Advance the subject.  Doesn't check for eof.
# 0.29, 0.30
def _cmark_advance(subj: _cmarkSubject):
    subj.pos += 1


def _cmark_skip_spaces(subj: _cmarkSubject) -> bool:
    skipped: bool = False
    while chr(_cmark_peek_char(subj)) == ' ' or chr(
            _cmark_peek_char(subj)) == '\t':
        _cmark_advance(subj)
        skipped = True
    return skipped


# 0.29, 0.30
def _cmark_skip_line_end(subj: _cmarkSubject) -> bool:
    seen_line_end_char: bool = False

    if chr(_cmark_peek_char(subj)) == '\r':
        _cmark_advance(subj)
        seen_line_end_char = True
    if chr(_cmark_peek_char(subj)) == '\n':
        _cmark_advance(subj)
        seen_line_end_char = True
    return seen_line_end_char or _cmark_is_eof(subj)


# Custom function.
def _cmark_take_while_loop_condition(subj: _cmarkSubject,
                                     function_name: str) -> bool:
    condition: bool = False

    c = _cmark_peek_char(subj)
    if function_name == '_cmark_isbacktick':
        condition = _cmark_isbacktick(c)

    return condition


# Take characters while a predicate holds, and return a string.
# Get backtick spanning.
# 0.29, 0.30
def _cmark_take_while(subj: _cmarkSubject,
                      function_name: str) -> _cmarkCmarkChunk:
    startpos: int = subj.pos
    length: int = 0

    while _cmark_take_while_loop_condition(subj, '_cmark_isbacktick'):
        _cmark_advance(subj)
        length += 1

    return _cmark_cmark_chunk_dup(subj.input, startpos, length)


# Return the number of newlines in a given span of text in a subject.  If
# the number is greater than zero, also return the number of characters
# between the last newline and the end of the span in `since_newline`.
# 0.29, 0.30
def _cmark_count_newlines(subj: _cmarkSubject, sfrom: int,
                          length: int) -> tuple:
    nls: int = 0
    since_nl: int = 0

    while length > 0:
        if subj.input.data[sfrom] == '\n':
            nls += 1
            since_nl = 0
        else:
            since_nl += 1

        sfrom += 1
        length -= 1

    if not nls:
        return 0

    since_newline = copy.deepcopy(since_nl)
    return nls, since_newline


# Adjust `node`'s `end_line`, `end_column`, and `subj`'s `line` and
# `column_offset` according to the number of newlines in a just-matched span
# of text in `subj`.
# 0.29, 0.30
def _cmark_adjust_subj_node_newlines(subj: _cmarkSubject,
                                     node: _cmarkCmarkNode, matchlen: int,
                                     extra: int, options: int):
    if not (options & md_parser['cmark']['generic']['CMARK_OPT_SOURCEPOS']):
        return

    newlines: int
    since_newline: int

    newlines, since_newline = _cmark_count_newlines(
        subj, subj.pos - matchlen - extra, matchlen)
    if newlines:
        subj.line += newlines
        node.end_line += newlines
        node.end_column = since_newline
        subj.column_offset = -subj.pos + since_newline + extra


# Try to process a backtick code span that began with a
# span of ticks of length openticklength length (already
# parsed).  Return 0 if you don't find matching closing
# backticks, otherwise return the position in the subject
# after the closing backticks.
# 0.29, 0.30
def _cmark_scan_to_closing_backticks(subj: _cmarkSubject,
                                     openticklength: int) -> int:
    found: bool = False

    if openticklength > md_parser['cmark']['generic']['MAXBACKTICKS']:
        # we limit backtick string length because of the array subj->backticks:
        return 0

    if (subj.scanned_for_backticks
            and subj.backticks[openticklength] <= subj.pos):
        # return if we already know there's no closer
        return 0

    while not found:
        # read non backticks
        c: int

        c = _cmark_peek_char(subj)
        while c and not _cmark_isbacktick(c):
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
    if (contains_nonspace and s.ptr[0] == ' ' and s.ptr[w - 1] == ' '):
        _cmark_cmark_strbuf_drop(s, 1)
        _cmark_cmark_strbuf_truncate(s, w - 2)
    else:
        _cmark_cmark_strbuf_truncate(s, w)


# Parse backtick code section or raw backticks, return an inline.
# Assumes that the subject has a backtick at the current position.
# 0.30
def _cmark_handle_backticks(subj: _cmarkSubject,
                            options: int) -> _cmarkCmarkNode:
    openticks: _cmarkCmarkChunk = _cmark_take_while(subj, '_cmark_isbacktick')
    startpos: int = subj.pos
    endpos: int = _cmark_scan_to_closing_backticks(subj, openticks.length)

    if endpos == 0:  # not found
        subj.pos = startpos  # rewind
        return _cmark_make_str(subj, subj.pos, subj.pos, openticks)
    else:
        buf = _cmark_CMARK_BUF_INIT(subj.mem)
        _cmark_cmark_strbuf_set(buf, subj.input.data[startpos:],
                                endpos - startpos - openticks.length)
        _cmark_S_normalize_code(buf)

        node: _cmarkCmarkNode = _cmark_make_literal(
            subj, md_parser['cmark']['cmark_node_type']['CMARK_NODE_CODE'],
            startpos, endpos - openticks.length - 1)
        node.length = buf.size
        node.data = _cmark_cmark_strbuf_detach(buf)
        _cmark_adjust_subj_node_newlines(subj, node, endpos - startpos,
                                         openticks.length, options)
        return node


# 0.30
def _cmark_scan_delims(subj: _cmarkSubject, c: str) -> tuple:
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
        while _cmark_peek_at(
                subj, before_char_pos) >> 6 == 2 and before_char_pos > 0:
            before_char_pos -= 1

        length, before_char = _cmark_cmark_utf8proc_iterate(
            subj.input.data[before_char_pos:],
            subj.pos - before_char_pos,
        )

        if length == -1:
            before_char = 10

    if c == '\'' or c == '"':
        numdelims += 1
        _cmark_advance(subj)  # limit to 1 delim for quotes
    else:
        while chr(_cmark_peek_char(subj)) == c:
            numdelims += 1
            _cmark_advance(subj)

    length, after_char = _cmark_cmark_utf8proc_iterate(
        subj.input.data[subj.pos:], subj.input.length - subj.pos)

    if length == -1:
        after_char = 10

    if (numdelims > 0 and (not _cmark_cmark_utf8proc_is_space(after_char))
            and (not _cmark_cmark_utf8proc_is_punctuation(after_char)
                 or _cmark_cmark_utf8proc_is_space(before_char)
                 or _cmark_cmark_utf8proc_is_punctuation(before_char))):
        left_flanking = True

    if (numdelims > 0 and (not _cmark_cmark_utf8proc_is_space(before_char))
            and (not _cmark_cmark_utf8proc_is_punctuation(before_char)
                 or _cmark_cmark_utf8proc_is_space(after_char)
                 or _cmark_cmark_utf8proc_is_punctuation(after_char))):
        right_flanking = True

    if c == '_':
        if (left_flanking
                and (not right_flanking
                     or _cmark_cmark_utf8proc_is_punctuation(before_char))):
            can_open = True
        if (right_flanking
                and (not left_flanking
                     or _cmark_cmark_utf8proc_is_punctuation(after_char))):
            can_close = True
    elif c == '\'' or c == '"':
        if (left_flanking and
            (not right_flanking or before_char == '(' or before_char == '[')
                and before_char != ']' and before_char != ')'):
            can_open = True
        can_close = right_flanking
    else:
        can_open = left_flanking
        can_close = right_flanking

    return numdelims, can_open, can_close


# 0.30
def _cmark_remove_delimiter(subj: _cmarkSubject, delim: _cmarkDelimiter):
    if delim is None:
        return
    if delim.next is None:
        # end of list:
        if delim != subj.last_delim:
            raise ValueError
        subj.last_delim = delim.previous
    else:
        delim.next.previous = delim.previous
    if delim.previous is not None:
        delim.previous.next = delim.next
    del delim


# 0.30
def _cmark_pop_bracket(subj: _cmarkSubject):
    b: _cmarkBracket
    if subj.last_bracket is None:
        return
    b = subj.last_bracket
    subj.last_bracket = subj.last_bracket.previous
    #     subj->mem->free(b);
    del b


# 0.29, 0.30
def _cmark_push_delimiter(
    subj: _cmarkSubject,
    c: str,
    can_open: bool,
    can_close: bool,
    inl_text: _cmarkCmarkNode,
):
    delim = _cmarkDelimiter()
    delim.delim_char = c
    delim.can_open = can_open
    delim.can_close = can_close
    delim.inl_text = inl_text
    delim.length = inl_text.length
    delim.previous = subj.last_delim
    delim.next = None
    if delim.previous is not None:
        delim.previous.next = delim
    subj.last_delim = delim


# 0.29, 0.30
def _cmark_push_bracket(subj: _cmarkSubject, image: bool,
                        inl_text: _cmarkCmarkNode):
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


# Assumes the subject has a c at the current position.
# 0.29, 0.30
def _cmark_handle_delim(subj: _cmarkSubject,
                        c: str,
                        smart: bool = False) -> _cmarkCmarkNode:
    numdelims: int
    inl_text: _cmarkCmarkNode
    can_open: bool
    can_close: bool
    contents: _cmarkCmarkChunk

    numdelims, can_open, can_close = _cmark_scan_delims(subj, c)

    if c == '\'' and smart:
        contents = _cmark_cmark_chunk_literal(
            md_parser['cmark']['generic']['RIGHTSINGLEQUOTE'])
    elif c == '"' and smart:
        if can_close:
            contents = _cmark_cmark_chunk_literal(
                md_parser['cmark']['generic']['RIGHTDOUBLEQUOTE'])
        else:
            contents = _cmark_cmark_chunk_literal(
                md_parser['cmark']['generic']['LEFTDOUBLEQUOTE'])
    else:
        contents = _cmark_cmark_chunk_dup(subj.input, subj.pos - numdelims,
                                          numdelims)

    inl_text = _cmark_make_str(subj, subj.pos - numdelims, subj.pos - 1,
                               contents)

    if (can_open or can_close) and (not (c == '\'' or c == '"') or smart):
        _cmark_push_delimiter(subj, c, can_open, can_close, inl_text)

    return inl_text


# 0.30
# Assumes we have a hyphen at the current position.
def _cmark_handle_hyphen(subj: _cmarkSubject, smart: bool) -> _cmarkCmarkNode:
    startpos: int = subj.pos

    _cmark_advance(subj)

    if not smart or chr(_cmark_peek_char(subj)) != '-':
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                               _cmark_cmark_chunk_literal('-'))

    while smart and chr(_cmark_peek_char(subj)) == '-':
        _cmark_advance(subj)

    numhyphens: int = subj.pos - startpos
    en_count: int = 0
    em_count: int = 0
    i: int
    buf: _cmarkCmarkStrbuf = _cmark_CMARK_BUF_INIT(subj.mem)

    if numhyphens % 3 == 0:  # if divisible by 3, use all em dashes
        em_count = numhyphens / 3
    elif numhyphens % 2 == 0:  # if divisible by 2, use all en dashes
        en_count = numhyphens / 2
    elif numhyphens % 3 == 2:  # use one en dash at end
        en_count = 1
        em_count = (numhyphens - 2) / 3
    else:  # use two en dashes at the end
        en_count = 2
        em_count = (numhyphens - 4) / 3

    for i in range(em_count, 0, step=-1):
        _cmark_cmark_strbuf_puts(buf, md_parser['cmark']['generic']['EMDASH'])

    for i in range(en_count, 0, step=-1):
        _cmark_cmark_strbuf_puts(buf, md_parser['cmark']['generic']['ENDASH'])

    return _cmark_make_str_from_buf(subj, startpos, subj.pos - 1, buf)


# 0.30
# Assumes we have a period at the current position.
def _cmark_handle_period(subj: _cmarkSubject, smart: bool) -> _cmarkCmarkNode:
    _cmark_advance(subj)
    if smart and chr(_cmark_peek_char(subj)) == '.':
        _cmark_advance(subj)
        if chr(_cmark_peek_char(subj)) == '.':
            _cmark_advance(subj)
            return _cmark_make_str(
                subj, subj.pos - 3, subj.pos - 1,
                _cmark_cmark_chunk_literal(
                    md_parser['cmark']['generic']['ELLIPSES']))
        else:
            return _cmark_make_str(subj, subj.pos - 2, subj.pos - 1,
                                   _cmark_cmark_chunk_literal('..'))
    else:
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                               _cmark_cmark_chunk_literal('.'))


# 0.30
def _cmark_process_emphasis(subj: _cmarkSubject, stack_bottom: _cmarkDelimiter,
                            ignore: list) -> list:
    closer: _cmarkDelimiter = subj.last_delim
    opener: _cmarkDelimiter
    old_closer: _cmarkDelimiter
    opener_found: bool
    openers_bottom_index: int = 0
    openers_bottom: list = [
        stack_bottom,
        stack_bottom,
        stack_bottom,
        stack_bottom,
        stack_bottom,
        stack_bottom,
        stack_bottom,
        stack_bottom,
        stack_bottom,
    ]

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
                openers_bottom_index = 3
                if closer.can_open:
                    openers_bottom_index += 3
                else:
                    openers_bottom_index += 0
                openers_bottom_index += closer.length % 3
            else:
                raise ValueError

            # Now look backwards for first matching opener:
            opener = closer.previous
            opener_found = False
            while opener is not None and opener != openers_bottom[
                    openers_bottom_index]:
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
                _cmark_cmark_node_set_literal(
                    closer.inl_text,
                    md_parser['cmark']['generic']['RIGHTSINGLEQUOTE'])
                if opener_found:
                    _cmark_cmark_node_set_literal(
                        opener.inl_text,
                        md_parser['cmark']['generic']['LEFTSINGLEQUOTE'])
                closer = closer.next
            elif closer.delim_char == '"':
                _cmark_cmark_node_set_literal(
                    closer.inl_text,
                    md_parser['cmark']['generic']['RIGHTDOUBLEQUOTE'])
                if opener_found:
                    _cmark_cmark_node_set_literal(
                        opener.inl_text,
                        md_parser['cmark']['generic']['LEFTDOUBLEQUOTE'])
                closer = closer.next

            if not opener_found:
                # set lower bound for future searches for openers
                openers_bottom[openers_bottom_index] = old_closer.previous
                if not old_closer.can_open:
                    # we can remove a closer that can't be an
                    # opener, once we've seen there's no
                    # matching opener:
                    _cmark_remove_delimiter(subj, old_closer)
        else:
            closer = closer.next

    # free all delimiters in list until stack_bottom:
    while subj.last_delim is not None and subj.last_delim != stack_bottom:
        _cmark_remove_delimiter(subj, subj.last_delim)


# 0.29, 0.30
def _cmark_remove_emph(subj: _cmarkSubject, opener: _cmarkDelimiter,
                       closer: _cmarkDelimiter, ignore: list):
    # This function replaces to S_insert_emph(). Some code is common
    # to that function.
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
    #   opener_inl->data[opener_num_chars] = 0;
    # No need to add string terminators.
    closer_inl.length = closer_num_chars
    #   closer_inl->data[closer_num_chars] = 0;
    # No need to add string terminators.

    # free delimiters between opener and closer
    delim = closer.previous
    while delim is not None and delim != opener:
        tmp_delim = delim.previous
        _cmark_remove_delimiter(subj, delim)
        delim = tmp_delim

    ############
    # Not useful for emphasis detection but we keep it as reference.
    #
    # create new emph or strong, and splice it in to our inlines
    # between the opener and closer                                 #
    if use_delims == 1:  #
        emph = _cmark_make_emph(subj.mem)  #
    else:  #
        emph = _cmark_make_strong(subj.mem)  #

    tmp = opener_inl.next  #
    while tmp and tmp != closer_inl:  #
        tmpnext = tmp.next  #
        _cmark_cmark_node_unlink(tmp)  #
        _cmark_append_child(emph, tmp)  #
        tmp = tmpnext  #

    _cmark_cmark_node_insert_after(opener_inl, emph)  #

    emph.start_line = opener_inl.start_line  #
    emph.end_line = closer_inl.end_line  #
    emph.start_column = opener_inl.start_column  #
    emph.end_column = closer_inl.end_column  #
    #############

    # Custom variables and computations.
    opener_relative_start = opener_inl.end_column - use_delims - opener.offset
    opener_relative_end = opener_inl.end_column - opener.offset
    closer_relative_start = closer_inl.start_column + closer.offset - 1
    closer_relative_end = closer_inl.start_column + use_delims + closer.offset - 1

    ignore.append(range(opener_relative_start, opener_relative_end))
    ignore.append(range(closer_relative_start, closer_relative_end))

    opener.offset += use_delims
    closer.offset += use_delims

    # if opener has 0 characters, remove it and its associated inline
    if opener_num_chars == 0:
        _cmark_cmark_node_free(opener_inl)
        _cmark_remove_delimiter(subj, opener)

    # if closer has 0 characters, remove it and its associated inline
    if closer_num_chars == 0:
        # remove empty closer inline
        _cmark_cmark_node_free(closer_inl)
        # remove closer from list
        tmp_delim = closer.next
        _cmark_remove_delimiter(subj, closer)
        closer = tmp_delim

    return closer


# 0.30
# Parse an autolink or HTML tag.
# Assumes the subject has a '<' character at the current position.
def _cmark_handle_pointy_brace(subj: _cmarkSubject,
                               options: int) -> _cmarkCmarkNode:
    matchlen: int = 0
    contents: _cmarkCmarkChunk

    _cmark_advance(subj)  # advance past first <

    # first try to match a URL autolink
    matchlen = _cmark_scan_autolink_uri(subj.input, subj.pos)
    if matchlen > 0:
        contents = _cmark_cmark_chunk_dup(subj.input, subj.pos, matchlen - 1)
        subj.pos += matchlen

        return _cmark_make_autolink(subj, subj.pos - 1 - matchlen,
                                    subj.pos - 1, contents, 0)

    # next try to match an email autolink
    matchlen = _cmark_scan_autolink_email(subj.input, subj.pos)
    if matchlen > 0:
        contents = _cmark_cmark_chunk_dup(subj.input, subj.pos, matchlen - 1)
        subj.pos += matchlen

        return _cmark_make_autolink(subj, subj.pos - 1 - matchlen,
                                    subj.pos - 1, contents, 1)

    # finally, try to match an html tag
    if subj.pos + 2 <= subj.input.length:
        c: str = subj.input.data[subj.pos]
        if c == '!':
            c = subj.input.data[subj.pos + 1]
            if c == '-':
                matchlen = _cmark_scan_html_comment(subj.input, subj.pos + 2)
                if matchlen > 0:
                    matchlen += 2  # prefix "<-"
            elif c == '[':
                if subj.flags & md_parser['cmark']['generic'][
                        'FLAG_SKIP_HTML_CDATA'] == 0:
                    matchlen = _cmark_scan_html_cdata(subj.input, subj.pos + 2)
                    if matchlen > 0:
                        # The regex doesn't require the final "]]>". But if we're not at
                        # the end of input, it must come after the match. Otherwise,
                        # disable subsequent scans to avoid quadratic behavior.
                        matchlen += 5  # prefix "![", suffix "]]>"
                        if subj.pos + matchlen > subj.input.length:
                            subj.flags |= md_parser['cmark']['generic'][
                                'FLAG_SKIP_HTML_CDATA']
                            matchlen = 0
            elif subj.flags & md_parser['cmark']['generic'][
                    'FLAG_SKIP_HTML_DECLARATION'] == 0:
                matchlen = _cmark_scan_html_declaration(
                    subj.input, subj.pos + 1)
                if matchlen > 0:
                    matchlen += 2  # prefix "!", suffix ">"
                    if subj.pos + matchlen > subj.input.length:
                        subj.flags |= md_parser['cmark']['generic'][
                            'FLAG_SKIP_HTML_DECLARATION']
                        matchlen = 0
        elif c == '?':
            if subj.flags & md_parser['cmark']['generic'][
                    'FLAG_SKIP_HTML_PI'] == 0:
                # Note that we allow an empty match.
                matchlen = _cmark_scan_html_pi(subj.input, subj.pos + 1)
                matchlen += 3  # prefix "?", suffix "?>"
                if subj.pos + matchlen > subj.input.length:
                    subj.flags |= md_parser['cmark']['generic'][
                        'FLAG_SKIP_HTML_PI']
                    matchlen = 0
        else:
            matchlen = _cmark_scan_html_tag(subj.input, subj.pos)
    if matchlen > 0:
        src: str = subj.input.data[subj.pos - 1:]
        length: int = matchlen + 1
        subj.pos += matchlen
        node: _cmarkCmarkNode = _cmark_make_literal(
            subj,
            md_parser['cmark']['cmark_node_type']['CMARK_NODE_HTML_INLINE'],
            subj.pos - matchlen - 1, subj.pos - 1)

        # node->data = (unsigned char *)subj->mem->realloc(NULL, len + 1);

        # memcpy(node->data, src, len);
        node.data = copy.deepcopy(src[:length])

        # node->data[len] = 0;

        node.length = length
        _cmark_adjust_subj_node_newlines(subj, node, matchlen, 1, options)
        return node

    # if nothing matches, just return the opening <:
    return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                           _cmark_cmark_chunk_literal("<"))


# Parse backslash-escape or just a backslash, returning an inline.
# 0.29, 0.30
def _cmark_handle_backslash(subj: _cmarkSubject):
    _cmark_advance(subj)
    nextchar: int = _cmark_peek_char(subj)

    if _cmark_cmark_ispunct(
            nextchar):  # only ascii symbols and newline can be escaped
        _cmark_advance(subj)
        return _cmark_make_str(
            subj, subj.pos - 2, subj.pos - 1,
            _cmark_cmark_chunk_dup(subj.input, subj.pos - 1, 1))
    elif (not _cmark_is_eof(subj)) and _cmark_skip_line_end(subj):
        return _cmark_make_linebreak(subj.mem)
    else:
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                               _cmark_cmark_chunk_literal('\\'))


# Parse an entity or a regular "&" string.
# Assumes the subject has an '&' character at the current position.
def _cmark_handle_entity(subj: _cmarkSubject) -> _cmarkCmarkNode:
    r"""TODO."""
    """
    ent: _cmarkCmarkStrbuf = _cmark_CMARK_BUF_INIT(subj.mem)
    length: int

    _cmark_advance(subj)

    length = _cmark_houdini_unescape_ent(ent, subj.input.data + subj.pos,
                                         subj.input.len - subj.pos)

    if length <= 0:
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                               _cmark_cmark_chunk_literal('&'))

    subj.pos += length
    return _cmark_make_str_from_buf(subj, subj.pos - 1 - length, subj.pos - 1,
                                    ent)
    """


# Clean a URL: remove surrounding whitespace, and remove \ that escape
# punctuation.
# 0.30
def _cmark_cmark_clean_url(mem: _cmarkCmarkMem, url: _cmarkCmarkChunk) -> str:
    buf: _cmarkCmarkStrbuf = _cmark_CMARK_BUF_INIT(mem)

    _cmark_cmark_chunk_trim(url)

    _cmark_houdini_unescape_html_f(buf, url.data, url.length)

    _cmark_cmark_strbuf_unescape(buf)
    return _cmark_cmark_strbuf_detach(buf)


def _cmark_cmark_clean_title(mem: _cmarkCmarkMem,
                             title: _cmarkCmarkChunk) -> str:
    buf: _cmarkCmarkStrbuf = _cmark_CMARK_BUF_INIT(mem)
    first: str
    last: str

    if title.length == 0:
        return None

    first = title.data[0]
    last = title.data[title.length - 1]

    # remove surrounding quotes if any:
    if ((first == "'" and last == "'") or (first == '(' and last == ')')
            or (first == '"' and last == '"')):
        _cmark_houdini_unescape_html_f(buf, title.data[1:], title.length - 2)
    else:
        _cmark_houdini_unescape_html_f(buf, title.data, title.length)

    _cmark_cmark_strbuf_unescape(buf)
    return _cmark_cmark_strbuf_detach(buf)


# Parse a link label.  Returns 1 if successful.
# Note:  unescaped brackets are not allowed in labels.
# The label begins with `[` and ends with the first `]` character
# encountered.  Backticks in labels do not start code spans.
# 0.30
def _cmark_link_label(subj: _cmarkSubject, raw_label: _cmarkCmarkChunk) -> int:
    startpos: int = subj.pos
    length: int = 0
    c: int
    no_match: bool = False

    # advance past [
    if chr(_cmark_peek_char(subj)) == '[':
        _cmark_advance(subj)
    else:
        return 0

    c = chr(_cmark_peek_char(subj))
    while c and c != '[' and c != ']':
        if c == '\\':
            _cmark_advance(subj)
            length += 1
            if _cmark_cmark_ispunct(_cmark_peek_char(subj)):
                _cmark_advance(subj)
                length += 1
        else:
            _cmark_advance(subj)
            length += 1

        # MAX_LINK_LABEL_LENGTH is defined as 1000 while
        # parser['cmark']['link']['max chars label'] is defined as 999.
        #     if (length > MAX_LINK_LABEL_LENGTH) {
        if length > md_parser['cmark']['link']['max chars label'] + 1:
            no_match = True

        c = chr(_cmark_peek_char(subj))

    if no_match:
        subj.pos = startpos  # rewind
        return 0
    else:
        if c == ']':  # match found
            raw_label = _cmark_cmark_chunk_dup(subj.input, startpos + 1,
                                               subj.pos - (startpos + 1))
        _cmark_cmark_chunk_trim(raw_label)
        _cmark_advance(subj)  # advance past ]
        return 1


# 0.30
def _cmark_manual_scan_link_url_2(input: _cmarkCmarkChunk,
                                  offset: int) -> tuple:
    i: int = offset
    nb_p: int = 0

    while i < input.length:
        if (input.data[i] == '\\' and i + 1 < input.length
                and _cmark_cmark_ispunct(ord(input.data[i + 1]))):
            i += 2
        elif input.data[i] == '(':
            nb_p += 1
            i += 1
            if nb_p > 32:
                return -1, None
        elif input.data[i] == ')':
            if nb_p == 0:
                break
            nb_p -= 1
            i += 1
        elif _cmark_cmark_isspace(ord(input.data[i])):
            if i == offset:
                return -1, None
            break
        else:
            i += 1

    if i >= input.length or nb_p != 0:
        return -1, None

    result: _cmarkCmarkChunk = _cmarkCmarkChunk(input.data[offset:],
                                                i - offset)
    output = copy.deepcopy(result)

    return i - offset, output


# 0.30
def _cmark_manual_scan_link_url(input: _cmarkCmarkChunk, offset: int) -> tuple:
    i: int = offset

    # Pointy bracket link destination.
    if i < input.length and input.data[i] == '<':
        i += 1
        while i < input.length:
            if input.data[i] == '>':
                i += 1
                break
            elif input.data[i] == '\\':
                i += 2
            elif input.data[i] == '\n' or input.data[i] == '<':
                return -1, None
            else:
                i += 1
    else:
        # Not pointy bracket link destination.
        return _cmark_manual_scan_link_url_2(input, offset)

    if i >= input.length:
        return -1, None

    result: _cmarkCmarkChunk = _cmarkCmarkChunk(input.data[offset + 1:],
                                                i - 2 - offset)
    output = copy.deepcopy(result)

    return i - offset, output


# 0.30
# Return a link, an image, or a literal close bracket.
def _cmark_handle_close_bracket(subj: _cmarkSubject,
                                ignore: list) -> _cmarkCmarkNode:
    initial_pos: int
    after_link_text_pos: int
    endurl: int
    starttitle: int
    endtitle: int
    endall: int
    sps: int
    n: int
    ref: _cmarkCmarkReference = None
    url_chunk: _cmarkCmarkChunk
    title_chunk: _cmarkCmarkChunk
    url: str
    title: str
    opener: _cmarkBracket
    inl: _cmarkCmarkNode
    raw_label: _cmarkCmarkChunk
    found_label: int
    tmp: _cmarkCmarkNode
    tmpnext: _cmarkCmarkNode
    is_image: bool
    match_0: bool = False
    no_match_0: bool = False

    _cmark_advance(subj)  # advance past ]
    initial_pos = subj.pos

    # get last [ or ![
    opener = subj.last_bracket

    if opener is None:
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                               _cmark_cmark_chunk_literal(']'))

    if not opener.active:
        # take delimiter off stack
        _cmark_pop_bracket(subj)
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                               _cmark_cmark_chunk_literal(']'))

    # If we got here, we matched a potential link/image text.
    # Now we check to see if it's a link/image.
    is_image = opener.image

    after_link_text_pos = subj.pos

    in_inline_link: bool = False
    # First, look for an inline link.
    if chr(_cmark_peek_char(subj)) == '(':
        sps = _cmark_scan_spacechars(subj.input, subj.pos + 1)
        if sps > -1:
            n, url_chunk = _cmark_manual_scan_link_url(subj.input,
                                                       subj.pos + 1 + sps)
            if n > -1:
                in_inline_link = True

    if in_inline_link:
        # try to parse an explicit link:
        endurl = subj.pos + 1 + sps + n
        starttitle = endurl + _cmark_scan_spacechars(subj.input, endurl)

        # ensure there are spaces between url and title
        if starttitle == endurl:
            endtitle = starttitle
        else:
            endtitle = starttitle + _cmark_scan_link_title(
                subj.input, starttitle)

        endall = endtitle + _cmark_scan_spacechars(subj.input, endtitle)

        if chr(_cmark_peek_at(subj, endall)) == ')':
            subj.pos = endall + 1

            title_chunk = _cmark_cmark_chunk_dup(subj.input, starttitle,
                                                 endtitle - starttitle)
            url = _cmark_cmark_clean_url(subj.mem, url_chunk)
            title = _cmark_cmark_clean_title(subj.mem, title_chunk)
            _cmark_cmark_chunk_free(url_chunk)
            _cmark_cmark_chunk_free(title_chunk)

            #     goto match
            match_0 = True
        else:
            # it could still be a shortcut reference link
            subj.pos = after_link_text_pos

    if not match_0:
        # Next, look for a following [link label] that matches in refmap.
        # skip spaces
        raw_label = _cmark_cmark_chunk_literal("")
        found_label = _cmark_link_label(subj, raw_label)
        if not found_label:
            # If we have a shortcut reference link, back up
            # to before the spacse we skipped.
            subj.pos = initial_pos

        if ((not found_label or raw_label.length == 0)
                and not opener.bracket_after):
            _cmark_cmark_chunk_free(raw_label)
            raw_label = _cmark_cmark_chunk_dup(
                subj.input, opener.position, initial_pos - opener.position - 1)
            found_label = True

        if found_label:
            ref = _cmark_cmark_reference_lookup(subj.refmap, raw_label)
            _cmark_cmark_chunk_free(raw_label)

        if ref is not None:  # found
            url = _cmark_cmark_strdup(subj.mem, ref.url)
            title = _cmark_cmark_strdup(subj.mem, ref.title)
            match_0 = True
        else:
            no_match_0 = True

    if match_0:
        if is_image:
            param = md_parser['cmark']['cmark_node_type']['CMARK_NODE_IMAGE']
        else:
            param = md_parser['cmark']['cmark_node_type']['CMARK_NODE_LINK']
        inl = _cmark_make_simple(subj.mem, param)
        inl.as_link.url = url
        inl.as_link.title = title
        inl.start_line = inl.end_line = subj.line
        inl.start_column = opener.inl_text.start_column
        inl.end_column = subj.pos + subj.column_offset + subj.block_offset
        _cmark_cmark_node_insert_before(opener.inl_text, inl)
        # Add link text:
        tmp = opener.inl_text.next
        while tmp:
            tmpnext = tmp.next
            _cmark_cmark_node_unlink(tmp)
            _cmark_append_child(inl, tmp)
            tmp = tmpnext

        # Free the bracket [:
        _cmark_cmark_node_free(opener.inl_text)

        _cmark_process_emphasis(subj, opener.previous_delimiter, ignore)
        _cmark_pop_bracket(subj)

        # Now, if we have a link, we also want to deactivate earlier link
        # delimiters. (This code can be removed if we decide to allow links
        # inside links.)
        if not is_image:
            opener = subj.last_bracket
            while opener is not None:
                if not opener.image:
                    if not opener.active:
                        break
                    else:
                        opener.active = False
                opener = opener.previous

        return None

    elif no_match_0:
        # If we fall through to here, it means we didn't match a link:
        _cmark_pop_bracket(subj)  # remove this opener from delimiter list
        subj.pos = initial_pos
        return _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                               _cmark_cmark_chunk_literal(']'))


# 0.30
# Parse a hard or soft linebreak, returning an inline.
# Assumes the subject has a cr or newline at the current position.
def _cmark_handle_newline(subj: _cmarkSubject) -> _cmarkCmarkNode:
    nlpos: int = subj.pos
    # skip over cr, crlf, or lf:
    if chr(_cmark_peek_at(subj, subj.pos)) == '\r':
        _cmark_advance(subj)
    if chr(_cmark_peek_at(subj, subj.pos)) == '\n':
        _cmark_advance(subj)

    subj.line += 1

    # FIXME TODO: The next instruction messes up some tests!
    #       subj.column_offset = - subj.pos

    # skip spaces at beginning of line
    _cmark_skip_spaces(subj)
    if (nlpos > 1 and chr(_cmark_peek_at(subj, nlpos - 1)) == ' '
            and chr(_cmark_peek_at(subj, nlpos - 2)) == ' '):
        return _cmark_make_linebreak(subj.mem)
    else:
        return _cmark_make_softbreak(subj.mem)


# 0.29, 0.30
def _cmark_subject_find_special_char(subj: _cmarkSubject, options: int) -> int:
    # "\r\n\\`&_*[]<!"
    SPECIAL_CHARS: list = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    # " ' . -
    SMART_PUNCT_CHARS: list = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    ]

    n: int = subj.pos + 1

    # Patch to avoid overflow problems.
    # FIXME: this should not be needed!
    if n > subj.input.length - 1:
        return subj.input.length
    if ord(subj.input.data[n]) > len(SPECIAL_CHARS) - 1 or ord(
            subj.input.data[n]) > len(SMART_PUNCT_CHARS) - 1:
        return n
    # End patch.

    while n < subj.input.length:
        if SPECIAL_CHARS[ord(subj.input.data[n])] == 1:
            return n
        if options & md_parser['cmark']['generic'][
                'CMARK_OPT_SMART'] and SMART_PUNCT_CHARS[ord(
                    subj.input.data[n])]:
            return n
        n += 1

    return subj.input.length


# Parse an inline, advancing subject, and add it as a child of parent.
# Return 0 if no inline can be parsed, 1 otherwise.
# Handle all the different elements of a string.
# 0.29, 0.30
def _cmark_parse_inline(subj: _cmarkSubject,
                        parent: _cmarkCmarkNode,
                        options: int = 0,
                        ignore: list = list()) -> int:
    new_inl: _cmarkCmarkNode = None
    contents: str
    c: int
    startpos: int
    endpos: int

    c = _cmark_peek_char(subj)
    if c == 0:
        return 0
    elif chr(c) in ['\r', '\n']:
        new_inl = _cmark_handle_newline(subj)
    elif chr(c) in ['`']:
        new_inl = _cmark_handle_backticks(subj, options)
    elif chr(c) in ['\\']:
        new_inl = _cmark_handle_backslash(subj)
    elif chr(c) in ['&']:
        _cmark_advance(subj)
        # TODO
    elif chr(c) in ['<']:
        new_inl = _cmark_handle_pointy_brace(subj, options)
    elif chr(c) in ['*', '_', '\'', '"']:
        new_inl = _cmark_handle_delim(
            subj, chr(c),
            (options & md_parser['cmark']['generic']['CMARK_OPT_SMART']) != 0)
    elif chr(c) in ['-']:
        new_inl = _cmark_handle_hyphen(
            subj,
            (options & md_parser['cmark']['generic']['CMARK_OPT_SMART']) != 0)
    elif chr(c) in ['.']:
        new_inl = _cmark_handle_period(
            subj,
            (options & md_parser['cmark']['generic']['CMARK_OPT_SMART']) != 0)
    elif chr(c) in ['[']:
        _cmark_advance(subj)
        new_inl = _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                                  _cmark_cmark_chunk_literal('['))
        _cmark_push_bracket(subj, False, new_inl)
    elif chr(c) in [']']:
        _cmark_handle_close_bracket(subj, ignore)
    elif chr(c) in ['!']:
        _cmark_advance(subj)
        if _cmark_peek_char(subj) == '[':
            _cmark_advance(subj)
            new_inl = _cmark_make_str(subj, subj.pos - 2, subj.pos - 1,
                                      _cmark_cmark_chunk_literal('!['))
            _cmark_push_bracket(subj, True, new_inl)
        else:
            new_inl = _cmark_make_str(subj, subj.pos - 1, subj.pos - 1,
                                      _cmark_cmark_chunk_literal('!'))
    else:
        endpos = _cmark_subject_find_special_char(subj, options)
        contents = _cmark_cmark_chunk_dup(subj.input, subj.pos,
                                          endpos - subj.pos)
        startpos = subj.pos
        subj.pos = endpos

        # if we're at a newline, strip trailing spaces.
        if _cmark_S_is_line_end_char(_cmark_peek_char(subj)):
            _cmark_cmark_chunk_rtrim(contents)

        new_inl = _cmark_make_str(subj, startpos, endpos - 1, contents)

    if new_inl is not None:
        _cmark_append_child(parent, new_inl)

    return 1


# Parse inlines from parent's string_content, adding as children of parent.
# Get the ignore list.
# 0.30
def _cmark_cmark_parse_inlines(
    mem: _cmarkCmarkMem,
    parent: _cmarkCmarkNode,
    refmap: _cmarkCmarkReferenceMap,
    options: int,
) -> list:
    subj: _cmarkSubject = _cmarkSubject()
    content: _cmarkCmarkChunk = _cmarkCmarkChunk(parent.data, parent.length)
    _cmark_subject_from_buf(mem, parent.start_line,
                            parent.start_column - 1 + parent.internal_offset,
                            subj, content, refmap)
    _cmark_cmark_chunk_rtrim(subj.input)

    ignore = list()
    while not _cmark_is_eof(subj):
        _cmark_parse_inline(subj, parent, options, ignore)

    # When we hit the end of the input, we call the process emphasis procedure with stack_bottom = NULL.
    _cmark_process_emphasis(subj, None, ignore)
    # free bracket and delim stack
    while subj.last_delim:
        _cmark_remove_delimiter(subj, subj.last_delim)
    while subj.last_bracket:
        _cmark_pop_bracket(subj)

    return ignore


if __name__ == '__main__':
    pass
