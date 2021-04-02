#!/usr/bin/env python3
#
# tests.py
#
# Copyright (C) 2017-2020 frnmst (Franco Masotti) <franco.masotti@live.com>
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

from .. import (api, exceptions)
from ..constants import parser as md_parser
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
S5 = 5 * ' '
S10 = 10 * ' '
S18 = 18 * ' '
S21 = 21 * ' '

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
GITHUB_LINE_FOO = 'foo'
GITHUB_LINE_BAR = 'bar'
GITHUB_LINE_5_BOLT = '5 bolt'
GITHUB_LINE_HASHTAG = 'hashtag'
GITHUB_LINE_BAR_BAZ = '*bar* ' + LINE_ESCAPE + '*baz' + LINE_ESCAPE + '*'
GITHUB_LINE_B = 'b'
GITHUB_LINE_1000_CHARS = 1000 * 'c'

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
GITHUB_INFO_STRING_FOO = 'ruby'
GITHUB_INFO_STRING_GARBAGE = 'startline=3 $%@#$'

# github renders as list header types. Do not change these values.
BASE_CASE_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR = 1
GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR = 4
GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR_BIS = 5
BASE_CASE_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_FIRST = 1
GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_FIRST = 4

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

    @unittest.skip("empty test")
    def test_write_strings_on_files_between_markers(self):
        r"""Test that the TOC is written correctly on the files."""

    @unittest.skip("empty test")
    def test_build_toc(self):
        r"""Test that the TOC is built correctly.

        There is no need to test this since it is a wrapper for several
        other functions. Practically it is just an extended version
        of build_toc_line.

        TODO: tests will be needed eventually because the complexity of
        this function is growing.
        """

    @unittest.skip("empty test")
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

    @unittest.skip("empty test")
    def test_build_list_marker_log(self):
        r"""Test that the list_marker_log data structure is built correctly.

        There is no need to test this since it is a very simple function.
        """

    def _test_helper_assert_compute_toc_line_indentation_spaces(
            self, parser, log, header_type_curr, header_type_prev,
            expected_indentation_spaces, expected_index, expected_list_marker):
        self.assertEqual(log[header_type_curr]['indentation spaces'],
                         expected_indentation_spaces)
        self.assertEqual(log[header_type_curr]['index'], expected_index)
        self.assertEqual(log[header_type_curr]['list marker'],
                         expected_list_marker)
        if parser == 'github':
            if header_type_curr < header_type_prev:
                for i in range(
                        header_type_curr + 1,
                        md_parser['github']['header']['max levels'] + 1):
                    self.assertEqual(log[i]['index'], 0)
                    self.assertEqual(log[i]['indentation spaces'], 0)
                    self.assertEqual(log[i]['list marker'],
                                     expected_list_marker)

    def test_compute_toc_line_indentation_spaces(self):
        r"""Test that the TOC list indentation spaces are computed correctly."""
        # github.
        md_parser['github']['header']['max levels'] = 6

        # Unordered TOC.

        # 1. First TOC line.
        log = api.init_indentation_log('github', '-')
        api.compute_toc_line_indentation_spaces(GENERIC_HEADER_TYPE_CURR,
                                                BASE_CASE_HEADER_TYPE_PREV,
                                                'github', False, '-', log)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR,
            BASE_CASE_HEADER_TYPE_PREV, 0, 0, '-')

        # 2. First TOC line with the incorrect number of indentation spaces.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_CURR][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(GENERIC_HEADER_TYPE_CURR,
                                                BASE_CASE_HEADER_TYPE_PREV,
                                                'github', False, '-', log)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR,
            BASE_CASE_HEADER_TYPE_PREV, 0, 0, '-')

        # 3. A generic TOC line with number of previous indentation spaces = 0.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_CURR]['indentation spaces'] = 0
        api.compute_toc_line_indentation_spaces(GENERIC_HEADER_TYPE_CURR,
                                                GENERIC_HEADER_TYPE_PREV,
                                                'github', False, '-', log)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV,
            len(UNORDERED_LIST_SYMBOL) + len(S1), 0, '-')

        # 4. Base case same indentation.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_CURR][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(GENERIC_HEADER_TYPE_CURR,
                                                GENERIC_HEADER_TYPE_CURR,
                                                'github', False, '-', log)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_CURR,
            GENERIC_NUMBER_OF_INDENTATION_SPACES, 0, '-')

        # 5. Generic case more indentation.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_PREV][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(GENERIC_HEADER_TYPE_CURR,
                                                GENERIC_HEADER_TYPE_PREV,
                                                'github', False, '-', log)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV,
            GENERIC_NUMBER_OF_INDENTATION_SPACES + len(UNORDERED_LIST_SYMBOL) +
            len(S1), 0, '-')

        # 6. Generic case less indentation.
        # Note: the parameters GENERIC_HEADER_TYPE_PREV and GENERIC_HEADER_TYPE_CURR
        #       are inverted as the api.compute_toc_line_indentation_spaces
        #       function input, in respect to the usual positions.
        log = api.init_indentation_log('github', '-')
        log[GENERIC_HEADER_TYPE_PREV][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(GENERIC_HEADER_TYPE_PREV,
                                                GENERIC_HEADER_TYPE_CURR,
                                                'github', False, '-', log)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_PREV, GENERIC_HEADER_TYPE_CURR,
            GENERIC_NUMBER_OF_INDENTATION_SPACES, 0, '-')

        # Ordered TOC.

        # 7. First TOC line.
        log = api.init_indentation_log('github', '.')
        log[GENERIC_HEADER_TYPE_CURR]['indentation spaces'] = 0
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR, BASE_CASE_HEADER_TYPE_PREV, 'github',
            True, '.', log, GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV,
            0, GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX, '.')

        # 8. First TOC line with the incorrect number of indentation spaces.
        log = api.init_indentation_log('github', '.')
        log[GENERIC_HEADER_TYPE_CURR][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR, BASE_CASE_HEADER_TYPE_PREV, 'github',
            True, '.', log, GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV,
            0, GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX, '.')

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
            GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV, 'github', True,
            '.', log, GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV,
            expected_indentation_spaces,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX, '.')

        # 10. Another base case.
        log = api.init_indentation_log('github', '.')
        log[1]['index'] = 998
        log[2]['index'] = 999
        log[3]['index'] = 1001
        log[GENERIC_HEADER_TYPE_CURR][
            'indentation spaces'] = GENERIC_NUMBER_OF_INDENTATION_SPACES
        api.compute_toc_line_indentation_spaces(
            GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_CURR, 'github', True,
            '.', log, GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_CURR,
            GENERIC_NUMBER_OF_INDENTATION_SPACES,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX, '.')

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
            GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV, 'github', True,
            '.', log, GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_CURR, GENERIC_HEADER_TYPE_PREV,
            expected_indentation_spaces,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX, '.')

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
            GENERIC_HEADER_TYPE_PREV, GENERIC_HEADER_TYPE_CURR, 'github', True,
            '.', log, GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'github', log, GENERIC_HEADER_TYPE_PREV, GENERIC_HEADER_TYPE_CURR,
            expected_indentation_spaces,
            GENERIC_LIST_MARKER_LOG_ORDERED_NEXT_INDEX, '.')

        # redcarpet.
        md_parser['redcarpet']['header']['max levels'] = 6

        # 1. More indentation.
        log = api.init_indentation_log('redcarpet', '-')
        api.compute_toc_line_indentation_spaces(GENERIC_HEADER_TYPE_CURR,
                                                GENERIC_HEADER_TYPE_PREV,
                                                'redcarpet', False, '-', log)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'redcarpet', log, GENERIC_HEADER_TYPE_CURR,
            GENERIC_HEADER_TYPE_PREV,
            LIST_INDENTATION * (GENERIC_HEADER_TYPE_CURR - 1), 0, '-')

        # 2. Less indentation.
        log = api.init_indentation_log('redcarpet', '-')
        api.compute_toc_line_indentation_spaces(GENERIC_HEADER_TYPE_PREV,
                                                GENERIC_HEADER_TYPE_CURR,
                                                'redcarpet', False, '-', log)
        self._test_helper_assert_compute_toc_line_indentation_spaces(
            'redcarpet', log, GENERIC_HEADER_TYPE_PREV,
            GENERIC_HEADER_TYPE_CURR,
            LIST_INDENTATION * (GENERIC_HEADER_TYPE_PREV - 1), 0, '-')

    def test_build_toc_line_without_indentation(self):
        r"""Test TOC line building for different types of inputs."""
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

    @unittest.skip("empty test")
    def test_build_toc_line(self):
        r"""Test that the TOC line is built correctly.

        This function is a frontend to both the
        build_toc_line_without_indentation and
        compute_toc_line_indentation_spaces functions.
        Refer to those two functions for the unit tests.
        """

    def test_get_fdr_indices(self):
        r"""Test get flanking delimiter run indices.

        ..note: some examples in the documentation appear to be contradicting.
        """
        # Star character.
        self.assertEqual(api.get_fdr_indices('***abc', 'left', 'github'), {'*': [[0, 2]], '_': list(), })
        self.assertEqual(api.get_fdr_indices('**"abc"', 'left', 'github'), {'*': [[0, 1]], '_': list(), })
        self.assertEqual(api.get_fdr_indices(' abc***def', 'left', 'github'), {'*': [[4, 6]], '_': list(), })
        self.assertEqual(api.get_fdr_indices('***abc **def', 'left', 'github'), {'*': [[0, 2], [7, 8]], '_': list(), })

        self.assertEqual(api.get_fdr_indices('a*"foo"*', 'left', 'github'), {'*': list(), '_': list(), })

        self.assertEqual(api.get_fdr_indices('abc***', 'left', 'github'), {'*': list(), '_': list(), })
        self.assertEqual(api.get_fdr_indices('"abc"***', 'left', 'github'), {'*': list(), '_': list(), })

        # Underscore character.
        self.assertEqual(api.get_fdr_indices('  _abc', 'left', 'github'), {'*': list(), '_': [[2, 2]], })
        self.assertEqual(api.get_fdr_indices(' _"abc"', 'left', 'github'), {'*': list(), '_': [[1, 1]], })
        self.assertEqual(api.get_fdr_indices('"abc"_"def"', 'left', 'github'), {'*': list(), '_': [[5, 5]], })

        # Neither left nor right-flanking.
        self.assertEqual(api.get_fdr_indices('abc *** def', 'left', 'github'), {'*': list(), '_': list(), })
        self.assertEqual(api.get_fdr_indices('a _ b', 'left', 'github'), {'*': list(), '_': list(), })

        # Star character.
        self.assertEqual(api.get_fdr_indices(' abc***', 'right', 'github'), {'*': [[4, 6]], '_': list(), })
        self.assertEqual(api.get_fdr_indices('"abc"**', 'right', 'github'), {'*': [[5, 6]], '_': list(), })

        self.assertEqual(api.get_fdr_indices(' abc***def', 'right', 'github'), {'*': [[4, 6]], '_': list(), })

        # Underscore character.
        self.assertEqual(api.get_fdr_indices(' abc_', 'right', 'github'), {'*': list(), '_': [[4, 4]], })
        self.assertEqual(api.get_fdr_indices('"abc"_', 'right', 'github'), {'*': list(), '_': [[5, 5]], })
        self.assertEqual(api.get_fdr_indices('"abc"_"def"', 'right', 'github'), {'*': list(), '_': [[5, 5]], })

        # Neither left nor right-flanking.
        self.assertEqual(api.get_fdr_indices('abc *** def', 'right', 'github'), {'*': list(), '_': list(), })
        self.assertEqual(api.get_fdr_indices('a _ b', 'right', 'github'), {'*': list(), '_': list(), })

    def test_get_remove_emphasis_indices(self):
        r"""Test get remove emphasis indices."""
        # Example 331
        self.assertEqual(api.get_remove_emphasis_indices('*foo bar*'), [[8, 8], [0, 0]])

        # Example 332
        self.assertEqual(api.get_remove_emphasis_indices('a * foo bar*'), list())

        # Example 333
        self.assertEqual(api.get_remove_emphasis_indices('a*"foo"*'), list())

        # Example 334
        self.assertEqual(api.get_remove_emphasis_indices('* a *'), list())

        # Example 335
        self.assertEqual(api.get_remove_emphasis_indices('foo*bar*'), [[7, 7], [3, 3]])

        # Example 336
        self.assertEqual(api.get_remove_emphasis_indices('5*6*78'), [[3, 3], [1, 1]])

        # Example 337
        # self.assertEqual(api.get_remove_emphasis_indices('_foo bar_'), [[3, 3], [1, 1]])
        # Example 338
        # Example 339
        # Example 340
        # Example 341
        # Example 342
        # Example 343
        # Example 344
        # Example 345

        # Example 346
        self.assertEqual(api.get_remove_emphasis_indices('*foo bar *'), list())

        # Example 347
        self.assertEqual(api.get_remove_emphasis_indices('*foo bar\n*'), list())

        # Example 348
        self.assertEqual(api.get_remove_emphasis_indices('*(*foo)'), list())

        # Example 349
        self.assertEqual(api.get_remove_emphasis_indices('*(*foo*)*'), [[8, 8], [0, 0], [6, 6], [2, 2]])

        # Example 350
        self.assertEqual(api.get_remove_emphasis_indices('*foo*bar'), [[4, 4], [0, 0]])

        # Example 351
        # Example 352
        # Example 353
        # Example 354
        # Example 355
        # Example 356
        # Example 357

        # Example 358
        self.assertEqual(api.get_remove_emphasis_indices('**foo bar**'), [[9, 10], [0, 1]])

        # Example 359
        self.assertEqual(api.get_remove_emphasis_indices('** foo bar**'), list())

        # Example 360
        self.assertEqual(api.get_remove_emphasis_indices('a**"foo"**'), list())

        # Example 361
        self.assertEqual(api.get_remove_emphasis_indices('foo**bar**'), [[8, 9], [3, 4]])

        # Example 362
        # Example 363
        # Example 364
        # Example 365
        # Example 366
        # Example 367
        # Example 368
        # Example 369
        # Example 370

        # Example 371
        self.assertEqual(api.get_remove_emphasis_indices('**foo bar **'), list())

        # Example 372
        self.assertEqual(api.get_remove_emphasis_indices('**(**foo)'), list())

        # Example 373
        self.assertEqual(api.get_remove_emphasis_indices('*(**foo**)*'), [[10, 10], [0, 0], [7, 8], [2, 3]])

        # Example 374
#        self.assertEqual(api.get_remove_emphasis_indices('**Gomphocarpus (*Gomphocarpus physocarpus*, syn.\n*Asclepias physocarpa*)**'), [[0, 1], [16, 16], [41, 41], [49, 49], [70, 70], [72, 73]])

        # Example 375
        self.assertEqual(api.get_remove_emphasis_indices('**foo "*bar*" foo**'), [[17, 18], [0, 1], [11, 11], [7, 7]])

        # Example 376
        self.assertEqual(api.get_remove_emphasis_indices('**foo**bar'), [[5, 6], [0, 1]])

        # Example 377
        # Example 378
        # Example 379
        # Example 380
        # Example 381
        # Example 382
        # Example 383

        # Example 384
        self.assertEqual(api.get_remove_emphasis_indices('*foo [bar](/url)*'), [[16, 16], [0, 0]])

        # Example 385
        self.assertEqual(api.get_remove_emphasis_indices('*foo\nbar*'), [[8, 8], [0, 0]])

        # Example 386
        # Example 387
        # Example 388

        # Example 389
#        self.assertEqual(api.get_remove_emphasis_indices('*foo *bar**'), [[9, 10], [5, 5], [0, 0]])

        # Example 390
        self.assertEqual(api.get_remove_emphasis_indices('*foo **bar** baz*'), [[16, 16], [0, 0], [10, 11], [5, 6]])

        # Example 391

        # Example 392

        # Example 393

        # Example 394

        # Example 395

        # Example 396

        # Example 397

        # Example 398

        # Example 399

        # Example 400

        # Example 458

    def test_remove_html_tags(self):
        r"""Test remove html tags."""
        # Example 584
        self.assertEqual(
            api.remove_html_tags('<a><bab><c2c>', 'github'), str()
        )

        # Example 585
        self.assertEqual(
            api.remove_html_tags('<a/><b2/>', 'github'), str()
        )

        # Example 586
        self.assertEqual(
            api.remove_html_tags('<a  /><b2\ndata="foo" >', 'github'), str()
        )

        # Example 587
        self.assertEqual(
            api.remove_html_tags('<a foo="bar" bam = \'baz <em>"</em>\'\n_boolean zoop:33=zoop:33 />', 'github'), str()
        )

        # Example 588
        self.assertEqual(
            api.remove_html_tags('Foo <responsive-image src="foo.jpg" />', 'github'), 'Foo '
        )

        # Example 589
        self.assertEqual(
            api.remove_html_tags('<33> <__>', 'github'), '<33> <__>'
        )

        # Example 590
        self.assertEqual(
            api.remove_html_tags('<a h*#ref="hi">', 'github'), '<a h*#ref="hi">'
        )

        # Example 591
        self.assertEqual(
            api.remove_html_tags('<a href="hi\'> <a href=hi\'>', 'github'), '<a href="hi\'> <a href=hi\'>'
        )

        # Example 592
        self.assertEqual(
            api.remove_html_tags('< a><\nfoo><bar/ >', 'github'), '< a><\nfoo><bar/ >'
        )

        # Example 593
        self.assertEqual(
            api.remove_html_tags('<a href=\'bar\'title=title>', 'github'), '<a href=\'bar\'title=title>'
        )

        # Example 594
        self.assertEqual(
            api.remove_html_tags('</a></foo >', 'github'), str()
        )

        # Example 595
        self.assertEqual(
            api.remove_html_tags('</a href="foo">', 'github'), '</a href="foo">'
        )

        # Example 596
        self.assertEqual(
            api.remove_html_tags('foo <!-- this is a\ncomment - with hyphen -->', 'github'), 'foo '
        )

        # Example 597
        self.assertEqual(
            api.remove_html_tags('foo <!-- not a comment -- two hyphens -->', 'github'), 'foo <!-- not a comment -- two hyphens -->'
        )

        # Example 598
        self.assertEqual(
            api.remove_html_tags('foo <!--> foo -->'), 'foo <!--> foo -->'
        )
        self.assertEqual(
            api.remove_html_tags('foo <!-- foo--->'), 'foo <!-- foo--->'
        )

        # Example 599
        self.assertEqual(
            api.remove_html_tags('foo <?php echo $a; ?>', 'github'), 'foo '
        )

        # Example 600
        self.assertEqual(
            api.remove_html_tags('foo <!ELEMENT br EMPTY>', 'github'), 'foo '
        )

        # Example 601
        self.assertEqual(
            api.remove_html_tags('foo <![CDATA[>&<]]>', 'github'), 'foo '
        )

        # Example 602
        self.assertEqual(
            api.remove_html_tags('foo <a href="&ouml;">', 'github'), 'foo '
        )

        # Example 603
        self.assertEqual(
            api.remove_html_tags(r'foo <a href="\*">', 'github'), 'foo '
        )

        # Example 604
        self.assertEqual(
            api.remove_html_tags('<a href="\"">', 'github'), '<a href="\"">'
        )

        # GitHub Flavored Markdown Disallowed Raw HTML (extension).
        # See https://github.github.com/gfm/#disallowed-raw-html-extension-
        self.assertEqual(api.remove_html_tags('<title>', 'github'), '<title>')
        self.assertEqual(api.remove_html_tags('<textarea>', 'github'), '<textarea>')
        self.assertEqual(api.remove_html_tags('<style>', 'github'), '<style>')
        self.assertEqual(api.remove_html_tags('<xmp>', 'github'), '<xmp>')
        self.assertEqual(api.remove_html_tags('<iframe>', 'github'), '<iframe>')
        self.assertEqual(api.remove_html_tags('<noembed>', 'github'), '<noembed>')
        self.assertEqual(api.remove_html_tags('<noembed>', 'github'), '<noembed>')
        self.assertEqual(api.remove_html_tags('<noframes>', 'github'), '<noframes>')
        self.assertEqual(api.remove_html_tags('<script>', 'github'), '<script>')
        self.assertEqual(api.remove_html_tags('<plaintext>', 'github'), '<plaintext>')

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
        m_github = md_parser['github']['header']['max levels'] = 6

        # Example 32
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + GITHUB_LINE_FOO, m_github, 'github'),
            (1, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H2 + S1 + GITHUB_LINE_FOO, m_github, 'github'),
            (2, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + GITHUB_LINE_FOO, m_github, 'github'),
            (3, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H4 + S1 + GITHUB_LINE_FOO, m_github, 'github'),
            (4, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H5 + S1 + GITHUB_LINE_FOO, m_github, 'github'),
            (5, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H6 + S1 + GITHUB_LINE_FOO, m_github, 'github'),
            (6, GITHUB_LINE_FOO))

        # Example 33
        self.assertIsNone(
            api.get_atx_heading(H7 + S1 + GITHUB_LINE_FOO, 7, 'github'))

        # Example 34
        self.assertIsNone(
            api.get_atx_heading(H1 + GITHUB_LINE_5_BOLT, m_github, 'github'))
        self.assertIsNone(
            api.get_atx_heading(H1 + GITHUB_LINE_HASHTAG, m_github, 'github'))

        # Example 35
        self.assertIsNone(
            api.get_atx_heading(LINE_ESCAPE + H1 + S1 + GITHUB_LINE_FOO,
                                m_github, 'github'))

        # Example 36
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + GITHUB_LINE_FOO + S1 + GITHUB_LINE_BAR_BAZ, 3,
                'github'), (1, GITHUB_LINE_FOO + S1 + GITHUB_LINE_BAR_BAZ))

        # Example 37
        self.assertEqual(
            api.get_atx_heading(H1 + S18 + GITHUB_LINE_FOO + S21, m_github,
                                'github'), (1, GITHUB_LINE_FOO))

        # Example 38
        self.assertEqual(
            api.get_atx_heading(S1 + H1 + S1 + GITHUB_LINE_FOO, m_github,
                                'github'), (1, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(S2 + H1 + S1 + GITHUB_LINE_FOO, m_github,
                                'github'), (1, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(S3 + H1 + S1 + GITHUB_LINE_FOO, m_github,
                                'github'), (1, GITHUB_LINE_FOO))

        # Example 39
        self.assertIsNone(
            api.get_atx_heading(S4 + H1 + S1 + GITHUB_LINE_FOO, m_github,
                                'github'))

        # Example 40
        self.assertIsNone(
            api.get_atx_heading(GITHUB_LINE_FOO + LINE_NEWLINE + S4 + H1 + S1 + GITHUB_LINE_BAR, m_github,
                                'github'))

        # Example 41
        self.assertEqual(
            api.get_atx_heading(H2 + S1 + GITHUB_LINE_FOO + S1 + H2, m_github,
                                'github'), (2, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(S2 + H3 + S3 + GITHUB_LINE_BAR + S4 + H3,
                                m_github, 'github'), (3, GITHUB_LINE_BAR))

        # Example 42
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + GITHUB_LINE_FOO + S1 + H34, m_github,
                                'github'), (1, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(H5 + S1 + GITHUB_LINE_FOO + S1 + H2, m_github,
                                'github'), (5, GITHUB_LINE_FOO))

        # Extra test.
        self.assertIsNone(api.get_atx_heading(H5 * 7, m_github, 'github'))

        # Example 43
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + GITHUB_LINE_FOO + S1 + H3 + S5,
                                m_github, 'github'), (3, GITHUB_LINE_FOO))

        # Example 44
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + GITHUB_LINE_FOO + S1 + H3 + S1 + GITHUB_LINE_B,
                m_github, 'github'),
            (3, GITHUB_LINE_FOO + S1 + H3 + S1 + GITHUB_LINE_B))

        # Example 45
        self.assertEqual(
            api.get_atx_heading(H1 + S1 + GITHUB_LINE_FOO + H1, m_github,
                                'github'), (1, GITHUB_LINE_FOO + H1))

        # Example 46
        # Preserve the backslashes unlike the original example so that they
        # conform to the original ATX header.
        # See
        # https://github.com/github/cmark-gfm/blob/6b101e33ba1637e294076c46c69cd6a262c7539f/src/inlines.c#L756
        # and
        # https://spec.commonmark.org/0.28/#ascii-punctuation-character
        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + GITHUB_LINE_FOO + S1 + LINE_ESCAPE + H3, m_github,
                'github'), (3, GITHUB_LINE_FOO + S1 + LINE_ESCAPE + H3))
        self.assertEqual(
            api.get_atx_heading(
                H2 + S1 + GITHUB_LINE_FOO + S1 + H1 + LINE_ESCAPE + H2,
                m_github, 'github'),
            (2, GITHUB_LINE_FOO + S1 + H1 + LINE_ESCAPE + H2))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + GITHUB_LINE_FOO + S1 + LINE_ESCAPE + H1, m_github,
                'github'), (1, GITHUB_LINE_FOO + S1 + LINE_ESCAPE + H1))

        # Example 47 and 48 are not relevant for this function.

        # Example 49
        self.assertEqual(
            api.get_atx_heading(H2 + S1, m_github, 'github', True),
            (2, LINE_EMPTY))
        self.assertEqual(
            api.get_atx_heading(H1, m_github, 'github', True), (1, LINE_EMPTY))
        self.assertEqual(
            api.get_atx_heading(H3 + S1 + H3, m_github, 'github', True),
            (3, LINE_EMPTY))

        # Example 49 with link labels.
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
                H1 + S1 + LINE_SQUARE_BRACKET_OPEN + S1 + GITHUB_LINE_FOO + S1
                + LINE_SQUARE_BRACKET_OPEN + GITHUB_LINE_BAR +
                LINE_SQUARE_BRACKET_CLOSE + LINE_SQUARE_BRACKET_CLOSE,
                m_github, 'github'),
            (1, LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN + S1 + GITHUB_LINE_FOO +
             S1 + LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN + GITHUB_LINE_BAR +
             LINE_ESCAPE + LINE_SQUARE_BRACKET_CLOSE + LINE_ESCAPE +
             LINE_SQUARE_BRACKET_CLOSE))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + LINE_ESCAPE + LINE_ESCAPE + LINE_SQUARE_BRACKET_OPEN
                + S1 + GITHUB_LINE_FOO, m_github, 'github'),
            (1, LINE_ESCAPE + LINE_ESCAPE + LINE_ESCAPE +
             LINE_SQUARE_BRACKET_OPEN + S1 + GITHUB_LINE_FOO))

        # Test escape character space workaround.
        self.assertEqual(
            api.get_atx_heading(H2 + S1 + GITHUB_LINE_FOO + LINE_ESCAPE,
                                m_github, 'github'),
            (2, GITHUB_LINE_FOO + LINE_ESCAPE + S1))

        # Test MD_PARSER_GITHUB_MAX_CHARS_LINK_LABEL
        with self.assertRaises(exceptions.GithubOverflowCharsLinkLabel):
            api.get_atx_heading(H1 + S1 + GITHUB_LINE_1000_CHARS, m_github,
                                'github')

        # Test an empty line.
        self.assertIsNone(api.get_atx_heading(LINE_EMPTY, m_github, 'github'))

        # Test line endings.
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_NEWLINE, m_github, 'github', True),
            (1, LINE_EMPTY))
        self.assertEqual(
            api.get_atx_heading(H1 + LINE_CARRIAGE_RETURN, m_github, 'github',
                                True), (1, LINE_EMPTY))

        # CRLF marker tests.
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + GITHUB_LINE_FOO + LINE_NEWLINE + GITHUB_LINE_FOO,
                m_github, 'github'), (1, GITHUB_LINE_FOO))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + GITHUB_LINE_FOO + LINE_CARRIAGE_RETURN +
                GITHUB_LINE_FOO, m_github, 'github'), (1, GITHUB_LINE_FOO))

        # Test line endings with link labels.
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H1 + LINE_NEWLINE, m_github, 'github', False)
        with self.assertRaises(exceptions.GithubEmptyLinkLabel):
            api.get_atx_heading(H1 + LINE_CARRIAGE_RETURN, m_github, 'github',
                                False)

        # readcarpet
        # It does not seem that there are exaustive tests so we have to invent
        # our own. See https://github.com/vmg/redcarpet/tree/master/test
        # for more information.
        m_redcarpet = md_parser['redcarpet']['header']['max levels'] = 6

        self.assertIsNone(
            api.get_atx_heading(S1 + H1 + S1 + REDCARPET_LINE_FOO, m_redcarpet,
                                'redcarpet'))

        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO, m_redcarpet,
                                'redcarpet'), (1, REDCARPET_LINE_FOO))

        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO + S1 + H1,
                                m_redcarpet, 'redcarpet'),
            (1, REDCARPET_LINE_FOO))

        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO + S1 + H3,
                                m_redcarpet, 'redcarpet'),
            (1, REDCARPET_LINE_FOO))

        self.assertEqual(
            api.get_atx_heading(
                H3 + S1 + REDCARPET_LINE_FOO + S1 + H3 + LINE_NEWLINE,
                m_redcarpet, 'redcarpet'), (3, REDCARPET_LINE_FOO))

        self.assertEqual(
            api.get_atx_heading(H1 + S1 + REDCARPET_LINE_FOO + S1 + H3 + S1,
                                m_redcarpet, 'redcarpet'),
            (1, REDCARPET_LINE_FOO + S1 + H3))

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + S1 + H1 + LINE_ESCAPE +
                LINE_ESCAPE + H2, m_redcarpet, 'redcarpet'),
            (1, REDCARPET_LINE_FOO + S1 + H1 + LINE_ESCAPE + LINE_ESCAPE))

        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + H1 + LINE_ESCAPE + H1 + S1 + H1,
                m_redcarpet, 'redcarpet'),
            (1, REDCARPET_LINE_FOO + H1 + LINE_ESCAPE + H1))

        # Test escape character space workaround.
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + S1 + LINE_ESCAPE, m_redcarpet,
                'redcarpet'), (1, REDCARPET_LINE_FOO + S1 + LINE_ESCAPE + S1))

        # Test an empty line.
        self.assertIsNone(
            api.get_atx_heading(LINE_EMPTY, m_redcarpet, 'redcarpet'))

        # Test newline.
        self.assertIsNone(
            api.get_atx_heading(H1 + LINE_NEWLINE, m_redcarpet, 'redcarpet'))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + LINE_NEWLINE +
                REDCARPET_LINE_FOO, m_redcarpet, 'redcarpet'),
            (1, REDCARPET_LINE_FOO))
        self.assertIsNone(
            api.get_atx_heading(H1 + LINE_CARRIAGE_RETURN, m_redcarpet,
                                'redcarpet'))
        self.assertEqual(
            api.get_atx_heading(
                H1 + S1 + REDCARPET_LINE_FOO + LINE_CARRIAGE_RETURN +
                REDCARPET_LINE_FOO, m_redcarpet, 'redcarpet'),
            (1,
             REDCARPET_LINE_FOO + LINE_CARRIAGE_RETURN + REDCARPET_LINE_FOO))

    @unittest.skip("empty test")
    def test_get_md_header(self):
        r"""Test building of the header data structure.

        There is no need to test this since it is a wrapper for several
        other functions. None is retruned when get_md_header_type
        returns None.
        """

    def test_is_opening_code_fence(self):
        r"""Test detection of opening code fence."""
        # github.
        # Generic, spaces and headings. These are not code fences.
        self.assertIsNone(api.is_opening_code_fence(LINE))
        self.assertIsNone(api.is_opening_code_fence(LINE_EMPTY))
        self.assertIsNone(api.is_opening_code_fence(GITHUB_LINE_FOO))
        self.assertIsNone(
            api.is_opening_code_fence(GITHUB_LINE_FOO + LINE_NEWLINE))

        self.assertIsNone(api.is_opening_code_fence(S1))
        self.assertIsNone(api.is_opening_code_fence(S2))
        self.assertIsNone(api.is_opening_code_fence(S3))
        self.assertIsNone(api.is_opening_code_fence(S4))
        self.assertIsNone(api.is_opening_code_fence(S10))

        self.assertIsNone(api.is_opening_code_fence(H1))
        self.assertIsNone(api.is_opening_code_fence(H2))
        self.assertIsNone(api.is_opening_code_fence(H3))
        self.assertIsNone(api.is_opening_code_fence(H4))
        self.assertIsNone(api.is_opening_code_fence(H5))
        self.assertIsNone(api.is_opening_code_fence(H6))
        self.assertIsNone(api.is_opening_code_fence(H7))

        # Example 88.
        # Base case: no info string.
        # https://github.github.com/gfm/#example-88
        self.assertEqual(api.is_opening_code_fence(BACKTICK3), BACKTICK3)
        self.assertEqual(api.is_opening_code_fence(BACKTICK4), BACKTICK4)
        self.assertEqual(api.is_opening_code_fence(BACKTICK10), BACKTICK10)

        # Example 89.
        # https://github.github.com/gfm/#example-89
        self.assertEqual(api.is_opening_code_fence(TILDE3), TILDE3)
        self.assertEqual(api.is_opening_code_fence(TILDE4), TILDE4)
        self.assertEqual(api.is_opening_code_fence(TILDE10), TILDE10)

        # Example 90.
        # Backticks and tildes.
        # https://github.github.com/gfm/#example-90
        self.assertIsNone(api.is_opening_code_fence(BACKTICK1))
        self.assertIsNone(api.is_opening_code_fence(BACKTICK2))
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK2 + GITHUB_LINE_FOO))
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK2 + LINE_NEWLINE + BACKTICK1))

        self.assertIsNone(api.is_opening_code_fence(TILDE1))
        self.assertIsNone(api.is_opening_code_fence(TILDE2))
        self.assertIsNone(api.is_opening_code_fence(TILDE2 + GITHUB_LINE_FOO))
        self.assertIsNone(
            api.is_opening_code_fence(TILDE2 + LINE_NEWLINE + TILDE1))

        # Example 91->97 see test_is_closing_code_fence.

        # Example 98.
        # https://github.github.com/gfm/#example-98
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + LINE_NEWLINE + LINE_NEWLINE +
                                      S2), BACKTICK3)

        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + LINE_NEWLINE + LINE_NEWLINE +
                                      S2), TILDE3)

        # Example 99.
        # https://github.github.com/gfm/#example-99
        # See example 88.

        # Indentation.
        # Example 100.
        # https://github.github.com/gfm/#example-100
        self.assertEqual(api.is_opening_code_fence(S1 + BACKTICK3), BACKTICK3)

        self.assertEqual(api.is_opening_code_fence(S1 + TILDE3), TILDE3)

        # Example 101.
        # https://github.github.com/gfm/#example-101
        self.assertEqual(api.is_opening_code_fence(S2 + BACKTICK3), BACKTICK3)

        self.assertEqual(api.is_opening_code_fence(S2 + TILDE3), TILDE3)

        # Example 102.
        # https://github.github.com/gfm/#example-102
        self.assertEqual(api.is_opening_code_fence(S3 + BACKTICK3), BACKTICK3)

        self.assertEqual(api.is_opening_code_fence(S3 + TILDE3), TILDE3)

        # Example 103.
        # https://github.github.com/gfm/#example-103
        self.assertIsNone(api.is_opening_code_fence(S4 + BACKTICK3))

        self.assertIsNone(api.is_opening_code_fence(S4 + TILDE3))

        # An extension of examples 100 -> 103.
        self.assertEqual(api.is_opening_code_fence(S3 + BACKTICK3), BACKTICK3)
        self.assertEqual(api.is_opening_code_fence(S3 + BACKTICK4), BACKTICK4)
        self.assertEqual(
            api.is_opening_code_fence(S3 + BACKTICK10), BACKTICK10)

        self.assertEqual(api.is_opening_code_fence(S3 + TILDE3), TILDE3)
        self.assertEqual(api.is_opening_code_fence(S3 + TILDE4), TILDE4)
        self.assertEqual(api.is_opening_code_fence(S3 + TILDE10), TILDE10)

        # Example 104 -> 106 see test_is_closing_code_fence.

        # Example 107.
        # https://github.github.com/gfm/#example-107
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK3 + S1 + BACKTICK3))

        self.assertIsNone(api.is_opening_code_fence(TILDE3 + S1 + TILDE3))

        # Example 108 see test_is_closing_code_fence.

        # Example 109 -> 110 are not relevant.

        # Example 111.
        # https://github.github.com/gfm/#example-111
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK3 + GITHUB_INFO_STRING_FOO),
            BACKTICK3)

        self.assertEqual(
            api.is_opening_code_fence(TILDE3 + GITHUB_INFO_STRING_FOO), TILDE3)

        # Expansion of example 111.
        # Info string.
        # https://github.github.com/gfm/#example-111
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK4 + GITHUB_INFO_STRING_FOO),
            BACKTICK4)
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK10 + GITHUB_INFO_STRING_FOO),
            BACKTICK10)

        self.assertEqual(
            api.is_opening_code_fence(TILDE4 + GITHUB_INFO_STRING_FOO), TILDE4)
        self.assertEqual(
            api.is_opening_code_fence(TILDE10 + GITHUB_INFO_STRING_FOO),
            TILDE10)

        # Example 112.
        # Info string with garbage and foreign character.
        # https://github.github.com/gfm/#example-112
        self.assertEqual(
            api.is_opening_code_fence(BACKTICK4 + S4 + GITHUB_INFO_STRING_FOO +
                                      S1 + GITHUB_INFO_STRING_GARBAGE),
            BACKTICK4)

        self.assertEqual(
            api.is_opening_code_fence(TILDE4 + S4 + GITHUB_INFO_STRING_FOO +
                                      S1 + GITHUB_INFO_STRING_GARBAGE), TILDE4)

        # Example 113.
        # https://github.github.com/gfm/#example-113
        self.assertEqual(api.is_opening_code_fence(BACKTICK4 + ';'), BACKTICK4)

        self.assertEqual(api.is_opening_code_fence(TILDE4 + ';'), TILDE4)

        # Example 114.
        # https://github.github.com/gfm/#example-114
        self.assertIsNone(
            api.is_opening_code_fence(BACKTICK3 + S1 + 'aa' + S1 + BACKTICK3))

        self.assertIsNone(
            api.is_opening_code_fence(TILDE3 + S1 + 'aa' + S1 + TILDE3))

        # Example 115 see test_is_closing_code_fence.

    def test_is_closing_code_fence(self):
        r"""Test detection of closing code fence."""
        # github.
        # Example 91.
        # https://github.github.com/gfm/#example-91
        self.assertFalse(api.is_closing_code_fence(BACKTICK3, TILDE3))

        # Example 92.
        # https://github.github.com/gfm/#example-92
        self.assertFalse(api.is_closing_code_fence(TILDE3, BACKTICK3))

        # Example 93.
        # https://github.github.com/gfm/#example-93
        # "The closing code fence must be at least as long as the opening
        #  fence."
        self.assertFalse(api.is_closing_code_fence(BACKTICK3, BACKTICK4))

        # Example 94.
        # https://github.github.com/gfm/#example-94
        self.assertFalse(api.is_closing_code_fence(TILDE3, TILDE4))

        # Example 95.
        # https://github.github.com/gfm/#example-95
        self.assertTrue(api.is_closing_code_fence(LINE_EMPTY, BACKTICK3, True))

        self.assertTrue(api.is_closing_code_fence(LINE_EMPTY, TILDE3, True))

        # Example 96.
        # https://github.github.com/gfm/#example-96
        self.assertTrue(
            api.is_closing_code_fence(LINE_NEWLINE + BACKTICK3 + 'aaa',
                                      BACKTICK5, True))

        self.assertTrue(
            api.is_closing_code_fence(LINE_NEWLINE + TILDE3 + 'aaa', TILDE5,
                                      True))

        # Example 97 not relevant.

        # Example 104.
        # https://github.github.com/gfm/#example-104
        self.assertTrue(api.is_closing_code_fence(S2 + BACKTICK3, BACKTICK3))

        self.assertTrue(api.is_closing_code_fence(S2 + TILDE3, TILDE3))

        # Example 105.
        # https://github.github.com/gfm/#example-105
        self.assertTrue(
            api.is_closing_code_fence(S2 + BACKTICK3, S3 + BACKTICK3))

        self.assertTrue(api.is_closing_code_fence(S2 + TILDE3, S3 + TILDE3))

        # Example 106.
        # https://github.github.com/gfm/#example-106
        self.assertFalse(api.is_closing_code_fence(S4 + BACKTICK3, BACKTICK3))

        self.assertFalse(api.is_closing_code_fence(S4 + TILDE3, TILDE3))

        # Example 108.
        # https://github.github.com/gfm/#example-108
        self.assertFalse(
            api.is_closing_code_fence(TILDE3 + S1 + TILDE2, TILDE6))

        self.assertFalse(
            api.is_closing_code_fence(BACKTICK3 + S1 + BACKTICK2, BACKTICK6))

        # Example 115.
        # https://github.github.com/gfm/#example-115
        self.assertFalse(
            api.is_closing_code_fence(BACKTICK3 + S1 + 'aaa', BACKTICK3))

        self.assertFalse(
            api.is_closing_code_fence(TILDE3 + S1 + 'aaa', TILDE3))

    @unittest.skip("empty test")
    def test_init_indentation_status_list(self):
        r"""Test building of the indentation data structure.

        There is no need to test this since it is a trivial function.
        """

    def _test_helper_toc_renders_as_coherent_list(
            self, header_type_curr, header_type_first, indentation_list,
            expected_indentation_list, expected_result):
        result = api.toc_renders_as_coherent_list(
            header_type_curr, header_type_first, indentation_list)
        self.assertEqual(result, expected_result)
        self.assertEqual(indentation_list, expected_indentation_list)

    def test_toc_renders_as_coherent_list(self):
        r"""Test if the TOC renders as a list the user intended."""
        # github and redcarpet.

        # 1. header_type_first = 1; header_type_curr = 1.
        expected_indentation_list = [True, False, False, False, False, False]
        self._test_helper_toc_renders_as_coherent_list(
            BASE_CASE_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR,
            BASE_CASE_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_FIRST,
            api.init_indentation_status_list('github'),
            expected_indentation_list, True)

        # 2. header_type_first = 1; header_type_curr = generic > 1.
        indentation_list = api.init_indentation_status_list('github')
        for i in range(0, GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR - 1):
            indentation_list[i] = True
        expected_indentation_list = [True, True, True, True, False, False]
        self._test_helper_toc_renders_as_coherent_list(
            GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR,
            BASE_CASE_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_FIRST,
            indentation_list, expected_indentation_list, True)

        # 3. header_type_first = generic > 1; header_type_curr = 1.
        indentation_list = api.init_indentation_status_list('github')
        expected_indentation_list = [True, False, False, False, False, False]
        self._test_helper_toc_renders_as_coherent_list(
            BASE_CASE_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR,
            GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_FIRST, indentation_list,
            expected_indentation_list, False)

        # 4. header_type_first = generic > 1; header_type_curr = generic > 1; header_type_curr > header_type_first.
        indentation_list = api.init_indentation_status_list('github')
        indentation_list[GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_FIRST -
                         1] = True
        expected_indentation_list = [False, False, False, True, True, False]
        self._test_helper_toc_renders_as_coherent_list(
            GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR_BIS,
            GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_FIRST, indentation_list,
            expected_indentation_list, True)

        # 4. header_type_first = generic > 1; header_type_curr = generic > 1; header_type_curr == header_type_first.
        indentation_list = api.init_indentation_status_list('github')
        indentation_list[GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR -
                         1] = True
        expected_indentation_list = [False, False, False, True, False, False]
        self._test_helper_toc_renders_as_coherent_list(
            GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR,
            GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR, indentation_list,
            expected_indentation_list, True)

        # 5. header_type_first = generic > 1; header_type_curr = generic > 1; header_type_curr < header_type_first.
        indentation_list = api.init_indentation_status_list('github')
        indentation_list[GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR_BIS -
                         1] = True
        expected_indentation_list = [False, False, False, True, False, False]
        self._test_helper_toc_renders_as_coherent_list(
            GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_FIRST,
            GENERIC_GITHUB_RENDERS_AS_LIST_HEADER_TYPE_CURR_BIS,
            indentation_list, expected_indentation_list, False)


if __name__ == '__main__':
    unittest.main()
