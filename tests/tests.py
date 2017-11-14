from md_toc import api
from slugify import slugify
import string
import random
import unittest
from unittest.mock import patch, mock_open
import sys

ITERATION_TESTS = 256
RANDOM_STRING_LENGTH = 256

def generate_fake_markdown_file_as_string():
    data_to_be_read = '''# One\n## One.Two\n'''

    return data_to_be_read

def generate_fake_toc_non_ordered():

    fake_toc = '''- [One](one)\n    - [One.Two](one-two)\n'''

    return fake_toc

def generate_fake_toc_ordered():

    fake_toc = '''1. [One](one)\n    1. [One.Two](one-two)\n'''

    return fake_toc

def generate_fake_markdown_file_with_one_toc_marker_as_string():
    data_to_be_read = '''\
# One\n\
## One.Two\n\
Hello, this is some content\n\
[](TOC)\n\
This is some more content\n\
Bye\n\
'''
    return data_to_be_read

def generate_fake_markdown_file_with_two_toc_markers_as_string():
    data_to_be_read = '''\
# One\n\
## One.Two\n\
Hello, this is some content\n\
[](TOC)\n\
This is some more content\n\
Bye\n\
And again let there be\n\
more\n\
content.\n\
[](TOC)\n\
End of toc\n\
'''
    return data_to_be_read


class TestApi(unittest.TestCase):

    def test_get_md_header(self):
        i = 0
        while i < ITERATION_TESTS:
            test_text = ''.join([random.choice(string.printable) for n in range(RANDOM_STRING_LENGTH)])
            # Remove any leading '#' character that might pollute the tests.
            test_text = test_text.lstrip('#')

            # Test an empty string
            self.assertEqual(api.get_md_heading(''),None)

            # Test for a string without headers
            self.assertEqual(api.get_md_heading(test_text.replace('#','')),None)

            # Note that we need to compare the test_text as input with
            # test_text.strip() as output, since the string is stripped inside
            # the method

            # Test h1
            self.assertEqual(api.get_md_heading('#' + test_text),
{'type':1,'text_original':test_text.strip(),'text_slugified':slugify(test_text)})
            self.assertEqual(api.get_md_heading('# ' + test_text),
{'type':1,'text_original':test_text.strip(),'text_slugified':slugify(test_text)})

            # Test h2
            self.assertEqual(api.get_md_heading('##' + test_text),
{'type':2,'text_original':test_text.strip(),'text_slugified':slugify(test_text)})
            self.assertEqual(api.get_md_heading('## ' + test_text),
{'type':2,'text_original':test_text.strip(),'text_slugified':slugify(test_text)})

            # Test h3
            self.assertEqual(api.get_md_heading('###' + test_text),
{'type':3,'text_original':test_text.strip(),'text_slugified':slugify(test_text)})
            self.assertEqual(api.get_md_heading('### ' + test_text),
{'type':3,'text_original':test_text.strip(),'text_slugified':slugify(test_text)})

            # Test h whith h > h3
            self.assertEqual(api.get_md_heading('####'+test_text),None)
            self.assertEqual(api.get_md_heading('#### '+test_text),None)

            i+=1

    def _test_build_toc_line_common(self,text,header,indentation_space):
        md_substring = '[' + text.strip() + '](' + slugify(text) + ')'
        # Test both ordered and non ordered markdown toc.
        md_non_num_substring = '- ' + md_substring
        md_num_substring = '1. ' + md_substring
        self.assertEqual(api.build_toc_line(header),indentation_space + md_non_num_substring)
        self.assertEqual(api.build_toc_line(header,1),indentation_space + md_num_substring)


    def test_build_toc_line(self):
        i = 0
        while i < ITERATION_TESTS:
            test_text = ''.join([random.choice(string.printable) for n in range(RANDOM_STRING_LENGTH)])
            # Remove any leading '#' character that might pollute the tests.
            test_text = test_text.lstrip('#')

            # Test an empty header (originated from a non-title line).
            self.assertEqual(api.build_toc_line(None),None)

            h = {'type':1,
                  'text_original':test_text.strip(),
                  'text_slugified':slugify(test_text)}

            # Test h1
            h['type'] = 1
            indentation_space = 0*' '
            self._test_build_toc_line_common(test_text,h,indentation_space)

            # Test h2
            h['type'] = 2
            indentation_space = 4*' '
            self._test_build_toc_line_common(test_text,h,indentation_space)

            # Test h3
            h['type'] = 3
            indentation_space = 8*' '
            self._test_build_toc_line_common(test_text,h,indentation_space)

            i += 1

    def test_increment_index_ordered_list(self):
        ht = {
            '1': 0,
            '2': 0,
            '3': 0,
        }
        ht_prev=None
        ht_curr=None

        # Test the base case
        ht_prev=None
        ht_curr=1
        api.increment_index_ordered_list(ht,ht_prev,ht_curr)
        self.assertEqual(ht['1'],1)

        # Test two equal header types.
        ht['1'] = 1
        ht_curr = 1
        ht_prev = 1
        api.increment_index_ordered_list(ht,ht_prev,ht_curr)
        self.assertEqual(ht['1'],2)

        # Test two different header types.
        ht['1'] = 1
        ht['2'] = 1
        ht['3'] = 2
        ht_curr = 2
        ht_prev = 3
        api.increment_index_ordered_list(ht,ht_prev,ht_curr)
        self.assertEqual(ht['2'],2)

    def test_build_toc_non_ordered(self):
        # Test non-ordered lists.
        with patch('builtins.open', mock_open(read_data=generate_fake_markdown_file_as_string())) as m:
            toc = api.build_toc('foo.md')
        self.assertEqual(toc,generate_fake_toc_non_ordered())

        # Test ordered lists.
        with patch('builtins.open', mock_open(read_data=generate_fake_markdown_file_as_string())) as m:
            toc = api.build_toc('foo.md',ordered=True)
        self.assertEqual(toc,generate_fake_toc_ordered())

    def test_get_toc_markers_line_positions(self):
        # Test zero markers.
        with patch('builtins.open', mock_open(read_data=generate_fake_markdown_file_as_string())) as m:
           markers = api.get_toc_markers_line_positions('foo.md',toc_marker='[](TOC)')
        self.assertEqual(markers,{'first':None , 'second':None })

        # Test one marker.
        with patch('builtins.open', mock_open(read_data=generate_fake_markdown_file_with_one_toc_marker_as_string())) as m: 
           markers = api.get_toc_markers_line_positions('foo.md',toc_marker='[](TOC)')
        self.assertEqual(markers,{'first':4 , 'second':None })

        # Test two (or more) markers.
        with patch('builtins.open', mock_open(read_data=generate_fake_markdown_file_with_two_toc_markers_as_string())) as m: 
           markers = api.get_toc_markers_line_positions('foo.md',toc_marker='[](TOC)')
        self.assertEqual(markers,{'first':4 , 'second':10 })



if __name__ == '__main__':
    unitttest.main()
