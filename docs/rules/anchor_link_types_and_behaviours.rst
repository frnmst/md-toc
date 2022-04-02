Anchor link types and behaviours
================================

Generic
-------

``cmark``, ``github``
`````````````````````

A translated version of the Ruby algorithm is used in md-toc.
The original one is repored here:

- https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb

I could not find the code directly responsable for the anchor link generation.
See also:

- https://github.github.com/gfm/
- https://githubengineering.com/a-formal-spec-for-github-markdown/
- https://github.com/github/cmark/issues/65#issuecomment-343433978

Apparently GitHub (and possibly others) filter HTML tags in the anchor links.
This is an undocumented feature (?) so the ``remove_html_tags`` function was
added to address this problem. Instead of designing an algorithm to detect HTML tags,
regular expressions came in handy. All the rules
present in https://spec.commonmark.org/0.28/#raw-html have been followed by the
letter. Regular expressions are divided by type and are composed at the end
by concatenating all the strings. For example:

.. code-block:: python
   :linenos:

   # Comment start.
   COS = '<!--'
   # Comment text.
   COT = '((?!>|->)(?:(?!--).))+(?!-).?'
   # Comment end.
   COE = '-->'
   # Comment.
   CO = COS + COT + COE

HTML tags are stripped using the ``re.sub`` replace function, for example:

.. code-block:: ruby

   line = re.sub(CO, str(), line, flags=re.DOTALL)

GitHub added an extension in GFM to ignore certain HTML tags, valid at least from versions `0.27.1.gfm.3` to `0.29.0.gfm.0`:

- https://github.github.com/gfm/#disallowed-raw-html-extension-
- https://github.com/github/cmark-gfm/blob/fca380ca85c046233c39523717073153e2458c1e/extensions/tagfilter.c

``gitlab``
``````````

New rules have been written:

- https://docs.gitlab.com/ee/user/markdown.html#header-ids-and-links

``redcarpet``
`````````````

Treats consecutive dash characters by tranforming them
into a single dash character. A translated version of the C algorithm
is used in md-toc. The original version is here:

- https://github.com/vmg/redcarpet/blob/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae/ext/redcarpet/html.c#L274

See also:

- https://github.com/vmg/redcarpet/issues/618#issuecomment-306476184
- https://github.com/vmg/redcarpet/issues/307#issuecomment-261793668

Emphasis
--------

To be able to have working anchor links, emphasis must also be removed from the
link destination.

``cmark``,  ``github``, ``gitlab``
``````````````````````````````````

At the moment the implementation of emnphasis removal is incomplete
because of its complexity. See:

- https://spec.commonmark.org/0.30/#emphasis-and-strong-emphasis

The core functions for this feature have been ported directly
from the original cmark source with some differences:

#. things such as string manipulation, mallocs, etc are different in Python

#. the ``cmark_utf8proc_charlen`` uses ``length = 1``
   instead of ``length = utf8proc_utf8class[ord(line[0])]``
   (causes list overflow).

   The ``cmark_utf8proc_charlen`` function is related to
   the ``cmark_utf8proc_encode_char`` function. Have a look at that function to
   know character lengths in cmark.

   In Python 3, since all characters are UTF-8 by default, they are all
   represented with length 1. See:

   - https://rosettacode.org/wiki/String_length#Python
   - https://docs.python.org/3/howto/unicode.html#comparing-strings
