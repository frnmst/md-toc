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
from unittest.mock import patch, mock_open
import sys

# Some static variables.
STATIC_LINE = 'This is a static line'
LEADING_WHITESPACE = 10 * ' '
H1=1 * '#'
H2=2 * '#'
H3=3 * '#'
H4=4 * '#'

class TestApi(unittest.TestCase):
    """Pass."""

    def test_write_toc_on_md_file(self):
        """Pass."""

    def test_build_toc(self):
        """Pass."""

    def test_increment_index_ordered_list(self):
        r"""Pass."""

    def test_build_toc_line(self):
        r"""Test toc line building for different types of inputs.

        Types of inputs:
            ordered list, non-ordered list
            header_type
            links, no links
        """

    def test_build_anchor_link(self):
        r"""Test anchor link generation.

        Algorithm testing should be done upstream.
        Test duplicates for anchor_type='github' and anchor_type='gitlab'.
        """
        header_duplicate_counter=dict()
        api.build_anchor_link(STATIC_LINE,header_duplicate_counter,anchor_type='github')
        api.build_anchor_link(STATIC_LINE,header_duplicate_counter,anchor_type='github')
        for k in header_duplicate_counter:
            self.assertEqual(header_duplicate_counter[k],2)

        header_duplicate_counter=dict()
        api.build_anchor_link(STATIC_LINE,header_duplicate_counter,anchor_type='gitlab')
        api.build_anchor_link(STATIC_LINE,header_duplicate_counter,anchor_type='gitlab')
        for k in header_duplicate_counter:
            self.assertEqual(header_duplicate_counter[k],2)

    def test_get_md_header_type(self):
        r"""Test h{1,2,3} and h{4,Inf} headers and non-headers.

        Use the max_header variable set to the default value 3.
        Test 4 possible line configurations.
        """

        self.assertEqual(api.get_md_header_type(H1+STATIC_LINE),1)
        self.assertEqual(api.get_md_header_type(H2+STATIC_LINE),2)
        self.assertEqual(api.get_md_header_type(H3+STATIC_LINE),3)
        self.assertEqual(api.get_md_header_type(H4+STATIC_LINE),None)

        self.assertEqual(api.get_md_header_type(LEADING_WHITESPACE+H1+STATIC_LINE),1)
        self.assertEqual(api.get_md_header_type(LEADING_WHITESPACE+H2+STATIC_LINE),2)
        self.assertEqual(api.get_md_header_type(LEADING_WHITESPACE+H3+STATIC_LINE),3)
        self.assertEqual(api.get_md_header_type(LEADING_WHITESPACE+H4+STATIC_LINE),None)

        self.assertEqual(api.get_md_header_type(H1+LEADING_WHITESPACE+STATIC_LINE),1)
        self.assertEqual(api.get_md_header_type(H2+LEADING_WHITESPACE+STATIC_LINE),2)
        self.assertEqual(api.get_md_header_type(H3+LEADING_WHITESPACE+STATIC_LINE),3)
        self.assertEqual(api.get_md_header_type(H4+LEADING_WHITESPACE+STATIC_LINE),None)

        self.assertEqual(api.get_md_header_type(LEADING_WHITESPACE+H1+LEADING_WHITESPACE+STATIC_LINE),1)
        self.assertEqual(api.get_md_header_type(LEADING_WHITESPACE+H2+LEADING_WHITESPACE+STATIC_LINE),2)
        self.assertEqual(api.get_md_header_type(LEADING_WHITESPACE+H3+LEADING_WHITESPACE+STATIC_LINE),3)
        self.assertEqual(api.get_md_header_type(LEADING_WHITESPACE+H4+LEADING_WHITESPACE+STATIC_LINE),None)


    def test_remove_md_header_syntax(self):
        r"""Test line trimming with 5 possible configurations."""
        self.assertEqual(api.remove_md_header_syntax(H1+STATIC_LINE),STATIC_LINE)
        self.assertEqual(api.remove_md_header_syntax(LEADING_WHITESPACE+H1+STATIC_LINE),STATIC_LINE)
        self.assertEqual(api.remove_md_header_syntax(H1+LEADING_WHITESPACE+STATIC_LINE),STATIC_LINE)
        self.assertEqual(api.remove_md_header_syntax(LEADING_WHITESPACE+H1+LEADING_WHITESPACE+STATIC_LINE),STATIC_LINE)
        self.assertEqual(api.remove_md_header_syntax(LEADING_WHITESPACE+H1+LEADING_WHITESPACE+H1+STATIC_LINE),H1+STATIC_LINE)

    def test_get_md_header(self):
        r"""Test building of the header data structure.

        There is no need to test this since it is a wrapper for several
        other functions.
        """


if __name__ == '__main__':
    unittest.main()
