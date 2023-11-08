# -*- coding: utf-8 -*-
#
# generic.py
#
# Copyright (C) 2017-2022 Franco Masotti (see /README.md)
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
"""Generic functions."""

from __future__ import annotations

import re
import typing

import fpyutils


# _ctoi and _isascii taken from cpython source Lib/curses/ascii.py
# See:
# https://github.com/python/cpython/blob/283de2b9c18e38c9a573526d6c398ade7dd6f8e9/Lib/curses/ascii.py#L48
# https://github.com/python/cpython/blob/283de2b9c18e38c9a573526d6c398ade7dd6f8e9/Lib/curses/ascii.py#L56
#
# These two functions are released under the
# PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
# See https://directory.fsf.org/wiki/License:Python-2.0.1
def _ctoi(c: str) -> int:
    if not len(c) == 1:
        raise ValueError

    retval: str = c
    if isinstance(c, str):
        retval: int = ord(c)

    return retval


def _isascii(c) -> int:
    return 0 <= _ctoi(c) <= 127


def _extract_lines(input_file: str, start: int, end: int) -> str:
    r"""Extract lines from file between start and end line numbers, with line numbers starting from 1."""
    if start > end or start < 1 or end < 1:
        raise ValueError

    lines: list[str] = list()
    line_counter: int = 1

    with open(input_file, 'r') as f:
        line: str = f.readline()
        while line:
            if line_counter >= start and line_counter <= end:
                lines.append(line)
            line = f.readline()
            line_counter += 1

    return ''.join(lines)


def _remove_line_intervals(filename: str,
                           line_intervals: list[list[typing.Sequence]]):
    # A nested list of integers divided in couples is expected.
    # Example: [[1, 4], [8, 9]]
    for interval in line_intervals:
        if len(interval) != 2 or interval[0] < 1 or interval[
                1] < 1 or interval[0] > interval[1]:
            raise ValueError

        fpyutils.filelines.remove_line_interval(
            filename,
            interval[0],
            interval[1],
            filename,
        )


def _get_existing_toc(filename: str, marker: str) -> tuple:
    r"""Get the existing TOC in a file and return other important data about the TOC and its markers."""
    # TOC marker positions.
    marker_line_positions, lines = fpyutils.filelines.get_line_matches(
        filename,
        marker,
        0,
        loose_matching=True,
        keep_all_lines=True,
    )
    marker_line_positions_length: int = len(marker_line_positions)

    old_toc: str = str()
    first_marker: int = 1
    second_marker: int = 2
    two_or_more_markers: bool = False
    done: bool = False
    first_marker_line_number: int = 0
    lines_to_delete: list = list()

    if marker_line_positions_length > 0:
        first_marker_line_number = marker_line_positions[first_marker]

    # Possible pre-existing TOC.
    while not done and marker_line_positions_length >= 2:

        interval: str = _read_line_interval(
            lines, marker_line_positions[first_marker] + 1,
            marker_line_positions[second_marker] - 1)

        # Line intervals excluding the newline after the first <!--TOC-->
        # and before the last <!--TOC-->.
        interval_with_newline: str = _read_line_interval(
            lines, marker_line_positions[first_marker] + 2,
            marker_line_positions[second_marker] - 2)

        # TODO: add code fence detection.
        if _detect_toc_list(interval_with_newline) or _string_empty(interval):

            # Skip the opening and closing TOC markers.
            start_line: int = marker_line_positions[first_marker] + 1
            end_line: int = marker_line_positions[second_marker] - 1

            if start_line <= end_line:
                # Real TOC detected.
                old_toc = _extract_lines(filename, start_line,
                                         end_line).strip()
            else:
                old_toc = str()

            lines_to_delete.append([
                marker_line_positions[first_marker],
                marker_line_positions[second_marker]
            ])

            first_marker_line_number = marker_line_positions[first_marker]
            done = True

        first_marker += 1
        second_marker += 1
        marker_line_positions_length -= 1
        two_or_more_markers = True

    # Only 1 pre-existing marker. TOC is just the marker.
    if not two_or_more_markers and marker_line_positions_length == 1:
        old_toc = marker

    return old_toc, lines_to_delete, two_or_more_markers, marker_line_positions_length, marker_line_positions, first_marker_line_number


def _replace_substring(source: str, replacement: str, start: int,
                       end: int) -> str:
    r"""Given a string called source, replace it with a string called replacement between the start and end indices interval."""
    # Avoid possibility to pass lists to this function which the program would
    # happily process.
    if not isinstance(source, str):
        raise TypeError
    if not isinstance(replacement, str):
        raise TypeError

    if start > end:
        raise ValueError

    replaced: list = list()
    was_replaced: bool = False
    i: int = 0

    while i < len(source):
        if i < start or i > end:
            replaced.append(source[i])
        elif not was_replaced:
            # Only one replacement is possible.
            replaced.append(replacement)
            was_replaced = True
        i += 1

    return ''.join(replaced)


# A weaker version of C's strncmp: this one does not count the characters,
# it just notifies if there are differences.
def _strncmp(s1: str, s2: str, length: int) -> int:
    i: int = 0
    retval: int = 0
    process: bool = True

    s1_prime: str = s1[:length]
    s2_prime: str = s2[:length]
    s1_prime_length: int = len(s1_prime)
    s2_prime_length: int = len(s2_prime)
    min_length: int = min(s1_prime_length, s2_prime_length)

    if s1_prime_length < s2_prime_length:
        retval = -1
        process = False
    elif s1_prime_length > s2_prime_length:
        retval = 1
        process = False

    while process and i < min_length:
        int_s1: int = ord(s1_prime[i])
        int_s2: int = ord(s2_prime[i])

        if int_s1 < int_s2:
            retval = -1
            process = False
        elif int_s1 > int_s2:
            retval = 1
            process = False

        i += 1

    return retval


def _utf8_array_to_string(array: list[int]) -> str:
    r"""Given an array of integers corresponding to the representation of a UTF-8 string like this.

    >>> list(chr(0x10348).encode('UTF-8'))
    [240, 144, 141, 136]

    revert back to the original UTF-8 character.

    See the UTF-8 wikipedia page for these examples:

    vv = [240, 144, 141, 136]
    a = _utf8_array_to_string(vv)
    assert a == chr(66376)

    vv = [226, 130, 172]
    a = _utf8_array_to_string(vv)
    assert a == chr(8364)

    vv = [194, 163]
    a = _utf8_array_to_string(vv)
    assert a == chr(163)

    vv = [36]
    a = _utf8_array_to_string(vv)
    assert a == chr(36)
    """
    ll: list
    binary: list
    raw_binary_8_bit: list

    # Not a UTF-8 array.
    if len(array) < 1 or len(array) > 4:
        raise ValueError

    if len(array) == 1:
        ll = [array[0] - (array[0] & 0x0)]
        binary = [bin(f).replace('0b', '') for f in ll]
        raw_binary_8_bit = [binary[0].zfill(7)]

    if len(array) == 2:
        ll = [
            array[0] - (array[0] & 0xC0),
            array[1] - (array[1] & 0x80),
        ]
        binary = [bin(f).replace('0b', '') for f in ll]
        raw_binary_8_bit = [
            binary[0].zfill(4),
            binary[1].zfill(6),
        ]

    if len(array) == 3:
        ll = [
            array[0] - (array[0] & 0xE0),
            array[1] - (array[1] & 0x80),
            array[2] - (array[2] & 0x80),
        ]
        binary = [bin(f).replace('0b', '') for f in ll]
        raw_binary_8_bit = [
            binary[0].zfill(4),
            binary[1].zfill(6),
            binary[2].zfill(6),
        ]

    if len(array) == 4:
        ll = [
            array[0] - (array[0] & 0xF0),
            array[1] - (array[1] & 0x80),
            array[2] - (array[2] & 0x80),
            array[3] - (array[3] & 0x80),
        ]
        binary = [bin(f).replace('0b', '') for f in ll]
        raw_binary_8_bit = [
            binary[0].zfill(3),
            binary[1].zfill(6),
            binary[2].zfill(6),
            binary[3].zfill(6),
        ]

    return chr(int(''.join(raw_binary_8_bit), 2))


def _string_empty(lines: str) -> bool:
    empty: bool = True
    # Avoid matching \n\r
    if re.fullmatch(
            '((?!\u000a\u000d)|(?!\u000a\u000d)\u000d\u000a|(?!\u000a\u000d)\u000d|(?!\u000a\u000d)\u000a|(?!\u000a\u000d)\u000b|(?!\u000a\u000d)\u0020|(?!\u000a\u000d)\u0009)+',
            lines) is None:
        empty = False

    return empty


def _detect_toc_list(line: str) -> bool:
    # An heuristic to detect a TOC list generated by md-toc.
    # If a user deletes the first TOC list line by mistake
    # there might be additional spaces (max 3 possible)
    # at the start of the second line
    # See
    # https://spec.commonmark.org/0.30/#example-288
    # and
    # https://spec.commonmark.org/0.30/#example-289
    match: bool = True
    if re.fullmatch(
            r' {0,3}([-+*]|' + r'\d' + '+[.' + r'\)' +
            '])\u0020((?![\u0020\u0009\u000b]+).*)', line) is None:
        match = False

    return match


def _read_line_interval(lines: str, start: int, end: int) -> str:
    r"""Given a string get a line interval between start and end.

    Indices are 1 based.
    Newline characters are ignored.
    """
    done: bool = False
    i: int = 0
    line_counter: int = 1
    lines_length: int = len(lines)
    final_line: list = list()

    # Shortcut.
    if start > end or start < 1:
        done = True

    while not done:
        invalid_newline: bool = False

        # Skip \n\r
        while i + 1 < lines_length and lines[i] == '\u000a' and lines[
                i + 1] == '\u000d':
            i += 2
            invalid_newline = True

        # Get \r\n as a single newline character.
        while i + 1 < lines_length and lines[i] == '\u000d' and lines[
                i + 1] == '\u000a':
            line_counter += 1
            i += 2

        # Get \r or \n
        while i < lines_length and re.fullmatch('[\u000d\u000a]',
                                                lines[i]) is not None:
            line_counter += 1
            i += 1

        if i < lines_length and line_counter >= start and line_counter <= end:
            if invalid_newline:
                final_line.append('\u000a')
                final_line.append('\u000d')
            # Add non-newline character.
            final_line.append(lines[i])

        if i >= lines_length:
            done = True

        i += 1

    return ''.join(final_line)


if __name__ == '__main__':
    pass
