from md_toc import api
from slugify import slugify
import string
import random
import unittest
import sys

ITERATION_TESTS = 1024
RANDOM_STRING_LENGTH = 512

class TestApi(unittest.TestCase):

    def test_m_get_md_header(self):
        test_text = '# #ciao # bau'
        test_text = test_text.lstrip('#')
#        test_text = test_text.strip()
        print(test_text)

        self.assertEqual(api.get_md_heading('#' + test_text),
           {'type':1,'text_original':test_text.strip(),'text_slugified':slugify(test_text)})

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

    def test_build_toc_line(self):
            test_text = ''.join([random.choice(string.printable) for n in range(RANDOM_STRING_LENGTH)])
            # Remove any leading '#' character that might pollute the tests.
            test_text = test_text.lstrip('#')

            # Test an empty header (originated from a non-title line).
            self.assertEqual(api.build_toc_line(None),None)

            h = {'type':1,
                  'text_original':test_text.strip(),
                  'text_slugified':slugify(test_text)}
            md_substring = '[' + test_text.strip() + '](' + slugify(test_text) + ')'
            # Test both numeric and non numeric markdown toc.
            md_non_num_substring = '- ' + md_substring
            md_num_substring = '1. ' + md_substring

            # Test h1
            h['type'] = 1
            indentation_space = 0*' '
            self.assertEqual(api.build_toc_line(h),
indentation_space + md_non_num_substring)
            self.assertEqual(api.build_toc_line(h,1),
indentation_space + md_num_substring)

            # Test h2
            h['type'] = 2
            indentation_space = 4*' '
            self.assertEqual(api.build_toc_line(h),
indentation_space + md_non_num_substring)
            self.assertEqual(api.build_toc_line(h,1),
indentation_space + md_num_substring)


            # Test h3
            h['type'] = 3
            indentation_space = 8*' '
            self.assertEqual(api.build_toc_line(h),
indentation_space + md_non_num_substring)
            self.assertEqual(api.build_toc_line(h,1),
indentation_space + md_num_substring)

if __name__ == '__main__':
    unitttest.main()
