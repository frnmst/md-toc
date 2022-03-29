Headers
=======

Only ATX-style headings are supported in md-toc.

``cmark``, ``github``, ``gitlab``
---------------------------------

The code used in md-toc is a reverse engineering of the
behavour described in the following:

- https://spec.commonmark.org/0.30/#atx-heading

The escape character ``\`` will be left as-is since they are parsed by
Github's markdown parser already:

- https://spec.commonmark.org/0.30/#backslash-escapes

A line ending character is ``U+000A`` or the ``U+000D`` character,
respectively ``\n`` and ``\r`` (or ``\r\n`` if combined).
Everything following those characters is ignored.
This has also the benefit to automatically remove
the trailing newline or carriage return at the end of each line. This also
includes ATX headers with line endings only as main content, such as
``#\n`` or ``#\r``. See also:

- https://spec.commonmark.org/0.30/#line
- https://spec.commonmark.org/0.30/#line-ending

Every other rule for ATX headings is applied.

``redcarpet``
-------------

See license A

- https://github.com/vmg/redcarpet/blob/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae/ext/redcarpet/markdown.c#L1444
- https://github.com/vmg/redcarpet/blob/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae/ext/redcarpet/markdown.c#L1981

Line endings are generically ``\n`` or ``\r`` characters. See:

- https://github.com/vmg/redcarpet/blob/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae/ext/redcarpet/markdown.c#L2845
- https://github.com/vmg/redcarpet/blob/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae/ext/redcarpet/markdown.c#L2854
