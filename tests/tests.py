#
# tests.py
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
"""The tests module."""

from md_toc import api, exceptions
import unittest

# Some static generic variables.

# Lines.
LINE = 'This is a static line'
LINE_EMPTY = ''
LINE_ESCAPE = '\\'
LINE_NEWLINE = '\n'
LINE_CARRIAGE_RETURN = '\r'
LINE_SQUARE_BRACKET_OPEN = '['
LINE_SQUARE_BRACKET_CLOSE = ']'

# Spaces.
S1 = 1 * ' '
S2 = 2 * ' '
S3 = 3 * ' '
S4 = 4 * ' '
S10 = 10 * ' '

# ATX headers.
H1 = 1 * '#'
H2 = 2 * '#'
H3 = 3 * '#'
H4 = 4 * '#'
H5 = 5 * '#'
H6 = 6 * '#'
H7 = 7 * '#'

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

# list marker log.
GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX = 1000

# github test lines.
GITHUB_LINE_FOO = 'foo'
GITHUB_LINE_BAR = 'bar'
GITHUB_LINE_5_BOLT = '5 bolt'
GITHUB_LINE_HASHTAG = 'hashtag'
GITHUB_LINE_BAR_BAZ = '*bar* \*baz\*'
GITHUB_LINE_B = 'b'
GITHUB_LINE_1000_CHARS = 1000 * 'c'

BACKTICK1 = 1 * '`'
BACKTICK2 = 2 * '`'
BACKTICK3 = 3 * '`'
BACKTICK4 = 4 * '`'
BACKTICK10 = 10 * '`'

TILDE1 = 1 * '~'
TILDE2 = 2 * '~'
TILDE3 = 3 * '~'
TILDE4 = 4 * '~'
TILDE10 = 10 * '~'

# redcarpet test lines.
REDCARPET_LINE_FOO = 'foo'


class TestApi(unittest.TestCase):
    r"""Test the main API."""

    def test_write_string_on_file_between_markers(self):
        r"""Test that the TOC is written correctly on the file.

        Most of the job is done by the fpyutils library. Refer to that
        for the unit tests.
        """
        with self.assertRaises(exceptions.StdinIsNotAFileToBeWritten):
            api.write_string_on_file_between_markers('-', LINE, LINE)

    def test_build_multiple_tocs(self):
        r"""Test that the TOC is built correctly.

        There is no need to test this since it is a wrapper for several
        other functions. Practically it is just an extended version
        of build_toc_line.
        """

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
        ht[1] = 999999999
        with self.assertRaises(exceptions.GithubOverflowOrderedListMarker):
            api.increase_index_ordered_list(ht, 1, 1)

    def test_build_list_marker_log(self):
        r"""Test that the list_marker_log data structure is built correctly.

        There is no need to test this since it is a very simple function.
        """

    def test_compute_toc_line_indentation_spaces(self):
        r"""Test that the TOC list indentation spaces are computed correctly.
        """
        # github.
        # Unordered TOC. In this case there is no need to do specific tests
        # on the modified list marker log.

        # First TOC line.
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR, BASE_CASE_HEADER_TYPE_PREV, 0,
                'github'), 0)

        # First TOC line with the incorrect number of indentation spaces.
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR, BASE_CASE_HEADER_TYPE_PREV,
                GENERIC_NUMBER_OF_INDENTATION_SPACES, 'github'), 0)

        # A generic TOC line with no_of_indentation_spaces_prev=0.
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(GENERIC_HEADER_TYPE_CURR,
                                                    GENERIC_HEADER_TYPE_PREV,
                                                    0, 'github'),
            len(UNORDERED_LIST_SYMBOL) + len(S1))

        # Another base case.
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_CURR,
                GENERIC_NUMBER_OF_INDENTATION_SPACES, 'github'),
            GENERIC_NUMBER_OF_INDENTATION_SPACES)

        # Generic case more indentation.
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV,
                GENERIC_NUMBER_OF_INDENTATION_SPACES, 'github'),
            GENERIC_NUMBER_OF_INDENTATION_SPACES + len(UNORDERED_LIST_SYMBOL) +
            len(S1))

        # Generic case less indentation.
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_PREV, GENERIC_HEADER_TYPE_CURR,
                GENERIC_NUMBER_OF_INDENTATION_SPACES, 'github'),
            GENERIC_NUMBER_OF_INDENTATION_SPACES -
            (len(UNORDERED_LIST_SYMBOL) + len(S1)))

        # Ordered TOC.

        # First TOC line.
        list_marker_log = ['0.', '0.', '0.', '0.', '0.', '0.']
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR,
                BASE_CASE_HEADER_TYPE_PREV,
                0,
                'github',
                ordered=True,
                list_marker='.',
                list_marker_log=list_marker_log,
                index=GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX), 0)
        self.assertEqual(list_marker_log,
                         ['0.', '0.', '0.', '0.', '0.', '1000.'])

        # First TOC line with the incorrect number of indentation spaces.
        list_marker_log = ['0.', '0.', '0.', '0.', '0.', '0.']
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR,
                BASE_CASE_HEADER_TYPE_PREV,
                GENERIC_NUMBER_OF_INDENTATION_SPACES,
                'github',
                ordered=True,
                list_marker='.',
                list_marker_log=list_marker_log,
                index=GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX), 0)
        self.assertEqual(list_marker_log,
                         ['0.', '0.', '0.', '0.', '0.', '1000.'])

        # A generic TOC line with no_of_indentation_spaces_prev=0.
        list_marker_log = ['998.', '999.', '1001.', '0.', '0.', '0.']
        list_marker_log_cpy = list_marker_log.copy()
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR,
                GENERIC_HEADER_TYPE_PREV,
                0,
                'github',
                ordered=True,
                list_marker='.',
                list_marker_log=list_marker_log,
                index=GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX),
            len(list_marker_log_cpy[GENERIC_HEADER_TYPE_CURR - 1]) + len(S1))
        self.assertEqual(list_marker_log,
                         ['998.', '999.', '1001.', '0.', '0.', '1000.'])

        # Another base case.
        list_marker_log = ['998.', '999.', '1001.', '0.', '0.', '0.']
        list_marker_log_cpy = list_marker_log.copy()
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR,
                GENERIC_HEADER_TYPE_CURR,
                GENERIC_NUMBER_OF_INDENTATION_SPACES,
                'github',
                ordered=True,
                list_marker='.',
                list_marker_log=list_marker_log,
                index=GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX),
            GENERIC_NUMBER_OF_INDENTATION_SPACES)
        self.assertEqual(list_marker_log,
                         ['998.', '999.', '1001.', '0.', '0.', '1000.'])

        # Generic case more indentation.
        list_marker_log = ['998.', '999.', '1001.', '0.', '0.', '0.']
        list_marker_log_cpy = list_marker_log.copy()
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR,
                GENERIC_HEADER_TYPE_PREV,
                GENERIC_NUMBER_OF_INDENTATION_SPACES,
                'github',
                ordered=True,
                list_marker='.',
                list_marker_log=list_marker_log,
                index=GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX),
            GENERIC_NUMBER_OF_INDENTATION_SPACES +
            (len(list_marker_log_cpy[GENERIC_HEADER_TYPE_CURR - 1]) + len(S1)))
        self.assertEqual(list_marker_log,
                         ['998.', '999.', '1001.', '0.', '0.', '1000.'])

        # Generic case less indentation.
        # Note that the prev and curr variables are use in the opposite way.
        list_marker_log = ['998.', '999.', '1001.', '0.', '0.', '0.']
        list_marker_log_cpy = list_marker_log.copy()
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_PREV,
                GENERIC_HEADER_TYPE_CURR,
                GENERIC_NUMBER_OF_INDENTATION_SPACES,
                'github',
                ordered=True,
                list_marker='.',
                list_marker_log=list_marker_log,
                index=GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX),
            GENERIC_NUMBER_OF_INDENTATION_SPACES -
            (len(list_marker_log_cpy[GENERIC_HEADER_TYPE_PREV - 1]) + len(S1)))
        self.assertEqual(list_marker_log,
                         ['998.', '1000.', '0.', '0.', '0.', '0.'])

        # redcarpet.
        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV,
                GENERIC_NUMBER_OF_INDENTATION_SPACES, 'redcarpet'),
            LIST_INDENTATION * (GENERIC_HEADER_TYPE_CURR - 1))

        self.assertEqual(
            api.compute_toc_line_indentation_spaces(
                GENERIC_HEADER_TYPE_PREV, GENERIC_HEADER_TYPE_CURR,
                GENERIC_NUMBER_OF_INDENTATION_SPACES, 'redcarpet'),
            LIST_INDENTATION * (GENERIC_HEADER_TYPE_PREV - 1))

    def test_build_toc_line_without_indentation(self):
        r"""Test TOC line building for different types of inputs.
        """
        # github and redcarpet.
        header = {
            'type': GENERIC_HEADER_TYPE_CURR,
            'text_original': LINE,
            'text_anchor_link': LINE
        }

        # Unordered.
        self.assertEqual(
            api.build_toc_line_without_indentation(
                header, ordered=False, no_links=True, parser='github'),
            UNORDERED_LIST_SYMBOL + S1 + LINE)

        self.assertEqual(
            api.build_toc_line_without_indentation(
                header, ordered=False, no_links=False, parser='github'),
            UNORDERED_LIST_SYMBOL + S1 + '[' + LINE + ']' + '(#' + LINE + ')')

        # Ordered.
        self.assertEqual(
            api.build_toc_line_without_indentation(
                header,
                ordered=True,
                no_links=True,
                list_marker=ORDERED_LIST_SYMBOL,
                parser='github'), '1' + ORDERED_LIST_SYMBOL + S1 + LINE)

        self.assertEqual(
            api.build_toc_line_without_indentation(
                header,
                ordered=True,
                no_links=False,
                list_marker=ORDERED_LIST_SYMBOL,
                parser='github'), '1' + ORDERED_LIST_SYMBOL + S1 + '[' + LINE +
            ']' + '(#' + LINE + ')')

    def test_build_toc_line(self):
        r"""Test that the TOC line is built correctly.

        This function is a frontend to both the
        build_toc_line_without_indentation and
        compute_toc_line_indentation_spaces functions.
        Refer to those two functions for the unit tests.
        """

    def test_build_anchor_link(self):
        r"""Test anchor link generation.

        Algorithm testing should be done upstream.
        Test duplicates for parser='github'.
        """
        header_duplicate_counter = dict()
        api.build_anchor_link(LINE, header_duplicate_counter, parser='github')
        api.build_anchor_link(LINE, header_duplicate_counter, parser='github')
        for k in header_duplicate_counter:
            self.assertEqual(header_duplicate_counter[k], 2)

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

        # Example 32
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (1, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H2 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (2, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (3, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H4 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (4, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H5 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (5, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H6 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (6, GITHUB_LINE_FOO))

        # Example 33
        self.assertIsNone(
            api.get_atx_heading(H7 + S1 + GITHUB_LINE_FOO, 7, 'github'))

        # Example 34
        self.assertIsNone(
            api.get_atx_heading(H1 + GITHUB_LINE_5_BOLT, 6, 'github'))
        self.assertIsNone(
            api.get_atx_heading(H1 + GITHUB_LINE_HASHTAG, 6, 'github'))

        # Example 35
        self.assertIsNone(
            api.get_atx_heading(LINE_ESCAPE + H1 + S1 + GITHUB_LINE_FOO, 6,
                                'github'))

        # Example 36
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + GITHUB_LINE_FOO + S1 + GITHUB_LINE_BAR_BAZ, 3,
                'github'), (1, GITHUB_LINE_FOO + S1 + GITHUB_LINE_BAR_BAZ))

        # Example 37
        self.assertEqual(
            api.get_atx_heading(H1 + S10 + GITHUB_LINE_FOO + S10, 6, 'github'),
            (1, GITHUB_LINE_FOO))

        # Example 38
        self.assertEqual(
            api.get_atx_heading(S1 + H1 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (1, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(S2 + H1 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (1, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(S3 + H1 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (1, GITHUB_LINE_FOO))

        # Example 39 and 40
        self.assertIsNone(
            api.get_atx_heading(S4 + H1 + S1 + GITHUB_LINE_FOO, 6, 'github'))

        # Example 41
        self.assertEqual(
            api.get_atx_heading(H2 + S1 + GITHUB_LINE_FOO + S1 + H2, 6,
                                'github'), (2, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(S2 + H3 + S3 + GITHUB_LINE_BAR + S4 + H3, 6,
                                'github'), (3, GITHUB_LINE_BAR))

        # Example 42
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + GITHUB_LINE_FOO + S1, 6, 'github'),
            (1, GITHUB_LINE_FOO))
        self.assertIsNone(api.get_atx_heading(H5 * 7, 6, 'github'))
        self.assertEqual(
            api.get_atx_heading(H5 + S1 + GITHUB_LINE_FOO + S1 + H2, 6,
                                'github'), (5, GITHUB_LINE_FOO))

        # Example 43
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + GITHUB_LINE_FOO + S1 + H3 + S4, 6,
                                'github'), (3, GITHUB_LINE_FOO))

        # Example 44
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + GITHUB_LINE_FOO + S1 + H3 + S1 + GITHUB_LINE_B, 6,
                'github'), (3, GITHUB_LINE_FOO + S1 + H3 + S1 + GITHUB_LINE_B))

        # Example 45
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + GITHUB_LINE_FOO + H1, 6, 'github'),
            (1, GITHUB_LINE_FOO + H1))

        # Example 46
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + GITHUB_LINE_FOO + S1 + LINE_ESCAPE + H3, 6,
                'github'), (3, GITHUB_LINE_FOO + S1 + LINE_ESCAPE + H3))
        self.assertEqual(
            api.get_atx_heading(
                H2 + S1 + GITHUB_LINE_FOO + S1 + H1 + LINE_ESCAPE + H2, 6,
                'github'), (2, GITHUB_LINE_FOO + S1 + H1 + LINE_ESCAPE + H2))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + GITHUB_LINE_FOO + S1 + LINE_ESCAPE + H1, 6,
                'github'), (1, GITHUB_LINE_FOO + S1 + LINE_ESCAPE + H1))

        # Example 49
        self.assertEqual(
            api.get_atx_heading(H2 + S1, 6, 'github', True), (2, LINE_EMPTY))
        self.assertEqual(
            api.get_atx_heading(H1, 6, 'github', True), (1, LINE_EMPTY))
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + H3, 6, 'github', True),
            (3, LINE_EMPTY))

        # Example 49 with link labels.
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H2 + S1, 6, 'github', False)
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H1, 6, 'github', False)
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H3 + S1 + H3, 6, 'github', False)

        # Test escaping examples reported in the documentation.
        # A modified Example 302 and Example 496 (for square brackets).
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + LINE_SQUARE_BRACKET_OPEN + S1 + GITHUB_LINE_FOO + S1
                + LINE_SQUARE_BRACKET_OPEN + GITHUB_LINE_BAR +
                LINE_SQUARE_BRACKET_CLOSE + LINE_SQUARE_BRACKET_CLOSE, 6,
                'github'),
            (1, LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN + S1 + GITHUB_LINE_FOO +
             S1 + LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN + GITHUB_LINE_BAR +
             LINE_ESCAPE + LINE_SQUARE_BRACKET_CLOSE + LINE_ESCAPE +
             LINE_SQUARE_BRACKET_CLOSE))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + LINE_ESCAPE + LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN
                + S1 + GITHUB_LINE_FOO, 6, 'github'),
            (1, LINE_ESCAPE + LINE_ESCAPE + LINE_ESCAPE +
             LINE_SQUARE_BRACKET_OPEN + S1 + GITHUB_LINE_FOO))

        # Test escape character space workaround.
        self.assertEqual(
            api.get_atx_heading(H2 + S1 + GITHUB_LINE_FOO + LINE_ESCAPE, 6,
                                'github'),
            (2, GITHUB_LINE_FOO + LINE_ESCAPE + S1))

        # Test MD_PARSER_GITHUB_MAX_CHARS_LINK_LABEL
        with self.assertRaises(exceptions.GithubOverflowCharsLinkLabel):
            api.get_atx_heading(H1 + S1 + GITHUB_LINE_1000_CHARS, 6, 'github')

        # Test an empty line.
        self.assertIsNone(api.get_atx_heading(LINE_EMPTY, 6, 'github'))

        # Test line endings.
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_NEWLINE, 6, 'github', True),
            (1, LINE_EMPTY))
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_CARRIAGE_RETURN, 6, 'github', True),
            (1, LINE_EMPTY))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + GITHUB_LINE_FOO + LINE_NEWLINE + GITHUB_LINE_FOO, 6,
                'github'), (1, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + GITHUB_LINE_FOO + LINE_CARRIAGE_RETURN +
                GITHUB_LINE_FOO, 6, 'github'), (1, GITHUB_LINE_FOO))

        # Test line endings with link labels.
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H1 + LINE_NEWLINE, 6, 'github', False)
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H1 + LINE_CARRIAGE_RETURN, 6, 'github', False)

        # readcarpet
        # It does not seem that there are exaustive tests so we have to invent
        # our own. See https://github.com/vmg/redcarpet/tree/master/test
        # for more information.

        self.assertIsNone(
            api.get_atx_heading(S1 + H1 + S1 + REDCARPET_LINE_FOO, 6,
                                'redcarpet'))

        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO, 6, 'redcarpet'),
            (1, REDCARPET_LINE_FOO))

        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO + S1 + H1, 6,
                                'redcarpet'), (1, REDCARPET_LINE_FOO))

        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO + S1 + H3, 6,
                                'redcarpet'), (1, REDCARPET_LINE_FOO))

        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + REDCARPET_LINE_FOO + S1 + H3 + LINE_NEWLINE, 6,
                'redcarpet'), (3, REDCARPET_LINE_FOO))

        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO + S1 + H3 + S1, 6,
                                'redcarpet'),
            (1, REDCARPET_LINE_FOO + S1 + H3))

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + S1 + H1 + LINE_ESCAPE +
                LINE_ESCAPE + H2, 6, 'redcarpet'),
            (1, REDCARPET_LINE_FOO + S1 + H1 + LINE_ESCAPE + LINE_ESCAPE))

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + H1 + LINE_ESCAPE + H1 + S1 + H1,
                6, 'redcarpet'),
            (1, REDCARPET_LINE_FOO + H1 + LINE_ESCAPE + H1))

        # Test escape character space workaround.
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + S1 + LINE_ESCAPE, 6,
                'redcarpet'), (1, REDCARPET_LINE_FOO + S1 + LINE_ESCAPE + S1))

        # Test an empty line.
        self.assertIsNone(api.get_atx_heading(LINE_EMPTY, 6, 'redcarpet'))

        # Test newline.
        self.assertIsNone(
            api.get_atx_heading(H1 + LINE_NEWLINE, 6, 'redcarpet'))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + LINE_NEWLINE +
                REDCARPET_LINE_FOO, 6, 'redcarpet'), (1, REDCARPET_LINE_FOO))
        self.assertIsNone(
            api.get_atx_heading(H1 + LINE_CARRIAGE_RETURN, 6, 'redcarpet'))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + LINE_CARRIAGE_RETURN +
                REDCARPET_LINE_FOO, 6, 'redcarpet'),
            (1,
             REDCARPET_LINE_FOO + LINE_CARRIAGE_RETURN + REDCARPET_LINE_FOO))

    def test_get_md_header(self):
        r"""Test building of the header data structure.

        There is no need to test this since it is a wrapper for several
        other functions. None is retruned when get_md_header_type
        returns None.
        """

    # Examples 88 -> 115. TODO.
    def test_is_opening_code_fence(self):
        # github.
        # Generic.
        self.assertIsNone(api.is_opening_code_fence(LINE))
        self.assertIsNone(api.is_opening_code_fence(LINE_EMPTY))
        self.assertIsNone(api.is_opening_code_fence(GITHUB_LINE_FOO))
        self.assertIsNone(
            api.is_opening_code_fence(GITHUB_LINE_FOO + LINE_NEWLINE))

        # Spaces.
        self.assertIsNone(api.is_opening_code_fence(S1))
        self.assertIsNone(api.is_opening_code_fence(S2))
        self.assertIsNone(api.is_opening_code_fence(S3))
        self.assertIsNone(api.is_opening_code_fence(S4))
        self.assertIsNone(api.is_opening_code_fence(S10))

        # Headings.
        self.assertIsNone(api.is_opening_code_fence(H1))
        self.assertIsNone(api.is_opening_code_fence(H2))
        self.assertIsNone(api.is_opening_code_fence(H3))
        self.assertIsNone(api.is_opening_code_fence(H4))
        self.assertIsNone(api.is_opening_code_fence(H5))
        self.assertIsNone(api.is_opening_code_fence(H6))
        self.assertIsNone(api.is_opening_code_fence(H7))

        # Backticks.
        self.assertIsNone(api.is_opening_code_fence(BACKTICK1))
        self.assertIsNone(api.is_opening_code_fence(BACKTICK2))
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK2 + GITHUB_LINE_FOO))
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK2 + LINE_NEWLINE + BACKTICK1))

        self.assertEqual(api.is_opening_code_fence(BACKTICK3), BACKTICK3)
        self.assertEqual(api.is_opening_code_fence(BACKTICK4), BACKTICK4)
        self.assertEqual(api.is_opening_code_fence(BACKTICK10), BACKTICK10)

        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + GITHUB_LINE_FOO), BACKTICK3)
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK4 + GITHUB_LINE_FOO), BACKTICK4)
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK10 + GITHUB_LINE_FOO),
            BACKTICK10)
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + GITHUB_LINE_FOO), BACKTICK3)
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK4 + GITHUB_LINE_FOO), BACKTICK4)
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK10 + GITHUB_LINE_FOO),
            BACKTICK10)

        self.assertEqual(
            api.is_opening_code_fence(3 * ' ' + BACKTICK3), BACKTICK3)
        self.assertEqual(
            api.is_opening_code_fence(3 * ' ' + BACKTICK4), BACKTICK4)
        self.assertEqual(
            api.is_opening_code_fence(3 * ' ' + BACKTICK10), BACKTICK10)

        self.assertEqual(
            api.is_opening_code_fence(3 * ' ' + BACKTICK3 + GITHUB_LINE_FOO),
            BACKTICK3)
        self.assertEqual(
            api.is_opening_code_fence(3 * ' ' + BACKTICK4 + GITHUB_LINE_FOO),
            BACKTICK4)
        self.assertEqual(
            api.is_opening_code_fence(3 * ' ' + BACKTICK10 + GITHUB_LINE_FOO),
            BACKTICK10)

        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK3 + GITHUB_LINE_FOO + BACKTICK1 +
                                      GITHUB_LINE_BAR))

        self.assertIsNone(api.is_opening_code_fence(TILDE1))
        self.assertIsNone(api.is_opening_code_fence(TILDE2))
        self.assertIsNone(api.is_opening_code_fence(TILDE2 + GITHUB_LINE_FOO))
        self.assertIsNone(
            api.is_opening_code_fence(TILDE2 + LINE_NEWLINE + TILDE1))

        self.assertEqual(api.is_opening_code_fence(TILDE3), TILDE3)
        self.assertEqual(api.is_opening_code_fence(TILDE4), TILDE4)
        self.assertEqual(api.is_opening_code_fence(TILDE10), TILDE10)

        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + GITHUB_LINE_FOO), TILDE3)
        self.assertEqual(
            api.is_opening_code_fence(TILDE4 + GITHUB_LINE_FOO), TILDE4)
        self.assertEqual(
            api.is_opening_code_fence(TILDE10 + GITHUB_LINE_FOO), TILDE10)
        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + GITHUB_LINE_FOO), TILDE3)
        self.assertEqual(
            api.is_opening_code_fence(TILDE4 + GITHUB_LINE_FOO), TILDE4)
        self.assertEqual(
            api.is_opening_code_fence(TILDE10 + GITHUB_LINE_FOO), TILDE10)

        self.assertEqual(api.is_opening_code_fence(3 * ' ' + TILDE3), TILDE3)
        self.assertEqual(api.is_opening_code_fence(3 * ' ' + TILDE4), TILDE4)
        self.assertEqual(api.is_opening_code_fence(3 * ' ' + TILDE10), TILDE10)

        self.assertEqual(
            api.is_opening_code_fence(3 * ' ' + TILDE3 + GITHUB_LINE_FOO),
            TILDE3)
        self.assertEqual(
            api.is_opening_code_fence(3 * ' ' + TILDE4 + GITHUB_LINE_FOO),
            TILDE4)
        self.assertEqual(
            api.is_opening_code_fence(3 * ' ' + TILDE10 + GITHUB_LINE_FOO),
            TILDE10)

        self.assertIsNone(
            api.is_opening_code_fence(TILDE1 + GITHUB_LINE_FOO + BACKTICK1 +
                                      GITHUB_LINE_BAR))

    def test_is_closing_code_fence(self):
        self.assertFalse(api.is_closing_code_fence(BACKTICK1, BACKTICK3))
        self.assertFalse(api.is_closing_code_fence(BACKTICK2, BACKTICK3))

        self.assertTrue(api.is_closing_code_fence(BACKTICK3, BACKTICK3))
        self.assertTrue(api.is_closing_code_fence(BACKTICK4, BACKTICK3))
        self.assertTrue(api.is_closing_code_fence(BACKTICK10, BACKTICK3))

        self.assertFalse(api.is_closing_code_fence(BACKTICK3, BACKTICK4))
        self.assertFalse(api.is_closing_code_fence(BACKTICK4, BACKTICK10))

        self.assertFalse(
            api.is_closing_code_fence(BACKTICK3 + GITHUB_LINE_FOO, BACKTICK3))

        self.assertFalse(api.is_closing_code_fence(GITHUB_LINE_FOO, BACKTICK3))

        self.assertFalse(api.is_closing_code_fence(TILDE1, TILDE3))
        self.assertFalse(api.is_closing_code_fence(TILDE2, TILDE3))

        self.assertTrue(api.is_closing_code_fence(TILDE3, TILDE3))
        self.assertTrue(api.is_closing_code_fence(TILDE4, TILDE3))
        self.assertTrue(api.is_closing_code_fence(TILDE10, TILDE3))

        self.assertFalse(api.is_closing_code_fence(TILDE3, TILDE4))
        self.assertFalse(api.is_closing_code_fence(TILDE4, TILDE10))

        self.assertFalse(
            api.is_closing_code_fence(TILDE3 + GITHUB_LINE_FOO, TILDE3))

        self.assertFalse(api.is_closing_code_fence(GITHUB_LINE_FOO, TILDE3))

        self.assertFalse(api.is_closing_code_fence(BACKTICK3, TILDE3))
        self.assertFalse(api.is_closing_code_fence(TILDE3, BACKTICK3))


if __name__ == '__main__':
    unittest.main()
