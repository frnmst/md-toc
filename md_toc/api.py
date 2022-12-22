# -*- coding: utf-8 -*-
#
# api.py
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
"""The main file."""

import copy
import os
import re
import sys

import fpyutils

from . import generic
from .cmark import inlines_c, node_h, references_h
from .constants import common_defaults
from .constants import parser as md_parser
from .exceptions import (
    GithubEmptyLinkLabel,
    GithubOverflowCharsLinkLabel,
    GithubOverflowOrderedListMarker,
    StdinIsNotAFileToBeWritten,
    StringCannotContainNewlines,
    TocDoesNotRenderAsCoherentList,
)


def write_string_on_file_between_markers(
    filename: str,
    string: str,
    marker: str,
    newline_string: str = common_defaults['newline string'],
):
    r"""Write the table of contents on a single file.

    :parameter filename: the file that needs to be read or modified.
    :parameter string: the string that will be written on the file.
    :parameter marker: a marker that will identify the start
         and the end of the string.
    :parameter newline_string: the new line separator.
         Defaults to ``os.linesep``.
    :type filenames: str
    :type string: str
    :type marker: str
    :type newline_string: str
    :returns: None
    :rtype: None
    :raises: StdinIsNotAFileToBeWritten or an fpyutils exception
         or a built-in exception.
    """
    if filename == '-':
        raise StdinIsNotAFileToBeWritten

    final_string = marker + '\n\n' + string.rstrip() + '\n\n' + marker + '\n'
    marker_line_positions, lines = fpyutils.filelines.get_line_matches(
        filename,
        marker,
        0,
        loose_matching=True,
        keep_all_lines=True,
    )
    marker_line_positions_length: int = len(marker_line_positions)

    first_marker: int = 1
    second_marker: int = 2
    in_loop: bool = False
    done: bool = False
    first_marker_position: int = 0

    if marker_line_positions_length > 0:
        first_marker_position = marker_line_positions[first_marker]

    # Find appropriate TOC markers.
    while not done and marker_line_positions_length >= 2:
        interval: str = generic._read_line_interval(
            lines, marker_line_positions[first_marker] + 1,
            marker_line_positions[second_marker] - 1)
        interval_with_offset: str = generic._read_line_interval(
            lines, marker_line_positions[first_marker] + 2,
            marker_line_positions[second_marker] - 2)
        # TODO: add code fence detection.
        if generic._detect_toc_list(
                interval_with_offset) or generic._string_empty(interval):
            fpyutils.filelines.remove_line_interval(
                filename,
                marker_line_positions[first_marker],
                marker_line_positions[second_marker],
                filename,
            )
            first_marker_position = marker_line_positions[first_marker]
            done = True

        first_marker += 1
        second_marker += 1
        marker_line_positions_length -= 1
        in_loop = True

    if not in_loop and marker_line_positions_length == 1:
        fpyutils.filelines.remove_line_interval(
            filename,
            marker_line_positions[1],
            marker_line_positions[1],
            filename,
        )

    if marker_line_positions_length >= 1:
        fpyutils.filelines.insert_string_at_line(
            filename,
            final_string,
            first_marker_position,
            filename,
            append=False,
            newline_character=newline_string,
        )


def write_strings_on_files_between_markers(
    filenames: list,
    strings: list,
    marker: str,
    newline_string: str = common_defaults['newline string'],
):
    r"""Write the table of contents on multiple files.

    :parameter filenames: the files that needs to be read or modified.
    :parameter strings: the strings that will be written on the file. Each
         string is associated with one file.
    :parameter marker: a marker that will identify the start
         and the end of the string.
    :parameter newline_string: the new line separator.
         Defaults to ``os.linesep``.
    :type filenames: list
    :type strings: list
    :type marker: str
    :type newline_string: str
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
        write_string_on_file_between_markers(f, strings[file_id], marker,
                                             newline_string)
        file_id += 1


def build_toc(
    filename: str,
    ordered: bool = False,
    no_links: bool = False,
    no_indentation: bool = False,
    no_list_coherence: bool = False,
    keep_header_levels: int = 3,
    parser: str = 'github',
    list_marker: str = '-',
    skip_lines: int = 0,
    constant_ordered_list: bool = False,
    newline_string: str = common_defaults['newline string'],
) -> str:
    r"""Build the table of contents of a single file.

    :parameter filename: the file that needs to be read.
    :parameter ordered: decides whether to build an ordered list or not.
        Defaults to ``False``.
    :parameter no_links: disables the use of links.
        Defaults to ``False``.
    :parameter no_indentation: disables indentation in the list.
        Defaults to ``False``.
    :parameter no_list_coherence: if set to ``False`` checks
        header levels for consecutiveness. If they are not consecutive
        an exception is raised. For example: ``# ONE\n### TWO\n``
        are not consecutive header levels while ``# ONE\n## TWO\n``
        are. Defaults to ``False``.
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
    :parameter newline_string: the newline separator.
        Defaults to ``os.linesep``.
    :type filename: str
    :type ordered: bool
    :type no_links: bool
    :type no_indentation: bool
    :type no_list_coherence: bool
    :type keep_header_levels: int
    :type parser: str
    :type list_marker: str
    :type skip_lines: int
    :type constant_ordered_list: bool
    :type newline_string: str
    :returns: toc, the corresponding table of contents of the file.
    :rtype: str
    :raises: a built-in exception.

    .. warning:: In case of ordered TOCs you must explicitly pass one of the
        supported ordered list markers.
    """
    if not skip_lines >= 0:
        raise ValueError

    toc: list = list()
    header_type_counter: dict = dict()
    header_type_curr: int = 0
    header_type_prev: int = 0
    header_type_first: int = 0
    header_duplicate_counter: dict = dict()

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
    if (ordered and list_marker
            == md_parser[parser]['list']['unordered']['default marker']):
        list_marker = md_parser[parser]['list']['ordered'][
            'default closing marker']
    if constant_ordered_list:
        ordered = True
    if ordered and (
            list_marker is None or list_marker
            not in md_parser[parser]['list']['ordered']['closing markers']):
        list_marker = md_parser[parser]['list']['ordered'][
            'default closing marker']

    if skip_lines > 0:
        loop: bool = True
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
        # however more semantically correct.
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
                line,
                code_fence,
                is_document_end,
                parser,
            )
        else:
            code_fence = is_opening_code_fence(line, parser)
            if code_fence is not None:
                # Update the status of the next line.
                is_within_code_fence = True

        if not is_within_code_fence or code_fence is None:

            # Header detection and gathering.
            headers = get_md_header(
                line,
                header_duplicate_counter,
                keep_header_levels,
                parser,
                no_links,
            )

            # We only need to get the first element since all the lines
            # have been already separated here.
            header = headers[0]

            # Ignore invalid or to-be-invisible headers.
            if header is not None and header['visible']:
                header_type_curr = header['type']

                # Take care of the ordered TOC.
                if ordered and not constant_ordered_list:
                    increase_index_ordered_list(
                        header_type_counter,
                        header_type_prev,
                        header_type_curr,
                        parser,
                    )
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
                                header_type_curr,
                                header_type_first,
                                indentation_list,
                                parser,
                        ):
                            raise TocDoesNotRenderAsCoherentList

                    compute_toc_line_indentation_spaces(
                        header_type_curr,
                        header_type_prev,
                        parser,
                        ordered,
                        list_marker,
                        indentation_log,
                        index,
                    )
                    no_of_indentation_spaces_curr = indentation_log[
                        header_type_curr]['indentation spaces']

                # endif

                # Build a single TOC line.
                toc_line_no_indent = build_toc_line_without_indentation(
                    header,
                    ordered,
                    no_links,
                    index,
                    parser,
                    list_marker,
                )

                # Save the TOC line with the indentation.
                toc.append(
                    build_toc_line(
                        toc_line_no_indent,
                        no_of_indentation_spaces_curr,
                    ) + newline_string, )

                header_type_prev = header_type_curr

            # endif

        # endif

        line = f.readline()

    # endwhile

    f.close()

    toc_str = ''.join(toc)

    return toc_str


def build_multiple_tocs(
    filenames: list,
    ordered: bool = False,
    no_links: bool = False,
    no_indentation: bool = False,
    no_list_coherence: bool = False,
    keep_header_levels: int = 3,
    parser: str = 'github',
    list_marker: str = '-',
    skip_lines: int = 0,
    constant_ordered_list: bool = False,
    newline_string: str = common_defaults['newline string'],
) -> list:
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
    :parameter newline_string: the newline separator.
        Defaults to ``os.linesep``.
    :type filenames: list
    :type ordered: bool
    :type no_links: bool
    :type no_indentation: bool
    :type keep_header_levels: int
    :type parser: str
    :type list_marker: str
    :type skip_lines: int
    :type constant_ordered_list: bool
    :type newline_string: str
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
    toc_struct: list = [
        build_toc(
            filenames[file_id],
            ordered,
            no_links,
            no_indentation,
            no_list_coherence,
            keep_header_levels,
            parser,
            list_marker,
            skip_lines,
            constant_ordered_list,
            newline_string,
        ) for file_id in range(0, len(filenames))
    ]

    return toc_struct


def increase_index_ordered_list(
    header_type_count: dict,
    header_type_prev: int,
    header_type_curr: int,
    parser: str = 'github',
):
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

    if parser in ['github', 'cmark', 'gitlab', 'commonmarker']:
        if header_type_count[header_type_curr] > md_parser['github']['list'][
                'ordered']['max marker number']:
            raise GithubOverflowOrderedListMarker


def init_indentation_log(
    parser: str = 'github',
    list_marker: str = '-',
) -> dict:
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
            'indentation spaces': 0,
        }

    return indentation_log


def compute_toc_line_indentation_spaces(
    header_type_curr: int = 1,
    header_type_prev: int = 0,
    parser: str = 'github',
    ordered: bool = False,
    list_marker: str = '-',
    indentation_log: dict = init_indentation_log('github', '-'),
    index: int = 1,
):
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
    if parser in [
            'github', 'cmark', 'gitlab', 'commonmarker', 'goldmark',
            'redcarpet'
    ]:
        if ordered:
            if list_marker not in md_parser[parser]['list']['ordered'][
                    'closing markers']:
                raise ValueError
        else:
            if list_marker not in md_parser[parser]['list']['unordered'][
                    'bullet markers']:
                raise ValueError
    if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:
        if not len(indentation_log
                   ) == md_parser['github']['header']['max levels']:
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
                    str(indentation_log[header_type_prev]['index']), )
        else:
            index_length = 0

        if header_type_prev == 0:
            # Base case for the first toc line.
            indentation_log[header_type_curr]['indentation spaces'] = 0
        elif header_type_curr > header_type_prev:
            # More indentation.
            indentation_log[header_type_curr]['indentation spaces'] = (
                indentation_log[header_type_prev]['indentation spaces'] +
                len(indentation_log[header_type_prev]['list marker'], ) +
                index_length + len(' '))
        elif header_type_curr < header_type_prev:
            # Less indentation. Since we went "back" we must reset
            # all the sublists in the data structure. The indentation spaces are the ones
            # computed before.
            for i in range(
                    header_type_curr + 1,
                    md_parser['github']['header']['max levels'] + 1,
            ):
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


def build_toc_line_without_indentation(
    header: dict,
    ordered: bool = False,
    no_links: bool = False,
    index: int = 1,
    parser: str = 'github',
    list_marker: str = '-',
) -> str:
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
    if parser in [
            'github', 'cmark', 'gitlab', 'commonmarker', 'goldmark',
            'redcarpet'
    ]:
        if ordered:
            if list_marker not in md_parser[parser]['list']['ordered'][
                    'closing markers']:
                raise ValueError
        else:
            if list_marker not in md_parser[parser]['list']['unordered'][
                    'bullet markers']:
                raise ValueError

    toc_line_no_indent = str()

    if parser in [
            'github', 'cmark', 'gitlab', 'commonmarker', 'goldmark',
            'redcarpet'
    ]:
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


def build_toc_line(
    toc_line_no_indent: str,
    no_of_indentation_spaces: int = 0,
) -> str:
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
        line = re.sub(md_parser[parser]['re']['OT'],
                      str(),
                      line,
                      flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['CT'],
                      str(),
                      line,
                      flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['CO'],
                      str(),
                      line,
                      flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['PI'],
                      str(),
                      line,
                      flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['DE'],
                      str(),
                      line,
                      flags=re.DOTALL)
        line = re.sub(md_parser[parser]['re']['CD'],
                      str(),
                      line,
                      flags=re.DOTALL)

    return line


def remove_emphasis(line: str, parser: str = 'github') -> str:
    r"""Remove markdown emphasis.

    :parameter line: a string.
    :parameter parser: decides rules on how to find delimiters.
        Defaults to ``github``.
    :type line: str
    :type parser: str
    :returns: the input line without emphasis.
    :rtype: str
    :raises: a built-in exception.

    .. note:: Backslashes are preserved.
    """
    if parser in [
            'github', 'cmark', 'gitlab', 'commonmarker', 'goldmark',
            'redcarpet'
    ]:
        mem = None
        refmap = references_h._cmarkCmarkReferenceMap()

        parent = node_h._cmarkCmarkNode()
        parent.data = line
        parent.length = len(line)
        parent.start_line = 0
        parent.start_column = 0
        parent.internal_offset = 1

        ignore = inlines_c._cmark_cmark_parse_inlines(mem, parent, refmap, 0)
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
    rng: list = [list(r) for r in ranges]

    # Flatten list.
    ll = [item for e in rng for item in e]

    s = sorted(ll)
    final: list = [line[i] for i in range(0, len(line)) if i not in s]
    # The same as
    #
    #   i: int = 0
    #   final: list = list()
    #   while i < len(line):
    #       if i not in s:
    #           final.append(line[i])
    #       i += 1

    final_str: str = ''.join(final)

    return final_str


def build_anchor_link(
    header_text_trimmed: str,
    header_duplicate_counter: dict,
    parser: str = 'github',
) -> str:
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

    .. note: license B applies for the github part.
        See docs/copyright_license.rst

    .. note: license A applies for the redcarpet part.
        See docs/copyright_license.rst
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
                header_duplicate_counter[header_text_trimmed], )
        header_duplicate_counter[ht] += 1
        return header_text_trimmed
    elif parser in ['redcarpet']:
        # To ensure full compatibility what follows is a direct translation
        # of the rndr_header_anchor C function used in redcarpet.
        STRIPPED = " -&+$,/:;=?@\"#{}|^~[]`\\*()%.!'"
        header_text_trimmed_len = len(header_text_trimmed)
        inserted = 0
        stripped = 0
        header_text_trimmed_middle_stage = list()
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
            elif not generic._isascii(header_text_trimmed[i]) or STRIPPED.find(
                    header_text_trimmed[i], ) != -1:
                if inserted and not stripped:
                    header_text_trimmed_middle_stage.append('-')
                stripped = 1
            else:
                header_text_trimmed_middle_stage.append(
                    header_text_trimmed[i].lower(), )
                stripped = 0
                inserted += 1

        header_text_trimmed_middle_stage_str: str = ''.join(
            header_text_trimmed_middle_stage)
        if stripped > 0 and inserted > 0:
            header_text_trimmed_middle_stage_str = header_text_trimmed_middle_stage_str[
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
            header_text_trimmed_middle_stage_str = 'part-' + '{0:x}'.format(
                hash)

        return header_text_trimmed_middle_stage_str

    return None


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

    line_list: list = line.split('\n')

    return line_list


def get_atx_heading(
    line: str,
    keep_header_levels: int = 3,
    parser: str = 'github',
    no_links: bool = False,
) -> list:
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
    :returns: struct, a list of dictionaries with

        - ``header type`` (int)
        - ``header text trimmed`` (str)
        - ``visible`` (bool)

        as keys. ``header type`` and ``header text trimmed`` are
        set to ``None`` if the line does not contain header elements according
        to the rules of the selected markdown parser.
        ``visible`` is set to ``True`` if the line needs to be saved, ``False``
        if it just needed for duplicate counting.
    :rtype: list
    :raises: GithubEmptyLinkLabel or GithubOverflowCharsLinkLabel or a
         built-in exception.

    .. note: license A applies for the redcarpet part.
         See docs/copyright_license.rst

    .. note:: license B applies for the github part.
         See docs/copyright_license.rst
    """
    if not keep_header_levels >= 1:
        raise ValueError

    struct: list = list()
    line_visible: bool = True

    if len(line) == 0:
        return [{
            'header type': None,
            'header text trimmed': None,
            'visible': False
        }]

    for subl in replace_and_split_newlines(line):
        current_headers = None
        final_line = None

        if parser in ['github', 'cmark', 'gitlab', 'commonmarker', 'goldmark']:

            struct.append({
                'header type': None,
                'header text trimmed': None,
                'visible': False
            })

            # Empty substring or backslash.
            if len(subl) == 0 or subl[0] == '\u005c':
                continue

            # Preceding.
            i = 0
            while i < len(subl) and subl[i] == ' ' and i <= md_parser[
                    'github']['header']['max space indentation']:
                i += 1
            if i > md_parser['github']['header']['max space indentation']:
                continue

            # ATX characters.
            offset = i
            while i < len(subl) and subl[i] == '#' and i <= md_parser[
                    'github']['header']['max levels'] + offset:
                i += 1

            if (i - offset > md_parser['github']['header']['max levels']
                    or i - offset == 0):
                continue

            # We need to continue parsing to find possible duplicate headers
            # in other functions if we set keep_header_levels < max_levels.
            if i - offset > keep_header_levels:
                line_visible: bool = False

            current_headers = i - offset

            # At this moment GFM is still at version 0.29
            # while cmark is at 0.30. There are subtle differences
            # such as this one. Assume gitlab is on par with 0.30.
            if parser in ['github', 'commonmarker']:
                # GFM 0.29 and cmark 0.29.
                spaces = [' ']
            else:
                # cmark 0.30.
                spaces = [' ', '\u0009']

            # Include special cases for line endings which should not be
            # discarded as non-ATX headers.
            if i < len(subl) and subl[i] not in spaces + ['\u000a', '\u000d']:
                continue

            i += 1

            # Exclude leading whitespaces after the ATX header identifier.
            # [0.29]:
            #   The opening sequence of `#` characters must be followed
            #   by a space or by the end of line.
            # [0.30]:
            #   The opening sequence of `#` characters must be followed
            #   by spaces or tabs, or by the end of line.
            while i < len(subl) and subl[i] in spaces:
                i += 1

            # An algorithm to find the start and the end of the closing sequence (cs).
            # The closing sequence includes all the significant part of the
            # string. This algorithm has a complexity of O(n) with n being the
            # length of the line.
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
            # are not at the end of the line.
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
                if (subl_prime[i] not in spaces + ['#']
                        or hash_char_rounds > 1):
                    if i > hash_round_start and hash_char_rounds > 0:
                        cs_end = len_subl - hash_round_start
                    else:
                        cs_end = len_subl - i
                    go = False
                if go:
                    while subl_prime[i] in spaces:
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
                        final_line.strip('\u0020').strip('\u0009').strip(
                            '\u000a').strip('\u000b').strip('\u000c').strip(
                                '\u000d'), ) == 0:
                    raise GithubEmptyLinkLabel
                if len(final_line,
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
                        final_line = final_line[0:i] + tmp + final_line[i:]
                        i += 1 + len(tmp)
                    else:
                        i += 1

            # Overwrite the element with None as values.
            struct[-1] = {
                'header type': current_headers,
                'header text trimmed': final_line,
                'visible': line_visible
            }

        elif parser in ['redcarpet']:
            struct.append({
                'header type': None,
                'header text trimmed': None,
                'visible': False
            })

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
                if not no_links and len(
                        final_line) > 0 and final_line[-1] == '\\':
                    final_line += ' '
                    end += 1
                final_line = final_line[i:end]

            if final_line is None:
                current_headers = None
                line_visible = False

            struct[-1] = {
                'header type': current_headers,
                'header text trimmed': final_line,
                'visible': line_visible
            }

        # TODO: escape or remove '[', ']', '(', ')' in inline links for redcarpet,
        # TODO: check link label rules for redcarpet.
        # TODO: check live_visible

    # endfor

    return struct


def get_md_header(
    header_text_line: str,
    header_duplicate_counter: dict,
    keep_header_levels: int = 3,
    parser: str = 'github',
    no_links: bool = False,
) -> list:
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
    result = get_atx_heading(
        header_text_line,
        keep_header_levels,
        parser,
        no_links,
    )

    headers: list = [
        None if
        (r['header type'] is None and r['header text trimmed'] is None) else {
            'type':
            r['header type'],
            'text_original':
            r['header text trimmed'],
            'text_anchor_link':
            build_anchor_link(
                r['header text trimmed'],
                header_duplicate_counter,
                parser,
            ),
            'visible':
            r['visible'],
        } for r in result
    ]

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

        info_string: str
        info_string_start: int

        if not is_valid_code_fence_indent(line):
            return None

        line = line.lstrip(' ').rstrip('\n')
        if not line.startswith((markers['backtick'] * marker_min_length,
                                markers['tilde'] * marker_min_length)):
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
            # [0.29]
            #   The line with the opening code fence may optionally contain
            #   some text following the code fence; this is trimmed of leading
            #   and trailing whitespace and called the info string.
            # [0.30]
            #   The line with the opening code fence may optionally contain
            #   some text following the code fence; this is trimmed of leading
            #   and trailing spaces or tabs and called the info string.
            # This does not change the end result of this function.
            if parser in ['github', 'commonmarker']:
                spaces = ' '
            else:
                spaces = ' \u0009'
            info_string = info_string.strip(spaces)

        # Backticks or tildes in info strings are explicitly forbidden
        # in a backtick-opened code fence, for Commonmark 0.29.
        # This also solves example 107 [Commonmark 0.28]. See:
        # https://github.github.com/gfm/#example-107
        if markers['backtick'] in info_string and line[0] != markers['tilde']:
            return None

        return line[0:info_string_start]
    elif parser in ['redcarpet']:
        # TODO.
        return None

    return None


def is_closing_code_fence(
    line: str,
    fence: str,
    is_document_end: bool = False,
    parser: str = 'github',
) -> bool:
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
        fence = fence.rstrip(' \n')
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

        # [0.29]
        #   The closing code fence may be indented up to three spaces, and may be
        #   followed only by spaces, which are ignored.
        # [0.30]
        #   The closing code fence may be preceded by up to three spaces of
        #   indentation, and may be followed only by spaces or tabs,
        #   which are ignored.
        if parser in ['github', 'commonmarker']:
            spaces = ' '
        else:
            spaces = ' \u0009'
        line = line.rstrip(spaces + '\n')

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

    if parser in [
            'github', 'cmark', 'gitlab', 'commonmarker', 'goldmark',
            'redcarpet'
    ]:
        for i in range(0, md_parser[parser]['header']['max levels']):
            indentation_list.append(False)

    return indentation_list


def toc_renders_as_coherent_list(
    header_type_curr: int = 1,
    header_type_first: int = 1,
    indentation_list: list = init_indentation_status_list('github'),
    parser: str = 'github',
) -> bool:
    r"""Check if the TOC will render as a working list.

    :parameter header_type_curr: the current type of header (h[1,...,Inf]).
    :parameter header_type_first: the type of header first encountered (h[1,...,Inf]).
         This must correspond to the one with the least indentation.
    :parameter indentation_list: a list that holds the state of indentations.
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
    if parser in [
            'github', 'cmark', 'gitlab', 'commonmarker', 'goldmark',
            'redcarpet'
    ]:
        if not len(
                indentation_list) == md_parser[parser]['header']['max levels']:
            raise ValueError
    for e in indentation_list:
        if not isinstance(e, bool):
            raise TypeError

    renders_as_list: bool = True
    if parser in [
            'github', 'cmark', 'gitlab', 'commonmarker', 'goldmark',
            'redcarpet'
    ]:
        # Update with current information.
        indentation_list[header_type_curr - 1] = True

        # Reset next cells to False, as a detection mechanism.
        for i in range(
                header_type_curr,
                md_parser['github']['header']['max levels'],
        ):
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
