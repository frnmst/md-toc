Markdown spec
=============

Introduction
------------

md-toc aimes to be as conformant as possible to each supported markdown
parser. What follows is a list of parameters and rules used by md-toc to decide
how to parse markdown files and to generate the table of contents.

Compatibility table
```````````````````

.. |unknown| image:: assets/grey.png
    :width: 16
    :height: 16

.. |none| image:: assets/black.png
    :width: 16
    :height: 16

.. |low| image:: assets/red.png
    :width: 16
    :height: 16

.. |partial| image:: assets/orange.png
    :width: 16
    :height: 16

.. |good| image:: assets/yellow.png
    :width: 16
    :height: 16

.. |most| image:: assets/blue.png
    :width: 16
    :height: 16

.. |full| image:: assets/green.png
    :width: 16
    :height: 16

Key
^^^

============    ===========
Color           Meaning
============    ===========
|unknown|       unknown
|none|          none
|low|           low
|partial|       partial
|good|          good
|most|          most
|full|          full
============    ===========

Status
^^^^^^

=======================   =====================   ============   ========================================================================================================  =============================================
Parser                    Status                  Alias of       Supported parser version                                                                                  Source
=======================   =====================   ============   ========================================================================================================  =============================================
``cmark``                 |most|                  \-             Version 0.30 (2021-06-19) (GIT tag 0.30.0)                                                                https://github.com/commonmark/cmark
``commonmarker``          |good|                  ``github``     \-                                                                                                        https://github.com/gjtorikian/commonmarker
``github``                |good|                  \-             Version 0.29-gfm (2019-04-06) (GIT tag 0.29.gfm.0)                                                        https://github.com/github/cmark-gfm
``goldmark``              |most|                  ``cmark``      \-                                                                                                        https://github.com/yuin/goldmark
``gitlab``                |partial|               \-             Latest unknown version                                                                                    https://docs.gitlab.com/ee/user/markdown.html
``redcarpet``             |low|                   \-             `Redcarpet v3.5.0 <https://github.com/vmg/redcarpet/tree/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae>`_      https://github.com/vmg/redcarpet
Gogs                      |unknown|               \-             \-                                                                                                        https://gogs.io/
NotABug Gogs fork         |unknown|               \-             \-                                                                                                        https://notabug.org/hp/gogs/
Marked                    |unknown|               \-             \-                                                                                                        https://github.com/markedjs/marked
kramdown                  |unknown|               \-             \-                                                                                                        https://kramdown.gettalong.org/
GitLab Kramdown           |unknown|               \-             \-                                                                                                        https://gitlab.com/gitlab-org/gitlab_kramdown
Notabug                   |unknown|               \-             \-                                                                                                        https://notabug.org/hp/gogs/
=======================   =====================   ============   ========================================================================================================  =============================================

md-toc version tables
`````````````````````

Key
^^^

============    ==============================================================
Word            Meaning
============    ==============================================================
✘               not implemented
C               Commonmark
G               GitLab modified Redcarpet
============    ==============================================================

If a parser is not present in a version table it means that at that moment
it was not implemented.

Status history
^^^^^^^^^^^^^^

Version 0
.........

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - md-toc
     - ``github``
   * - 0.0.1
     - unknown version

Version 1
.........

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - md-toc
     - ``standard``
     - ``github``
     - ``gitlab``
     - ``redcarpet``

   * - 1.0.0
     - unknown version
     - latest version
     - G
     - |r1|

Version 2
.........

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - md-toc
     - ``cmark``
     - ``commonmarker``
     - ``github``
     - ``gitlab``
     - ``redcarpet``

   * - 2.0.0
     - latest version
     - latest version
     - C
     - G
     - |r2|
   * - 2.0.1
     - latest version
     - latest version
     - C
     - G
     - |r2|

Version 3
.........

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - md-toc
     - ``cmark``
     - ``commonmarker``
     - ``github``
     - ``gitlab``
     - ``redcarpet``
   * - 3.0.0
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 3.1.0
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|

Version 4
.........

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - md-toc
     - ``cmark``
     - ``commonmarker``
     - ``github``
     - ``gitlab``
     - ``redcarpet``

   * - 4.0.0
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|

Version 5
.........

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - md-toc
     - ``cmark``
     - ``commonmarker``
     - ``github``
     - ``gitlab``
     - ``redcarpet``

   * - 5.0.0
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 5.0.1
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|

Version 6
.........

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - md-toc
     - ``cmark``
     - ``commonmarker``
     - ``github``
     - ``gitlab``
     - ``redcarpet``
   * - 6.0.0
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 6.0.1
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 6.0.2
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|

Version 7
.........

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - md-toc
     - ``cmark``
     - ``commonmarker``
     - ``github``
     - ``gitlab``
     - ``redcarpet``
   * - 7.0.0
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 7.0.1
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 7.0.2
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 7.0.3
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 7.0.4
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 7.0.5
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - |r3|
   * - 7.1.0
     - ``github``
     - ``github``
     - 0.28.gfm.?
     - ``github``
     - v3.5.0
   * - 7.2.0
     - 0.28.? [#f1]_
     - 0.28.gfm.?
     - 0.28.gfm.?
     - ``github``
     - v3.5.0

Version 8
.........

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * - md-toc
     - ``cmark``
     - ``commonmarker``
     - ``github``
     - ``gitlab``
     - ``goldmark``
     - ``redcarpet``
   * - 8.0.0
     - 0.29.?
     - ``github``
     - 0.29.gfm.?
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.0.1
     - 0.29.?
     - ``github``
     - 0.29.gfm.?
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.0
     - 0.29.?
     - ``github``
     - 0.29.gfm.?
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.1
     - 0.30.?
     - ``github``
     - 0.29.gfm.? [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.2
     - 0.30.?
     - ``github``
     - 0.29.gfm.? [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.3
     - 0.30.0
     - ``github``
     - 0.29.gfm.0 [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.4
     - 0.30.0
     - ``github``
     - 0.29.gfm.0 [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.5
     - 0.30.0
     - ``github``
     - 0.29.gfm.0 [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.6
     - 0.30.0
     - ``github``
     - 0.29.gfm.0 [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.7
     - 0.30.0
     - ``github``
     - 0.29.gfm.0 [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.8
     - 0.30.0
     - ``github``
     - 0.29.gfm.0 [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.1.9
     - 0.30.0
     - ``github``
     - 0.29.gfm.0 [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0
   * - 8.2.0
     - 0.30.0
     - ``github``
     - 0.29.gfm.0 [#f2]_
     - latest version
     - ``cmark``
     - v3.5.0


.. |r1| replace:: https://github.com/vmg/redcarpet/tree/26c80f05e774b31cd01255b0fa62e883ac185bf3
.. |r2| replace:: https://github.com/vmg/redcarpet/tree/e3a1d0b00a77fa4e2d3c37322bea66b82085486f
.. |r3| replace:: https://github.com/vmg/redcarpet/tree/94f6e27bdf2395efa555a7c772a3d8b70fb84346

Supported markdown parsers
--------------------------

- ``cmark``:

  - "CommonMark parsing and rendering library and program in C".

- ``commonmarker``:

  - a "Ruby wrapper for libcmark (CommonMark parser)".

  - as described on their website: "It also includes extensions to
    the CommonMark spec as documented in the GitHub Flavored Markdown spec,
    such as support for tables, strikethroughs, and autolinking.". For this
    reason we assume that ``commonmarker`` is an alias of ``github``.

- ``github``:

  - uses a forked version of ``cmark`` with some added extensions.
    This language specification is called GitHub Flavored Markdown.

  - there are subtle differences that affect md-toc such as

    - the disallowed raw HTML extension which affects md-toc
    - emphasis processing

- ``gitlab``:

  - uses ``commonmarker``. Older versions of md-toc, prior to
    version ``3.0.0``, use ``gitlab`` as an alias of ``redcarpet`` while
    newer versions use ``github`` instead. In the past GitLab used
    Redcarpet as markdown parser.

  - some extensions used in GitLab Flavored Markdown, not to be confused
    with GitHub Flavored Markdown, are different from the ones used in GitHub Flavored Markdown.

  .. seealso::

     - _`Documentation Style Guide | GitLab - Documentation is the single source of truth (SSOT)` [#f3]_

- ``goldmark``:

  - this parser claims to be compliant with CommonMark: `goldmark is compliant with CommonMark 0.30.`.
    For this reason ``goldmark`` is an alias of ``cmark``.

- ``redcarpet``:

  - "The safe Markdown parser, reloaded."

Other markdown parsers
----------------------

If you have a look at [#f4]_
you will see that there are a ton of different markdown parsers out there.
Moreover, that list has not been updated in a while.

Markdown parsers have different behaviours regarding anchor links. Some of them
implement them while others don't; some act on the duplicate entry problem
while others don't; some strip consecutive dash characters while others don't.
And it's not just about anchor links, as you can read in the rules section.
For example:

- Gitea apparently uses ``goldmark`` as markdown parser. See [#f5]_ [#f6]_.
  There are same cases where there is a discrepancy with ``cmark``:

  - ``this is - a test`` is rendered as

    - ``this-is---a-test`` by cmark
    - ``this-is-a-test`` by Gitea

  Gitea adds an annoying ``user-content`` substring in the TOC's anchor links. This is true
  for versions since git tag v1.11.0. See [#f7]_ [#f8]_ [#f9]_ [#f10]_.

  The ``user-content`` substring does not seem to affect the functionality of the TOC.

  Older versions of Gitea used blackfriday. See [#f11]_.
- Gogs uses Marked as the markdown parser. See [#f12]_ [#f13]_ [#f14]_ [#f15]_.
- Notabug: *Notabug is powered by a liberated version of gogs*. See [#f16]_.
- Kramdown: It is unclear if this feature is available. See [#f17]_
- Gitlab Kramdown. See [#f18]_

Steps to add an unsupported markdown parser
```````````````````````````````````````````

1. Find the source code and/or documents.
2. Find the rules for each section, such as anchor link generation, title
   detection, etc... Rely more on the source code than on the documentation (if
   possible)
3. Add the relevant information on this page.
4. Write or adapt an algorithm for that section.
5. Write unit tests for it.
6. Add the new parser to the CLI interface.

.. rubric:: Footnotes

.. [#f1] used alias ``github``
.. [#f2] when this md-toc version was released GFM still needed to catch up with cmark
.. [#f3] https://docs.gitlab.com/ee/development/documentation/styleguide/#documentation-is-the-single-source-of-truth-ssot
.. [#f4] https://www.w3.org/community/markdown/wiki/MarkdownImplementations
.. [#f5] https://github.com/go-gitea/gitea
.. [#f6] https://github.com/go-gitea/gitea/blob/71aca93decc10253133dcd77b64dae5d311d7163/modules/markup/markdown/goldmark.go
.. [#f7] https://github.com/go-gitea/gitea/blob/71aca93decc10253133dcd77b64dae5d311d7163/modules/markup/markdown/goldmark.go#L230
.. [#f8] https://github.com/go-gitea/gitea/issues/12062
.. [#f9] https://github.com/go-gitea/gitea/pull/11903
.. [#f10] https://github.com/go-gitea/gitea/pull/12805
.. [#f11] https://github.com/go-gitea/gitea/blob/2a03e96bceadfcc5e18bd61e755980ee72dcdb15/modules/markup/markdown/markdown.go
.. [#f12] https://gogs.io/docs
.. [#f13] https://github.com/chjj/marked
.. [#f14] https://github.com/chjj/marked/issues/981
.. [#f15] https://github.com/chjj/marked/search?q=anchor&type=Issues&utf8=%E2%9C%93
.. [#f16] https://github.com/gettalong/kramdown/search?q=anchor&type=Issues&utf8=%E2%9C%93
.. [#f17] https://github.com/gettalong/kramdown/search?q=anchor&type=Issues&utf8=%E2%9C%93
.. [#f18] https://gitlab.com/gitlab-org/gitlab_kramdown/-/blob/master/lib/gitlab_kramdown/parser/header.rb
