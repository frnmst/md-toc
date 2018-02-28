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

# Some static variables.
LINE = 'This is a static line'
LINE_FOO = 'foo'
LINE_BAR = 'bar'
LINE_5_BOLT = '5 bolt'
LINE_HASHTAG = 'hashtag'
LINE_BAR_BAZ = '*bar* \*baz\*'
LINE_BAR_BAZ_NO_ESCAPE = '*bar* *baz*'
LINE_B = 'b'
LINE_ESCAPE = '\\'

S1 = 1 * ' '
S2 = 2 * ' '
S3 = 3 * ' '
S4 = 4 * ' '
S10 = 10 * ' '
H1 = 1 * '#'
H2 = 2 * '#'
H3 = 3 * '#'
H4 = 4 * '#'
H5 = 5 * '#'
H6 = 6 * '#'
H7 = 7 * '#'
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
            'text_original': LINE,
            'text_anchor_link': LINE
        }
        self.assertEqual(
            api.build_toc_line(header, ordered=False, no_links=True),
            (LIST_INDENTATION *
             (HEADER_TYPE_3 - 1)) + UNORDERED_LIST_SYMBOL + S1 + LINE)

        self.assertEqual(
            api.build_toc_line(header, ordered=False, no_links=False),
            (LIST_INDENTATION * (HEADER_TYPE_3 - 1)) + UNORDERED_LIST_SYMBOL +
            S1 + '[' + LINE + ']' + '(#' + LINE + ')')

    def test_build_anchor_link(self):
        r"""Test anchor link generation.

        Algorithm testing should be done upstream.
        Test duplicates for parser='github' and parser='gitlab'.
        """
        header_duplicate_counter = dict()
        api.build_anchor_link(LINE, header_duplicate_counter, parser='github')
        api.build_anchor_link(LINE, header_duplicate_counter, parser='github')
        for k in header_duplicate_counter:
            self.assertEqual(header_duplicate_counter[k], 2)

        header_duplicate_counter = dict()
        api.build_anchor_link(LINE, header_duplicate_counter, parser='gitlab')
        api.build_anchor_link(LINE, header_duplicate_counter, parser='gitlab')
        for k in header_duplicate_counter:
            self.assertEqual(header_duplicate_counter[k], 2)

    def test_get_atx_heading(self):
        r"""Test the title gathering for edge cases and various parsers.

        Github examples are the same ones reported in the GFM document, except
        for minor changes.
        """
        # github
        # Example 32
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + LINE_FOO, 6, 'github'),
            (1, LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H2 + S1 + LINE_FOO, 6, 'github'),
            (2, LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + LINE_FOO, 6, 'github'),
            (3, LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H4 + S1 + LINE_FOO, 6, 'github'),
            (4, LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H5 + S1 + LINE_FOO, 6, 'github'),
            (5, LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H6 + S1 + LINE_FOO, 6, 'github'),
            (6, LINE_FOO))

        # Example 33
        self.assertEqual(
            api.get_atx_heading(H7 + S1 + LINE_FOO, 7, 'github'), None)

        # Example 34
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_5_BOLT, 6, 'github'), None)
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_HASHTAG, 6, 'github'), None)

        # Example 35
        self.assertEqual(
            api.get_atx_heading(LINE_ESCAPE + H1 + S1 + LINE_FOO, 6, 'github'),
            None)

        # Example 36
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + LINE_FOO + S1 + LINE_BAR_BAZ, 3,
                                'github'), (1, LINE_FOO + S1 + LINE_BAR_BAZ))

        # Example 37
        self.assertEqual(
            api.get_atx_heading(H1 + S10 + LINE_FOO + S10, 6, 'github'),
            (1, LINE_FOO))

        # Example 38
        self.assertEqual(
            api.get_atx_heading(S1 + H1 + S1 + LINE_FOO, 6, 'github'),
            (1, LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(S2 + H1 + S1 + LINE_FOO, 6, 'github'),
            (1, LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(S3 + H1 + S1 + LINE_FOO, 6, 'github'),
            (1, LINE_FOO))

        # Example 39 and 40
        self.assertEqual(
            api.get_atx_heading(S4 + H1 + S1 + LINE_FOO, 6, 'github'), None)

        # Example 41
        self.assertEqual(
            api.get_atx_heading(H2 + S1 + LINE_FOO + S1 + H2, 6, 'github'),
            (2, LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(S2 + H3 + S3 + LINE_BAR + S4 + H3, 6,
                                'github'), (3, LINE_BAR))

        # Example 42
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + LINE_FOO + S1, 6, 'github'),
            (1, LINE_FOO))
        self.assertEqual(api.get_atx_heading(H5 * 7, 6, 'github'), None)
        self.assertEqual(
            api.get_atx_heading(H5 + S1 + LINE_FOO + S1 + H2, 6, 'github'),
            (5, LINE_FOO))

        # Example 43
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + LINE_FOO + S1 + H3 + S4, 6,
                                'github'), (3, LINE_FOO))

        # Example 44
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + LINE_FOO + S1 + H3 + S1 + LINE_B, 6,
                                'github'),
            (3, LINE_FOO + S1 + H3 + S1 + LINE_B))

        # Example 45
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + LINE_FOO + H1, 6, 'github'),
            (1, LINE_FOO + H1))

        # Example 46
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + LINE_FOO + S1 + LINE_ESCAPE + H3, 6,
                                'github'),
            (3, LINE_FOO + S1 + LINE_ESCAPE + H3))
        self.assertEqual(
            api.get_atx_heading(
                H2 + S1 + LINE_FOO + S1 + H1 + LINE_ESCAPE + H2, 6, 'github'),
            (2, LINE_FOO + S1 + H1 + LINE_ESCAPE + H2))
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + LINE_FOO + S1 + LINE_ESCAPE + H1, 6,
                                'github'),
            (1, LINE_FOO + S1 + LINE_ESCAPE + H1))

        # Example 49
        self.assertEqual(api.get_atx_heading(H2 + S1, 6, 'github'), (2, ''))
        self.assertEqual(api.get_atx_heading(H1, 6, 'github'), (1, ''))
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + H3, 6, 'github'), (3, ''))

        # TODO: readcarpet, github

    def test_get_md_header(self):
        r"""Test building of the header data structure.

        There is no need to test this since it is a wrapper for several
        other functions. None is retruned when get_md_header_type
        returns None.
        """


if __name__ == '__main__':
    unittest.main()
