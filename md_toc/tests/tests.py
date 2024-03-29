#
# tests.py
#
# Copyright (C) 2017-2023 Franco Masotti (see /README.md)
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
r"""The tests module."""

import doctest
import unittest
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase as pyfakefsTestCase

from .. import api, exceptions, generic
from ..constants import parser as md_parser

# Some static generic variables.

# Lines.
LINE = 'This is a static line'
LINE_EMPTY = ''
LINE_ESCAPE = '\\'
LINE_LINE_FEED = '\n'
LINE_CARRIAGE_RETURN = '\r'
LINE_SQUARE_BRACKET_OPEN = '['
LINE_SQUARE_BRACKET_CLOSE = ']'
LINE_DASH = '-'

# Marker.
MARKER = '<!--TOC-->'

# Spaces.
S1 = 1 * ' '
S2 = 2 * ' '
S3 = 3 * ' '
S4 = 4 * ' '
S5 = 5 * ' '
S10 = 10 * ' '
S18 = 18 * ' '
S21 = 21 * ' '

# Tabs.
T1 = 1 * '\u0009'
T2 = 2 * '\u0009'
T3 = 3 * '\u0009'
T4 = 4 * '\u0009'
T5 = 5 * '\u0009'
T10 = 10 * '\u0009'
T18 = 18 * '\u0009'
T21 = 21 * '\u0009'

# ATX headers.
H1 = 1 * '#'
H2 = 2 * '#'
H3 = 3 * '#'
H4 = 4 * '#'
H5 = 5 * '#'
H6 = 6 * '#'
H7 = 7 * '#'
H34 = 34 * '#'

# Lists.
LIST_INDENTATION = 4
UNORDERED_LIST_SYMBOL = '-'
ORDERED_LIST_SYMBOL = '.'

# Header types.
GENERIC_HEADER_TYPE_PREV = 2
GENERIC_HEADER_TYPE_CURR = 6
BASE_CASE_HEADER_TYPE_PREV = 0

# Indentation.
GENERIC_NUMBER_OF_INDENTATION_SPACES = 128

# List marker log.
GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX = 1000

# github test lines.
CMARK_LINE_FOO = 'foo'
CMARK_LINE_BAR = 'bar'
CMARK_LINE_BAZ = 'baz'
CMARK_LINE_5_BOLT = '5 bolt'
CMARK_LINE_HASHTAG = 'hashtag'
CMARK_LINE_BAR_BAZ = '*bar* ' + LINE_ESCAPE + '*baz' + LINE_ESCAPE + '*'
CMARK_LINE_B = 'b'
CMARK_LINE_1000_CHARS = 1000 * 'c'

# Code fences.
BACKTICK1 = 1 * '`'
BACKTICK2 = 2 * '`'
BACKTICK3 = 3 * '`'
BACKTICK4 = 4 * '`'
BACKTICK5 = 5 * '`'
BACKTICK6 = 6 * '`'
BACKTICK10 = 10 * '`'
TILDE1 = 1 * '~'
TILDE2 = 2 * '~'
TILDE3 = 3 * '~'
TILDE4 = 4 * '~'
TILDE5 = 5 * '~'
TILDE6 = 6 * '~'
TILDE10 = 10 * '~'
CMARK_INFO_STRING_FOO = 'ruby'
CMARK_INFO_STRING_GARBAGE = 'startline=3 $%@#$'

# github renders as list header types. Do not change these values.
BASE_CASE_CMARK_RENDERS_AS_LIST_HEADER_TYPE_CURR = 1
GENERIC_CMARK_RENDERS_AS_LIST_HEADER_TYPE_CURR = 4
GENERIC_CMARK_RENDERS_AS_LIST_HEADER_TYPE_CURR_BIS = 5
BASE_CASE_CMARK_RENDERS_AS_LIST_HEADER_TYPE_FIRST = 1
GENERIC_CMARK_RENDERS_AS_LIST_HEADER_TYPE_FIRST = 4

# redcarpet test lines.
REDCARPET_LINE_FOO = 'foo'


def load_tests(loader, tests, ignore):
    r"""Run tests against docstrings examples."""
    tests.addTests(doctest.DocTestSuite(api))
    tests.addTests(doctest.DocTestSuite(generic))
    return tests


class TestGeneric(pyfakefsTestCase):
    r"""Test the generic functions."""

    def setUp(self):
        r"""Fake filesystem."""
        self.setUpPyfakefs()

    def test__extract_lines(self):
        r"""Test extracting lines between line intervals."""
        with open('foo.md', 'w') as f:
            f.write(CMARK_LINE_FOO)
        self.assertEqual(generic._extract_lines('foo.md', 2, 2), '')
        self.assertEqual(generic._extract_lines('foo.md', 1024, 2048), '')
        self.assertEqual(generic._extract_lines('foo.md', 1, 1),
                         CMARK_LINE_FOO)

        with open('foo.md', 'w') as f:
            f.write(CMARK_LINE_FOO + LINE_LINE_FEED + CMARK_LINE_BAR)
        self.assertEqual(generic._extract_lines('foo.md', 2, 2),
                         CMARK_LINE_BAR)
        self.assertEqual(generic._extract_lines('foo.md', 1, 2),
                         CMARK_LINE_FOO + LINE_LINE_FEED + CMARK_LINE_BAR)

        with open('foo.md', 'w') as f:
            f.write(CMARK_LINE_FOO + LINE_LINE_FEED + CMARK_LINE_BAR +
                    LINE_LINE_FEED)
        self.assertEqual(
            generic._extract_lines('foo.md', 1, 1024),
            CMARK_LINE_FOO + LINE_LINE_FEED + CMARK_LINE_BAR + LINE_LINE_FEED)
        self.assertEqual(generic._extract_lines('foo.md', 2, 2),
                         CMARK_LINE_BAR + LINE_LINE_FEED)
        self.assertEqual(generic._extract_lines('foo.md', 2, 3),
                         CMARK_LINE_BAR + LINE_LINE_FEED)

        with self.assertRaises(ValueError):
            generic._extract_lines('foo.md', 0, 0)
        with self.assertRaises(ValueError):
            generic._extract_lines('foo.md', 0, 1)
        with self.assertRaises(ValueError):
            generic._extract_lines('foo.md', 1, 0)

    def test__remove_line_intervals(self):
        r"""Test removing multiple line intervals from a file."""
        with open('foo.md', 'w') as f:
            f.write(CMARK_LINE_FOO + LINE_LINE_FEED + CMARK_LINE_FOO +
                    LINE_LINE_FEED)
        with self.assertRaises(ValueError):
            generic._remove_line_intervals('foo.md', [[1, 2], [4, 5, 6]])
        with self.assertRaises(ValueError):
            generic._remove_line_intervals('foo.md', [[1, 2, 3], [4, 5]])
        with self.assertRaises(ValueError):
            generic._remove_line_intervals('foo.md', [[2, 1]])
        with self.assertRaises(ValueError):
            generic._remove_line_intervals('foo.md', [[0, 1]])
        with self.assertRaises(ValueError):
            generic._remove_line_intervals('foo.md', [[1, 0]])

        # The rest of the function involves fpyutils.

    def test__get_existing_toc(self):
        r"""Test retrieving the existing TOC. See the TestApi.test_write_string_on_file_between_markers method for more tests."""
        # The function returns:
        # old_toc, lines_to_delete, two_or_more_markers, marker_line_positions_length, marker_line_positions, first_marker_line_number

        # No existing TOC == str().
        with open('foo.md', 'w') as f:
            f.write(H1 + S1 + CMARK_LINE_FOO)
        self.assertEqual(generic._get_existing_toc('foo.md', '<!--TOC-->'),
                         ('', list(), False, 0, dict(), 0))

        # 1 TOC marker: TOC == marker.
        with open('foo.md', 'w') as f:
            f.write(MARKER + LINE_LINE_FEED + H1 + S1 + CMARK_LINE_FOO)
        self.assertEqual(generic._get_existing_toc('foo.md', MARKER),
                         (MARKER, list(), False, 1, {
                             1: 1
                         }, 1))

        # Normal existing TOC (2 TOC markers)
        with open('foo.md', 'w') as f:
            f.write(MARKER + LINE_LINE_FEED + LINE_LINE_FEED + '- [t](#t)' +
                    LINE_LINE_FEED + LINE_LINE_FEED + MARKER + LINE_LINE_FEED +
                    LINE_LINE_FEED + H1 + S1 + CMARK_LINE_FOO)
        self.assertEqual(generic._get_existing_toc('foo.md', MARKER),
                         ('- [t](#t)', [[1, 5]], True, 1, {
                             1: 1,
                             2: 5
                         }, 1))

        # More than 2 TOC markers
        with open('foo.md', 'w') as f:
            f.write(MARKER + LINE_LINE_FEED + LINE_LINE_FEED + '- [t](#t)' +
                    LINE_LINE_FEED + LINE_LINE_FEED + MARKER + LINE_LINE_FEED +
                    MARKER + LINE_LINE_FEED + LINE_LINE_FEED + H1 + S1 +
                    CMARK_LINE_FOO)
        self.assertEqual(generic._get_existing_toc('foo.md', MARKER),
                         ('- [t](#t)', [[1, 5]], True, 2, {
                             1: 1,
                             2: 5,
                             3: 6
                         }, 1))

        # 2 markers, wrong TOC content (not a TOC)
        with open('foo.md', 'w') as f:
            f.write(MARKER + LINE_LINE_FEED + LINE_LINE_FEED +
                    '     - [t](#t)' + LINE_LINE_FEED + LINE_LINE_FEED +
                    MARKER + LINE_LINE_FEED + LINE_LINE_FEED + H1 + S1 +
                    CMARK_LINE_FOO)
        self.assertEqual(generic._get_existing_toc('foo.md', MARKER),
                         ('', list(), True, 1, {
                             1: 1,
                             2: 5
                         }, 1))

    def test__replace_substring(self):
        r"""Test that the string is replaced with another one between the two specified indices."""
        self.assertEqual(generic._replace_substring('', '', 0, 0), '')
        self.assertEqual(generic._replace_substring('', '', 1024, 1024), '')

        self.assertEqual(generic._replace_substring('', CMARK_LINE_FOO, 0, 0),
                         '')
        self.assertEqual(generic._replace_substring(CMARK_LINE_FOO, '', 0, 0),
                         'oo')
        self.assertEqual(generic._replace_substring('', CMARK_LINE_FOO, 0, 0),
                         '')
        # Replace first 'f' of 'foo' with 'foo' -> 'foo|oo'
        self.assertEqual(
            generic._replace_substring(CMARK_LINE_FOO, CMARK_LINE_FOO, 0, 0),
            'foooo')
        # Replace first 'o' of 'foo' with 'foo' -> 'f|foo|o'
        self.assertEqual(
            generic._replace_substring(CMARK_LINE_FOO, CMARK_LINE_FOO, 1, 1),
            'ffooo')
        # Replace last 'o' of 'foo' with 'foo' -> 'fo|foo'
        self.assertEqual(
            generic._replace_substring(CMARK_LINE_FOO, CMARK_LINE_FOO, 2, 2),
            'fofoo')
        # Replace last 'oo' of 'foo' with 'foo' -> 'f|foo'
        self.assertEqual(
            generic._replace_substring(CMARK_LINE_FOO, CMARK_LINE_FOO, 1, 2),
            'ffoo')
        # Replace 'foo' with 'foo' -> 'foo'
        self.assertEqual(
            generic._replace_substring(CMARK_LINE_FOO, CMARK_LINE_FOO, 0, 2),
            CMARK_LINE_FOO)

        # Check the single replacement policy.
        # Replace the first 'o' of the second 'foo' of 'foofoofoofoo' with 'a' -> 'foof|a|foo'
        self.assertEqual(
            generic._replace_substring(
                CMARK_LINE_FOO + CMARK_LINE_FOO + CMARK_LINE_FOO +
                CMARK_LINE_FOO, 'a', 4, 8), 'foofafoo')

        self.assertEqual(generic._replace_substring('b', 'a', 0, 0), 'a')
        self.assertEqual(generic._replace_substring('b', 'a', 0, 1), 'a')
        self.assertEqual(generic._replace_substring('b', 'a', 1, 1), 'b')

        self.assertEqual(generic._replace_substring('bcdef', 'a', 4, 4),
                         'bcdea')
        self.assertEqual(generic._replace_substring('bcdef', 'a', 0, 0),
                         'acdef')

        self.assertEqual(generic._replace_substring('bcdef', 'a', 1, 4), 'ba')
        self.assertEqual(
            generic._replace_substring('bcdef', 'a', 1, 999999999999), 'ba')
        self.assertEqual(generic._replace_substring('bcdef', 'a', 0, 2), 'aef')
        self.assertEqual(
            generic._replace_substring('bcdef', 'a', 0, 999999999999), 'a')

        with self.assertRaises(TypeError):
            generic._replace_substring(['ba'], 'a', 0, 0)
        with self.assertRaises(TypeError):
            generic._replace_substring('ba', ['a'], 0, 0)
        with self.assertRaises(TypeError):
            generic._replace_substring(['ba'], ['a'], 0, 0)

        with self.assertRaises(ValueError):
            generic._replace_substring('ba', 'a', 1, 0)
        with self.assertRaises(ValueError):
            generic._replace_substring('ba', 'a', 4, 2)

    def test__string_empty(self):
        r"""A string is empty if it contains whitespace characters, excluding consecutive sequences of \n\r."""
        self.assertTrue(generic._string_empty(''))
        self.assertTrue(generic._string_empty('\u000a'))
        self.assertTrue(generic._string_empty('\u000d'))
        self.assertTrue(generic._string_empty('\u000b'))
        self.assertTrue(generic._string_empty('\u0009'))
        self.assertTrue(generic._string_empty('\u0020'))
        self.assertTrue(generic._string_empty('\u000d\u000a'))
        self.assertTrue(generic._string_empty('\u0020\u000d\u000a'))
        self.assertTrue(
            generic._string_empty('\u0020\u000d\u000d\u000a\u000d'))
        self.assertFalse(
            generic._string_empty('\u0020\u000d\u000a\u000a\u000d'))

        # \n\r
        self.assertFalse(generic._string_empty('\u000a\u000d'))

        self.assertFalse(generic._string_empty('\u0020\u000da\u000d'))
        self.assertTrue(generic._string_empty('\u0020\u000d\u0020\u000d'))
        self.assertFalse(generic._string_empty('\u0020abcd\u0020'))

    def test__detect_toc_list(self):
        r"""Detect a markdown list generated by md-toc."""
        self.assertFalse(generic._detect_toc_list(''))

        # Unordered list.
        self.assertTrue(generic._detect_toc_list('- list'))
        self.assertTrue(generic._detect_toc_list('+ list'))
        self.assertTrue(generic._detect_toc_list('* list'))
        self.assertTrue(generic._detect_toc_list('- [list'))
        self.assertTrue(generic._detect_toc_list('+ [list'))
        self.assertTrue(generic._detect_toc_list('* [list'))
        # Not a list.
        self.assertFalse(generic._detect_toc_list('-  list'))
        self.assertFalse(generic._detect_toc_list('+  list'))
        self.assertFalse(generic._detect_toc_list('*  list'))
        self.assertFalse(generic._detect_toc_list('- \u0009list'))
        self.assertFalse(generic._detect_toc_list('+ \u0009list'))
        self.assertFalse(generic._detect_toc_list('* \u0009list'))
        self.assertFalse(generic._detect_toc_list('- \u0009[list'))
        self.assertFalse(generic._detect_toc_list('+ \u0009[list'))
        self.assertFalse(generic._detect_toc_list('* \u0009[list'))

        self.assertTrue(generic._detect_toc_list(' - list'))
        self.assertTrue(generic._detect_toc_list(' + list'))
        self.assertTrue(generic._detect_toc_list(' * list'))
        self.assertTrue(generic._detect_toc_list('  - list'))
        self.assertTrue(generic._detect_toc_list('  + list'))
        self.assertTrue(generic._detect_toc_list('  * list'))
        self.assertTrue(generic._detect_toc_list('   - list'))
        self.assertTrue(generic._detect_toc_list('   + list'))
        self.assertTrue(generic._detect_toc_list('   * list'))
        self.assertFalse(generic._detect_toc_list('    - list'))
        self.assertFalse(generic._detect_toc_list('    + list'))
        self.assertFalse(generic._detect_toc_list('    * list'))

        self.assertTrue(generic._detect_toc_list(' - [list'))
        self.assertTrue(generic._detect_toc_list(' + [list'))
        self.assertTrue(generic._detect_toc_list(' * [list'))
        self.assertTrue(generic._detect_toc_list('  - [list'))
        self.assertTrue(generic._detect_toc_list('  + [list'))
        self.assertTrue(generic._detect_toc_list('  * [list'))
        self.assertTrue(generic._detect_toc_list('   - [list'))
        self.assertTrue(generic._detect_toc_list('   + [list'))
        self.assertTrue(generic._detect_toc_list('   * [list'))

        self.assertFalse(generic._detect_toc_list(' - \u0009list'))
        self.assertFalse(generic._detect_toc_list(' + \u0009list'))
        self.assertFalse(generic._detect_toc_list(' * \u0009list'))
        self.assertFalse(generic._detect_toc_list(' - \u0009[list'))
        self.assertFalse(generic._detect_toc_list(' + \u0009[list'))
        self.assertFalse(generic._detect_toc_list(' * \u0009[list'))

        # Ordered list.
        self.assertTrue(generic._detect_toc_list('1. list'))
        self.assertTrue(generic._detect_toc_list('9999. list'))
        self.assertTrue(generic._detect_toc_list('1) list'))
        self.assertTrue(generic._detect_toc_list('9999) list'))
        self.assertTrue(generic._detect_toc_list('1) [list'))
        self.assertTrue(generic._detect_toc_list('9999) [list'))
        self.assertFalse(generic._detect_toc_list('1.  list'))
        self.assertFalse(generic._detect_toc_list('9999.  list'))
        self.assertFalse(generic._detect_toc_list('1)  list'))
        self.assertFalse(generic._detect_toc_list('9999)  list'))
        self.assertFalse(generic._detect_toc_list('1)  [list'))
        self.assertFalse(generic._detect_toc_list('9999)  [list'))

        self.assertTrue(generic._detect_toc_list(' 1. list'))
        self.assertTrue(generic._detect_toc_list(' 9999. list'))
        self.assertTrue(generic._detect_toc_list(' 1) list'))
        self.assertTrue(generic._detect_toc_list(' 9999) list'))
        self.assertTrue(generic._detect_toc_list(' 1) [list'))
        self.assertTrue(generic._detect_toc_list(' 9999) [list'))
        self.assertFalse(generic._detect_toc_list(' 1.  list'))
        self.assertFalse(generic._detect_toc_list(' 9999.  list'))
        self.assertFalse(generic._detect_toc_list(' 1)  list'))
        self.assertFalse(generic._detect_toc_list(' 9999)  list'))
        self.assertFalse(generic._detect_toc_list(' 1)  [list'))
        self.assertFalse(generic._detect_toc_list(' 9999)  [list'))

        self.assertTrue(generic._detect_toc_list('  1. list'))
        self.assertTrue(generic._detect_toc_list('  9999. list'))
        self.assertTrue(generic._detect_toc_list('  1) list'))
        self.assertTrue(generic._detect_toc_list('  9999) list'))
        self.assertTrue(generic._detect_toc_list('  1) [list'))
        self.assertTrue(generic._detect_toc_list('  9999) [list'))
        self.assertFalse(generic._detect_toc_list('  1.  list'))
        self.assertFalse(generic._detect_toc_list('  9999.  list'))
        self.assertFalse(generic._detect_toc_list('  1)  list'))
        self.assertFalse(generic._detect_toc_list('  9999)  list'))
        self.assertFalse(generic._detect_toc_list('  1)  [list'))
        self.assertFalse(generic._detect_toc_list('  9999)  [list'))

        self.assertTrue(generic._detect_toc_list('   1. list'))
        self.assertTrue(generic._detect_toc_list('   9999. list'))
        self.assertTrue(generic._detect_toc_list('   1) list'))
        self.assertTrue(generic._detect_toc_list('   9999) list'))
        self.assertTrue(generic._detect_toc_list('   1) [list'))
        self.assertTrue(generic._detect_toc_list('   9999) [list'))
        self.assertFalse(generic._detect_toc_list('   1.  list'))
        self.assertFalse(generic._detect_toc_list('   9999.  list'))
        self.assertFalse(generic._detect_toc_list('   1)  list'))
        self.assertFalse(generic._detect_toc_list('   9999)  list'))
        self.assertFalse(generic._detect_toc_list('   1)  [list'))
        self.assertFalse(generic._detect_toc_list('   9999)  [list'))

        self.assertFalse(generic._detect_toc_list('    1. list'))
        self.assertFalse(generic._detect_toc_list('    9999. list'))
        self.assertFalse(generic._detect_toc_list('    1) list'))
        self.assertFalse(generic._detect_toc_list('    9999) list'))
        self.assertFalse(generic._detect_toc_list('    1) [list'))
        self.assertFalse(generic._detect_toc_list('    9999) [list'))
        self.assertFalse(generic._detect_toc_list('    1.  list'))
        self.assertFalse(generic._detect_toc_list('    9999.  list'))
        self.assertFalse(generic._detect_toc_list('    1)  list'))
        self.assertFalse(generic._detect_toc_list('    9999)  list'))
        self.assertFalse(generic._detect_toc_list('    1)  [list'))
        self.assertFalse(generic._detect_toc_list('    9999)  [list'))

    def test__read_line_interval(self):
        r"""Extract a line interval."""
        self.assertEqual(generic._read_line_interval('', 1, 1), '')
        self.assertEqual(generic._read_line_interval('', 0, 1), '')
        self.assertEqual(generic._read_line_interval('', 1, 0), '')
        self.assertEqual(generic._read_line_interval('', 0, 0), '')
        self.assertEqual(generic._read_line_interval('a', 1, 1), 'a')
        self.assertEqual(generic._read_line_interval('a', 0, 1), '')
        self.assertEqual(generic._read_line_interval('a', 1, 0), '')
        self.assertEqual(generic._read_line_interval('a', 0, 0), '')
        self.assertEqual(generic._read_line_interval('a\u000da', 1, 1), 'a')
        self.assertEqual(generic._read_line_interval('a\u000da', 1, 2), 'aa')
        self.assertEqual(generic._read_line_interval('a\u000da', 2, 2), 'a')
        self.assertEqual(generic._read_line_interval('a\u000d\u000aa', 2, 2),
                         'a')
        self.assertEqual(generic._read_line_interval('a\u000a\u000db', 1, 1),
                         'a\u000a\u000db')
        self.assertEqual(
            generic._read_line_interval('a\u000a\u000db\u000d\u000ac', 1, 2),
            'a\u000a\u000dbc')
        self.assertEqual(generic._read_line_interval('ab\u000d\u000ac', 1, 2),
                         'abc')
        self.assertEqual(generic._read_line_interval('ab\u000d\u000ac', 2, 2),
                         'c')
        self.assertEqual(
            generic._read_line_interval('ab\u000d\u000a\u000ac', 2, 2), '')
        self.assertEqual(
            generic._read_line_interval('ab\u000d\u000a\u000ac', 2, 3), 'c')


class TestApi(pyfakefsTestCase):
    r"""Test the main API."""

    def setUp(self):
        r"""Fake filesystem."""
        self.setUpPyfakefs()

    @unittest.skip('empty test')
    def test_tocs_equal(self):
        r"""Test if two TOCs are equal."""

    def test_write_string_on_file_between_markers(self):
        r"""Test that the TOC is written correctly on the file.

        Most of the job is done by the fpyutils library. Refer to that
        for the unit tests.
        """
        with self.assertRaises(exceptions.StdinIsNotAFileToBeWritten):
            api.write_string_on_file_between_markers('-',
                                                     LINE,
                                                     LINE,
                                                     newline_string='\n')

        # 0 TOC markers.
        with open('foo.md', 'w') as f:
            f.write('hello')
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(lines, 'hello')

        # 1 TOC markers.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines,
            'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER + '\n')

        # 2 consecutive TOC markers.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(lines, 'hello' + '\n' + MARKER + MARKER)

        # 2 TOC markers, valid list, not empty.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + '- [hi](#hi)' + '\n\n' +
                    MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines,
            'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER + '\n')

        # 2 TOC markers, valid list, less space, not empty.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n' + '- [hi](#hi)' + '\n' +
                    MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + MARKER + '\n' + '- [hi](#hi)' + '\n' + MARKER)

        # 2 TOC markers, valid list, not empty, 1 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + S1 + '- [hi](#hi)' +
                    '\n\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines,
            'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER + '\n')

        # 2 TOC markers, valid list, not empty, 2 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + S2 + '- [hi](#hi)' +
                    '\n\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines,
            'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER + '\n')

        # 2 TOC markers, valid list, not empty, 3 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + S3 + '- [hi](#hi)' +
                    '\n\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines,
            'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER + '\n')

        # 2 TOC markers, INvalid list, not empty, 4 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + S4 + '- [hi](#hi)' +
                    '\n\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + MARKER + '\n\n' + S4 + '- [hi](#hi)' + '\n\n' + MARKER)

        # 2 TOC markers, valid list, not empty, 1 leading space, less space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n' + S1 + '- [hi](#hi)' +
                    '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + MARKER + '\n' + S1 + '- [hi](#hi)' + '\n' + MARKER)

        # 2 TOC markers, valid list, not empty, 2 leading space, less space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n' + S2 + '- [hi](#hi)' +
                    '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + MARKER + '\n' + S2 + '- [hi](#hi)' + '\n' + MARKER)

        # 2 TOC markers, valid list, not empty, 3 leading space, less space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n' + S3 + '- [hi](#hi)' +
                    '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + MARKER + '\n' + S3 + '- [hi](#hi)' + '\n' + MARKER)

        # 2 TOC markers, no list, empty.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines,
            'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER + '\n')

        # 2 TOC markers, no list, empty, less space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines,
            'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER + '\n')

        # More than 2 TOC markers, valid list.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n' + MARKER + '\n' +
                    '- [hi](#hi)' + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + '- [hi](#hi)' + '\n' + MARKER)

        # More than 2 TOC markers, valid list, 1 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n' + MARKER + '\n' + S1 +
                    '- [hi](#hi)' + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + S1 + '- [hi](#hi)' + '\n' + MARKER)

        # More than 2 TOC markers, valid list, 2 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n' + MARKER + '\n' + S2 +
                    '- [hi](#hi)' + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + S2 + '- [hi](#hi)' + '\n' + MARKER)

        # More than 2 TOC markers, valid list, 3 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n' + MARKER + '\n' + S3 +
                    '- [hi](#hi)' + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + S3 + '- [hi](#hi)' + '\n' + MARKER)

        # More than 2 TOC markers, valid list first.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + '- [hi](#hi)' + '\n\n' +
                    MARKER + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + MARKER)

        # More than 2 TOC markers, valid list first, 1 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + S1 + '- [hi](#hi)' +
                    '\n\n' + MARKER + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + MARKER)

        # More than 2 TOC markers, valid list first, 2 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + S2 + '- [hi](#hi)' +
                    '\n\n' + MARKER + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + MARKER)

        # More than 2 TOC markers, valid list first, 3 leading space.
        with open('foo.md', 'w') as f:
            f.write('hello' + '\n' + MARKER + '\n\n' + S3 + '- [hi](#hi)' +
                    '\n\n' + MARKER + '\n' + MARKER)
        api.write_string_on_file_between_markers('foo.md',
                                                 LINE,
                                                 MARKER,
                                                 newline_string='\n')
        with open('foo.md') as f:
            lines = f.readlines()
        lines = ''.join(lines)
        self.assertEqual(
            lines, 'hello' + '\n' + MARKER + '\n\n' + LINE + '\n\n' + MARKER +
            '\n' + MARKER)

    @unittest.skip('empty test')
    def test_write_strings_on_files_between_markers(self):
        r"""Test that the TOC is written correctly on the files."""

    @unittest.skip('empty test')
    def test_build_toc(self):
        r"""Test that the TOC is built correctly.

        TODO: tests will be needed eventually because the complexity of
        this function is growing.
        """

    @unittest.skip('empty test')
    def test_build_multiple_tocs(self):
        r"""Test that the TOC is built correctly for multiple files."""

    def test_increase_index_ordered_list(self):
        r"""Test that the list index increases correctly.

        Test both base cases and the non-base case by verifying that the index
        increases or resets.
        """
        # Check that the index increases if we are on the same sublist.
        ht = dict()
        api.increase_index_ordered_list(ht, 0, 1)
        self.assertEqual(ht[1], 1)
        api.increase_index_ordered_list(ht, 1, 1)
        self.assertEqual(ht[1], 2)

        # Check that the index resets if we are starting a new sublist.
        ht = dict()
        ht[1] = 1
        ht[2] = 3
        ht[3] = 1
        api.increase_index_ordered_list(ht, 2, 3)
        self.assertEqual(ht[3], 1)

        # Check overflow rule for github.
        ht[1] = md_parser['github']['list']['ordered'][
            'max marker number'] = 999999999
        with self.assertRaises(exceptions.GithubOverflowOrderedListMarker):
            api.increase_index_ordered_list(ht, 1, 1)

    @unittest.skip('empty test')
    def test_build_list_marker_log(self):
        r"""Test that the list_marker_log data structure is built correctly.

        There is no need to test this since it is a very simple function.
        """

    def _test_helper_assert_compute_toc_line_indentation_spaces(
        self,
        parser,
        log,
        header_type_curr,
        header_type_prev,
        expected_indentation_spaces,
        expected_index,
        expected_list_marker,
    ):
        self.assertEqual(
            log[header_type_curr]['indentation spaces'],
            expected_indentation_spaces,
        )
        self.assertEqual(log[header_type_curr]['index'], expected_index)
        self.assertEqual(
            log[header_type_curr]['list marker'],
            expected_list_marker,
        )
        if parser == 'github':
            if header_type_curr < header_type_prev:
                for i in range(
                        header_type_curr + 1,
                        md_parser['github']['header']['max levels'] + 1,
                ):
                    self.assertEqual(log[i]['index'], 0)
                    self.assertEqual(log[i]['indentation spaces'], 0)
                    self.assertEqual(
                        log[i]['list marker'],
                        expected_list_marker,
                    )

    def test_compute_toc_line_indentation_spaces(self):
        r"""Test that the TOC list indentation spaces are computed correctly."""
        # github.
        md_parser['github']['header']['max levels'] = 6

        # Unordered TOC.

        # 1. First TOC line.
        log = api.init_indentation_log('github', '-')
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            BASE_CASE_HEADER_TYPE_PREV,
            'github',
            False,
            '-',
            log,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            BASE_CASE_HEADER_TYPE_PREV,
            0,
            0,
            '-',
        )

        # 2. First TOC line with the incorrect number of indentation spaces.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_CURR][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            BASE_CASE_HEADER_TYPE_PREV,
            'github',
            False,
            '-',
            log,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            BASE_CASE_HEADER_TYPE_PREV,
            0,
            0,
            '-',
        )

        # 3. A generic TOC line with number of previous indentation spaces = 0.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_CURR]['indentation spaces'] = 0
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            'github',
            False,
            '-',
            log,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            len(UNORDERED_LIST_SYMBOL) + len(S1),
            0,
            '-',
        )

        # 4. Base case same indentation.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_CURR][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_CURR,
            'github',
            False,
            '-',
            log,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_NUMBER_OF_INDENTATION_SPACES,
            0,
            '-',
        )

        # 5. Generic case more indentation.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_PREV][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            'github',
            False,
            '-',
            log,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            GENERIC_NUMBER_OF_INDENTATION_SPACES + len(UNORDERED_LIST_SYMBOL) +
            len(S1),
            0,
            '-',
        )

        # 6. Generic case less indentation.
        # Note: the parameters GENERIC_HEADER_TYPE_PREV and GENERIC_HEADER_TYPE_CURR
        #       are inverted as the api.compute_toc_line_indentation_spaces
        #       function input, in respect to the usual positions.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_PREV][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_PREV,
            GENERIC_HEADER_TYPE_CURR,
            'github',
            False,
            '-',
            log,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_PREV,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_NUMBER_OF_INDENTATION_SPACES,
            0,
            '-',
        )

        # Ordered TOC.

        # 7. First TOC line.
        log = api.init_indentation_log('github', '.')
        log[GENERIC_HEADER_TYPE_CURR]['indentation spaces'] = 0
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            BASE_CASE_HEADER_TYPE_PREV,
            'github',
            True,
            '.',
            log,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            0,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
            '.',
        )

        # 8. First TOC line with the incorrect number of indentation spaces.
        log = api.init_indentation_log('github', '.')
        log[GENERIC_HEADER_TYPE_CURR][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            BASE_CASE_HEADER_TYPE_PREV,
            'github',
            True,
            '.',
            log,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            0,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
            '.',
        )

        # 9. A generic TOC line with no_of_indentation_spaces_prev=0.
        log = api.init_indentation_log('github', '.')
        log[1]['index'] = 998
        log[2]['index'] = 999
        log[3]['index'] = 1001
        expected_indentation_spaces = log[GENERIC_HEADER_TYPE_PREV][
            'indentation spaces'] + len(
                str(log[GENERIC_HEADER_TYPE_PREV]['index'])) + len('.') + len(
                    S1)
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            'github',
            True,
            '.',
            log,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            expected_indentation_spaces,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
            '.',
        )

        # 10. Another base case.
        log = api.init_indentation_log('github', '.')
        log[1]['index'] = 998
        log[2]['index'] = 999
        log[3]['index'] = 1001
        log[GENERIC_HEADER_TYPE_CURR][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_CURR,
            'github',
            True,
            '.',
            log,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_NUMBER_OF_INDENTATION_SPACES,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
            '.',
        )

        # 11. Generic case more indentation. This is very similar to example 9.
        log = api.init_indentation_log('github', '.')
        log[1]['index'] = 998
        log[2]['index'] = 999
        log[3]['index'] = 1001
        log[GENERIC_HEADER_TYPE_PREV][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        expected_indentation_spaces = log[GENERIC_HEADER_TYPE_PREV][
            'indentation spaces'] + len(
                str(log[GENERIC_HEADER_TYPE_PREV]['index'])) + len('.') + len(
                    S1)
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            'github',
            True,
            '.',
            log,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            expected_indentation_spaces,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
            '.',
        )

        # 12. Generic case less indentation. See example 6.
        log = api.init_indentation_log('github', '.')
        log[1]['index'] = 998
        log[2]['index'] = 999
        log[3]['index'] = 1001
        log[GENERIC_HEADER_TYPE_PREV][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        expected_indentation_spaces = log[GENERIC_HEADER_TYPE_PREV][
            'indentation spaces']
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_PREV,
            GENERIC_HEADER_TYPE_CURR,
            'github',
            True,
            '.',
            log,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github',
            log,
            GENERIC_HEADER_TYPE_PREV,
            GENERIC_HEADER_TYPE_CURR,
            expected_indentation_spaces,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX,
            '.',
        )

        # redcarpet.
        md_parser['redcarpet']['header']['max levels'] = 6

        # 1. More indentation.
        log = api.init_indentation_log('redcarpet', '-')
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            'redcarpet',
            False,
            '-',
            log,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'redcarpet',
            log,
            GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            LIST_INDENTATION * (GENERIC_HEADER_TYPE_CURR - 1),
            0,
            '-',
        )

        # 2. Less indentation.
        log = api.init_indentation_log('redcarpet', '-')
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_PREV,
            GENERIC_HEADER_TYPE_CURR,
            'redcarpet',
            False,
            '-',
            log,
        )
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'redcarpet',
            log,
            GENERIC_HEADER_TYPE_PREV,
            GENERIC_HEADER_TYPE_CURR,
            LIST_INDENTATION * (GENERIC_HEADER_TYPE_PREV - 1),
            0,
            '-',
        )

    def test_build_toc_line_without_indentation(self):
        r"""Test TOC line building for different types of inputs."""
        # github and redcarpet.
        header = {
            'type': GENERIC_HEADER_TYPE_CURR,
            'text_original': LINE,
            'text_anchor_link': LINE,
            'visible': True,
        }

        # Unordered.
        self.assertEqual(
            api.build_toc_line_without_indentation(
                header,
                ordered=False,
                no_links=True,
                parser='github',
            ),
            UNORDERED_LIST_SYMBOL + S1 + LINE,
        )

        self.assertEqual(
            api.build_toc_line_without_indentation(
                header,
                ordered=False,
                no_links=False,
                parser='github',
            ),
            UNORDERED_LIST_SYMBOL + S1 + '[' + LINE + ']' + '(#' + LINE + ')',
        )

        # Ordered.
        self.assertEqual(
            api.build_toc_line_without_indentation(
                header,
                ordered=True,
                no_links=True,
                list_marker=ORDERED_LIST_SYMBOL,
                parser='github',
            ),
            '1' + ORDERED_LIST_SYMBOL + S1 + LINE,
        )

        self.assertEqual(
            api.build_toc_line_without_indentation(
                header,
                ordered=True,
                no_links=False,
                list_marker=ORDERED_LIST_SYMBOL,
                parser='github',
            ),
            '1' + ORDERED_LIST_SYMBOL + S1 + '[' + LINE + ']' + '(#' + LINE +
            ')',
        )

    @unittest.skip('empty test')
    def test_build_toc_line(self):
        r"""Test that the TOC line is built correctly.

        This function is a frontend to both the
        build_toc_line_without_indentation and
        compute_toc_line_indentation_spaces functions.
        Refer to those two functions for the unit tests.
        """

    def test_filter_indices_from_line(self):
        r"""Test removing indices from a string."""
        self.assertEqual(api.filter_indices_from_line('foo', [range(0, 3)]),
                         '')
        self.assertEqual(api.filter_indices_from_line('', [range(0, 1024)]),
                         '')
        self.assertEqual(api.filter_indices_from_line('', [range(0, 0)]), '')
        self.assertEqual(
            api.filter_indices_from_line(512 * '1', [range(0, 512 - 1)]), '1')
        self.assertEqual(api.filter_indices_from_line(512 * '1', []),
                         512 * '1')
        self.assertEqual(
            api.filter_indices_from_line(
                'foo bar', [range(1, 2), range(4, 7)]), 'fo ')

    def test_remove_emphasis(self):
        r"""Test that removing emphasis works correctly correctly.

        .. note: not all tests are enabled because of a missing implementation
            and possible bugs.
        """
        # Example 331 [Commonmark 0.28].
        # Example 350 [Commonmark 0.29].
        # Example 350 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo bar*'), 'foo bar')

        # Example 332 [Commonmark 0.28].
        # Example 351 [Commonmark 0.29].
        # Example 351 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('a * foo bar*'), 'a * foo bar*')

        # Example 333 [Commonmark 0.28].
        # Example 352 [Commonmark 0.29].
        # Example 352 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('a*"foo"*'), 'a*"foo"*')

        # Example 334 [Commonmark 0.28].
        # Example 353 [Commonmark 0.29].
        # Example 353 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('* a *'), '* a *')

        # Example 335 [Commonmark 0.28].
        # Example 354 [Commonmark 0.29].
        # Example 354 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo*bar*'), 'foobar')

        # Example 336 [Commonmark 0.28].
        # Example 355 [Commonmark 0.29].
        # Example 355 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('5*6*78'), '5678')

        # Example 337 [Commonmark 0.28].
        # Example 356 [Commonmark 0.29].
        # Example 356 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo bar_'), 'foo bar')

        # Example 338 [Commonmark 0.28].
        # Example 357 [Commonmark 0.29].
        # Example 357 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_ foo bar_'), '_ foo bar_')

        # Example 339 [Commonmark 0.28].
        # Example 358 [Commonmark 0.29].
        # Example 358 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('a_"foo"_'), 'a_"foo"_')

        # Example 340 [Commonmark 0.28].
        # Example 359 [Commonmark 0.29].
        # Example 359 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo_bar_'), 'foo_bar_')

        # Example 341 [Commonmark 0.28].
        # Example 360 [Commonmark 0.29].
        # Example 360 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('5_6_78'), '5_6_78')

        # Example 342 [Commonmark 0.28].
        # Example 361 [Commonmark 0.29].
        # Example 361 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('пристаням_стремятся_'),
                         'пристаням_стремятся_')

        # Example 343 [Commonmark 0.28].
        # Example 362 [Commonmark 0.29].
        # Example 362 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('aa_"bb"_cc'), 'aa_"bb"_cc')

        # Example 344 [Commonmark 0.28].
        # Example 363 [Commonmark 0.29].
        # Example 363 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo-_(bar)_'), 'foo-(bar)')

        # Example 345 [Commonmark 0.28].
        # Example 364 [Commonmark 0.29].
        # Example 364 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo*'), '_foo*')

        # Example 346 [Commonmark 0.28].
        # Example 365 [Commonmark 0.29].
        # Example 365 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo bar *'), '*foo bar *')

        # Example 347 [Commonmark 0.28].
        # Example 366 [Commonmark 0.29].
        # Example 366 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo bar\n*'), '*foo bar\n*')

        # Example 348 [Commonmark 0.28].
        # Example 367 [Commonmark 0.29].
        # Example 367 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*(*foo)'), '*(*foo)')

        # Example 349 [Commonmark 0.28].
        # Example 368 [Commonmark 0.29].
        # Example 368 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*(*foo*)*'), '(foo)')

        # Example 350 [Commonmark 0.28].
        # Example 369 [Commonmark 0.29].
        # Example 369 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo*bar'), 'foobar')

        # Example 351 [Commonmark 0.28].
        # Example 370 [Commonmark 0.29].
        # Example 370 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo bar _'), '_foo bar _')

        # Example 352 [Commonmark 0.28].
        # Example 371 [Commonmark 0.29].
        # Example 371 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_(_foo)'), '_(_foo)')

        # Example 353 [Commonmark 0.28].
        # Example 372 [Commonmark 0.29].
        # Example 372 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_(_foo_)_'), '(foo)')

        # Example 354 [Commonmark 0.28].
        # Example 373 [Commonmark 0.29].
        # Example 373 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo_bar'), '_foo_bar')

        # Example 355 [Commonmark 0.28].
        # Example 374 [Commonmark 0.29].
        # Example 374 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_пристаням_стремятся'),
                         '_пристаням_стремятся')

        # Example 356 [Commonmark 0.28].
        # Example 375 [Commonmark 0.29].
        # Example 375 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo_bar_baz_'), 'foo_bar_baz')

        # Example 357 [Commonmark 0.28].
        # Example 376 [Commonmark 0.29].
        # Example 376 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_(bar)_.'), '(bar).')

        # Example 358 [Commonmark 0.28].
        # Example 377 [Commonmark 0.29].
        # Example 377 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo bar**'), 'foo bar')

        # Example 359 [Commonmark 0.28].
        # Example 378 [Commonmark 0.29].
        # Example 378 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('** foo bar**'), '** foo bar**')

        # Example 360 [Commonmark 0.28].
        # Example 379 [Commonmark 0.29].
        # Example 379 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('a**"foo"**'), 'a**"foo"**')

        # Example 361 [Commonmark 0.28].
        # Example 380 [Commonmark 0.29].
        # Example 380 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo**bar**'), 'foobar')

        # Example 362 [Commonmark 0.28].
        # Example 381 [Commonmark 0.29].
        # Example 381 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo bar__'), 'foo bar')

        # Example 363 [Commonmark 0.28].
        # Example 382 [Commonmark 0.29].
        # Example 382 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__ foo bar__'), '__ foo bar__')

        # Example 364 [Commonmark 0.28].
        # Example 383 [Commonmark 0.29].
        # Example 383 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__\nfoo bar__'), '__\nfoo bar__')

        # Example 365 [Commonmark 0.28].
        # Example 384 [Commonmark 0.29].
        # Example 384 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('a__"foo"__'), 'a__"foo"__')

        # Example 366 [Commonmark 0.28].
        # Example 385 [Commonmark 0.29].
        # Example 385 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo__bar__'), 'foo__bar__')

        # Example 367 [Commonmark 0.28].
        # Example 386 [Commonmark 0.29].
        # Example 386 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('5__6__78'), '5__6__78')

        # Example 368 [Commonmark 0.28].
        # Example 387 [Commonmark 0.29].
        # Example 387 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('пристаням__стремятся__'),
                         'пристаням__стремятся__')

        # Example 369 [Commonmark 0.28].
        # Example 388 [Commonmark 0.29].
        # Example 388 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo, __bar__, baz__'),
                         'foo, bar, baz')

        # Example 370 [Commonmark 0.28].
        # Example 389 [Commonmark 0.29].
        # Example 389 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo-__(bar)__'), 'foo-(bar)')

        # Example 371 [Commonmark 0.28].
        # Example 390 [Commonmark 0.29].
        # Example 390 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo bar **'), '**foo bar **')

        # Example 372 [Commonmark 0.28].
        # Example 391 [Commonmark 0.29].
        # Example 391 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**(**foo)'), '**(**foo)')

        # Example 373 [Commonmark 0.28].
        # Example 392 [Commonmark 0.29].
        # Example 392 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*(**foo**)*'), '(foo)')

        # Example 374 [Commonmark 0.28].
        # Example 393 [Commonmark 0.29].
        # Example 393 [Commonmark 0.30].
        self.assertEqual(
            api.remove_emphasis(
                '**Gomphocarpus (*Gomphocarpus physocarpus*, syn.\n*Asclepias physocarpa*)**'
            ),
            'Gomphocarpus (Gomphocarpus physocarpus, syn.\nAsclepias physocarpa)'
        )

        # Example 375 [Commonmark 0.28].
        # Example 394 [Commonmark 0.29].
        # Example 394 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo "*bar*" foo**'),
                         'foo "bar" foo')

        # Example 376 [Commonmark 0.28].
        # Example 395 [Commonmark 0.29].
        # Example 395 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo**bar'), 'foobar')

        # Example 377 [Commonmark 0.28].
        # Example 396 [Commonmark 0.29].
        # Example 396 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo bar __'), '__foo bar __')

        # Example 378 [Commonmark 0.28].
        # Example 397 [Commonmark 0.29].
        # Example 397 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__(__foo)'), '__(__foo)')

        # Example 379 [Commonmark 0.28].
        # Example 398 [Commonmark 0.29].
        # Example 398 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_(__foo__)_'), '(foo)')

        # Example 380 [Commonmark 0.28].
        # Example 399 [Commonmark 0.29].
        # Example 399 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo__bar'), '__foo__bar')

        # Example 381 [Commonmark 0.28].
        # Example 400 [Commonmark 0.29].
        # Example 400 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__пристаням__стремятся'),
                         '__пристаням__стремятся')

        # Example 382 [Commonmark 0.28].
        # Example 401 [Commonmark 0.29].
        # Example 401 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo__bar__baz__'),
                         'foo__bar__baz')

        # Example 383 [Commonmark 0.28].
        # Example 402 [Commonmark 0.29].
        # Example 402 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__(bar)__.'), '(bar).')

        # Example 384 [Commonmark 0.28].
        # Example 403 [Commonmark 0.29].
        # Example 403 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo [bar](/url)*'),
                         'foo [bar](/url)')

        # Example 385 [Commonmark 0.28].
        # Example 404 [Commonmark 0.29].
        # Example 404 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo\nbar*'), 'foo\nbar')

        # Example 386 [Commonmark 0.28].
        # Example 405 [Commonmark 0.29].
        # Example 405 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo __bar__ baz_'),
                         'foo bar baz')

        # Example 387 [Commonmark 0.28].
        # Example 406 [Commonmark 0.29].
        # Example 406 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo _bar_ baz_'), 'foo bar baz')

        # Example 388 [Commonmark 0.28].
        # Example 407 [Commonmark 0.29].
        # Example 407 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo_ bar_'), 'foo bar')

        # Example 389 [Commonmark 0.28].
        # Example 408 [Commonmark 0.29].
        # Example 408 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo *bar**'), 'foo bar')

        # Example 390 [Commonmark 0.28].
        # Example 409 [Commonmark 0.29].
        # Example 409 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo **bar** baz*'),
                         'foo bar baz')

        # Example 391 [Commonmark 0.28].
        # Example 410 [Commonmark 0.29].
        # Example 410 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo**bar**baz*'), 'foobarbaz')

        # Example 411 [Commonmark 0.29].
        # Example 411 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo**bar*'), 'foo**bar')

        # Example 392 [Commonmark 0.28].
        # Example 412 [Commonmark 0.29].
        # Example 412 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('***foo** bar*'), 'foo bar')

        # Example 393 [Commonmark 0.28].
        # Example 413 [Commonmark 0.29].
        # Example 413 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo **bar***'), 'foo bar')

        # Example 394 [Commonmark 0.28].
        # Example 414 [Commonmark 0.29].
        # Example 414 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo**bar***'), 'foobar')

        # Example 415 [Commonmark 0.29].
        # Example 415 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo***bar***baz'), 'foobarbaz')

        # Example 416 [Commonmark 0.29].
        # Example 416 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo******bar*********baz'),
                         'foobar***baz')

        # Example 395 [Commonmark 0.28].
        # Example 417 [Commonmark 0.29].
        # Example 417 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo **bar *baz* bim** bop*'),
                         'foo bar baz bim bop')

        # Example 396 [Commonmark 0.28].
        # Example 418 [Commonmark 0.29].
        # Example 418 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo [*bar*](/url)*'),
                         'foo [bar](/url)')

        # Example 397 [Commonmark 0.28].
        # Example 419 [Commonmark 0.29].
        # Example 419 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('** is not an empty emphasis'),
                         '** is not an empty emphasis')

        # Example 398 [Commonmark 0.28].
        # Example 420 [Commonmark 0.29].
        # Example 420 [Commonmark 0.30].
        self.assertEqual(
            api.remove_emphasis('**** is not an empty strong emphasis'),
            '**** is not an empty strong emphasis')

        # Example 399 [Commonmark 0.28].
        # Example 421 [Commonmark 0.29].
        # Example 421 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo [bar](/url)**'),
                         'foo [bar](/url)')

        # Example 400 [Commonmark 0.28].
        # Example 422 [Commonmark 0.29].
        # Example 422 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo\nbar**'), 'foo\nbar')

        # Example 401 [Commonmark 0.28].
        # Example 423 [Commonmark 0.29].
        # Example 423 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo _bar_ baz__'),
                         'foo bar baz')

        # Example 402 [Commonmark 0.28].
        # Example 424 [Commonmark 0.29].
        # Example 424 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo __bar__ baz__'),
                         'foo bar baz')

        # Example 403 [Commonmark 0.28].
        # Example 425 [Commonmark 0.29].
        # Example 425 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('____foo__ bar__'), 'foo bar')

        # Example 404 [Commonmark 0.28].
        # Example 426 [Commonmark 0.29].
        # Example 426 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo **bar****'), 'foo bar')

        # Example 405 [Commonmark 0.28].
        # Example 427 [Commonmark 0.29].
        # Example 427 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo *bar* baz**'),
                         'foo bar baz')

        # Example 406 [Commonmark 0.28].
        # Example 428 [Commonmark 0.29].
        # Example 428 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo*bar*baz**'), 'foobarbaz')

        # Example 407 [Commonmark 0.28].
        # Example 429 [Commonmark 0.29].
        # Example 429 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('***foo* bar**'), 'foo bar')

        # Example 408 [Commonmark 0.28].
        # Example 430 [Commonmark 0.29].
        self.assertEqual(api.remove_emphasis('**foo *bar***'), 'foo bar')

        # Example 409 [Commonmark 0.28].
        # Example 431 [Commonmark 0.29].
        # Example 431 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo *bar **baz**\nbim* bop**'),
                         'foo bar baz\nbim bop')

        # Example 410 [Commonmark 0.28].
        # Example 432 [Commonmark 0.29].
        # Example 432 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo [*bar*](/url)**'),
                         'foo [bar](/url)')

        # Example 411 [Commonmark 0.28].
        # Example 433 [Commonmark 0.29].
        # Example 433 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__ is not an empty emphasis'),
                         '__ is not an empty emphasis')

        # Example 412 [Commonmark 0.28].
        # Example 434 [Commonmark 0.29].
        # Example 434 [Commonmark 0.30].
        self.assertEqual(
            api.remove_emphasis('____ is not an empty strong emphasis'),
            '____ is not an empty strong emphasis')

        # Example 413 [Commonmark 0.28].
        # Example 435 [Commonmark 0.29].
        # Example 435 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo ***'), 'foo ***')

        # Example 414 [Commonmark 0.28].
        # Example 436 [Commonmark 0.29].
        # Example 436 [Commonmark 0.30].
        # Removing backslashes is not implemented for these cases because they are already removed
        # with a regex in the build_anchor_link function.
        self.assertEqual(
            api.remove_emphasis(r'foo *\**').replace(LINE_ESCAPE, ''),
            ('foo ' + LINE_ESCAPE + '*').replace(LINE_ESCAPE, ''))
        self.assertEqual(api.remove_emphasis(r'foo *\**'),
                         'foo ' + LINE_ESCAPE + '*')

        # Example 415 [Commonmark 0.28].
        # Example 437 [Commonmark 0.29].
        # Example 437 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo *_*'), 'foo _')

        # Example 416 [Commonmark 0.28].
        # Example 438 [Commonmark 0.29].
        # Example 438 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo ****'), 'foo ****')

        # Example 417 [Commonmark 0.28].
        # Example 439 [Commonmark 0.29].
        # Example 439 [Commonmark 0.30].
        self.assertEqual(
            api.remove_emphasis(r'foo **\***').replace(LINE_ESCAPE, ''),
            ('foo ' + LINE_ESCAPE + '*').replace(LINE_ESCAPE, ''))
        self.assertEqual(api.remove_emphasis(r'foo **\***'),
                         'foo ' + LINE_ESCAPE + '*')

        # Example 418 [Commonmark 0.28].
        # Example 440 [Commonmark 0.29].
        # Example 440 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo **_**'), 'foo _')

        # Example 419 [Commonmark 0.28].
        # Example 441 [Commonmark 0.29].
        # Example 441 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo*'), '*foo')

        # Example 420 [Commonmark 0.28].
        # Example 442 [Commonmark 0.29].
        # Example 442 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo**'), 'foo*')

        # Example 421 [Commonmark 0.28].
        # Example 443 [Commonmark 0.29].
        # Example 443 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('***foo**'), '*foo')

        # Example 422 [Commonmark 0.28].
        # Example 444 [Commonmark 0.29].
        # Example 444 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('****foo*'), '***foo')

        # Example 423 [Commonmark 0.28].
        # Example 445 [Commonmark 0.29].
        # Example 445 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo***'), 'foo*')

        # Example 424 [Commonmark 0.28].
        # Example 446 [Commonmark 0.29].
        # Example 446 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo****'), 'foo***')

        # Example 425 [Commonmark 0.28].
        # Example 447 [Commonmark 0.29].
        # Example 447 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo ___'), 'foo ___')

        # Example 426 [Commonmark 0.28].
        # Example 448 [Commonmark 0.29].
        # Example 448 [Commonmark 0.30].
        self.assertEqual(
            api.remove_emphasis(r'foo _\__').replace(LINE_ESCAPE, ''),
            ('foo ' + LINE_ESCAPE + '_').replace(LINE_ESCAPE, ''))
        self.assertEqual(api.remove_emphasis(r'foo _\__'),
                         'foo ' + LINE_ESCAPE + '_')

        # Example 427 [Commonmark 0.28].
        # Example 449 [Commonmark 0.29].
        # Example 449 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo _*_'), 'foo *')

        # Example 428 [Commonmark 0.28].
        # Example 450 [Commonmark 0.29].
        # Example 450 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo _____'), 'foo _____')

        # Example 429 [Commonmark 0.28].
        # Example 451 [Commonmark 0.29].
        # Example 451 [Commonmark 0.30].
        self.assertEqual(
            api.remove_emphasis(r'foo __\___').replace(LINE_ESCAPE, ''),
            ('foo ' + LINE_ESCAPE + '_').replace(LINE_ESCAPE, ''))
        self.assertEqual(api.remove_emphasis(r'foo __\___'),
                         'foo ' + LINE_ESCAPE + '_')

        # Example 430 [Commonmark 0.28].
        # Example 452 [Commonmark 0.29].
        # Example 452 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('foo __*__'), 'foo *')

        # Example 431 [Commonmark 0.28].
        # Example 453 [Commonmark 0.29].
        # Example 453 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo_'), '_foo')

        # Example 432 [Commonmark 0.28].
        # Example 454 [Commonmark 0.29].
        # Example 454 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo__'), 'foo_')

        # Example 433 [Commonmark 0.28].
        # Example 455 [Commonmark 0.29].
        # Example 455 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('___foo__'), '_foo')

        # Example 434 [Commonmark 0.28].
        # Example 456 [Commonmark 0.29].
        # Example 456 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('____foo_'), '___foo')

        # Example 435 [Commonmark 0.28].
        # Example 457 [Commonmark 0.29].
        # Example 457 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo___'), 'foo_')

        # Example 436 [Commonmark 0.28].
        # Example 458 [Commonmark 0.29].
        # Example 458 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo____'), 'foo___')

        # Example 437 [Commonmark 0.28].
        # Example 459 [Commonmark 0.29].
        # Example 459 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo**'), 'foo')

        # Example 438 [Commonmark 0.28].
        # Example 460 [Commonmark 0.29].
        # Example 460 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*_foo_*'), 'foo')

        # Example 439 [Commonmark 0.28].
        # Example 461 [Commonmark 0.29].
        # Example 461 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__foo__'), 'foo')

        # Example 440 [Commonmark 0.28].
        # Example 462 [Commonmark 0.29].
        # Example 462 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_*foo*_'), 'foo')

        # Example 441 [Commonmark 0.28].
        # Example 463 [Commonmark 0.29].
        # Example 463 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('****foo****'), 'foo')

        # Example 442 [Commonmark 0.28].
        # Example 464 [Commonmark 0.29].
        # Example 464 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('____foo____'), 'foo')

        # Example 443 [Commonmark 0.28].
        # Example 465 [Commonmark 0.29].
        # Example 465 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('******foo******'), 'foo')

        # Example 444 [Commonmark 0.28].
        # Example 466 [Commonmark 0.29].
        # Example 466 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('***foo***'), 'foo')

        # Example 445 [Commonmark 0.28].
        # Example 467 [Commonmark 0.29].
        # Example 467 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_____foo_____'), 'foo')

        # Example 446 [Commonmark 0.28].
        # Example 468 [Commonmark 0.29].
        # Example 468 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo _bar* baz_'),
                         'foo _bar baz_')

        # Example 447 [Commonmark 0.28].
        # Example 469 [Commonmark 0.29].
        # Example 469 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo __bar *baz bim__ bam*'),
                         'foo bar *baz bim bam')

        # Example 448 [Commonmark 0.28].
        # Example 470 [Commonmark 0.29].
        # Example 470 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**foo **bar baz**'),
                         '**foo bar baz')

        # Example 449 [Commonmark 0.28].
        # Example 471 [Commonmark 0.29].
        # Example 471 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*foo *bar baz*'), '*foo bar baz')

        # Example 450 [Commonmark 0.28].
        # Example 472 [Commonmark 0.29].
        # Example 472 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[bar*](/url)'), '*[bar*](/url)')

        # Extra examples.
        self.assertEqual(api.remove_emphasis('*[*bar](/url)'), '*[*bar](/url)')
        self.assertEqual(api.remove_emphasis('*[*bar](*/url*)'),
                         '*[*bar](*/url*)')
        self.assertEqual(api.remove_emphasis('*[bar](/url)*'), '[bar](/url)')
        self.assertEqual(api.remove_emphasis('*[bar*] (/url)'), '[bar] (/url)')
        self.assertEqual(api.remove_emphasis('[bar](/url*)*'), '[bar](/url*)*')
        self.assertEqual(api.remove_emphasis('[bar](/url**)**'),
                         '[bar](/url**)**')

        # Example 451 [Commonmark 0.28].
        # Example 473 [Commonmark 0.29].
        # Example 473 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_foo [bar_](/url)'),
                         '_foo [bar_](/url)')

        # Example 452 [Commonmark 0.28].
        # Example 474 [Commonmark 0.29].
        # Example 474 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*<img src="foo" title="*"/>'),
                         '*<img src="foo" title="*"/>')

        # Example 453 [Commonmark 0.28].
        # Example 475 [Commonmark 0.29].
        # Example 475 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('**<a href="**">'),
                         '**<a href="**">')

        # Example 454 [Commonmark 0.28].
        # Example 476 [Commonmark 0.29].
        # Example 476 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('__<a href="__">'),
                         '__<a href="__">')

        # Example 455 [Commonmark 0.28].
        # Example 477 [Commonmark 0.29].
        # Example 477 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*a `*`*'), 'a `*`')

        # Extra examples.
        self.assertEqual(api.remove_emphasis('*a `****`*'), 'a `****`')
        self.assertEqual(api.remove_emphasis('*a `** **`*'), 'a `** **`')
        self.assertEqual(api.remove_emphasis('*a `**** `*'), 'a `**** `')

        # Example 456 [Commonmark 0.28].
        # Example 478 [Commonmark 0.29].
        # Example 478 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('_a `_`_'), 'a `_`')

        # Extra examples.
        self.assertEqual(api.remove_emphasis('_a `____`_'), 'a `____`')
        self.assertEqual(api.remove_emphasis('_a `__ __`_'), 'a `__ __`')
        self.assertEqual(api.remove_emphasis('_a `____ `_'), 'a `____ `')

        # Example 457 [Commonmark 0.28].
        # Example 479 [Commonmark 0.29].
        # Example 479 [Commonmark 0.30].
        #        self.assertEqual(api.remove_emphasis('**a<http://foo.bar/?q=**>'), '**a<http://foo.bar/?q=**>')
        #

        # Example 458 [Commonmark 0.28].
        # Example 480 [Commonmark 0.29].
        # Example 480 [Commonmark 0.30].
        #        self.assertEqual(api.remove_emphasis('__a<http://foo.bar/?q=__>'), '__a<http://foo.bar/?q=__>')

        # Examples 481 -> 525 [Commonmark 0.30].
        # Note: most of these are modified examples for emphasis only.

        # Example 481 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[bar*](/uri "title")'),
                         '*[bar*](/uri "title")')
        #        self.assertEqual(api.remove_emphasis('[bar](/uri *"title")*'), '[bar](/uri *"title")*')
        self.assertEqual(api.remove_emphasis('_[bar_](/uri "title")'),
                         '_[bar_](/uri "title")')
        #        self.assertEqual(api.remove_emphasis('[bar](/uri _"title")_'), '[bar](/uri _"title")_')

        # Example 482 [Commonmark 0.30].
        # ignore

        # Example 483 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[*](./target.md)'),
                         '*[*](./target.md)')
        self.assertEqual(api.remove_emphasis('[](*./target.md)*'),
                         '[](*./target.md)*')
        self.assertEqual(api.remove_emphasis('_[_](./target.md)'),
                         '_[_](./target.md)')
        self.assertEqual(api.remove_emphasis('[](_./target.md)_'),
                         '[](_./target.md)_')

        # Example 484 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*]()'), '*[link*]()')
        self.assertEqual(api.remove_emphasis('[link](*)*'), '[link](*)*')
        self.assertEqual(api.remove_emphasis('_[link_]()'), '_[link_]()')
        self.assertEqual(api.remove_emphasis('[link](_)_'), '[link](_)_')

        # Example 485 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*](<>)'), '*[link*](<>)')
        self.assertEqual(api.remove_emphasis('[link](*<>)*'), '[link](*<>)*')
        self.assertEqual(api.remove_emphasis('_[link_](<>)'), '_[link_](<>)')
        self.assertEqual(api.remove_emphasis('[link](_<>)_'), '[link](_<>)_')

        # Example 486 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[*]()'), '*[*]()')
        self.assertEqual(api.remove_emphasis('[](*)*'), '[](*)*')
        self.assertEqual(api.remove_emphasis('_[_]()'), '_[_]()')
        self.assertEqual(api.remove_emphasis('[](_)_'), '[](_)_')

        # Example 487 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*](/my uri)'),
                         '[link](/my uri)')
        self.assertEqual(api.remove_emphasis('[link](*/my uri)*'),
                         '[link](/my uri)')
        #        self.assertEqual(api.remove_emphasis('_[link_](/my uri)'), '[link](/my uri)')
        self.assertEqual(api.remove_emphasis('[link](_/my uri)_'),
                         '[link](/my uri)')

        # Example 488 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*](</my uri>)'),
                         '*[link*](</my uri>)')
        self.assertEqual(api.remove_emphasis('[link](</my *uri>)*'),
                         '[link](</my *uri>)*')
        self.assertEqual(api.remove_emphasis('_[link_](</my uri>)'),
                         '_[link_](</my uri>)')
        self.assertEqual(api.remove_emphasis('[link](</my _uri>)_'),
                         '[link](</my _uri>)_')

        # Example 489 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*](foo\nbar)'),
                         '[link](foo\nbar)')
        self.assertEqual(api.remove_emphasis('[link](*foo\nbar)*'),
                         '[link](foo\nbar)')
        #        self.assertEqual(api.remove_emphasis('_[link_](foo\nbar)'), '[link](foo\nbar)')
        self.assertEqual(api.remove_emphasis('[link](_foo\nbar)_'),
                         '[link](foo\nbar)')

        # Example 490 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*](<foo\nbar>)'),
                         '[link](<foo\nbar>)')
        self.assertEqual(api.remove_emphasis('[link](*<foo\nbar>)*'),
                         '[link](<foo\nbar>)')
        #        self.assertEqual(api.remove_emphasis('_[link_](<foo\nbar>)'), '[link](<foo\nbar>)')
        self.assertEqual(api.remove_emphasis('[link](_<foo\nbar>)_'),
                         '[link](<foo\nbar>)')

        # Example 491 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[a*](<b)c>)'), '*[a*](<b)c>)')
        self.assertEqual(api.remove_emphasis('[a](*<b)c>)*'), '[a](*<b)c>)*')
        self.assertEqual(api.remove_emphasis('_[a_](<b)c>)'), '_[a_](<b)c>)')
        self.assertEqual(api.remove_emphasis('[a](_<b)c>)_'), '[a](_<b)c>)_')

        # Example 492 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*](<foo\>)'),
                         r'[link](<foo\>)')
        #        self.assertEqual(api.remove_emphasis('[link](*<foo\>)*'), '[link](<foo\>)')
        #        self.assertEqual(api.remove_emphasis('_[link_](<foo\>)'), '[link](<foo\>)')
        #        self.assertEqual(api.remove_emphasis('[link](_<foo\>)_'), '[link](<foo\>)')

        # Example 493 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[a*](<b)c'), '[a](<b)c')
        #        self.assertEqual(api.remove_emphasis('[a](*<b)c*'), '[a](<b)c')
        #        self.assertEqual(api.remove_emphasis('_[a_](<b)c'), '[a](<b)c')
        #        self.assertEqual(api.remove_emphasis('[a](_<b)c_'), '[a](<b)c')

        self.assertEqual(api.remove_emphasis('*[a*](<b)c>'), '[a](<b)c>')
        #        self.assertEqual(api.remove_emphasis('[a](*<b)c>*'), '[a](<b)c>')
        #        self.assertEqual(api.remove_emphasis('_[a_](<b)c>'), '[a](<b)c>')
        #        self.assertEqual(api.remove_emphasis('[a](_<b)c>_'), '[a](<b)c>')

        self.assertEqual(api.remove_emphasis('*[a*](<b>c)'), '[a](<b>c)')
        #        self.assertEqual(api.remove_emphasis('[a](*<b>c)*'), '[a](<b>c)')
        #        self.assertEqual(api.remove_emphasis('_[a_](<b>c)'), '[a](<b>c)')
        #        self.assertEqual(api.remove_emphasis('[a](_<b>c)_'), '[a](<b>c)')

        # Example 494 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*](\(foo\))'),
                         r'*[link*](\(foo\))')
        self.assertEqual(api.remove_emphasis(r'[link](*\(foo\))*'),
                         r'[link](*\(foo\))*')
        self.assertEqual(api.remove_emphasis(r'_[link_](\(foo\))'),
                         r'_[link_](\(foo\))')
        self.assertEqual(api.remove_emphasis(r'[link](_\(foo\))_'),
                         r'[link](_\(foo\))_')

        # Example 495 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*](foo(and(bar)))'),
                         '*[link*](foo(and(bar)))')
        self.assertEqual(api.remove_emphasis('[link](*foo(and(bar)))*'),
                         '[link](*foo(and(bar)))*')
        self.assertEqual(api.remove_emphasis('_[link_](foo(and(bar)))'),
                         '_[link_](foo(and(bar)))')
        self.assertEqual(api.remove_emphasis('[link](_foo(and(bar)))_'),
                         '[link](_foo(and(bar)))_')

        # Example 496 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*](foo(and(bar))'),
                         '[link](foo(and(bar))')
        self.assertEqual(api.remove_emphasis('[link](*foo(and(bar))*'),
                         '[link](foo(and(bar))')
        #        self.assertEqual(api.remove_emphasis('_[link_](foo(and(bar))'), '[link](foo(and(bar))')
        self.assertEqual(api.remove_emphasis('[link](_foo(and(bar))_'),
                         '[link](foo(and(bar))')

        # Example 497 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*](foo\(and\(bar\))'),
                         r'*[link*](foo\(and\(bar\))')
        self.assertEqual(api.remove_emphasis(r'[link](*foo\(and\(bar\))*'),
                         r'[link](*foo\(and\(bar\))*')
        self.assertEqual(api.remove_emphasis(r'_[link_](foo\(and\(bar\))'),
                         r'_[link_](foo\(and\(bar\))')
        self.assertEqual(api.remove_emphasis(r'[link](_foo\(and\(bar\))_'),
                         r'[link](_foo\(and\(bar\))_')

        # Example 498 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*](<foo(and(bar)>)'),
                         '*[link*](<foo(and(bar)>)')
        #        self.assertEqual(api.remove_emphasis('[link](*<foo(and(bar)>)*'), '[link](*<foo(and(bar)>)*')
        self.assertEqual(api.remove_emphasis('_[link_](<foo(and(bar)>)'),
                         '_[link_](<foo(and(bar)>)')
        #        self.assertEqual(api.remove_emphasis('[link](_<foo(and(bar)>)_'), '[link](_<foo(and(bar)>)_')

        # Example 499 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*](foo\)\:)'),
                         r'*[link*](foo\)\:)')
        self.assertEqual(api.remove_emphasis(r'[link](*foo\)\:)*'),
                         r'[link](*foo\)\:)*')
        self.assertEqual(api.remove_emphasis(r'_[link_](foo\)\:)'),
                         r'_[link_](foo\)\:)')
        self.assertEqual(api.remove_emphasis(r'[link](_foo\)\:)_'),
                         r'[link](_foo\)\:)_')

        # Example 500 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[*link](#fragment)'),
                         '*[*link](#fragment)')
        self.assertEqual(api.remove_emphasis('[link](#fragment*)*'),
                         '[link](#fragment*)*')
        self.assertEqual(api.remove_emphasis('_[_link](#fragment)'),
                         '_[_link](#fragment)')
        self.assertEqual(api.remove_emphasis('[link](#fragment_)_'),
                         '[link](#fragment_)_')

        self.assertEqual(
            api.remove_emphasis('*[*link](http://example.com#fragment)'),
            '*[*link](http://example.com#fragment)')
        self.assertEqual(
            api.remove_emphasis('[link](http://example.com#fragment*)*'),
            '[link](http://example.com#fragment*)*')
        self.assertEqual(
            api.remove_emphasis('_[_link](http://example.com#fragment)'),
            '_[_link](http://example.com#fragment)')
        self.assertEqual(
            api.remove_emphasis('[link](http://example.com#fragment_)_'),
            '[link](http://example.com#fragment_)_')

        self.assertEqual(
            api.remove_emphasis('*[*link](http://example.com?foo=3#frag)'),
            '*[*link](http://example.com?foo=3#frag)')
        self.assertEqual(
            api.remove_emphasis('[link](http://example.com?foo=3#frag*)*'),
            '[link](http://example.com?foo=3#frag*)*')
        self.assertEqual(
            api.remove_emphasis('_[_link](http://example.com?foo=3#frag)'),
            '_[_link](http://example.com?foo=3#frag)')
        self.assertEqual(
            api.remove_emphasis('[link](http://example.com?foo=3#frag_)_'),
            '[link](http://example.com?foo=3#frag_)_')

        # Example 501 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*](foo\bar)'),
                         r'*[link*](foo\bar)')
        self.assertEqual(api.remove_emphasis(r'[link](*foo\bar)*'),
                         r'[link](*foo\bar)*')
        self.assertEqual(api.remove_emphasis(r'_[link_](foo\bar)'),
                         r'_[link_](foo\bar)')
        self.assertEqual(api.remove_emphasis(r'[link](_foo\bar)_'),
                         r'[link](_foo\bar)_')

        # Example 502 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*](foo%20b&auml;)'),
                         r'*[link*](foo%20b&auml;)')
        self.assertEqual(api.remove_emphasis(r'[link](*foo%20b&auml;)*'),
                         r'[link](*foo%20b&auml;)*')
        self.assertEqual(api.remove_emphasis(r'_[link_](foo%20b&auml;)'),
                         r'_[link_](foo%20b&auml;)')
        self.assertEqual(api.remove_emphasis(r'[link](_foo%20b&auml;)_'),
                         r'[link](_foo%20b&auml;)_')

        # Example 503 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*]("title")'),
                         r'*[link*]("title")')
        self.assertEqual(api.remove_emphasis(r'[link](*"title")*'),
                         r'[link](*"title")*')
        self.assertEqual(api.remove_emphasis(r'_[link_]("title")'),
                         r'_[link_]("title")')
        self.assertEqual(api.remove_emphasis(r'[link](_"title")_'),
                         r'[link](_"title")_')

        # Example 504 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*](/url "title")'),
                         r'*[link*](/url "title")')

        self.assertEqual(api.remove_emphasis(r"*[link*](/url 'title')"),
                         r"*[link*](/url 'title')")

        #        self.assertEqual(api.remove_emphasis(r'*[link*](/url (title))'), r'*[link*](/url (title))')

        # Example 505 [Commonmark 0.30].
        #        self.assertEqual(api.remove_emphasis(r'*[link*](/url "title \"&quot;")'), r'*[link*](/url "title \"&quot;")')

        # Example 506 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*](/url "title")'),
                         r'*[link*](/url "title")')

        # Example 507 [Commonmark 0.30].
        self.assertEqual(
            api.remove_emphasis(r'*[link*](/url "title "and" title")'),
            r'[link](/url "title "and" title")')

        # Example 508 [Commonmark 0.30].
        self.assertEqual(
            api.remove_emphasis("*[link*](/url 'title \"and\" title')"),
            "*[link*](/url 'title \"and\" title')")

        # Example 509 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis('*[link*](   /uri\n  "title"  )'),
                         '*[link*](   /uri\n  "title"  )')

        # Example 510 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*] (uri)'),
                         r'[link] (uri)')
        self.assertEqual(api.remove_emphasis(r'[link] (*uri)*'),
                         r'[link] (uri)')
        #        self.assertEqual(api.remove_emphasis(r'_[link_] (uri)'), r'[link] (uri)')
        self.assertEqual(api.remove_emphasis(r'[link] (_uri)_'),
                         r'[link] (uri)')

        # Example 511 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link* [foo [bar]]](/uri)'),
                         r'*[link* [foo [bar]]](/uri)')

        # Example 512 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link*] (uri)'),
                         r'[link] (uri)')

        # Example 513 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link* *[bar*](/uri)'),
                         r'[link *[bar*](/uri)')

        # Example 514 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[link* *\[bar*](/uri)'),
                         r'*[link* \[bar](/uri)')

        # Example 515 [Commonmark 0.30].
        #      self.assertEqual(api.remove_emphasis(r'[link *foo **bar** `#`*](/uri)'), r'[link foo bar `#`](/uri)')

        # Example 516 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'[![moon](moon.jpg)](/uri)'),
                         r'[![moon](moon.jpg)](/uri)')

        # Example 517 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[foo* [bar](/uri)](/uri)'),
                         r'[foo [bar](/uri)](/uri)')

        # Example 518 [Commonmark 0.30].
        #      self.assertEqual(api.remove_emphasis(r'[foo *[bar [baz](/uri)](/uri)*](/uri)'), r'[foo [bar [baz](/uri)](/uri)](/uri)')

        # Example 519 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'![[[foo](uri1)](uri2)](uri3)'),
                         r'![[[foo](uri1)](uri2)](uri3)')

        # Example 520 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*[foo*](/uri)'),
                         r'*[foo*](/uri)')

        # Example 521 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'[foo *bar](baz*)'),
                         r'[foo *bar](baz*)')

        # Example 522 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'*foo [bar* baz]'),
                         r'foo [bar baz]')

        # Example 523 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'[foo <bar attr="](baz)">'),
                         r'[foo <bar attr="](baz)">')

        # Example 524 [Commonmark 0.30].
        self.assertEqual(api.remove_emphasis(r'[foo`](/uri)`'),
                         r'[foo`](/uri)`')

        # Example 525 [Commonmark 0.30].
        self.assertEqual(
            api.remove_emphasis(r'[foo<http://example.com/?search=](uri)>'),
            r'[foo<http://example.com/?search=](uri)>')

        # Possibly all the way up to 592 [Commonmark 0.30]?

        # Extra examples.
        self.assertEqual(api.remove_emphasis(r'_j\_'),
                         '_j' + LINE_ESCAPE + '_')

    def test_remove_html_tags(self):
        r"""Test remove html tags."""
        # Example 584 [Commonmark 0.28].
        # Example 609 [Commonmark 0.29].
        # Example 612 [Commonmark 0.30].
        # Example 632 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('<a><bab><c2c>', 'github'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('<a><bab><c2c>', 'cmark'),
            '',
        )

        # Example 585 [Commonmark 0.28].
        # Example 610 [Commonmark 0.29].
        # Example 613 [Commonmark 0.30].
        # Example 633 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('<a/><b2/>', 'github'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('<a/><b2/>', 'cmark'),
            '',
        )

        # Example 586 [Commonmark 0.28].
        # Example 611 [Commonmark 0.29].
        # Example 614 [Commonmark 0.30].
        # Example 634 [GFM 0.29.0.gfm.2].
        # Original example with extensions.
        self.assertEqual(
            api.remove_html_tags('<a  /><b2\ndata="foo" >', 'github'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('<a  /><b2\r\ndata="foo" >', 'github'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('<a  /><b2\rdata="foo" >', 'github'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('<a  /><b2\n\rdata="foo" >', 'github'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('<a\t/><b2\ndata="foo" >', 'github'),
            '',
        )
        # Two newlines.
        self.assertEqual(
            api.remove_html_tags('<a\t\t  /><b2\n\ndata="foo" >', 'github'),
            '',
        )

        self.assertEqual(
            api.remove_html_tags('<a  /><b2\ndata="foo" >', 'cmark'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('<a  /><b2\r\ndata="foo" >', 'cmark'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('<a  /><b2\rdata="foo" >', 'cmark'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('<a  /><b2\n\rdata="foo" >', 'cmark'),
            '<b2\n\rdata="foo" >',
        )
        self.assertEqual(
            api.remove_html_tags('<a\t\t  /><b2\ndata="foo" >', 'cmark'),
            '',
        )
        # Two newlines.
        self.assertEqual(
            api.remove_html_tags('<a\t/><b2\n\ndata="foo" >', 'cmark'),
            '<b2\n\ndata="foo" >',
        )

        # Example 587 [Commonmark 0.28].
        # Example 612 [Commonmark 0.29].
        # Example 615 [Commonmark 0.30].
        # Example 635 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags(
                '<a foo="bar" bam = \'baz <em>"</em>\'\n_boolean zoop:33=zoop:33 />',
                'github'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags(
                '<a foo="bar" bam = \'baz <em>"</em>\'\n_boolean zoop:33=zoop:33 />',
                'cmark'),
            '',
        )

        # Example 588 [Commonmark 0.28].
        # Example 613 [Commonmark 0.29].
        # Example 616 [Commonmark 0.30].
        # Example 636 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('Foo <responsive-image src="foo.jpg" />',
                                 'github'),
            'Foo ',
        )
        self.assertEqual(
            api.remove_html_tags('Foo <responsive-image src="foo.jpg" />',
                                 'cmark'),
            'Foo ',
        )

        # Example 589 [Commonmark 0.28].
        # Example 614 [Commonmark 0.29].
        # Example 617 [Commonmark 0.30].
        # Example 637 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('<33> <__>', 'github'),
            '<33> <__>',
        )
        self.assertEqual(
            api.remove_html_tags('<33> <__>', 'cmark'),
            '<33> <__>',
        )

        # Example 590 [Commonmark 0.28].
        # Example 615 [Commonmark 0.29].
        # Example 618 [Commonmark 0.30].
        # Example 638 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('<a h*#ref="hi">', 'github'),
            '<a h*#ref="hi">',
        )
        self.assertEqual(
            api.remove_html_tags('<a h*#ref="hi">', 'cmark'),
            '<a h*#ref="hi">',
        )

        # Example 591 [Commonmark 0.28].
        # Example 616 [Commonmark 0.29].
        # Example 619 [Commonmark 0.30].
        # Example 639 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('<a href="hi\'> <a href=hi\'>', 'github'),
            '<a href="hi\'> <a href=hi\'>',
        )
        self.assertEqual(
            api.remove_html_tags('<a href="hi\'> <a href=hi\'>', 'cmark'),
            '<a href="hi\'> <a href=hi\'>',
        )

        # Example 592 [Commonmark 0.28].
        # Example 617 [Commonmark 0.29].
        # Example 620 [Commonmark 0.30].
        # Example 640 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('< a><\nfoo><bar/ >', 'github'),
            '< a><\nfoo><bar/ >',
        )
        self.assertEqual(
            api.remove_html_tags('< a><\nfoo><bar/ >', 'cmark'),
            '< a><\nfoo><bar/ >',
        )

        # Example 593 [Commonmark 0.28].
        # Example 618 [Commonmark 0.29].
        # Example 621 [Commonmark 0.30].
        # Example 641 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags(r"<a href='bar'title=title>", 'github'),
            r"<a href='bar'title=title>",
        )
        self.assertEqual(
            api.remove_html_tags(r"<a href='bar'title=title>", 'cmark'),
            r"<a href='bar'title=title>",
        )

        # Example 594 [Commonmark 0.28].
        # Example 619 [Commonmark 0.29].
        # Example 622 [Commonmark 0.30].
        # Example 642 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('</a></foo >', 'github'),
            '',
        )
        self.assertEqual(
            api.remove_html_tags('</a></foo >', 'cmark'),
            '',
        )

        # Example 595 [Commonmark 0.28].
        # Example 620 [Commonmark 0.29].
        # Example 623 [Commonmark 0.30].
        # Example 643 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('</a href="foo">', 'github'),
            '</a href="foo">',
        )
        self.assertEqual(
            api.remove_html_tags('</a href="foo">', 'cmark'),
            '</a href="foo">',
        )

        # Example 596 [Commonmark 0.28].
        # Example 621 [Commonmark 0.29].
        # Example 624 [Commonmark 0.30].
        # Example 644 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags(
                'foo <!-- this is a\ncomment - with hyphen -->', 'github'),
            'foo ',
        )
        self.assertEqual(
            api.remove_html_tags(
                'foo <!-- this is a\ncomment - with hyphen -->', 'cmark'),
            'foo ',
        )

        # Example 597 [Commonmark 0.28].
        # Example 622 [Commonmark 0.29].
        # Example 625 [Commonmark 0.30].
        # Example 645 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('foo <!-- not a comment -- two hyphens -->',
                                 'github'),
            'foo <!-- not a comment -- two hyphens -->',
        )
        self.assertEqual(
            api.remove_html_tags('foo <!-- not a comment -- two hyphens -->',
                                 'cmark'),
            'foo <!-- not a comment -- two hyphens -->',
        )

        # Example 598 [Commonmark 0.28].
        # Example 623 [Commonmark 0.29].
        # Example 626 [Commonmark 0.30].
        # Example 646 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('foo <!--> foo -->', 'cmark'),
            'foo <!--> foo -->',
        )
        self.assertEqual(
            api.remove_html_tags('foo <!-- foo--->', 'cmark'),
            'foo <!-- foo--->',
        )
        self.assertEqual(
            api.remove_html_tags('foo <!--> foo -->', 'cmark'),
            'foo <!--> foo -->',
        )
        self.assertEqual(
            api.remove_html_tags('foo <!-- foo--->', 'cmark'),
            'foo <!-- foo--->',
        )

        # Example 599 [Commonmark 0.28].
        # Example 624 [Commonmark 0.29].
        # Example 627 [Commonmark 0.30].
        # Example 647 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('foo <?php echo $a; ?>', 'github'),
            'foo ',
        )
        self.assertEqual(
            api.remove_html_tags('foo <?php echo $a; ?>', 'cmark'),
            'foo ',
        )

        # Example 600 [Commonmark 0.28].
        # Example 625 [Commonmark 0.29].
        # Example 628 [Commonmark 0.30].
        # Example 648 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('foo <!ELEMENT br EMPTY>', 'github'),
            'foo ',
        )
        self.assertEqual(
            api.remove_html_tags('foo <!ELEMENT br EMPTY>', 'cmark'),
            'foo ',
        )

        # Example 601 [Commonmark 0.28].
        # Example 626 [Commonmark 0.29].
        # Example 629 [Commonmark 0.30].
        # Example 649 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('foo <![CDATA[>&<]]>', 'github'),
            'foo ',
        )
        self.assertEqual(
            api.remove_html_tags('foo <![CDATA[>&<]]>', 'cmark'),
            'foo ',
        )

        # Example 602 [Commonmark 0.28].
        # Example 627 [Commonmark 0.29].
        # Example 630 [Commonmark 0.30].
        # Example 650 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('foo <a href="&ouml;">', 'github'),
            'foo ',
        )
        self.assertEqual(
            api.remove_html_tags('foo <a href="&ouml;">', 'cmark'),
            'foo ',
        )

        # Example 603 [Commonmark 0.28].
        # Example 628 [Commonmark 0.29].
        # Example 631 [Commonmark 0.30].
        # Example 651 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags(r'foo <a href="\*">', 'github'),
            'foo ',
        )
        self.assertEqual(
            api.remove_html_tags(r'foo <a href="\*">', 'cmark'),
            'foo ',
        )

        # Example 604 [Commonmark 0.28].
        # Example 629 [Commonmark 0.29].
        # Example 632 [Commonmark 0.30].
        # Example 652 [GFM 0.29.0.gfm.2].
        self.assertEqual(
            api.remove_html_tags('<a href="\"">', 'github'),
            '<a href="\"">',
        )
        self.assertEqual(
            api.remove_html_tags('<a href="\"">', 'cmark'),
            '<a href="\"">',
        )

        # GitHub Flavored Markdown Disallowed Raw HTML (extension).
        # Paragraph 6.11.
        # See https://github.github.com/gfm/#disallowed-raw-html-extension-
        self.assertEqual(api.remove_html_tags('<title>', 'github'), '<title>')
        self.assertEqual(api.remove_html_tags('<textarea>', 'github'),
                         '<textarea>')
        self.assertEqual(api.remove_html_tags('<style>', 'github'), '<style>')
        self.assertEqual(api.remove_html_tags('<xmp>', 'github'), '<xmp>')
        self.assertEqual(api.remove_html_tags('<iframe>', 'github'),
                         '<iframe>')
        self.assertEqual(api.remove_html_tags('<noembed>', 'github'),
                         '<noembed>')
        self.assertEqual(api.remove_html_tags('<noembed>', 'github'),
                         '<noembed>')
        self.assertEqual(api.remove_html_tags('<noframes>', 'github'),
                         '<noframes>')
        self.assertEqual(api.remove_html_tags('<script>', 'github'),
                         '<script>')
        self.assertEqual(api.remove_html_tags('<plaintext>', 'github'),
                         '<plaintext>')

    def test_build_anchor_link(self):
        r"""Test anchor link generation.

        Algorithm testing should be done in calling functions.
        Test duplicates for parser='github'.
        """
        header_duplicate_counter = dict()
        api.build_anchor_link(LINE, header_duplicate_counter, parser='github')
        api.build_anchor_link(LINE, header_duplicate_counter, parser='github')
        [
            self.assertEqual(header_duplicate_counter[k], 2)
            for k in header_duplicate_counter
        ]

        # Check if the exception is raised for newlines.
        header_duplicate_counter = dict()
        with self.assertRaises(exceptions.StringCannotContainNewlines):
            api.build_anchor_link(CMARK_LINE_FOO + LINE_LINE_FEED +
                                  CMARK_LINE_FOO,
                                  header_duplicate_counter,
                                  parser='github')

        # Check the GitLab Flavored Markdown multiple dash rule.
        header_duplicate_counter = dict()
        self.assertEqual(
            api.build_anchor_link(CMARK_LINE_FOO + S3 + CMARK_LINE_FOO,
                                  header_duplicate_counter,
                                  parser='gitlab'),
            CMARK_LINE_FOO + LINE_DASH + CMARK_LINE_FOO)
        header_duplicate_counter = dict()
        self.assertEqual(
            api.build_anchor_link(
                CMARK_LINE_FOO + LINE_DASH * 6 + CMARK_LINE_FOO,
                header_duplicate_counter,
                parser='gitlab'), CMARK_LINE_FOO + LINE_DASH + CMARK_LINE_FOO)
        self.assertEqual(
            api.build_anchor_link(CMARK_LINE_FOO + LINE_DASH * 6,
                                  header_duplicate_counter,
                                  parser='gitlab'), CMARK_LINE_FOO + LINE_DASH)
        self.assertEqual(
            api.build_anchor_link(LINE_DASH * 6 + CMARK_LINE_FOO,
                                  header_duplicate_counter,
                                  parser='gitlab'), LINE_DASH + CMARK_LINE_FOO)

    def test_replace_and_split_newlines(self):
        r"""Test the replacement and splitting of newlines in a string."""
        self.assertEqual(
            api.replace_and_split_newlines(LINE_LINE_FEED + CMARK_LINE_FOO +
                                           LINE_LINE_FEED), [CMARK_LINE_FOO])
        self.assertEqual(
            api.replace_and_split_newlines(LINE_LINE_FEED +
                                           LINE_CARRIAGE_RETURN +
                                           CMARK_LINE_FOO + LINE_LINE_FEED),
            [CMARK_LINE_FOO])
        self.assertEqual(
            api.replace_and_split_newlines(CMARK_LINE_BAR +
                                           LINE_CARRIAGE_RETURN +
                                           LINE_LINE_FEED + CMARK_LINE_FOO +
                                           LINE_LINE_FEED),
            [CMARK_LINE_BAR, CMARK_LINE_FOO])
        self.assertEqual(
            api.replace_and_split_newlines(LINE_CARRIAGE_RETURN +
                                           LINE_LINE_FEED + LINE_LINE_FEED +
                                           LINE_LINE_FEED + CMARK_LINE_BAR),
            [CMARK_LINE_BAR])
        self.assertEqual(
            api.replace_and_split_newlines(LINE_LINE_FEED + LINE_LINE_FEED +
                                           LINE_LINE_FEED + CMARK_LINE_BAR),
            [CMARK_LINE_BAR])
        self.assertEqual(
            api.replace_and_split_newlines(LINE_LINE_FEED + CMARK_LINE_FOO +
                                           LINE_LINE_FEED + LINE_LINE_FEED +
                                           LINE_CARRIAGE_RETURN +
                                           LINE_LINE_FEED + CMARK_LINE_BAR),
            [CMARK_LINE_FOO, '', '', CMARK_LINE_BAR])

    def test_get_atx_heading(self):
        r"""Test the title gathering for edge cases and various parsers.

        GitHub examples are the same ones reported in the GFM document, except
        for minor changes. The example numbers are the same ones reported in
        the cited document. There are also some more tests for special
        cases.

        Redcarpet examples are different from the ones present
        in the test directory of the source code.
        """
        # github
        m_github = md_parser['github']['header']['max levels'] = 6

        # Example 32 [Commonmark 0.28].
        # Example 32 [Commonmark 0.29].
        # Example 62 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H1 + T1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H1 + T1 + CMARK_LINE_FOO, m_github, 'cmark'),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(H2 + S1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': 2,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H2 + T1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H2 + T1 + CMARK_LINE_FOO, m_github, 'cmark'),
            [{
                'header type': 2,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(H3 + S1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': 3,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H3 + T1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H3 + T1 + CMARK_LINE_FOO, m_github, 'cmark'),
            [{
                'header type': 3,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(H4 + S1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': 4,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H4 + T1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H4 + T1 + CMARK_LINE_FOO, m_github, 'cmark'),
            [{
                'header type': 4,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(H5 + S1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': 5,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H5 + T1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H5 + T1 + CMARK_LINE_FOO, m_github, 'cmark'),
            [{
                'header type': 5,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(H6 + S1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': 6,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H6 + T1 + CMARK_LINE_FOO, m_github, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H6 + T1 + CMARK_LINE_FOO, m_github, 'cmark'),
            [{
                'header type': 6,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        # Example 33 [Commonmark 0.28].
        # Example 33 [Commonmark 0.29].
        # Example 63 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(H7 + S1 + CMARK_LINE_FOO, 7, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Example 34 [Commonmark 0.28].
        # Example 34 [Commonmark 0.29].
        # Example 64 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                H1 + CMARK_LINE_5_BOLT + LINE_LINE_FEED + LINE_LINE_FEED + H1 +
                CMARK_LINE_HASHTAG, m_github, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }, {
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }, {
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Example 35 [Commonmark 0.28].
        # Example 35 [Commonmark 0.29].
        self.assertEqual(
            api.get_atx_heading(
                LINE_ESCAPE + H1 + S1 + CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Example 65 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                LINE_ESCAPE + H2 + S1 + CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Example 66 [Commonmark 0.30].
        # Note: emphasis is trated separately.
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + S1 + '*' + CMARK_LINE_BAR + '*' +
                S1 + LINE_ESCAPE + '*' + CMARK_LINE_BAZ + LINE_ESCAPE + '*',
                m_github,
                'github',
            ),
            [{
                'header type':
                1,
                'header text trimmed':
                CMARK_LINE_FOO + S1 + '*' + CMARK_LINE_BAR + '*' + S1 +
                LINE_ESCAPE + '*' + CMARK_LINE_BAZ + LINE_ESCAPE + '*',
                'visible':
                True
            }],
        )

        # Example 36 [Commonmark 0.28].
        # Example 36 [Commonmark 0.29].
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + S1 + CMARK_LINE_BAR_BAZ,
                3,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed':
                CMARK_LINE_FOO + S1 + CMARK_LINE_BAR_BAZ,
                'visible': True
            }],
        )

        # Example 37 [Commonmark 0.28].
        # Example 37 [Commonmark 0.29].
        # Example 67 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                H1 + S18 + CMARK_LINE_FOO + S21,
                m_github,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + T18 + CMARK_LINE_FOO + T21,
                m_github,
                'github',
            ),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + T18 + CMARK_LINE_FOO + T21,
                m_github,
                'cmark',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        # Example 38 [Commonmark 0.28].
        # Example 38 [Commonmark 0.29].
        # Example 68 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                S1 + H3 + S1 + CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type': 3,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                S2 + H2 + S1 + CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type': 2,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                S3 + H1 + S1 + CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        # Example 39 [Commonmark 0.28].
        # Example 39 [Commonmark 0.29].
        # Example 69 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                S4 + H1 + S1 + CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Example 40 [Commonmark 0.28].
        # Example 40 [Commonmark 0.29].
        # Example 70 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                CMARK_LINE_FOO + LINE_LINE_FEED + S4 + H1 + S1 +
                CMARK_LINE_BAR,
                m_github,
                'github',
            ),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }, {
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Example 41 [Commonmark 0.28].
        # Example 41 [Commonmark 0.29].
        # Example 71 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                H2 + S1 + CMARK_LINE_FOO + S1 + H2,
                m_github,
                'github',
            ),
            [{
                'header type': 2,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                S2 + H3 + S3 + CMARK_LINE_BAR + S4 + H3,
                m_github,
                'github',
            ),
            [{
                'header type': 3,
                'header text trimmed': CMARK_LINE_BAR,
                'visible': True
            }],
        )

        # Example 42 [Commonmark 0.28].
        # Example 42 [Commonmark 0.29].
        # Example 72 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + S1 + H34,
                m_github,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H5 + S1 + CMARK_LINE_FOO + S1 + H2,
                m_github,
                'github',
            ),
            [{
                'header type': 5,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        # Extra test.
        self.assertEqual(
            api.get_atx_heading(H5 * 7, m_github, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Example 43 [Commonmark 0.28].
        # Example 43 [Commonmark 0.29].
        # Example 73 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + CMARK_LINE_FOO + S1 + H3 + S5,
                m_github,
                'github',
            ),
            [{
                'header type': 3,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + CMARK_LINE_FOO + S1 + H3 + T5,
                m_github,
                'github',
            ),
            [{
                'header type': 3,
                'header text trimmed': CMARK_LINE_FOO + S1 + H3 + T5,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + CMARK_LINE_FOO + S1 + H3 + T5,
                m_github,
                'cmark',
            ),
            [{
                'header type': 3,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        # Example 44 [Commonmark 0.28].
        # Example 44 [Commonmark 0.29].
        # Example 74 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + CMARK_LINE_FOO + S1 + H3 + S1 + CMARK_LINE_B,
                m_github,
                'github',
            ),
            [{
                'header type': 3,
                'header text trimmed':
                CMARK_LINE_FOO + S1 + H3 + S1 + CMARK_LINE_B,
                'visible': True
            }],
        )

        # Example 45 [Commonmark 0.28].
        # Example 45 [Commonmark 0.29].
        # Example 75 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + H1,
                m_github,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO + H1,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + S1 + H1,
                m_github,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + T1 + H1,
                m_github,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO + T1 + H1,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + T1 + H1,
                m_github,
                'cmark',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }],
        )

        # Example 46 [Commonmark 0.28].
        # Example 46 [Commonmark 0.29].
        # Example 76 [Commonmark 0.30].
        # Preserve the backslashes unlike the original example so that they
        # conform to the original ATX header. The backslash is infact removed
        # from the markdown parser used by GitHub, GitLab, etc...
        #
        # See
        # https://github.com/github/cmark-gfm/blob/6b101e33ba1637e294076c46c69cd6a262c7539f/src/inlines.c#L756
        # and
        # https://spec.commonmark.org/0.28/#ascii-punctuation-character
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + CMARK_LINE_FOO + S1 + LINE_ESCAPE + H3,
                m_github,
                'github',
            ),
            [{
                'header type': 3,
                'header text trimmed': CMARK_LINE_FOO + S1 + LINE_ESCAPE + H3,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H2 + S1 + CMARK_LINE_FOO + S1 + H1 + LINE_ESCAPE + H2,
                m_github,
                'github',
            ),
            [{
                'header type': 2,
                'header text trimmed':
                CMARK_LINE_FOO + S1 + H1 + LINE_ESCAPE + H2,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + S1 + LINE_ESCAPE + H1,
                m_github,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO + S1 + LINE_ESCAPE + H1,
                'visible': True
            }],
        )

        # Example 47 [Commonmark 0.28].
        # Example 47 [Commonmark 0.29].
        # Example 77 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                '****' + LINE_LINE_FEED + H2 + S1 + CMARK_LINE_FOO +
                LINE_LINE_FEED + '****',
                m_github,
                'github',
            ),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }, {
                'header type': 2,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }, {
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Example 48 [Commonmark 0.28].
        # Example 48 [Commonmark 0.29].
        # Example 78 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(
                'Foo' + S1 + CMARK_LINE_BAR + LINE_LINE_FEED + H1 + S1 +
                CMARK_LINE_BAZ + LINE_LINE_FEED + 'Bar' + S1 + CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }, {
                'header type': 1,
                'header text trimmed': CMARK_LINE_BAZ,
                'visible': True
            }, {
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Example 49 [Commonmark 0.28].
        # Example 49 [Commonmark 0.29].
        # Example 79 [Commonmark 0.30].
        self.assertEqual(
            api.get_atx_heading(H2 + S1, m_github, 'github', True),
            [{
                'header type': 2,
                'header text trimmed': LINE_EMPTY,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H1, m_github, 'github', True),
            [{
                'header type': 1,
                'header text trimmed': LINE_EMPTY,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + H3, m_github, 'github', True),
            [{
                'header type': 3,
                'header text trimmed': LINE_EMPTY,
                'visible': True
            }],
        )

        # Example 49 with link labels: link lables cannot be empty
        # Example 49 [Commonmark 0.28].
        # Example 49 [Commonmark 0.29].
        # Example 79 [Commonmark 0.30].
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H2 + S1, m_github, 'github', False)
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H1, m_github, 'github', False)
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H3 + S1 + H3, m_github, 'github', False)

        # Test escaping examples reported in the documentation.
        # A modified Example 302 and Example 496 (for square brackets).
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + LINE_SQUARE_BRACKET_OPEN + S1 + CMARK_LINE_FOO + S1 +
                LINE_SQUARE_BRACKET_OPEN + CMARK_LINE_BAR +
                LINE_SQUARE_BRACKET_CLOSE + LINE_SQUARE_BRACKET_CLOSE,
                m_github,
                'github',
            ),
            [{
                'header type':
                1,
                'header text trimmed':
                LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN + S1 + CMARK_LINE_FOO +
                S1 + LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN + CMARK_LINE_BAR +
                LINE_ESCAPE + LINE_SQUARE_BRACKET_CLOSE + LINE_ESCAPE +
                LINE_SQUARE_BRACKET_CLOSE,
                'visible':
                True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + LINE_ESCAPE + LINE_ESCAPE +
                LINE_SQUARE_BRACKET_OPEN + S1 + CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type':
                1,
                'header text trimmed':
                LINE_ESCAPE + LINE_ESCAPE + LINE_ESCAPE +
                LINE_SQUARE_BRACKET_OPEN + S1 + CMARK_LINE_FOO,
                'visible':
                True
            }],
        )

        # Test escape character space workaround.
        self.assertEqual(
            api.get_atx_heading(
                H2 + S1 + CMARK_LINE_FOO + LINE_ESCAPE,
                m_github,
                'github',
            ),
            [{
                'header type': 2,
                'header text trimmed': CMARK_LINE_FOO + LINE_ESCAPE + S1,
                'visible': True
            }],
        )

        # Test MD_PARSER_CMARK_MAX_CHARS_LINK_LABEL
        with self.assertRaises(exceptions.GithubOverflowCharsLinkLabel):
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_1000_CHARS,
                m_github,
                'github',
            )

        # Test an empty line.
        self.assertEqual(
            api.get_atx_heading(LINE_EMPTY, m_github, 'github'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Test multiple lines at once.
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + LINE_LINE_FEED + LINE_LINE_FEED +
                H1 + S1 + CMARK_LINE_FOO + LINE_LINE_FEED,
                m_github,
                'github',
            ),
            [
                {
                    'header type': 1,
                    'header text trimmed': CMARK_LINE_FOO,
                    'visible': True
                },
                {
                    'header type': None,
                    'header text trimmed': None,
                    'visible': False
                },
                {
                    'header type': 1,
                    'header text trimmed': CMARK_LINE_FOO,
                    'visible': True
                },
            ],
        )

        # Test line endings.
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_LINE_FEED, m_github, 'github', True),
            [{
                'header type': 1,
                'header text trimmed': LINE_EMPTY,
                'visible': True
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + LINE_CARRIAGE_RETURN,
                m_github,
                'github',
                True,
            ),
            [{
                'header type': 1,
                'header text trimmed': LINE_EMPTY,
                'visible': True
            }],
        )

        # CRLF marker tests.
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + LINE_LINE_FEED + CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }, {
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + CMARK_LINE_FOO + LINE_CARRIAGE_RETURN +
                CMARK_LINE_FOO,
                m_github,
                'github',
            ),
            [{
                'header type': 1,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': True
            }, {
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Test line endings with link labels.
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H1 + LINE_LINE_FEED, m_github, 'github', False)
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(
                H1 + LINE_CARRIAGE_RETURN,
                m_github,
                'github',
                False,
            )

        # Test valid lines with header levels > keep_header_levels
        # (and header levels < max_header_levels since they are all valid
        # headers)
        self.assertEqual(
            api.get_atx_heading(
                H2 + S1 + CMARK_LINE_FOO,
                1,
                'github',
            ),
            [{
                'header type': 2,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + CMARK_LINE_FOO,
                1,
                'github',
            ),
            [{
                'header type': 3,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H5 + S1 + CMARK_LINE_FOO,
                2,
                'github',
            ),
            [{
                'header type': 5,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H6 + S1 + CMARK_LINE_FOO,
                5,
                'github',
            ),
            [{
                'header type': 6,
                'header text trimmed': CMARK_LINE_FOO,
                'visible': False
            }],
        )

        # readcarpet
        # It does not seem that there are exaustive tests so we have to invent
        # our own. See https://github.com/vmg/redcarpet/tree/master/test
        # for more information.
        m_redcarpet = md_parser['redcarpet']['header']['max levels'] = 6

        self.assertEqual(
            api.get_atx_heading(
                S1 + H1 + S1 + REDCARPET_LINE_FOO,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': 1,
                'header text trimmed': REDCARPET_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + S1 + H1,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': 1,
                'header text trimmed': REDCARPET_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + S1 + H3,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': 1,
                'header text trimmed': REDCARPET_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + REDCARPET_LINE_FOO + S1 + H3 + LINE_LINE_FEED,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': 3,
                'header text trimmed': REDCARPET_LINE_FOO,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + S1 + H3 + S1,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': 1,
                'header text trimmed': REDCARPET_LINE_FOO + S1 + H3,
                'visible': True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + S1 + H1 + LINE_ESCAPE +
                LINE_ESCAPE + H2,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type':
                1,
                'header text trimmed':
                REDCARPET_LINE_FOO + S1 + H1 + LINE_ESCAPE + LINE_ESCAPE,
                'visible':
                True
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + H1 + LINE_ESCAPE + H1 + S1 + H1,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': 1,
                'header text trimmed':
                REDCARPET_LINE_FOO + H1 + LINE_ESCAPE + H1,
                'visible': True
            }],
        )

        # Test escape character space workaround.
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + S1 + LINE_ESCAPE,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': 1,
                'header text trimmed':
                REDCARPET_LINE_FOO + S1 + LINE_ESCAPE + S1,
                'visible': True
            }],
        )

        # Test an empty line.
        self.assertEqual(
            api.get_atx_heading(LINE_EMPTY, m_redcarpet, 'redcarpet'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        # Test newline.
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_LINE_FEED, m_redcarpet, 'redcarpet'),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + LINE_LINE_FEED +
                REDCARPET_LINE_FOO,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': 1,
                'header text trimmed': REDCARPET_LINE_FOO,
                'visible': True
            }, {
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + LINE_CARRIAGE_RETURN,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + LINE_CARRIAGE_RETURN +
                REDCARPET_LINE_FOO,
                m_redcarpet,
                'redcarpet',
            ),
            [{
                'header type': 1,
                'header text trimmed': REDCARPET_LINE_FOO,
                'visible': True
            }, {
                'header type': None,
                'header text trimmed': None,
                'visible': False
            }],
        )

    def test_get_md_header(self):
        r"""Test building of the header data structure."""
        # Mock the get_atx_heading, build_anchor_link function calls.
        # result = [{None None False}]:
        # First if.
        with patch('md_toc.api.get_atx_heading',
                   return_value=[{
                       'header type': None,
                       'header text trimmed': None,
                       'visible': False
                   }]):
            with patch('md_toc.api.build_anchor_link', return_value=''):
                self.assertEqual(api.get_md_header(CMARK_LINE_FOO, dict(), 1),
                                 [None])

        # Cannot happen.
        # result = [{None None True}]
        # First if.
        with patch('md_toc.api.get_atx_heading',
                   return_value=[{
                       'header type': None,
                       'header text trimmed': None,
                       'visible': True
                   }]):
            with patch('md_toc.api.build_anchor_link', return_value=''):
                self.assertEqual(api.get_md_header(CMARK_LINE_FOO, dict(), 1),
                                 [None])

        # result = [{alpha beta False}]
        # Second if.
        with patch('md_toc.api.get_atx_heading',
                   return_value=[{
                       'header type': 2,
                       'header text trimmed': CMARK_LINE_FOO,
                       'visible': False
                   }]):
            with patch('md_toc.api.build_anchor_link',
                       return_value=CMARK_LINE_FOO):
                self.assertEqual(
                    api.get_md_header(H2 + S1 + CMARK_LINE_FOO, dict(), 1),
                    [{
                        'type': 2,
                        'text_original': CMARK_LINE_FOO,
                        'text_anchor_link': CMARK_LINE_FOO,
                        'visible': False
                    }])

        # result = [{alpha beta True}]
        # Second if.
        with patch('md_toc.api.get_atx_heading',
                   return_value=[{
                       'header type': 1,
                       'header text trimmed': CMARK_LINE_FOO,
                       'visible': True
                   }]):
            with patch('md_toc.api.build_anchor_link',
                       return_value=CMARK_LINE_FOO):
                self.assertEqual(
                    api.get_md_header(H1 + S1 + CMARK_LINE_FOO, dict(), 1),
                    [{
                        'type': 1,
                        'text_original': CMARK_LINE_FOO,
                        'text_anchor_link': CMARK_LINE_FOO,
                        'visible': True
                    }])

    def test_is_opening_code_fence(self):
        r"""Test detection of opening code fence."""
        # github.
        # Generic, spaces and headings. These are not code fences.
        self.assertIsNone(api.is_opening_code_fence(LINE))
        self.assertIsNone(api.is_opening_code_fence(LINE_EMPTY))
        self.assertIsNone(api.is_opening_code_fence(CMARK_LINE_FOO))
        self.assertIsNone(
            api.is_opening_code_fence(CMARK_LINE_FOO + LINE_LINE_FEED), )

        self.assertIsNone(api.is_opening_code_fence(S1))
        self.assertIsNone(api.is_opening_code_fence(S2))
        self.assertIsNone(api.is_opening_code_fence(S3))
        self.assertIsNone(api.is_opening_code_fence(S4))
        self.assertIsNone(api.is_opening_code_fence(S10))

        self.assertIsNone(api.is_opening_code_fence(H1))
        self.assertIsNone(api.is_opening_code_fence(H2))
        # Example 122->128 [Commonmark 0.30].
        self.assertIsNone(api.is_opening_code_fence(H3))
        self.assertIsNone(api.is_opening_code_fence(H4))
        self.assertIsNone(api.is_opening_code_fence(H5))
        self.assertIsNone(api.is_opening_code_fence(H6))
        self.assertIsNone(api.is_opening_code_fence(H7))

        # Example 88 [Commonmark 0.28].
        # Example 89 [Commonmark 0.29].
        # Example 119 [Commonmark 0.30].
        # Base case: no info string.
        self.assertEqual(api.is_opening_code_fence(BACKTICK3), BACKTICK3)
        self.assertEqual(api.is_opening_code_fence(BACKTICK4), BACKTICK4)
        self.assertEqual(api.is_opening_code_fence(BACKTICK10), BACKTICK10)

        # Example 89 [Commonmark 0.28].
        # Example 90 [Commonmark 0.29].
        # Example 120 [Commonmark 0.30].
        self.assertEqual(api.is_opening_code_fence(TILDE3), TILDE3)
        self.assertEqual(api.is_opening_code_fence(TILDE4), TILDE4)
        self.assertEqual(api.is_opening_code_fence(TILDE10), TILDE10)

        # Example 90 [Commonmark 0.28].
        # Example 91 [Commonmark 0.29].
        # Example 121 [Commonmark 0.30].
        # Backticks and tildes.
        self.assertIsNone(api.is_opening_code_fence(BACKTICK1))
        self.assertIsNone(api.is_opening_code_fence(BACKTICK2))
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK2 + CMARK_LINE_FOO), )
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK2 + LINE_LINE_FEED +
                                      BACKTICK1), )

        self.assertIsNone(api.is_opening_code_fence(TILDE1))
        self.assertIsNone(api.is_opening_code_fence(TILDE2))
        self.assertIsNone(api.is_opening_code_fence(TILDE2 + CMARK_LINE_FOO))
        self.assertIsNone(
            api.is_opening_code_fence(TILDE2 + LINE_LINE_FEED + TILDE1), )

        # Example 91 -> 97 [Commonmark 0.28].
        # Example 92 -> 98 [Commonmark 0.29].
        # Example 122 -> 128 [Commonmark 0.30].
        # See test_is_closing_code_fence.

        # Example 98 [Commonmark 0.28].
        # Example 99 [Commonmark 0.29].
        # Example 129 [Commonmark 0.30].
        self.assertEqual(
            api.is_opening_code_fence(
                BACKTICK3 + LINE_LINE_FEED + LINE_LINE_FEED + S2, ),
            BACKTICK3,
        )

        self.assertEqual(
            api.is_opening_code_fence(
                TILDE3 + LINE_LINE_FEED + LINE_LINE_FEED + S2, ),
            TILDE3,
        )

        # Example 99 [Commonmark 0.28].
        # Example 100 [Commonmark 0.29].
        # Example 130 [Commonmark 0.30].
        # See example 88 [Commonmark 0.28].

        # Indentation.
        # Example 100 [Commonmark 0.28].
        # Example 101 [Commonmark 0.29].
        # Example 131 [Commonmark 0.30].
        self.assertEqual(api.is_opening_code_fence(S1 + BACKTICK3), BACKTICK3)

        self.assertEqual(api.is_opening_code_fence(S1 + TILDE3), TILDE3)

        # Example 101 [Commonmark 0.28].
        # Example 102 [Commonmark 0.29].
        # Example 132 [Commonmark 0.30].
        self.assertEqual(api.is_opening_code_fence(S2 + BACKTICK3), BACKTICK3)

        self.assertEqual(api.is_opening_code_fence(S2 + TILDE3), TILDE3)

        # Example 102 [Commonmark 0.28].
        # Example 103 [Commonmark 0.29].
        # Example 133 [Commonmark 0.30].
        self.assertEqual(api.is_opening_code_fence(S3 + BACKTICK3), BACKTICK3)

        self.assertEqual(api.is_opening_code_fence(S3 + TILDE3), TILDE3)

        # Example 103 [Commonmark 0.28].
        # Example 104 [Commonmark 0.29].
        # Example 134 [Commonmark 0.30].
        self.assertIsNone(api.is_opening_code_fence(S4 + BACKTICK3))

        self.assertIsNone(api.is_opening_code_fence(S4 + TILDE3))

        # An extension of examples 100 -> 103 [Commonmark 0.28].
        #                          101 -> 104 [Commonmark 0.29].
        self.assertEqual(api.is_opening_code_fence(S3 + BACKTICK3), BACKTICK3)
        self.assertEqual(api.is_opening_code_fence(S3 + BACKTICK4), BACKTICK4)
        self.assertEqual(
            api.is_opening_code_fence(S3 + BACKTICK10),
            BACKTICK10,
        )

        self.assertEqual(api.is_opening_code_fence(S3 + TILDE3), TILDE3)
        self.assertEqual(api.is_opening_code_fence(S3 + TILDE4), TILDE4)
        self.assertEqual(api.is_opening_code_fence(S3 + TILDE10), TILDE10)

        # Example 104 -> 106 [Commonmark 0.28].
        # Example 105 -> 107 [Commonmark 0.29].
        # Example 135 -> 137 [Commonmark 0.30].
        # See test_is_closing_code_fence.

        # Example 107 [Commonmark 0.28].
        # Example 108 [Commonmark 0.29].
        # Example 138 [Commonmark 0.30].
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK3 + S1 + BACKTICK3), )

        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + S1 + TILDE3),
            TILDE3,
        )

        # Example 108 [Commonmark 0.28].
        # Example 109 [Commonmark 0.29].
        # Example 139 [Commonmark 0.30].
        # See test_is_closing_code_fence.

        # Example 109 -> 110 [Commonmark 0.28].
        # Example 110 -> 111 [Commonmark 0.29].
        # Example 140 -> 141 [Commonmark 0.30].
        # Not relevant.

        # Example 24 [Commonmark 0.30].
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + S1 + CMARK_LINE_FOO +
                                      LINE_ESCAPE + CMARK_LINE_BAR),
            BACKTICK3,
        )

        # Example 111 [Commonmark 0.28].
        # Example 112 [Commonmark 0.29].
        # Example 142 [Commonmark 0.30].
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + CMARK_INFO_STRING_FOO),
            BACKTICK3,
        )

        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + CMARK_INFO_STRING_FOO),
            TILDE3,
        )

        # Expansion of
        # example 111 [Commonmark 0.28].
        # example 112 [Commonmark 0.29].
        # example 142 [Commonmark 0.30].
        # Info string.
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + CMARK_INFO_STRING_FOO),
            BACKTICK3,
        )
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK4 + CMARK_INFO_STRING_FOO),
            BACKTICK4,
        )
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK10 + CMARK_INFO_STRING_FOO),
            BACKTICK10,
        )
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + S3 + CMARK_INFO_STRING_FOO),
            BACKTICK3,
        )
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + S3 + CMARK_INFO_STRING_FOO,
                                      'cmark'),
            BACKTICK3,
        )
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + T3 + CMARK_INFO_STRING_FOO),
            BACKTICK3,
        )
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + T3 + CMARK_INFO_STRING_FOO,
                                      'cmark'),
            BACKTICK3,
        )

        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + CMARK_INFO_STRING_FOO),
            TILDE3,
        )
        self.assertEqual(
            api.is_opening_code_fence(TILDE4 + CMARK_INFO_STRING_FOO),
            TILDE4,
        )
        self.assertEqual(
            api.is_opening_code_fence(TILDE10 + CMARK_INFO_STRING_FOO),
            TILDE10,
        )
        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + S3 + CMARK_INFO_STRING_FOO),
            TILDE3,
        )
        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + S3 + CMARK_INFO_STRING_FOO,
                                      'cmark'),
            TILDE3,
        )
        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + T3 + CMARK_INFO_STRING_FOO),
            TILDE3,
        )
        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + T3 + CMARK_INFO_STRING_FOO,
                                      'cmark'),
            TILDE3,
        )

        # Example 112 [Commonmark 0.28].
        # Example 113 [Commonmark 0.29].
        # Example 143 [Commonmark 0.30].
        # Info string with garbage and foreign character.
        self.assertEqual(
            api.is_opening_code_fence(
                BACKTICK4 + S4 + CMARK_INFO_STRING_FOO + S1 +
                CMARK_INFO_STRING_GARBAGE, ),
            BACKTICK4,
        )

        self.assertEqual(
            api.is_opening_code_fence(
                TILDE4 + S4 + CMARK_INFO_STRING_FOO + S1 +
                CMARK_INFO_STRING_GARBAGE, ),
            TILDE4,
        )

        # Example 113 [Commonmark 0.28].
        # Example 114 [Commonmark 0.29].
        # Example 144 [Commonmark 0.30].
        self.assertEqual(api.is_opening_code_fence(BACKTICK4 + ';'), BACKTICK4)

        self.assertEqual(api.is_opening_code_fence(TILDE4 + ';'), TILDE4)

        # Example 114 [Commonmark 0.28].
        # Example 115 [Commonmark 0.29].
        # Example 145 [Commonmark 0.30].
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK3 + S1 + 'aa' + S1 +
                                      BACKTICK3), )

        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + S1 + 'aa' + S1 + TILDE3),
            TILDE3,
        )

        # Example 116 [Commonmark 0.29].
        # Example 146 [Commonmark 0.30].
        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + S1 + 'aa' + S1 + BACKTICK3 +
                                      S1 + TILDE3),
            TILDE3,
        )

        # Extension of Example 146 [Commonmark 0.30].
        # Info strings for backtick code blocks CANNOT contain tildes and backtics.
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK3 + S1 + 'aa' + S1 + TILDE3 +
                                      S1 + BACKTICK3), )

        # Example 115 [Commonmark 0.28].
        # Example 117 [Commonmark 0.29].
        # Example 147 [Commonmark 0.30].
        # See test_is_closing_code_fence.

    def test_is_closing_code_fence(self):
        r"""Test detection of closing code fence."""
        # github.
        # Example 91 [Commonmark 0.28].
        # Example 92 [Commonmark 0.29].
        # Example 122 [Commonmark 0.30].
        self.assertFalse(api.is_closing_code_fence(BACKTICK3, TILDE3))

        # Example 92 [Commonmark 0.28].
        # Example 93 [Commonmark 0.29].
        # Example 123 [Commonmark 0.30].
        self.assertFalse(api.is_closing_code_fence(TILDE3, BACKTICK3))

        # Example 93 [Commonmark 0.28].
        # Example 94 [Commonmark 0.29].
        # Example 124 [Commonmark 0.30].
        self.assertFalse(api.is_closing_code_fence(BACKTICK3, BACKTICK4))

        # Example 94 [Commonmark 0.28].
        # Example 95 [Commonmark 0.29].
        # Example 125 [Commonmark 0.30].
        self.assertFalse(api.is_closing_code_fence(TILDE3, TILDE4))

        # Example 95 [Commonmark 0.28].
        # Example 96 [Commonmark 0.29].
        # Example 126 [Commonmark 0.30].
        self.assertTrue(api.is_closing_code_fence(LINE_EMPTY, BACKTICK3, True))

        self.assertTrue(api.is_closing_code_fence(LINE_EMPTY, TILDE3, True))

        # Example 96 [Commonmark 0.28].
        # Example 97 [Commonmark 0.29].
        # Example 127 [Commonmark 0.30].
        # End of document.
        self.assertTrue(
            api.is_closing_code_fence(
                LINE_LINE_FEED + BACKTICK3 + LINE_LINE_FEED + 'aaa',
                BACKTICK5,
                True,
            ), )

        self.assertTrue(
            api.is_closing_code_fence(
                LINE_LINE_FEED + TILDE3 + LINE_LINE_FEED + 'aaa',
                TILDE5,
                True,
            ), )

        # Example 97 [Commonmark 0.28].
        # Example 98 [Commonmark 0.29].
        # Example 128 [Commonmark 0.30].
        # Not relevant because we don't have to find headings inside blockquotes.

        # Example 129 -> 134 [Commonmark 0.30].
        # See test_is_opening_code_fence.

        # Example 104 [Commonmark 0.28].
        # Example 105 [Commonmark 0.29].
        # Example 135 [Commonmark 0.30].
        self.assertTrue(api.is_closing_code_fence(S2 + BACKTICK3, BACKTICK3))

        self.assertTrue(api.is_closing_code_fence(S2 + TILDE3, TILDE3))

        # Example 105 [Commonmark 0.28].
        # Example 106 [Commonmark 0.29].
        # Example 136 [Commonmark 0.30].
        self.assertTrue(
            api.is_closing_code_fence(S2 + BACKTICK3, S3 + BACKTICK3), )

        self.assertTrue(api.is_closing_code_fence(S2 + TILDE3, S3 + TILDE3))

        # Example 106 [Commonmark 0.28].
        # Example 107 [Commonmark 0.29].
        # Example 137 [Commonmark 0.30].
        self.assertFalse(api.is_closing_code_fence(S4 + BACKTICK3, BACKTICK3))

        self.assertFalse(api.is_closing_code_fence(S4 + TILDE3, TILDE3))

        # Example 138 [Commonmark 0.30].
        self.assertTrue(api.is_closing_code_fence(S1 + BACKTICK3, BACKTICK3))

        # Example 108 [Commonmark 0.28].
        # Example 109 [Commonmark 0.29].
        # Example 139 [Commonmark 0.30].
        self.assertFalse(
            api.is_closing_code_fence(TILDE3 + S1 + TILDE2, TILDE6), )

        self.assertFalse(
            api.is_closing_code_fence(BACKTICK3 + S1 + BACKTICK2, BACKTICK6), )

        # Example 140 -> 146 [Commonmark 0.30].
        # See test_is_opening_code_fence.

        # Example 115 [Commonmark 0.28].
        # Example 117 [Commonmark 0.29].
        # Example 147 [Commonmark 0.30].
        self.assertFalse(
            api.is_closing_code_fence(BACKTICK3 + S1 + 'aaa', BACKTICK3), )

        self.assertFalse(
            api.is_closing_code_fence(TILDE3 + S1 + 'aaa', TILDE3), )

        # Extra examples for tabs [Commonmark 0.30].
        self.assertTrue(
            api.is_closing_code_fence(BACKTICK3 + T1, BACKTICK3, 'cmark'), )
        self.assertFalse(api.is_closing_code_fence(BACKTICK3 + T1,
                                                   BACKTICK3), )
        self.assertTrue(
            api.is_closing_code_fence(BACKTICK3 + T4 + S4, BACKTICK3,
                                      'cmark'), )
        self.assertFalse(
            api.is_closing_code_fence(BACKTICK3 + T4 + S4, BACKTICK3), )

        self.assertTrue(
            api.is_closing_code_fence(TILDE3 + T1, TILDE3, 'cmark'), )
        self.assertFalse(api.is_closing_code_fence(TILDE3 + T4 + S4, TILDE3), )
        self.assertTrue(
            api.is_closing_code_fence(TILDE3 + T1, TILDE3, 'cmark'), )
        self.assertFalse(api.is_closing_code_fence(TILDE3 + T4 + S4, TILDE3), )


if __name__ == '__main__':
    unittest.main()
