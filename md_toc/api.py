#
# api.py
#
# Copyright (C) 2017-2018 frnmst (Franco Masotti) <franco.masotti@live.com>
#                                            <franco.masotti@student.unife.it>
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

import fpyutils
import re
import curses.ascii
import sys
from .exceptions import (GithubOverflowCharsLinkLabel, GithubEmptyLinkLabel,
                         GithubOverflowOrderedListMarker)
from .constants import common_defaults
from .constants import parser as md_parser

# FIXME: Fix all docstrings.


def write_string_on_file_between_markers(filename, string, marker):
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
    :raises: one of the fpyutils exceptions or one of the built-in exceptions.
    """
    assert isinstance(filename, str)
    assert isinstance(string, str)
    assert isinstance(marker, str)

    final_string = marker + '\n\n' + string.rstrip() + '\n\n' + marker + '\n'
    marker_line_positions = fpyutils.get_line_matches(
        filename, marker, 2, loose_matching=True)

    if 1 in marker_line_positions:
        if 2 in marker_line_positions:
            fpyutils.remove_line_interval(filename, marker_line_positions[1],
                                          marker_line_positions[2], filename)
        else:
            fpyutils.remove_line_interval(filename, marker_line_positions[1],
                                          marker_line_positions[1], filename)
        fpyutils.insert_string_at_line(
            filename,
            final_string,
            marker_line_positions[1],
            filename,
            append=False)


def write_strings_on_files_between_markers(filenames, strings, marker):
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
    :raises: one of the fpyutils exceptions or one of the built-in exceptions.
    """
    assert isinstance(filenames, list)
    if len(filenames) > 0:
        for f in filenames:
            assert isinstance(f, str)
    assert isinstance(strings, list)
    if len(strings) > 0:
        for s in strings:
            assert isinstance(s, str)

    file_id = 0
    for f in filenames:
        write_string_on_file_between_markers(f, strings[file_id], marker)
        file_id += 1


def build_multiple_tocs(filenames,
                        ordered=False,
                        no_links=False,
                        no_indentation=False,
                        keep_header_levels=3,
                        parser='github',
                        list_marker='-'):
    r"""Parse file by line and build the table of contents.

    :parameter filenames: the file that needs to be read.
    :parameter ordered: decides whether to build an ordered list or not.
    :parameter no_links: disables the use of links.
    :parameter keep_header_levels: the maximum level of headers to be
         considered as such when building the table of contents. Defaults to
         ``3``.
    :parameter parser: decides rules on how to generate anchor links.
         Defaults to ``github``.
    :type filenames: str
    :type ordered: bool
    :type no_links: bool
    :type keep_header_levels: int
    :type parser: str
    :returns: the corresponding table of contents for each input file.
    :rtype: list
    :raises: one of the built-in exceptions.
    """
    assert isinstance(filenames, list)
    if len(filenames) > 0:
        for f in filenames:
            assert isinstance(f, str)

    if len(filenames) == 0:
        filenames.append('-')

    header_type_counter = dict()
    header_type_curr = 0
    header_type_prev = 0
    header_duplicate_counter = dict()
    file_id = 0
    toc_struct = list()

    while file_id < len(filenames):
        if filenames[file_id] == '-':
            f = sys.stdin
        else:
            f = open(filenames[file_id], 'r')
        line = f.readline()
        toc_struct.append('')
        while line:
            header = get_md_header(line, header_duplicate_counter,
                                   keep_header_levels, parser, no_links)
            if header is not None:
                header_type_curr = header['type']
                if ordered:
                    increase_index_ordered_list(header_type_counter,
                                                header_type_prev,
                                                header_type_curr, parser)
                    index = header_type_counter[header_type_curr]
                else:
                    index = 1
                toc_struct[file_id] += build_toc_line(
                    header, ordered, no_links, index, parser, list_marker,
                    header_type_prev) + '\n'
                header_type_prev = header_type_curr
            line = f.readline()
        f.close()

        file_id += 1

    return toc_struct


def increase_index_ordered_list(header_type_count,
                                header_type_prev,
                                header_type_curr,
                                parser='github'):
    r"""Compute the current index for ordered list table of contents.

    :parameter header_type_count: the count of each header type.
    :parameter header_type_prev: the previous type of header (h[1-Inf]).
    :parameter header_type_curr: the current type of header (h[1-Inf]).
    :parameter parser: decides rules on how to generate ordered list markers
    :type header_type_count: dict
    :type header_type_prev: int
    :type header_type_curr: int
    :type parser: str
    :returns: None
    :rtype: None
    :raises: one of the built in exceptions
    """
    assert isinstance(header_type_count, dict)
    assert isinstance(header_type_prev, int)
    assert isinstance(header_type_curr, int)
    # header_type_prev might be 0 while header_type_curr can't.
    assert header_type_curr > 0
    assert isinstance(parser, str)

    # Base cases for a new table of contents or a new index type.
    if header_type_prev == 0:
        header_type_prev = header_type_curr
    if (header_type_curr not in header_type_count or
            header_type_prev < header_type_curr):
        header_type_count[header_type_curr] = 0

    header_type_count[header_type_curr] += 1

    if (parser == 'github' or parser == 'cmark' or parser == 'gitlab' or
            parser == 'commonmarker'):
        if header_type_count[header_type_curr] > md_parser['github']['list'][
                'ordered']['max_marker_number']:
            raise GithubOverflowOrderedListMarker


# TODO
# TODO
# FIXME
# FIXME: Check if the TOC MIGHT NOT RENDER as list. This depends
#        on the parser.
def toc_renders_as_list(header_type_curr=1,
                        parser='github',
                        indentation_array=list()):
    r"""Check if the TOC will render as a working list.

    :parameter header_type_curr: the current type of header (h[1-Inf]).
    :parameter parser: decides rules on how to generate ordered list markers
    :type header_type_curr: int
    :type parser: str
    :returns: renders_as_list
    :rtype: bool
    :raises: one of the built in exceptions
    """
    assert isinstance(header_type_curr, int)
    assert header_type_curr > 0
    assert isinstance(parser, str)
    assert isinstance(indentation_array, list)
    if (parser == 'github' or parser == 'cmark' or parser == 'gitlab' or
            parser == 'commonmarker'):
        if len(indentation_array) > 0:
            assert len(indentation_array
                       ) == parser['github']['header']['max_levels'] + 1

    renders_as_list = True
    if (parser == 'github' or parser == 'cmark' or parser == 'gitlab' or
            parser == 'commonmarker'):
        # 0. Build indentation_array.
        if indentation_array == list():
            indentation_array[0] = True
            for i in range(1, parser['github']['header']['max_levels'] + 1):
                indentation_array[i].append(False)

        # 1. Update with current information.
        indentation_array[header_type_curr] = True

        # 2. Reset next cells to false as a detection mechanism.
        indentation_array[(header_type_curr +
                           1):parser['github']['header']['max_levels']] = False

        # 3. Check for previous false cells. If there is a "hole" in the array
        #    it means that the TOC will have extra indentation space, thus not
        #    rendering as an HTML list.
        i = header_type_curr
        while i >= 0 and indentation_array[i]:
            i -= 1
        if i > 0:
            renders_as_list = False

    elif parser == 'redcarpet':
        pass
        # TODO

    return renders_as_list, indentation_array


def compute_toc_line_indentation_spaces(header_type_curr=1,
                                        header_type_prev=0,
                                        index_prev=0,
                                        no_of_indentation_spaces_prev=0,
                                        parser='github',
                                        list_marker='-',
                                        ordered=False):
    r"""
    """
    assert isinstance(header_type_curr, int)
    assert header_type_curr > 0
    assert isinstance(header_type_prev, int)
    assert header_type_prev >= 0
    assert isinstance(parser, str)
    assert isinstance(list_marker, str)
    if (parser == 'github' or parser == 'cmark' or parser == 'gitlab' or
            parser == 'commonmarker'):
        if ordered:
            assert list_marker in md_parser['github']['list']['ordered'][
                'closing_markers']
        else:
            assert list_marker in md_parser['github']['list']['unordered'][
                'bullet_markers']
    elif parser == 'redcarpet':
        if ordered:
            assert list_marker in md_parser['redcarpet']['list']['ordered'][
                'closing_markers']
        else:
            assert list_marker in md_parser['redcarpet']['list']['unordered'][
                'bullet_markers']
    assert isinstance(ordered, bool)
    assert isinstance(index_prev, int)
    assert index_prev >= 0
    assert isinstance(no_of_indentation_spaces_prev, int)
    assert no_of_indentation_spaces_prev >= 0

    if (parser == 'github' or parser == 'cmark' or parser == 'gitlab' or
            parser == 'commonmarker'):
        if header_type_prev == 0:
            # Base case for the first toc line or for a previous h1.
            no_of_indentation_spaces_curr = 0
        elif header_type_curr == header_type_prev:
            # Base case for same indentation. Please note that this function
            # assumes that no_of_indentation_spaces_prev contains the correct
            # number of spaces. There is no way to check it. FIXME.
            # TODO: In theory we can check for possible overflows especially
            # TODO: for ordered lists: if 6 * no_of_indentation_spaces_curr > \
            # TODO: len(parser['github']['list']['ordered']['max_levels']) then \
            # TODO: FAIL
            no_of_indentation_spaces_curr = no_of_indentation_spaces_prev
        else:
            # Generic cases.
            if header_type_curr > header_type_prev:
                # More indentation.
                if ordered:
                    list_marker_prev = str(index_prev) + list_marker
                else:
                    list_marker_prev = list_marker
                no_of_indentation_spaces_curr = (no_of_indentation_spaces_prev +
                                                 len(list_marker_prev) + len(' '))
            elif header_type_curr < header_type_prev:
                # Less indentation.
                if ordered:
                    list_marker_prev = str(index_prev) + list_marker
                else:
                    list_marker_prev = list_marker
                no_of_indentation_spaces_curr = (no_of_indentation_spaces_prev -
                                                 len(list_marker_prev) - len(' '))

#        if header_type_prev == 0 or header_type_prev == 1:
#            if no_of_indentation_spaces_curr != 0:
#                # FIXME.
#                raise Error


    # TODO: how does redcarpet deal with this?
    elif parser == 'redcarpet':
        no_of_indentation_spaces_curr = 4 * (header_type_curr - 1)

    return no_of_indentation_spaces_curr


def build_toc_line_without_indentation(header,
                                       ordered=False,
                                       no_links=False,
                                       index=1,
                                       parser='github',
                                       list_marker='-'):
    r"""Return a list element of the table of contents.

    :parameter header: a data structure that contains the original
         text, the trimmed text and the type of header.
    :parameter ordered: if set to ``True``, numbers will be used
         as list ids or otherwise a dash character, otherwise. Defaults
         to ``False``.
    :parameter no_links: disables the use of links.
    :parameter index: a number that will be used as list id in case of an
         ordered table of contents. Defaults to ``1``.
    :parameter header_type_prev: Defaults to ``0``.
    :type header: dict
    :type ordered: bool
    :type no_links: bool
    :type index: int
    :type header_type_prev: int
    :returns: a single line of the table of contents.
    :rtype: str
    :raises: one of the built-in exceptions.
    """
    assert isinstance(header, dict)
    assert 'type' in header
    assert 'text_original' in header
    assert 'text_anchor_link' in header
    assert isinstance(header['type'], int)
    assert isinstance(header['text_original'], str)
    assert isinstance(header['text_anchor_link'], str)
    assert header['type'] > 0
    assert isinstance(ordered, bool)
    assert isinstance(no_links, bool)
    assert isinstance(index, int)
    assert index > 0
    assert isinstance(parser, str)
    assert isinstance(list_marker, str)
    if (parser == 'github' or parser == 'cmark' or parser == 'gitlab' or
            parser == 'commonmarker'):
        if ordered:
            assert list_marker in md_parser['github']['list']['ordered'][
                'closing_markers']
        else:
            assert list_marker in md_parser['github']['list']['unordered'][
                'bullet_markers']
    elif parser == 'redcarpet':
        if ordered:
            assert list_marker in md_parser['redcarpet']['list']['ordered'][
                'closing_markers']
        else:
            assert list_marker in md_parser['redcarpet']['list']['unordered'][
                'bullet_markers']

    if ordered:
        list_marker = str(index) + list_marker

    # FIXME: is this always correct?
    if no_links:
        line = header['text_original']
    else:
        line = '[' + header['text_original'] + ']' + '(#' + header[
            'text_anchor_link'] + ')'
    toc_line_no_indent = list_marker + ' ' + line

    return toc_line_no_indent


# No need to test the following function.
def build_toc_line(toc_line_no_indent, no_of_indentation_spaces=0):
    indentation = no_of_indentation_spaces * ' '
    toc_line = indentation + toc_line_no_indent

    return toc_line


def build_anchor_link(header_text_trimmed,
                      header_duplicate_counter,
                      parser='github'):
    r"""Apply the specified slug rule to build the anchor link.

    :parameter header_text_trimmed: the text that needs to be transformed in a link
    :parameter header_duplicate_counter: a data structure that keeps track of
         possible duplicate header links in order to avoid them. This is
         meaningful only for certain values of parser.
    :parameter parser: decides rules on how to generate anchor links.
         Defaults to ``github``. Supported anchor types are: ``github``,
         ``gitlab``, ``redcarpet``.
    :type header_text_trimmed: str
    :type header_duplicate_counter: dict
    :type parser: str
    :returns: None if the specified parser is not recognized, or the anchor
         link, otherwise.
    :rtype: str
    :raises: one of the built-in exceptions.
    :note: The licenses of each markdown parser algorithm are reported on
        the 'Markdown spec' documentation page.
    """
    assert isinstance(header_text_trimmed, str)
    assert isinstance(header_duplicate_counter, dict)
    assert isinstance(parser, str)

    if (parser == 'github' or parser == 'cmark' or parser == 'gitlab' or
            parser == 'commonmarker'):
        header_text_trimmed = header_text_trimmed.lower()
        # Remove punctuation: Keep spaces, hypens and "word characters"
        # only.
        header_text_trimmed = re.sub(r'[^\w\s\- ]', '', header_text_trimmed)
        header_text_trimmed = header_text_trimmed.replace(' ', '-')

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
    elif parser == 'redcarpet':
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
            elif not curses.ascii.isascii(
                    header_text_trimmed[i]) or STRIPPED.find(
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


def get_atx_heading(line,
                    keep_header_levels=3,
                    parser='github',
                    no_links=False):
    r"""Given a line extract the link label and its type.

    :parameter line: the line to be examined.
    :parameter keep_header_levels: the maximum level of headers to be
         considered as such when building the table of contents. Defaults to ``3``.
    :parameter parser: decides rules on how to generate the anchor text.
         Defaults to ``github``. Supported anchor types are: ``github``,
         ``gitlab``, ``redcarpet``.
    :parameter no_links: disables the use of links.
    :type line: str
    :type keep_header_levels: int
    :type parser: str
    :type np_links: bool
    :returns: None if the line does not contain header elements according to
         the rules of the selected markdown parser, or a tuple containing the
         header type and the trimmed header text, according to the selected
         parser rules, otherwise.
    :rtype: tuple
    :raises: one of the built in exceptions or GithubEmptyLinkLabel or
         GithubOverflowCharsLinkLabel
    :warning: the parameter keep_header_levels must be greater than 0.
    """
    assert isinstance(line, str)
    assert isinstance(keep_header_levels, int)
    assert keep_header_levels > 0
    assert isinstance(parser, str)
    assert isinstance(no_links, bool)

    if len(line) == 0:
        return None

    if (parser == 'github' or parser == 'cmark' or parser == 'gitlab' or
            parser == 'commonmarker'):

        if line[0] == '\u005c':
            return None

        i = 0
        while i < len(line) and line[i] == ' ' and i <= md_parser['github'][
                'header']['max_space_indentation']:
            i += 1
        if i > md_parser['github']['header']['max_space_indentation']:
            return None

        offset = i
        while i < len(line) and line[i] == '#' and i <= md_parser['github'][
                'header']['max_levels'] + offset:
            i += 1
        if i - offset > md_parser['github']['header'][
                'max_levels'] or i - offset > keep_header_levels or i - offset == 0:
            return None
        current_headers = i - offset

        # Include special cases for line endings which should not be
        # discarded as non-ATX headers.
        if i < len(line) and (line[i] != ' ' and line[i] != '\u000a' and
                              line[i] != '\u000d'):
            return None

        i += 1
        # Exclude leading whitespaces after the ATX header identifier.
        while i < len(line) and line[i] == ' ':
            i += 1

        # An algorithm to find the start and the end of the closing sequence.
        # The closing sequence includes all the significant part of the
        # string. This algorithm has a complexity of O(n) with n being the
        # length of the line.
        cs_start = i
        cs_end = cs_start
        line_prime = line[::-1]
        hash_char_rounds = 0
        go_on = True
        i = 0
        i_prev = i
        while i < len(line) - cs_start - 1 and go_on:
            if ((line_prime[i] != ' ' and line_prime[i] != '#') or
                    hash_char_rounds > 1):
                if i > i_prev:
                    cs_end = len(line_prime) - i_prev
                else:
                    cs_end = len(line_prime) - i
                go_on = False
            while go_on and line_prime[i] == ' ':
                i += 1
            i_prev = i
            while go_on and line_prime[i] == '#':
                i += 1
            if i > i_prev:
                hash_char_rounds += 1

        # Instead of changing the whole algorithm to check for line
        # endings, this seems cleaner.
        find_newline = line.find('\u000a')
        find_carriage_return = line.find('\u000d')
        if find_newline != -1:
            cs_end = min(cs_end, find_newline)
        if find_carriage_return != -1:
            cs_end = min(cs_end, find_carriage_return)

        final_line = line[cs_start:cs_end]

        if not no_links:
            if len(final_line) > 0 and final_line[-1] == '\u005c':
                final_line += ' '
            if len(
                    final_line.strip('\u0020').strip('\u0009').strip('\u000a').
                    strip('\u000b').strip('\u000c').strip('\u000d')) == 0:
                raise GithubEmptyLinkLabel
            if len(final_line
                   ) > md_parser['github']['link']['max_chars_label']:
                raise GithubOverflowCharsLinkLabel
            # Escape square brackets if not already escaped.
            i = 0
            while i < len(final_line):
                if (final_line[i] == '[' or final_line[i] == ']'):
                    j = i - 1
                    consecutive_escape_characters = 0
                    while j >= 0 and final_line[j] == '\u005c':
                        consecutive_escape_characters += 1
                        j -= 1
                    if ((consecutive_escape_characters > 0 and
                         consecutive_escape_characters % 2 == 0) or
                            consecutive_escape_characters == 0):
                        tmp = '\u005c'
                    else:
                        tmp = str()
                    final_line = final_line[0:i] + tmp + final_line[i:len(
                        final_line)]
                    i += 1 + len(tmp)
                else:
                    i += 1

    elif parser == 'redcarpet':

        if line[0] != '#':
            return None

        i = 0
        while (i < len(line) and
               i < md_parser['redcarpet']['header']['max_levels'] and
               line[i] == '#'):
            i += 1
        current_headers = i

        if i < len(line) and line[i] != ' ':
            return None

        while i < len(line) and line[i] == ' ':
            i += 1

        end = i
        while end < len(line) and line[end] != '\n':
            end += 1

        while end > 0 and line[end - 1] == '#':
            end -= 1

        while end > 0 and line[end - 1] == ' ':
            end -= 1

        if end > i:
            final_line = line
            if not no_links and len(final_line) > 0 and final_line[-1] == '\\':
                final_line += ' '
                end += 1
            final_line = final_line[i:end]
        else:
            return None

    # TODO: escape or remove '[', ']', '(', ')' in inline links for redcarpet,
    # TODO: check link label rules for redcarpet.

    return current_headers, final_line


def get_md_header(header_text_line,
                  header_duplicate_counter,
                  keep_header_levels=3,
                  parser='github',
                  no_links=False):
    r"""Build a data structure with the elements needed to create a TOC line.

    :parameter header_text_line: a single markdown line that needs to be
         transformed into a TOC line.
    :parameter header_duplicate_counter: a data structure that contains the
         number of occurrencies of each header anchor link. This is used to
         avoid duplicate anchor links and it is meaningful only for certain
         values of parser.
    :parameter keep_header_levels: the maximum level of headers to be
         considered as such when building the table of contents. Defaults to ``3``.
    :parameter parser: decides rules on how to generate anchor links.
         Defaults to ``github``.
    :type header_text_line: str
    :type header_duplicate_counter: dict
    :type keep_header_levels: int
    :type parser: str
    :returns: None if the input line does not correspond to one of the
         designated cases or a data structure containing the necessary
         components to create a table of contents line, otherwise.
    :rtype: dict
    :raises: one of the built-in exceptions.
    :note: this works like a wrapper to other functions.
    """
    result = get_atx_heading(header_text_line, keep_header_levels, parser,
                             no_links)
    if result is None:
        return result
    else:
        header_type, header_text_trimmed = result
        header = {
            'type':
            header_type,
            'text_original':
            header_text_trimmed,
            'text_anchor_link':
            build_anchor_link(header_text_trimmed, header_duplicate_counter,
                              parser)
        }
        return header


if __name__ == '__main__':
    pass
