#
# tests.py
#
# Copyright (C) 2017 frnmst (Franco Masotti) <franco.masotti@live.com>
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

# Some static variables.
STATIC_LINE = 'This is a static line'
LEADING_WHITESPACE_10 = 10 * ' '
LEADING_WHITESPACE_1 = 1 * ' '
H1 = 1 * '#'
H2 = 2 * '#'
H3 = 3 * '#'
H4 = 4 * '#'
LIST_INDENTATION = 4 * ' '
HEADER_TYPE_1 = 1
HEADER_TYPE_2 = 2
HEADER_TYPE_3 = 3
UNORDERED_LIST_SYMBOL = '-'


class TestApi(unittest.TestCase):
    r"""Test the main API."""

    def test_write_string_on_file_between_markers(self):
        r"""Test that the TOC is written correcly on the file.

        Most of the job is done by the fpyutils library. Refer to that
        for the unit tests. There is nothing of relevance to be tested
        otherwise.
        """

    def test_build_toc(self):
        r"""Test that the TOC is built correctly.

        There is no need to test this since it is a wrapper for several
        other functions. Practically it is just an extended version
        of build_toc_line.
        """

    def test_increase_index_ordered_list(self):
        r"""Test that the list index increases correctly.

        Test both base cases and the non-base case by verifying that the index
        increases.
        """
        ht = dict()
        api.increase_index_ordered_list(ht, 0, HEADER_TYPE_1)
        self.assertEqual(ht[HEADER_TYPE_1], 1)
        api.increase_index_ordered_list(ht, HEADER_TYPE_1, HEADER_TYPE_1)
        self.assertEqual(ht[HEADER_TYPE_1], 2)

    def test_build_toc_line(self):
        r"""Test toc line building for different types of inputs.

        Types of inputs to be tested:
            non-ordered list
            header_type > 1
            links, no links
        Ordered and non-ordered lists generate the same kind of
        strings, so there is no point in testing both cases.
        """
        header = {
            'type': HEADER_TYPE_3,
            'text_original': STATIC_LINE,
            'text_anchor_link': STATIC_LINE
        }
        self.assertEqual(
            api.build_toc_line(header, ordered=False, no_links=True),
            (LIST_INDENTATION * (HEADER_TYPE_3 - 1)) + UNORDERED_LIST_SYMBOL +
            LEADING_WHITESPACE_1 + STATIC_LINE)

        self.assertEqual(
            api.build_toc_line(header, ordered=False, no_links=False),
            (LIST_INDENTATION * (HEADER_TYPE_3 - 1)) + UNORDERED_LIST_SYMBOL +
            LEADING_WHITESPACE_1 + '[' + STATIC_LINE + ']' + '(#' +
            STATIC_LINE + ')')

    def test_build_anchor_link(self):
        r"""Test anchor link generation.

        Algorithm testing should be done upstream.
        Test duplicates for anchor_type='github' and anchor_type='gitlab'.
        """
        header_duplicate_counter = dict()
        api.build_anchor_link(
            STATIC_LINE, header_duplicate_counter, anchor_type='github')
        api.build_anchor_link(
            STATIC_LINE, header_duplicate_counter, anchor_type='github')
        for k in header_duplicate_counter:
            self.assertEqual(header_duplicate_counter[k], 2)

        header_duplicate_counter = dict()
        api.build_anchor_link(
            STATIC_LINE, header_duplicate_counter, anchor_type='gitlab')
        api.build_anchor_link(
            STATIC_LINE, header_duplicate_counter, anchor_type='gitlab')
        for k in header_duplicate_counter:
            self.assertEqual(header_duplicate_counter[k], 2)

    def test_get_md_header_type(self):
        r"""Test h{1,2,3} and h{4,Inf} headers and non-headers.

        Use the max_header variable set to the default value 3.
        Test several possible line configurations.
        """
        self.assertEqual(api.get_md_header_type(H1 + STATIC_LINE), 1)
        self.assertEqual(api.get_md_header_type(H2 + STATIC_LINE), 2)
        self.assertEqual(api.get_md_header_type(H3 + STATIC_LINE), 3)
        self.assertEqual(api.get_md_header_type(H4 + STATIC_LINE), None)

        self.assertEqual(
            api.get_md_header_type(LEADING_WHITESPACE_10 + H1 + STATIC_LINE),
            1)
        self.assertEqual(
            api.get_md_header_type(LEADING_WHITESPACE_10 + H2 + STATIC_LINE),
            2)
        self.assertEqual(
            api.get_md_header_type(LEADING_WHITESPACE_10 + H3 + STATIC_LINE),
            3)
        self.assertEqual(
            api.get_md_header_type(LEADING_WHITESPACE_10 + H4 + STATIC_LINE),
            None)

        self.assertEqual(
            api.get_md_header_type(H1 + LEADING_WHITESPACE_10 + STATIC_LINE),
            1)
        self.assertEqual(
            api.get_md_header_type(H2 + LEADING_WHITESPACE_10 + STATIC_LINE),
            2)
        self.assertEqual(
            api.get_md_header_type(H3 + LEADING_WHITESPACE_10 + STATIC_LINE),
            3)
        self.assertEqual(
            api.get_md_header_type(H4 + LEADING_WHITESPACE_10 + STATIC_LINE),
            None)

        self.assertEqual(
            api.get_md_header_type(LEADING_WHITESPACE_10 + H1 +
                                   LEADING_WHITESPACE_10 + STATIC_LINE), 1)
        self.assertEqual(
            api.get_md_header_type(LEADING_WHITESPACE_10 + H2 +
                                   LEADING_WHITESPACE_10 + STATIC_LINE), 2)
        self.assertEqual(
            api.get_md_header_type(LEADING_WHITESPACE_10 + H3 +
                                   LEADING_WHITESPACE_10 + STATIC_LINE), 3)
        self.assertEqual(
            api.get_md_header_type(LEADING_WHITESPACE_10 + H4 +
                                   LEADING_WHITESPACE_10 + STATIC_LINE), None)

        self.assertEqual(api.get_md_header_type(STATIC_LINE), None)

        self.assertEqual(api.get_md_header_type(''), None)

        self.assertEqual(api.get_md_header_type(H1), None)

    def test_remove_md_header_syntax(self):
        r"""Test line trimming with 5 possible configurations."""
        self.assertEqual(
            api.remove_md_header_syntax(H1 + STATIC_LINE), STATIC_LINE)
        self.assertEqual(
            api.remove_md_header_syntax(
                LEADING_WHITESPACE_10 + H1 + STATIC_LINE), STATIC_LINE)
        self.assertEqual(
            api.remove_md_header_syntax(
                H1 + LEADING_WHITESPACE_10 + STATIC_LINE), STATIC_LINE)
        self.assertEqual(
            api.remove_md_header_syntax(LEADING_WHITESPACE_10 + H1 +
                                        LEADING_WHITESPACE_10 + STATIC_LINE),
            STATIC_LINE)
        self.assertEqual(
            api.remove_md_header_syntax(
                LEADING_WHITESPACE_10 + H1 + LEADING_WHITESPACE_10 + H1 +
                STATIC_LINE), H1 + STATIC_LINE)

    def test_get_md_header(self):
        r"""Test building of the header data structure.

        There is no need to test this since it is a wrapper for several
        other functions. None is retruned when get_md_header_type
        returns None.
        """


if __name__ == '__main__':
    unittest.main()
