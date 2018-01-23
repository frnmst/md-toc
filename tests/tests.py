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
import string
import unittest
from unittest.mock import patch, mock_open
import sys


class TestApi(unittest.TestCase):
    """Pass."""

    def test_write_toc_on_md_file(self):
        """Pass."""

    def test_build_toc(self):
        """Pass."""

    def test_increment_index_ordered_list(self):
        """Pass."""

    def build_anchor_link(self):
        """Pass."""

    def test_build_toc_line(self):
        """Pass."""

    def test_get_md_header_type(self):
        """Pass."""

    def test_get_md_header(self):
        """Test h{1,2,3} and h{4,Inf} headers and non-headers.

        Do not test the link generation part.
        """
        STATIC_LINE = 'This is a static line'
        LEADING_WHITESPACE = 10 * ' '
        H1=1 * '#'
        H2=2 * '#'
        H3=3 * '#'
        H4=4 * '#'

        # h1
        api.get_md_heading(

        # h2

        # h3


if __name__ == '__main__':
    unittest.main()
