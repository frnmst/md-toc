CLI Usage helps
===============

Main help
---------

::

    usage: md_toc [-h] [-i] [-n] [-o] [-p {github,redcarpet,gitlab}]
                  [-t TOC_MARKER] [-l HEADER_LEVELS] [-v]
                  FILE_NAME

    Markdown Table Of Contents

    positional arguments:
      FILE_NAME             the I/O file name

    optional arguments:
      -h, --help            show this help message and exit
      -i, --in-place        overwrite the input file
      -n, --no-links        avoids adding links to corresponding content
      -o, --ordered         write as an ordered list
      -p {github,cmark,redcarpet,gitlab}, --parser {github,cmark,redcarpet,gitlab}
                            decide what markdown parser will be used to generate
                            the links. Defaults to github
      -t TOC_MARKER, --toc-marker TOC_MARKER
                            set the string to be used as the marker for
                            positioning the table of contents. Defaults to [](TOC)
      -l HEADER_LEVELS, --header-levels HEADER_LEVELS
                            set the maximum level of headers to be considered as
                            part of the TOC
      -v, --version         show program's version number and exit

    Return values: 0 OK, 1 Error, 2 Invalid command

    Copyright (C) 2018 Franco Masotti, frnmst
    License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.

