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
    :parameter anchor_type: decides rules on how to generate anchor links.
         Defaults to ``standard``.
    :type filename: str
    :type ordered: bool
    :type no_links: bool
    :type anchor_type: str
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

    toc = ''
    # Header type counter. Useful for ordered lists.
    # TODO This needs to be changed for a generic number of indentation levels.
    # TODO Change the dict to ints only.
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
            header = get_md_header(line, header_duplicate_counter,
                                   anchor_type)
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


# TODO: FIXME so that we have e.g.: 1.1.x. 1.2.x. 1.x. 1.
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
    assert header['type'] >= 1
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
    #    2*(header['type']-1) as a separate case.
    no_of_indentation_spaces = 4 * (header['type'] - 1)
    indentation_spaces = no_of_indentation_spaces * ' '

    # 3.1. Build the plain line with or without link.
    if no_links:
        line = header['text_original']
    else:
        line = '[' + header['text_original'] + ']' + '(#' + header['text_anchor_link'] + ')'

    # 4. String concatenation.
    toc_line = indentation_spaces + list_symbol + ' ' + line

    return toc_line


def build_anchor_link(header_text_trimmed,
                      header_duplicate_counter,
                      anchor_type='standard'):
    r"""Apply the specified slug rule to build the anchor link.

    :parameter header_text_trimmed: the text that needs to be transformed in a link
    :parameter header_duplicate_counter: a data structure that keeps track of
         possible duplicate header links in order to avoid them. This is
         meaningful only for certain values of anchor_type.
    :parameter anchor_type: decides rules on how to generate anchor links.
         Defaults to ``standard``. Supported anchor types are: ``standard``,
         ``github``, ``gitlab``, ``redcarpet``, ``gogs``, ``notabug``,
         ``kramdown``.
    :type header_text_trimmed: str
    :type header_duplicate_counter: dict
    :type anchor_type: str
    :returns: the anchor link.
    :rtype: str
    :raises: one of the built-in exceptions.

    :note: For a detailed description of the behaviour of each anchor type
        please refer to the 'Markdown spec' documentation page.
    """
    assert isinstance(header_text_trimmed, str)
    assert isinstance(header_duplicate_counter, dict)
    assert isinstance(anchor_type, str)

    # 1. Return the same text as-is.
    if anchor_type == 'standard':
        return header_text_trimmed

    # 2. Return the header text with the applied rules for GitHub.
    elif anchor_type == 'github':
        # This is based on the ruby algorithm. See md_toc's documentation.
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
        header_text_trimmed = header_text_trimmed.lower()
        # 2.2. Remove punctuation: Keep spaces, hypens and "word characters"
        #      only.
        #      See https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb#L26
        header_text_trimmed = re.sub(r'[^\w\s\- ]', '', header_text_trimmed)
        # 2.3. Replace spaces with dashes.
        header_text_trimmed = header_text_trimmed.replace(' ', '-')

        # 2.4. Check for duplicates.
        ht = header_text_trimmed
        # Set the initial value if we are examining the first occurrency.
        # The state of header_duplicate_counter is available to the caller
        # functions.
        if header_text_trimmed not in header_duplicate_counter:
            header_duplicate_counter[header_text_trimmed] = 0
        if header_duplicate_counter[header_text_trimmed] > 0:
            header_text_trimmed = header_text_trimmed + '-' + str(
                header_duplicate_counter[header_text_trimmed])
        header_duplicate_counter[ht] += 1

        return header_text_trimmed

    # 3. Return the header text with the applied rules for GitLab and RedCarpet.
    # https://github.com/vmg/redcarpet/blob/26c80f05e774b31cd01255b0fa62e883ac185bf3/ext/redcarpet/html.c#L274
    elif anchor_type == 'gitlab' or anchor_type == 'redcarpet':
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
        # 3.1. To ensure full compatibility what follows is a direct translation
        #      of the rndr_header_anchor C function used in redcarpet.
        STRIPPED = " -&+$,/:;=?@\"#{}|^~[]`\\*()%.!'"
        header_text_trimmed_len = len(header_text_trimmed)
        inserted = 0
        stripped = 0
        header_text_trimmed_middle_stage = ''
        for i in range(0, header_text_trimmed_len):
            if header_text_trimmed[i] == '<':
                while i < header_text_trimmed_len and header_text_trimmed[i] != '>':
                    i += 1
            elif header_text_trimmed[i] == '&':
                while i < header_text_trimmed_len and header_text_trimmed[i] != ';':
                    i += 1
            # str.find() == -1 if character is not found in str.
            # https://docs.python.org/3.6/library/stdtypes.html?highlight=find#str.find
            elif not curses.ascii.isascii(
                    header_text_trimmed[i]) or STRIPPED.find(header_text_trimmed[i]) != -1:
                if inserted and not stripped:
                    header_text_trimmed_middle_stage += '-'
                stripped = 1
            else:
                header_text_trimmed_middle_stage += header_text_trimmed[i].lower()
                stripped = 0
                inserted += 1

        if stripped > 0 and inserted > 0:
            header_text_trimmed_middle_stage = header_text_trimmed_middle_stage[0:-1]

        if inserted == 0 and header_text_trimmed_len > 0:
            hash = 5381
            for i in range(0, header_text_trimmed_len):
                # Get the unicode representation with ord.
                # Unicode should be equal to ASCII in ASCII's range of
                # characters.
                hash = ((hash << 5) + hash) + ord(header_text_trimmed[i])

            # This is equivalent to %x in C. In Python we don't have
            # the length problem so %x is equal to %lx in this case.
            # Apparently there is no %l in Python...
            header_text_trimmed_middle_stage = 'part-' + '{0:x}'.format(hash)

        # 3.2. Check for duplicates (this is working in github only).
        #      https://gitlab.com/help/user/markdown.md#header-ids-and-links
        if anchor_type == 'gitlab':
            # Apparently redcarpet does not handle duplicate entries, but
            # Gitlab does, although I cannot find the code responsable for it.
            ht = header_text_trimmed_middle_stage
            # Set the initial value if we are examining the first occurrency
            if header_text_trimmed_middle_stage not in header_duplicate_counter:
                header_duplicate_counter[header_text_trimmed_middle_stage] = 0
            if header_duplicate_counter[header_text_trimmed_middle_stage] > 0:
                header_text_trimmed_middle_stage = header_text_trimmed_middle_stage + '-' + str(
                    header_duplicate_counter[header_text_trimmed_middle_stage])
            header_duplicate_counter[ht] += 1

        return header_text_trimmed_middle_stage

    # 4. Situation of seems unclear. Needs to be implemented.
    elif anchor_type == 'gogs' or anchor_type == 'marked' or anchor_type == 'notabug':
        return header_text_trimmed

    # 5. Unclear if there is this feature. Needs to be implemented.
    elif anchor_type == 'kramdown':
        return header_text_trimmed

    # 6. Same as 1.
    else:
        return header_text_trimmed


def get_md_header_type(line, max_header_levels=3):
    r"""Given a line extract the title type.

    :parameter line: the line to be examined.
    :parameter max_header_levels: the maximum levels.... TODO.
    """
    assert isinstance(line, str)
    assert isinstance(max_header_levels, int)
    assert max_header_levels > 0

    # 1. Remove leading and whitespace from line to engage a lax parsing.
    line = line.lstrip()

    # 2. Determine the header type by counting the number of the
    #    first consecutive '#' characters in the line.
    #    Count until we are in the range of max_header_levels.
    header_type = 0
    line_length = len(line)
    while header_type < line_length and line[header_type] == '#' and header_type <= max_header_levels:
        header_type += 1
    if header_type == 0 or header_type > max_header_levels:
        return None
    else:
        return header_type


def remove_md_header_syntax(header_text):
    r"""Return a trimmed version of the input line without the markdown header syntax."""
    assert isinstance(header_text, str)
    # 1. Remove the leading and trailing whitespace
    header_text = header_text.lstrip()

    # 2. Remove the leading '#' consecutive characters.
    header_text = header_text.lstrip('#')

    # 3. Remove possible whitespace after removing the '#'s.
    trimmed_text =  header_text.lstrip()

    return trimmed_text


def get_md_header(header_text,
                  header_duplicate_counter,
                  max_header_levels=3,
                  anchor_type='standard'):
    r"""Build a data structure with the elements needed to create a TOC line.

    :parameter header_duplicate_counter: a data structure that contains the
         number of occurrencies of each header anchor link. This is used to
         avoid duplicate anchor links and it is meaningful only for certain
         values of anchor_type.
    :parameter anchor_type: decides rules on how to generate anchor links.
         Defaults to ``standard``.
    :type line: str
    :type header_duplicate_counter: dict
    :type anchor_type: str
    :returns: None if the input line does not correspond to one of the
         designated cases or a data structure containing the necessary
         components to create a table of contents line, otherwise.
    :rtype: dict
    :raises: one of the built-in exceptions.

    :Example:

    >>> print(md_toc.api.get_md_header(' ## hi hOw Are YOu!!? ? #'))
    {'type': 2, 'text_original': 'hi hOw Are YOu!!? ? #', 'text_anchor_link': 'hi-how-are-you'}
    """
    header_text_trimmed = remove_md_header_syntax(header_text)
    header = {
        'type':
        get_md_header_type(header_text,max_header_levels),
        'text_original':
        header_text_trimmed,
        'text_anchor_link':
        build_anchor_link(header_text_trimmed, header_duplicate_counter, anchor_type)
    }
    return header


if __name__ == '__main__':
    pass
