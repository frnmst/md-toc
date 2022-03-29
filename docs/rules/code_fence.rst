Code fence
==========

Code fences are sections of a markdown document where some parsers treat the
text within them as verbatim. Usually the purpose of these sections is to
display source code. Some programming languages use the character ``#`` as a
way to comment a line in the code. For this reason md-toc needs to ignore code
fences in order not to treat the ``#`` character as an ATX-style heading and thus
get parsed as an element of the TOC.

``cmark``, ``github``, ``gitlab``
---------------------------------

The rules followed are the ones reported on the
documentation:

- https://spec.commonmark.org/0.30/#code-fence

``redcarpet``
-------------

Needs to be implemented:

- https://github.com/vmg/redcarpet/blob/26c80f05e774b31cd01255b0fa62e883ac185bf3/ext/redcarpet/markdown.c#L1389
