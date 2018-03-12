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
LINE = 'This is a static line'
LINE_EMPTY = ''
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
UNORDERED_LIST_SYMBOL = '-'
LINE_ESCAPE = '\\'
LINE_NEWLINE = '\n'
LINE_CARRIAGE_RETURN = '\r'
LINE_SQUARE_BRACKET_OPEN = '['
LINE_SQUARE_BRACKET_CLOSE = ']'

# github test lines.
GITHUB_LINE_FOO = 'foo'
GITHUB_LINE_BAR = 'bar'
GITHUB_LINE_5_BOLT = '5 bolt'
GITHUB_LINE_HASHTAG = 'hashtag'
GITHUB_LINE_BAR_BAZ = '*bar* \*baz\*'
GITHUB_LINE_B = 'b'
GITHUB_LINE_1000_CHARS = 1000 * 'c'

# redcarpet test lines.
REDCARPET_LINE_FOO = 'foo'


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

    def test_build_toc_line(self):
        r"""Test toc line building for different types of inputs.

        Types of inputs to be tested:
            non-ordered list
            header_type > 1
            links, no links
        Ordered and non-ordered lists generate the same kind of
        strings, so there is no point in testing both cases.
        """
        header = {'type': 3, 'text_original': LINE, 'text_anchor_link': LINE}
        self.assertEqual(
            api.build_toc_line(header, ordered=False, no_links=True),
            (LIST_INDENTATION * (3 - 1)) + UNORDERED_LIST_SYMBOL + S1 + LINE)

        self.assertEqual(
            api.build_toc_line(header, ordered=False,
                               no_links=False), (LIST_INDENTATION * (3 - 1)) +
            UNORDERED_LIST_SYMBOL + S1 + '[' + LINE + ']' + '(#' + LINE + ')')

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

        GitHub examples are the same ones reported in the GFM document, except
        for minor changes. The example numbers are the same ones reported in
        the cited document. There are also some more tests for special
        cases.

        Redcarpet and GitLab examples are different from the ones present
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
        self.assertEqual(
            api.get_atx_heading(H7 + S1 + GITHUB_LINE_FOO, 7, 'github'), None)

        # Example 34
        self.assertEqual(
            api.get_atx_heading(H1 + GITHUB_LINE_5_BOLT, 6, 'github'), None)
        self.assertEqual(
            api.get_atx_heading(H1 + GITHUB_LINE_HASHTAG, 6, 'github'), None)

        # Example 35
        self.assertEqual(
            api.get_atx_heading(LINE_ESCAPE + H1 + S1 + GITHUB_LINE_FOO, 6,
                                'github'), None)

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
        self.assertEqual(
            api.get_atx_heading(S4 + H1 + S1 + GITHUB_LINE_FOO, 6, 'github'),
            None)

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
        self.assertEqual(api.get_atx_heading(H5 * 7, 6, 'github'), None)
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
                H1 + S1 + LINE_SQUARE_BRACKET_OPEN + S1 + GITHUB_LINE_FOO +
                S1 + LINE_SQUARE_BRACKET_OPEN + GITHUB_LINE_BAR +
                LINE_SQUARE_BRACKET_CLOSE + LINE_SQUARE_BRACKET_CLOSE, 6,
                'github'),
            (1, LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN + S1 + GITHUB_LINE_FOO +
             S1 + LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN + GITHUB_LINE_BAR +
             LINE_ESCAPE + LINE_SQUARE_BRACKET_CLOSE + LINE_ESCAPE +
             LINE_SQUARE_BRACKET_CLOSE))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + LINE_ESCAPE + LINE_ESCAPE +
                LINE_SQUARE_BRACKET_OPEN + S1 + GITHUB_LINE_FOO, 6, 'github'),
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
        self.assertEqual(api.get_atx_heading(LINE_EMPTY, 6, 'github'), None)

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
            api.get_atx_heading(H1 + S1 + GITHUB_LINE_FOO +
                                LINE_CARRIAGE_RETURN + GITHUB_LINE_FOO, 6,
                                'github'), (1, GITHUB_LINE_FOO))

        # Test line endings with link labels.
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H1 + LINE_NEWLINE, 6, 'github', False)
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H1 + LINE_CARRIAGE_RETURN, 6, 'github', False)

        # readcarpet and gitlab
        # It does not seem that there are exaustive tests so we have to invent
        # our own. See https://github.com/vmg/redcarpet/tree/master/test
        # for more information.

        self.assertEqual(
            api.get_atx_heading(S1 + H1 + S1 + REDCARPET_LINE_FOO, 6,
                                'redcarpet'), None)

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
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO + S1 + H1 +
                                LINE_ESCAPE + LINE_ESCAPE + H2, 6,
                                'redcarpet'),
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
        self.assertEqual(api.get_atx_heading(LINE_EMPTY, 6, 'redcarpet'), None)

        # Test newline.
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_NEWLINE, 6, 'gitlab'), None)
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO + LINE_NEWLINE +
                                REDCARPET_LINE_FOO, 6, 'gitlab'),
            (1, REDCARPET_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_CARRIAGE_RETURN, 6, 'gitlab'), None)
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO +
                                LINE_CARRIAGE_RETURN + REDCARPET_LINE_FOO, 6,
                                'gitlab'),
            (1,
             REDCARPET_LINE_FOO + LINE_CARRIAGE_RETURN + REDCARPET_LINE_FOO))

    def test_get_md_header(self):
        r"""Test building of the header data structure.

        There is no need to test this since it is a wrapper for several
        other functions. None is retruned when get_md_header_type
        returns None.
        """


if __name__ == '__main__':
    unittest.main()
