Markdown spec
=============

Introduction
------------

md-toc aimes to be as conformant as possible to each supported markdown
parser. What follows is a list of parameters and rules used by md-toc to decide
how to parse markdown files and to generate the table of contents.

.. include:: compatibility_table.rst

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

  - there are subtle differences such as
    the disallowed raw HTML extension which affects md-toc.

- ``gitlab``:

  - uses ``commonmarker``. Older versions of md-toc, prior to
    version ``3.0.0``, use ``gitlab`` as an alias of ``redcarpet`` while
    newer versions use ``github`` instead. In the past GitLab used
    Redcarpet as markdown parser.

  - some extensions used in GitLab Flavored Markdown, not to be confused
    with GitHub Flavored Markdown, are different from the ones used in GitHub Flavored Markdown.

  - see also

    - https://docs.gitlab.com/ee/development/documentation/styleguide/#documentation-is-the-single-source-of-truth-ssot

- ``goldmark``:

    - this parser claims to be compliant with CommonMark: `goldmark is compliant with CommonMark 0.30.`.
      For this reason ``goldmark`` is an alias of ``cmark``.

- ``redcarpet``:

  - "The safe Markdown parser, reloaded."

Other markdown parsers
----------------------

If you have a look at
https://www.w3.org/community/markdown/wiki/MarkdownImplementations
you will see that there are a ton of different markdown parsers out there.
Moreover, that list has not been updated in a while.

Markdown parsers have different behaviours regarding anchor links. Some of them
implement them while others don't; some act on the duplicate entry problem
while others don't; some strip consecutive dash characters while others don't.
And it's not just about anchor links, as you have read earlier. For example:

- Gitea apparently uses ``goldmark`` as markdown parser. See:

  - https://github.com/go-gitea/gitea
  - https://github.com/go-gitea/gitea/blob/71aca93decc10253133dcd77b64dae5d311d7163/modules/markup/markdown/goldmark.go

  Gitea adds an annoying ``user-content`` substring in the TOC's anchor links. This is true
  for versions since git tag v1.11.0. See:

  - https://github.com/go-gitea/gitea/blob/71aca93decc10253133dcd77b64dae5d311d7163/modules/markup/markdown/goldmark.go#L230
  - https://github.com/go-gitea/gitea/issues/12062
  - https://github.com/go-gitea/gitea/pull/11903
  - https://github.com/go-gitea/gitea/pull/12805

  The ``user-content`` substring does not seem to affect the functionality of the TOC.

  Older versions of Gitea used blackfriday. See:

  - https://github.com/go-gitea/gitea/blob/2a03e96bceadfcc5e18bd61e755980ee72dcdb15/modules/markup/markdown/markdown.go

- Gogs uses Marked as the markdown parser:

  - https://gogs.io/docs
  - https://github.com/chjj/marked
  - https://github.com/chjj/marked/issues/981
  - https://github.com/chjj/marked/search?q=anchor&type=Issues&utf8=%E2%9C%93

- Notabug: *Notabug is powered by a liberated version of gogs*:

  - https://notabug.org/hp/gogs/

- Kramdown: It is unclear if this feature is available. See:

  - https://github.com/gettalong/kramdown/search?q=anchor&type=Issues&utf8=%E2%9C%93

- Gitlab Kramdown

  - https://gitlab.com/gitlab-org/gitlab_kramdown/-/blob/master/lib/gitlab_kramdown/parser/header.rb

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

Curiosities
-----------

- GitLab added an extension called ``Table of contents`` to
  its `Gitlab Flavored Mardown`. See:
  https://docs.gitlab.com/ee/user/markdown.html#table-of-contents
- in March 2021 GitHub added an interactive TOC button on the readme files of repositories which works
  works for markdown and other systems.
