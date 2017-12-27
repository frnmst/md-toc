CLI Usage helps
===============

Main help
---------

    usage: md_toc [-h] [-v] {wtoc} ...

    Markdown Table Of Contents

    positional arguments:
      {wtoc}
        wtoc         write the table of contents

    optional arguments:
      -h, --help     show this help message and exit
      -v, --version  show program's version number and exit

    Return values: 0 OK, 1 Error, 2 Invalid command
             
wtoc sub-command
----------------

    usage: md_toc wtoc [-h] [-i] [-o] [-t TOC_MARKER] FILE_NAME

    positional arguments:
      FILE_NAME             the i/o file name

    optional arguments:
      -h, --help            show this help message and exit
      -i, --in-place        overwrite the input file
      -o, --ordered         write as an ordered list
      -t TOC_MARKER, --toc-marker TOC_MARKER
                            set the string to be used as the marker for
                            positioning the table of contents


