Features
========

===     ===============
Key     Meaning
===     ===============
✓       implemented
/       partial support
✘       not implemented
?       unknown
P       feature planned
===     ===============

.. note:: These feature tables might not be up to date or accurate! Do your own
          research. If you find a mistake you are welcome to open an issue
          or pull request.

Inputs and outputs
------------------

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - Feature
     - md-toc
     - `github-markdown-toc <https://github.com/ekalinin/github-markdown-toc>`_
     - `markdown-toc <https://github.com/jonschlinkert/markdown-toc>`_
     - `remark-toc <https://github.com/remarkjs/remark-toc>`_
     - `markdown-it-table-of-contents <https://github.com/cmaas/markdown-it-table-of-contents>`_
     - `gfm-toc <https://github.com/waynerv/github-markdown-toc>`_
     - `md-toc-creator <https://github.com/mcb2003/md-toc-creator>`_
     - `mdformat-toc <https://github.com/hukkin/mdformat-toc>`_
     - `git-toc <https://github.com/PrzemekWirkus/git-toc>`_
     - `markdown-github-bear-toc <https://github.com/alexander-lee/markdown-github-bear-toc>`_
     - `mdtoc <https://github.com/scottfrazer/mdtoc>`_
     - `markdown-toc-cli <https://github.com/noahp/markdown-toc-cli>`_
     - `toc2md <https://pypi.org/project/toc2md/>`_
   * - Indented & non-indented list
     - ✓
     - ✘
     - ✘
     - ?
     - ✘
     - ✘
     - ✓
     - ?
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Ordered & unordered list
     - ✓
     - ✘
     - ✘
     - ✓
     - ✓
     - ✘
     - ✘
     - ?
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Anchor links & plain text list
     - ✓
     - ✘
     - ✘
     - ?
     - ?
     - ✘
     - ✓
     - ✓
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Reads from stdin
     - ✓
     - ✓
     - ✓
     - ?
     - ?
     - ✘
     - ?
     - ✘
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Inplace & stdout
     - ✓
     - ✓
     - ✓
     - ?
     - ?
     - ✓
     - ✓
     - ✘
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Non-markdown output
     - ✘ [P]
     - ✘
     - ✓
     - ?
     - ✓
     - ✘
     - ✘
     - ?
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - List marker selection
     - ✓
     - ✘
     - ✓
     - ?
     - ?
     - ✘
     - ?
     - ?
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Newline marker selection
     - ✓
     - ✘
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Universal anchor links
     - ✘
     - ?
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ✓
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Last TOC update string
     - ✘
     - ✓
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
   * - Remove TOC marker after inserting TOC inplace
     - ✘
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?

Filtering
---------

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - Feature
     - md-toc
     - `github-markdown-toc <https://github.com/ekalinin/github-markdown-toc>`_
     - `markdown-toc <https://github.com/jonschlinkert/markdown-toc>`_
     - `remark-toc <https://github.com/remarkjs/remark-toc>`_
     - `markdown-it-table-of-contents <https://github.com/cmaas/markdown-it-table-of-contents>`_
     - `gfm-toc <https://github.com/waynerv/github-markdown-toc>`_
     - `md-toc-creator <https://github.com/mcb2003/md-toc-creator>`_
     - `mdformat-toc <https://github.com/hukkin/mdformat-toc>`_
     - `git-toc <https://github.com/PrzemekWirkus/git-toc>`_
     - `markdown-github-bear-toc <https://github.com/alexander-lee/markdown-github-bear-toc>`_
     - `mdtoc <https://github.com/scottfrazer/mdtoc>`_
     - `markdown-toc-cli <https://github.com/noahp/markdown-toc-cli>`_
     - `toc2md <https://pypi.org/project/toc2md/>`_
   * - Max header level in TOC
     - ✓
     - ✘
     - ?
     - ✓
     - ✓
     - ✘
     - ✘
     - ✓
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Min header level in TOC
     - ✘
     - ✘
     - ✘
     - ✘
     - ✓
     - ✘
     - ✘
     - ✓
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Skip first n lines
     - ✓
     - ✘
     - ?
     - ?
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Include headings regex pattern
     - ✘
     - ✘
     - ?
     - ✓
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Skip headings regex pattern
     - ✘
     - ✘
     - ?
     - ✓
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Skip headings based on a marker
     - `✘ <https://github.com/frnmst/md-toc/issues/37>`_
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - Skip all headings before the TOC marker
     - ✘
     - ✓
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?

Remote usage
------------

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - Feature
     - md-toc
     - `github-markdown-toc <https://github.com/ekalinin/github-markdown-toc>`_
     - `markdown-toc <https://github.com/jonschlinkert/markdown-toc>`_
     - `remark-toc <https://github.com/remarkjs/remark-toc>`_
     - `markdown-it-table-of-contents <https://github.com/cmaas/markdown-it-table-of-contents>`_
     - `gfm-toc <https://github.com/waynerv/github-markdown-toc>`_
     - `md-toc-creator <https://github.com/mcb2003/md-toc-creator>`_
     - `mdformat-toc <https://github.com/hukkin/mdformat-toc>`_
     - `git-toc <https://github.com/PrzemekWirkus/git-toc>`_
     - `markdown-github-bear-toc <https://github.com/alexander-lee/markdown-github-bear-toc>`_
     - `mdtoc <https://github.com/scottfrazer/mdtoc>`_
     - `markdown-toc-cli <https://github.com/noahp/markdown-toc-cli>`_
     - `toc2md <https://pypi.org/project/toc2md/>`_
   * - Works offline
     - ✓
     - ✘
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ?
   * - Remote markdown files
     - ✘
     - ✓
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ✘
     - ?

Other
-----

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - Feature
     - md-toc
     - `github-markdown-toc <https://github.com/ekalinin/github-markdown-toc>`_
     - `markdown-toc <https://github.com/jonschlinkert/markdown-toc>`_
     - `remark-toc <https://github.com/remarkjs/remark-toc>`_
     - `markdown-it-table-of-contents <https://github.com/cmaas/markdown-it-table-of-contents>`_
     - `gfm-toc <https://github.com/waynerv/github-markdown-toc>`_
     - `md-toc-creator <https://github.com/mcb2003/md-toc-creator>`_
     - `mdformat-toc <https://github.com/hukkin/mdformat-toc>`_
     - `git-toc <https://github.com/PrzemekWirkus/git-toc>`_
     - `markdown-github-bear-toc <https://github.com/alexander-lee/markdown-github-bear-toc>`_
     - `mdtoc <https://github.com/scottfrazer/mdtoc>`_
     - `markdown-toc-cli <https://github.com/noahp/markdown-toc-cli>`_
     - `toc2md <https://pypi.org/project/toc2md/>`_
   * - Provides CLI
     - ✓
     - ✓
     - ✓
     - ✘
     - ✘
     - ✓
     - ✓
     - ✘
     - ✓
     - ?
     - ?
     - ?
     - ?
   * - Provides API
     - ✓
     - ✘
     - ✓
     - ?
     - ✓
     - ?
     - ?
     - ✓
     - ?
     - ?
     - ?
     - ?
     - ?
   * - Tries to follow markdown specs literally
     - ✓
     - ?
     - ?
     - ?
     - ?
     - ✘
     - ✘
     - /
     - ✘
     - ?
     - ?
     - ?
     - ?
   * - pre-commit hook
     - ✓
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
     - ?
   * - Active project
     - ✓
     - ✓
     - ✓
     - ✓
     - ✓
     - ✘
     - ✘
     - ✓
     - ✓
     - ?
     - ?
     - ?
     - ?
