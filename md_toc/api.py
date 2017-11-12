#!/usr/bin/env python3

from slugify import slugify


def build_toc(filename, ordered = False):
    """ Parse file by line and build the table of contents.
    """

    assert isinstance(filename, str)
    assert isinstance(ordered, bool)

    toc_line = ''
    # Header type counter. Useful for ordered lists.
    ht = {
        '1': 0,
        '2': 0,
        '3': 0,
    }
    ht_prev=None
    ht_curr=None

    # 1. Get file content by line
    with open(filename, 'r') as f:
        for line in f:
            # 1.1. Get the basic information.
            header = get_md_heading(line)
            # 1.2. Consider valid lines only.
            if header is not None:
                # 1.2.1. Get the current header type.
                ht_curr = header['type']

                # 1.2.2. Get the current index if necessary.
                if ordered:
                    increment_index_numeric_list(ht,ht_prev,ht_curr)
                # 1.2.3. Get the table of contents line and append it to the
                #        final string.
                toc_line += build_toc_line(header,ordered,ht[str(ht_curr)]) + '\n'

                ht_prev = ht_curr

    return toc_line

def increment_index_numeric_list(header_type_count,header_type_prev,header_type_curr):
    """ Compute current index for ordered list table of contents.
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

def build_toc_line(header,ordered=False,index=1):
    """ Return a string which corresponds to a list element
        in the markdown syntax. If ordered is true then the rendered list
        will use numbers instead of bullets. For this reason the index
        variable must be passed to the method.
    """

    if header is None:
        return header

    assert isinstance(header, dict)
    assert 'type' in header
    assert 'text_original' in header
    assert 'text_slugified' in header
    assert isinstance(header['type'],int)
    assert isinstance(header['text_original'],str)
    assert isinstance(header['text_slugified'],str)
    assert header['type'] >= 1 and header['type']<= 3

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

    # 3. Build the link.
    link = '[' + header['text_original'] + ']' + '(' + header['text_slugified'] + ')'

    # 4. String concatenation.
    toc_line = indentation_spaces + list_symbol + ' ' + link

    return toc_line

def get_md_heading(line):
    """ Given a line extract the title type and its text.
        Return the three variable components needed to create a line.
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
    header_type = len(line)-len(header_text)

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
               'text_slugified': slugify(header_text)
             }
    return header

if __name__ == '__main__':
    pass
