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

.. note:: This feature table might not be up to date or accurate! Do your own
          research. If you find a mistake you are welcome to open an issue
          or pull request.

.. list-table:: Feature comparison
   :header-rows: 1

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
