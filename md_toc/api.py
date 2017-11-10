#!/usr/bin/env python3

# Table of contents.

from slugify import slugify

def build_toc_line(header):
    """ Return a string which corresponds to a list element
        in the markdown syntax.
    """

    assert isinstance(header, dict)



def get_md_heading(line):
    """ Given a line extract the title type and its text.
    """

    assert isinstance(line, str)

    # 1. Remove leading and trailing whitespace from line.
    line = line.strip()

    # 2. If first char of line is not '#' return None. This means
    # we don't care about this line
    if line[0] != '#':
        return None

    # 3. Remove the leading '#'s.
    header_text = line.lstrip('#')

    # 4. Count the number of '#' character to determine what kind of title it
    #    is.
    #
    #    Waring: This is computationally unconvenient: O(n) where n =
    #    len(line). It is however more elegant than iterating on the line
    #    itself.
    header_type = len(line)-len(header_text)

    # 5. Remove possible whitespace after removing the '#'s.
    header_text.strip()

    # 6. Return a dict with the two data sets we need.
    header = {
               type: header_type,
               text: slugify(header_text)
             }
    return header

if __name__ == '__main__':
    pass
