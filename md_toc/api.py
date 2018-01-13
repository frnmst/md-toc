#
# api.py
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
"""The main file."""

import fpyutils
import re
import curses.ascii

def write_toc_on_md_file(input_file, toc, in_place=True, toc_marker='[](TOC)'):
    r"""Write the table of contents.

    :parameter input_file: the file that needs to be read or modified.
    :parameter toc: the table of contents.
    :parameter in_place: decides whether to overwrite the input
         file or return the table of contents. Defaults to ``True``.
    :parameter toc_marker: a marker that will identify the start
         and the end of the table of contents. Defaults to ``[](TOC)``.
    :type input_file: str
    :type toc: str
    :type in_place: bool
    :type toc_marker: str
    :returns: None if ``in_place`` is ``True`` or the table of contents with
         the markers in between, otherwise.
    :rtype: str
    :raises: one of the fpyutils exceptions or one of the built-in exceptions.

    :Example:

    ::

        >>> import md_toc
        >>> f = open('foo.md')
        >>> print(f.read(),end='')
        # The main title

        ## Hello there!sdfc

        [](TOC)

        Here (up) will lie the toc

        # Some other content ;,.-_ # bye

        a
        b
        c

        ### zzz

        # Again

        ## qwerty

        ## uiop

        vbnm

        ### asdf

        zxc
        >>> print(md_toc.api.write_toc_on_md_file('foo.md',md_toc.api.build_toc('foo.md'),in_place=False),end='')
            [](TOC)

            - [The main title](#the-main-title)
                - [Hello there!](#hello-there)
            - [Some other content ;,.-_ # bye](#some-other-content-bye)
                    - [zzz](#zzz)
            - [Again](#again)
                - [qwerty](#qwerty)
                - [uiop](#uiop)
                    - [asdf](#asdf)

            [](TOC)
    """
    assert isinstance(input_file, str)
    assert isinstance(toc, str)
    assert isinstance(in_place, bool)
    assert isinstance(toc_marker, str)

    # 1. Remove trailing new line(s).
    toc = toc.rstrip()

    # 2. Create the string that needs to be written. Note that if this string
    #    is written, the first toc will already be present in the markdown
    #    file.
    final_string = '\n' + toc + '\n\n' + toc_marker + '\n'

    # 3.1. Write on the file.
    if in_place:
        # 3.1.1. Get the toc markers line positions.
        toc_marker_lines = fpyutils.get_line_matches(
            input_file, toc_marker, 2, loose_matching=True)

        # 3.1.2.1. No toc marker in file: nothing to do.
        if 1 not in toc_marker_lines and 2 not in toc_marker_lines:
            pass

        # 3.1.2.2. 1 toc marker: Insert the toc in that position.
        elif 1 in toc_marker_lines and 2 not in toc_marker_lines:
            fpyutils.insert_string_at_line(input_file, final_string,
                                           toc_marker_lines[1], input_file)

        # 3.1.2.3. 2 toc markers: replace old toc with new one.
        else:
            # Remove the old toc but preserve the first toc marker: that's why the
            # +1 is there.
            fpyutils.remove_line_interval(input_file, toc_marker_lines[1] + 1,
                                          toc_marker_lines[2], input_file)
            fpyutils.insert_string_at_line(input_file, final_string,
                                           toc_marker_lines[1], input_file)
    # 3.2. Return the TOC.
    else:
        # 3.2.1. If the toc is an empty string, return the empty string.
        if toc == '':
            final_string = toc
        # 3.2.2. Return the toc with the toc markers.
        else:
            final_string = toc_marker + '\n' + final_string
        return final_string


def build_toc(filename, ordered=False, no_links=False, anchor_type='standard'):
    r"""Parse file by line and build the table of contents.

    :parameter filename: the file that needs to be read.
    :parameter ordered: decides whether to build an ordered list or not.
    :parameter no_links: disables the use of links.
    :type filename: str
    :type ordered: bool
    :type no_links: bool
    :returns: the table of contents.
    :rtype: str
    :raises: one of the built-in exceptions.

    :Example:

    ::

        >>> import md_toc
        >>> f = open('foo.md')
        >>> print(f.read(),end='')
        # The main title

        ## Hello there!

        [](TOC)

        Here (up) will lie the toc

        # Some other content ;,.-_ # bye

        a
        b
        c

        ### zzz

        # Again

        ## qwerty

        ## uiop

        vbnm

        ### asdf

        zxc

        >>> print(md_toc.api.build_toc('foo.md',ordered=True),end='')
        1. [The main title](#the-main-title)
            1. [Hello there!](#hello-there)
        2. [Some other content ;,.-_ # bye](#some-other-content-bye)
                1. [zzz](#zzz)
        3. [Again](#again)
            2. [qwerty](#qwerty)
            3. [uiop](#uiop)
                2. [asdf](#asdf)
    """
    assert isinstance(filename, str)
    assert isinstance(ordered, bool)
    assert isinstance(no_links, bool)

    toc = ''
    # Header type counter. Useful for ordered lists.
    ht = {
        '1': 0,
        '2': 0,
        '3': 0,
    }
    ht_prev = None
    ht_curr = None

    header_duplicate_counter = dict()

    # 1. Get file content by line
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            # 1.1. Get the basic information.
            header = get_md_heading(line, header_duplicate_counter, anchor_type)
            # 1.2. Consider valid lines only.
            if header is not None:
                # 1.2.1. Get the current header type.
                ht_curr = header['type']

                # 1.2.2. Get the current index. This makes sense only for
                #        ordered tocs.
                increment_index_ordered_list(ht, ht_prev, ht_curr)

                # 1.2.3. Get the table of contents line and append it to the
                #        final string.
                toc += build_toc_line(header, ordered, no_links,
                                      ht[str(ht_curr)]) + '\n'

                ht_prev = ht_curr

            line = f.readline()

    return toc


def increment_index_ordered_list(header_type_count, header_type_prev,
                                 header_type_curr):
    r"""Compute current index for ordered list table of contents.

    :parameter: header_type_count: the index numbers for all headers.
    :parameter: header_type_prev: the previous type of header (h1, h2 or h3).
    :parameter: header_type_curr: the current type of header (h1, h2 or h3).
    :type header_type_count: dict
    :type header_type_prev: int
    :type header_type_curr: int
    :returns: None
    :rtype: None
    :raises: one of the built in exceptions

    :Example:

    >>> ht = {'1':0, '2':0, '3':0}
    >>> md_toc.api.increment_index_ordered_list(ht,3,3)
    >>> ht
    {'1': 0, '2': 0, '3': 1}
    """
    assert isinstance(header_type_count, dict)
    assert '1' in header_type_count
    assert '2' in header_type_count
    assert '3' in header_type_count
    # header_type_prev might be None while header_type_curr can't.
    assert header_type_curr is not None

    # 1. Base case: header_type_prev is set to None since
    #    it corresponds to a new table of contents.
    if header_type_prev is None:
        header_type_prev = header_type_curr

    # 2. Increment the current index.
    header_type_count[str(header_type_curr)] += 1


def build_anchor_link(header_text,header_duplicate_counter,anchor_type='standard'):
    r"""Apply the specified slug rule to build the anchor link.

    :parameter anchor_type: supported anchor types are: 'standard', 'github',
         'gitlab', 'gogs', 'notabug'.

    :note: the 'standard' anchor types does not handle duplicate entries.
    """
    assert isinstance(header_text, str)
    assert isinstance(header_duplicate_counter, dict)
    assert isinstance(anchor_type, str)

    # 1. Return the same text as-is.
    if anchor_type == 'standard':
        return header_text

    # 2. Return the header text with the applied rules for GitHub.
    # Link to the Ruby algorithm:
    # https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb
    elif anchor_type == 'github':
        """
        Copyright (c) 2012 GitHub Inc. and Jerry Cheung
        Copyright (c) 2018, Franco Masotti <franco.masotti@student.unife.it>

        MIT License

        Permission is hereby granted, free of charge, to any person obtaining
        a copy of this software and associated documentation files (the
        "Software"), to deal in the Software without restriction, including
        without limitation the rights to use, copy, modify, merge, publish,
        distribute, sublicense, and/or sell copies of the Software, and to
        permit persons to whom the Software is furnished to do so, subject to
        the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
        NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
        LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
        OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
        WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        """
        # 2.1. Lowercase.
        header_text = header_text.lower()
        # 2.2. Remove punctuation: Keep spaces, hypens and "word characters"
        #      only.
        #      See https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb#L26
        header_text = re.sub(r'[^\w\s\- ]','',header_text)
        # 2.3. Replace spaces with dashes.
        header_text = header_text.replace(' ','-')

        # 2.4. Check for duplicates.
        ht = header_text
        # Set the initial value if we are examining the first occurrency
        if header_text not in header_duplicate_counter:
            header_duplicate_counter[header_text] = 0
        if header_duplicate_counter[header_text] > 0:
            header_text = header_text + '-' + str(header_duplicate_counter[header_text])
        header_duplicate_counter[ht] += 1

        return header_text

    # 3. Return the header text with the applied rules for GitLab.
    # https://gitlab.com/help/user/markdown.md#header-ids-and-links
    # https://gitlab.com/help/user/markdown.md#gitlab-flavored-markdown-gfm
    # https://github.com/vmg/redcarpet/blob/26c80f05e774b31cd01255b0fa62e883ac185bf3/ext/redcarpet/html.c#L274
    # https://github.com/vmg/redcarpet/blob/26c80f05e774b31cd01255b0fa62e883ac185bf3/ext/redcarpet/html.c#L674
    elif anchor_type == 'gitlab':
        """
        /*
         * Copyright (c) 2009, Natacha Porté
         * Copyright (c) 2015, Vicent Marti
         * Copyright (c) 2018, Franco Masotti <franco.masotti@student.unife.it>
         *
         * Permission is hereby granted, free of charge, to any person obtaining a copy
         * of this software and associated documentation files (the "Software"), to deal
         * in the Software without restriction, including without limitation the rights
         * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
         * copies of the Software, and to permit persons to whom the Software is
         * furnished to do so, subject to the following conditions:
         *
         * The above copyright notice and this permission notice shall be included in
         * all copies or substantial portions of the Software.
         *
         * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
         * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
         * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
         * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
         * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,  ARISING FROM,
         * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER  DEALINGS IN
         * THE SOFTWARE.
         */
        """
        # To ensure full compatibility what follows is a direct translation
        # of the rndr_header_anchor C function used in redcarpet.
        STRIPPED = " -&+$,/:;=?@\"#{}|^~[]`\\*()%.!'"
        header_text_len = len(header_text)
        inserted = 0
        stripped = 0
        header_text_intermediate_stage = ''
        for i in range(0,header_text_len):
            if header_text[i] == '<':
                while i < header_text_len and a[i] != '>':
                    i+=1
            elif header_text[i] == '&':
                while i < header_text_len and header_text[i] != ';':
                    i+=1
            # str.find() == -1 if character is not found in str.
            # https://docs.python.org/3.6/library/stdtypes.html?highlight=find#str.find
            elif not curses.ascii.isascii(header_text[i]) or STRIPPED.find(header_text[i]) != -1:
                if inserted and  not stripped:
                    header_text_intermediate_stage += '-'
                stripped = 1
            else:
                header_text_intermediate_stage += header_text[i].lower()
                stripped = 0
                inserted += 1

        if stripped > 0 and inserted > 0:
            header_text_intermediate_stage = header_text_intermediate_stage[0:-1]

        if inserted == 0 and header_text_len > 0:
            hash = 5381
            for i in range(0,header_text_len):
                # Get the unicode representation with ord.
                # Unicode should be equal to ASCII in ASCII's range of
                # characters.
                hash = ((hash << 5) + hash) + ord(header_text[i])

            # This is equivalent to %x in C. In Python we don't have
            # the length problem so %x is equal to %lx in this case.
            # Apparently there is no %l in Python...
            header_text_intermediate_stage = 'part-' + '{0:x}'.format(hash)

        # 3.2. Check for duplicates.

        # TODO TODO: Check where this is done in the original code.
        ht = header_text_intermediate_stage
        # Set the initial value if we are examining the first occurrency
        if header_text_intermediate_stage not in header_duplicate_counter:
            header_duplicate_counter[header_text_intermediate_stage] = 0
        if header_duplicate_counter[header_text_intermediate_stage] > 0:
            header_text_intermediate_stage = header_text_intermediate_stage + '-' + str(header_duplicate_counter[header_text_intermediate_stage])
        header_duplicate_counter[ht] += 1

        return header_text_intermediate_stage

    # 4. Situation of using anchor links with Gogs seems unclear at the moment.
    # https://gogs.io/docs
    # https://github.com/chjj/marked
    # https://github.com/chjj/marked/issues/981
    # https://github.com/chjj/marked/search?q=anchor&type=Issues&utf8=%E2%9C%93
    # https://notabug.org/hp/gogs/
    elif anchor_type == 'gogs' or anchor_type == 'notabug':
        # Needs to be implemented.
        return header_text

    # 5. Same as 1.
    else:
        return header_text


def build_toc_line(header, ordered=False, no_links=False, index=1):
    r"""Return a list element of the table of contents.

    :parameter header: a data structure that contains the original
         text, the slugified text and the type of header.
    :parameter ordered: if set to ``True``, numbers will be used
         as list ids or otherwise a dash character, otherwise. Defaults
         to ``False``.
    :parameter no_links: disables the use of links.
    :parameter index: a number that will be used as list id in case of an
         ordered table of contents. Defaults to ``1``.
    :type header: dict
    :type ordered: bool
    :type no_links: bool
    :type index: int
    :returns: a single line of the table of contents.
    :rtype: str
    :raises: one of the built-in exceptions.

    :Example:

    >>> header =  {'type': 2, 'text_original': 'hi hOw Are YOu!!? ? #', 'text_anchor_link': 'hi-how-are-you'}
    >>> print(md_toc.api.build_toc_line(header,ordered=True,index=3))
        3. [hi hOw Are YOu!!? ? #](#hi-how-are-you)
    """
    if header is None:
        return header

    assert isinstance(header, dict)
    assert 'type' in header
    assert 'text_original' in header
    assert 'text_anchor_link' in header
    assert isinstance(header['type'], int)
    assert isinstance(header['text_original'], str)
    assert isinstance(header['text_anchor_link'], str)
    assert header['type'] >= 1 and header['type'] <= 3
    assert isinstance(ordered, bool)
    assert isinstance(no_links, bool)
    assert isinstance(index, int)

    # 1. Get the list symbol.
    if ordered:
        list_symbol = str(index) + '.'
    else:
        list_symbol = '-'

    # 2. Compute the indentation spaces.
    #    ordered list require 4-level indentation,
    #    while unordered either 2 or 4. To simplify the code we
    #    will keep only the common case. To implement
    #    2-level indentation it is sufficient to do:
    #    2**(header['type']-1) as a separate case.
    if header['type'] == 1:
        no_of_indentation_spaces = 0
    else:
        no_of_indentation_spaces = 2**header['type']
    indentation_spaces = no_of_indentation_spaces * ' '

    if no_links:
        # 3.1. Build the plain line.
        line = header['text_original']
    else:
        # 3.2. Build the line as a link.
        line = '[' + header['text_original'] + ']' + '(#' + header['text_anchor_link'] + ')'

    # 4. String concatenation.
    toc_line = indentation_spaces + list_symbol + ' ' + line

    return toc_line

def get_md_heading(line,header_duplicate_counter=dict(),anchor_type='standard'):
    r"""Given a line extract the title type and its text.

    :parameter: line
    :type line: str
    :returns: None if the input line does not correspond to one of the
         designated cases or a data structure containing the necessary
         components to create a table of contents line, otherwise.
    :rtype: dict
    :raises: one of the built-in exceptions.

    :Example:

    >>> print(md_toc.api.get_md_heading(' ## hi hOw Are YOu!!? ? #'))
    {'type': 2, 'text_original': 'hi hOw Are YOu!!? ? #', 'text_anchor_link': 'hi-how-are-you'}
    """
    assert isinstance(line, str)

    # 1. Remove leading and trailing whitespace from line.
    line = line.strip()

    # 2. If first char of line is not '#' return None. This means
    # we don't care about this line. Check also if it's an empty string.
    if len(line) == 0:
        return None
    if line[0] != '#':
        return None

    # 3. Remove the leading '#'s.
    header_text = line.lstrip('#')

    # 4. Count the number of leading '#' character to determine what kind of
    # title it is.
    #
    #    Waring: This is computationally unconvenient: O(n) where n =
    #    len(line). It is however more elegant than iterating on the line
    #    itself.
    header_type = len(line) - len(header_text)

    # 5. If it's a 4 (or more) title level we will ignore it.
    if header_type > 3:
        return None

    # 6. Remove possible whitespace after removing the '#'s.
    header_text = header_text.strip()

    # 7. Return a dict with the three data sets we need. Note that we need the
    # title text to be slugified so it can be used as link.
    header = {
        'type': header_type,
        'text_original': header_text,
        'text_anchor_link': build_anchor_link(header_text,header_duplicate_counter,anchor_type)
    }
    return header


if __name__ == '__main__':
    pass
