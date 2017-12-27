# L+C
"""The tests module."""

from md_toc import api, exceptions
from slugify import slugify
import string
import random
import unittest
from unittest.mock import patch, mock_open
import sys

RANDOM_STRING_LENGTH = 32


# Note:
# To preserve the success of the tests,
# these generate_* functions are
# not to be modified.
def generate_fake_markdown_file_with_no_toc_markers():
    """Refer to the non-toc marker version."""
    DATA_TO_BE_READ = '''\
# One\n\
## One.Two\n\
'''
    return DATA_TO_BE_READ


def generate_fake_toc_non_ordered_no_toc_markers():
    """Refer to the non-toc marker version."""
    TOC = '''\
- [One](one)\n\
    - [One.Two](one-two)\n\
'''
    return TOC


def generate_fake_toc_ordered_no_toc_markers():
    """Refer to the non-toc marker version."""
    TOC = '''\
1. [One](one)\n\
    1. [One.Two](one-two)\n\
'''
    return TOC


def generate_fake_markdown_file_with_one_toc_marker():
    """Refer to the one marker non-ordered version."""
    DATA_TO_BE_READ = '''\
# One\n\
Hello, this is some content\n\
[](TOC)\n\
This is some more content\n\
Bye\n\
## One.Two\n\
'''
    return DATA_TO_BE_READ


def generate_fake_toc_non_ordered_one_toc_marker():
    """Refer to the one marker ordered version."""
    TOC = '''\
- [One](one)\n\
    - [One.Two](one-two)\n\
'''
    return TOC


def generate_fake_markdown_file_with_two_toc_markers():
    """Refer to the two marker ordered version."""
    DATA_TO_BE_READ = '''\
# Toc\n\
Hello, this is some content for the two markers version\n\
[](TOC)\n\
- [Toc](toc)
- [One](one)
    - [One.Two](one-two)
[](TOC)\n\
# One\n\
## One.Two\n\
End of toc\n\
'''
    return DATA_TO_BE_READ


def generate_fake_toc_non_ordered_two_toc_markers():
    """Refer to the two marker version."""
    TOC = '''\
- [Toc](tocddddddddddddddddddddd)\n\
- [One](one)\n\
    - [One.Two](one-two)\n\
'''
    return TOC


class TestApi(unittest.TestCase):
    """Pass."""

    def test_get_md_header(self):
        """Pass."""
        test_text = ''.join([
            random.choice(string.printable)
            for n in range(RANDOM_STRING_LENGTH)
        ])
        # Remove any leading '#' character that might pollute the tests.
        test_text = test_text.lstrip('#')

        # Test an empty string
        self.assertEqual(api.get_md_heading(''), None)

        # Test for a string without headers
        self.assertEqual(api.get_md_heading(test_text.replace('#', '')), None)
        # Note that we need to compare the test_text as input with
        # test_text.strip() as output, since the string is stripped inside
        # the method

        # Test h1
        self.assertEqual(
            api.get_md_heading('#' + test_text), {
                'type': 1,
                'text_original': test_text.strip(),
                'text_slugified': slugify(test_text)
            })
        self.assertEqual(
            api.get_md_heading('# ' + test_text), {
                'type': 1,
                'text_original': test_text.strip(),
                'text_slugified': slugify(test_text)
            })

        # Test h2
        self.assertEqual(
            api.get_md_heading('##' + test_text), {
                'type': 2,
                'text_original': test_text.strip(),
                'text_slugified': slugify(test_text)
            })
        self.assertEqual(
            api.get_md_heading('## ' + test_text), {
                'type': 2,
                'text_original': test_text.strip(),
                'text_slugified': slugify(test_text)
            })

        # Test h3
        self.assertEqual(
            api.get_md_heading('###' + test_text), {
                'type': 3,
                'text_original': test_text.strip(),
                'text_slugified': slugify(test_text)
            })
        self.assertEqual(
            api.get_md_heading('### ' + test_text), {
                'type': 3,
                'text_original': test_text.strip(),
                'text_slugified': slugify(test_text)
            })

        # Test h whith h > h3
        self.assertEqual(api.get_md_heading('####' + test_text), None)
        self.assertEqual(api.get_md_heading('#### ' + test_text), None)

    def _test_build_toc_line_common(self, text, header, indentation_space):
        md_substring = '[' + text.strip() + '](' + slugify(text) + ')'
        # Test both ordered and non ordered markdown toc.
        md_non_num_substring = '- ' + md_substring
        md_num_substring = '1. ' + md_substring
        self.assertEqual(
            api.build_toc_line(header),
            indentation_space + md_non_num_substring)
        self.assertEqual(
            api.build_toc_line(header, 1),
            indentation_space + md_num_substring)

    def test_build_toc_line(self):
        """Pass."""
        test_text = ''.join([
            random.choice(string.printable)
            for n in range(RANDOM_STRING_LENGTH)
        ])
        # Remove any leading '#' character that might pollute the tests.
        test_text = test_text.lstrip('#')

        # Test an empty header (originated from a non-title line).
        self.assertEqual(api.build_toc_line(None), None)

        h = {
            'type': 1,
            'text_original': test_text.strip(),
            'text_slugified': slugify(test_text)
        }

        # Test h1
        h['type'] = 1
        indentation_space = 0 * ' '
        self._test_build_toc_line_common(test_text, h, indentation_space)

        # Test h2
        h['type'] = 2
        indentation_space = 4 * ' '
        self._test_build_toc_line_common(test_text, h, indentation_space)

        # Test h3
        h['type'] = 3
        indentation_space = 8 * ' '
        self._test_build_toc_line_common(test_text, h, indentation_space)

    def test_increment_index_ordered_list(self):
        """Pass."""
        ht = {
            '1': 0,
            '2': 0,
            '3': 0,
        }
        ht_prev = None
        ht_curr = None

        # Test the base case
        ht_prev = None
        ht_curr = 1
        api.increment_index_ordered_list(ht, ht_prev, ht_curr)
        self.assertEqual(ht['1'], 1)

        # Test two equal header types.
        ht['1'] = 1
        ht_curr = 1
        ht_prev = 1
        api.increment_index_ordered_list(ht, ht_prev, ht_curr)
        self.assertEqual(ht['1'], 2)

        # Test two different header types.
        ht['1'] = 1
        ht['2'] = 1
        ht['3'] = 2
        ht_curr = 2
        ht_prev = 3
        api.increment_index_ordered_list(ht, ht_prev, ht_curr)
        self.assertEqual(ht['2'], 2)

    def test_build_toc_non_ordered(self):
        """Pass."""
        # Test non-ordered lists.
        with patch(
                'builtins.open',
                mock_open(
                    read_data=generate_fake_markdown_file_with_no_toc_markers(
                    ))):
            toc = api.build_toc('foo.md')
        self.assertEqual(toc, generate_fake_toc_non_ordered_no_toc_markers())

        # Test ordered lists.
        with patch(
                'builtins.open',
                mock_open(
                    read_data=generate_fake_markdown_file_with_no_toc_markers(
                    ))):
            toc = api.build_toc('foo.md', ordered=True)
        self.assertEqual(toc, generate_fake_toc_ordered_no_toc_markers())

    def test_write_toc_on_md_file(self):
        """Pass."""
        # Case 1: No toc marker in file: nothing to do.
        with patch(
                'builtins.open',
                mock_open(
                    read_data=generate_fake_markdown_file_with_no_toc_markers(
                    ))) as m0:
            toc = generate_fake_toc_non_ordered_no_toc_markers()
            api.write_toc_on_md_file('foo.md', toc, in_place=True)
        #    assert not called write (insert nor delete).
        assert 'call().readline()' not in m0.mock_calls

        # Case 2: 1 toc marker: Insert the toc in that position.
        #         assert not called write (delete): assert not called write with toc
        #         as argument
        with patch(
                'builtins.open',
                mock_open(
                    read_data=generate_fake_markdown_file_with_one_toc_marker(
                    ))) as m1:
            toc = generate_fake_toc_non_ordered_one_toc_marker()
            api.write_toc_on_md_file('foo.md', toc, in_place=True)
        assert "call().write('" + toc + "')" not in m1.mock_calls

        # Case 3: 2 toc markers: replace old toc with new one.
        # assert called write (insert and delete)
        mock_write_call_index = 32
        with patch(
                'builtins.open',
                mock_open(
                    read_data=generate_fake_markdown_file_with_two_toc_markers(
                    ))) as m2:
            toc = generate_fake_toc_non_ordered_two_toc_markers()
            api.write_toc_on_md_file('foo.md', toc, in_place=True)
        expected_string = r"call().write('[](TOC)\n\n" + repr(
            toc) + r"\n[](TOC)\n')"
        treated_expected_string = repr(expected_string).replace("'", "")
        treated_result = repr(str(
            m2.mock_calls[mock_write_call_index])).replace("'", "")
        self.assertEqual(treated_expected_string, treated_result)

        # Note: we don't need to test the non-inplace flow since it only
        # concatenates two strings


if __name__ == '__main__':
    unittest.main()
