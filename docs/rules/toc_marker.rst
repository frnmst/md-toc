TOC marker
==========

A TOC marker is a string that marks that the start and the end of the table
of contents in a markdown file.

By default it was decided to use ``[](TOC)`` as the default TOC marker because
it would result invisible in some markdown parsers. In other cases, however, such
as the one used by Gitea, that particular TOC marker was still visible. HTML
comments seem to be a better solution.

``cmark``, ``github``, ``gitlab``
---------------------------------

- https://spec.commonmark.org/0.30/#html-comment

``redcarpet``
-------------

I cannot find the corresponding code, but I found this:

- https://github.com/vmg/redcarpet/blob/master/test/MarkdownTest_1.0.3/Tests/Inline%20HTML%20comments.html
