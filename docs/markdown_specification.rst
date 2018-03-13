Markdown spec
=============

Introduction
------------

md_toc aimes to be as conformant as possible to each supported markdown 
parser. What follows is a list of parameters and rules used by md_toc to decide
how to parse markdown files and to generate the table of contents.

Supported markdown parsers
--------------------------

- ``cmark``:

  - https://github.com/commonmark/cmark

- ``github`` uses a forked version of ``cmark``: with some extensions added:

  - https://github.com/github/cmark

  The extension used in GFM (Github Flavored Markdown) should not concern
  md_toc. For this reason we assume that ``cmark`` is an alias of ``github``
  in md_toc.

- ``redcarpet``:

  - https://github.com/vmg/redcarpet

- ``gitlab``:

  Uses ``redcarpet`` with minor modifications. See next.

What are headers and what are not
---------------------------------

Only ATX-style headings are supported in md_toc.

- ``github``: the code used in md_toc is a reverse engineering of the 
  behavour described in the following:

  - https://github.github.com/gfm/#atx-heading

  The escape character ``\`` will be left as-is since they are parsed by 
  Github's markdown parser already:

  - https://github.github.com/gfm/#backslash-escapes

  A line ending character is ``U+000A`` or the ``U+000D`` character,
  respectively ``\n`` and ``\r``. Everything following those characters
  is ignored. This has also the benefit to automatically remove
  the trailing newline or carriage return at the end of each line. This also
  includes ARX headers with line endings only as main content, such as
  ``#\n`` or ``#\r``. See also:

  - https://github.github.com/gfm/#line
  - https://github.github.com/gfm/#line-ending

  Every other rule for ATX headings is applied.

- ``redcarpet``: assume that ``gitlab`` uses the redcarpet algorithm.

  This is the license used in md_toc:

  ::

        Copyright (c) 2009, Natacha Porté
        Copyright (c) 2015, Vicent Marti
        Copyright (c) 2018, Franco Masotti <franco.masotti@student.unife.it>

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:
        
        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.
        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,  ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER  DEALINGS IN
        THE SOFTWARE.


  - https://github.com/vmg/redcarpet/blob/e3a1d0b00a77fa4e2d3c37322bea66b82085486f/ext/redcarpet/markdown.c#L1444
  - https://github.com/vmg/redcarpet/blob/e3a1d0b00a77fa4e2d3c37322bea66b82085486f/ext/redcarpet/markdown.c#L1981

List item rules
---------------

- ``github``: 

  - https://github.github.com/gfm/#list-items

  We are interested in sublists indentation rules...

  Ordered list markers cannot exceed ``99999999`` according to the following. 
  If that is the case, a ``GithubOverflowOrderedListMarker`` exception 
  is raised:

  - https://github.github.com/gfm/#ordered-list-marker

  We are not concerned about using ``0`` or negative numbers as list markers.


All bullet and ordered list markers are supported.

Link label rules
----------------

If the user decides to generate the table of contents with the anchor links,
then link label rules will be applied.

- ``github``:

  - https://github.github.com/gfm/#link-label

  If a line ends in 1 or more '\' characters, this disrupts the anchor
  title. For example ``- [xdmdmsdm\](#xdmdmsdm)`` becomes 
  ``<ul><li>[xdmdmsdm](#xdmdmsdm)</li></ul>`` instead of 
  ``<ul><li><a href="xdmdmsdm">xdmdmsdm\</a></li></ul>``.
  The workaround used in md_toc is to add a space character at the end of the 
  string, so it becomes: ``<ul><li><a href="xdmdmsdm">xdmdmsdm\ </a></li></ul>``

  If the link label contains only whitespace characters a ``GithubEmptyLinkLabel``
  exception is raised.

  If the number of characters inside the link label is over 999 a 
  ``GithubOverflowCharsLinkLabel`` is raised.

  If the headers contains ``[`` or ``]``, these characters 
  are treated with the following rules.

  - https://github.github.com/gfm/#link-text
  - https://github.github.com/gfm/#example-302
  - https://github.github.com/gfm/#example-496

  According to a function in the source code, balanced square brackets do not
  work, however they do when interpeted by the web interface. It is however 
  possible that they are supported within the ``handle_close_bracket`` 
  function.

  - https://github.com/github/cmark/blob/6b101e33ba1637e294076c46c69cd6a262c7539f/src/inlines.c#L881
  - https://github.com/github/cmark/blob/6b101e33ba1637e294076c46c69cd6a262c7539f/src/inlines.c#L994


  Here is the original C function with some more comments added:

  .. highlight:: c

  ::

        // Parse a link label.  Returns 1 if successful.
        // Note:  unescaped brackets are not allowed in labels.
        // The label begins with `[` and ends with the first `]` character
        // encountered.  Backticks in labels do not start code spans.
        static int link_label(subject *subj, cmark_chunk *raw_label) {
          bufsize_t startpos = subj->pos;
          int length = 0;
          unsigned char c;

          // advance past [
          //
          // Ignore the open link label identifier
          // peek_char simply returns the current char if we are
          // in range of the string, 0 otherwise.
          if (peek_char(subj) == '[') {
            advance(subj);
          } else {
            return 0;
          }

          while ((c = peek_char(subj)) && c != '[' && c != ']') {
            // If there is an escape and the next character is (for example) 
            // '[' or ']' then,
            // ignore the loop conditions.
            // If there are nested balanced square brakets this loop ends.
            if (c == '\\') {
              advance(subj);
              length++;

              // Puntuation characters are the ones defined at:
              // https://github.github.com/gfm/#ascii-punctuation-character
              if (cmark_ispunct(peek_char(subj))) {
                advance(subj);
                length++;
              }
            } else {
              advance(subj);
              length++;
            }
            // MAX_LINK_LABEL_LENGTH is a constant defined at
            // https://github.com/github/cmark/blob/master/src/parser.h#L13
            if (length > MAX_LINK_LABEL_LENGTH) {
              goto noMatch;
            }
          }

          // If the loop terminates when the current character is ']' then 
          // everything between '[' and ']' is the link label...
          if (c == ']') { // match found
            *raw_label =
                cmark_chunk_dup(&subj->input, startpos + 1, subj->pos - (startpos + 1));
            cmark_chunk_trim(raw_label);
            advance(subj); // advance past ]
            return 1;
          }

        // ...otherwise return error.
        // This label always get executed according to C rules.
        noMatch:
          subj->pos = startpos; // rewind
          return 0;
        }


  For simpleness the escape ``[`` and ``]`` rule is used.


- ``redcarpet``, ``gitlab``:

  - https://github.com/vmg/redcarpet/blob/e3a1d0b00a77fa4e2d3c37322bea66b82085486f/ext/redcarpet/markdown.c#L998

  Lets inspect this loop (from https://github.com/vmg/redcarpet/blob/e3a1d0b00a77fa4e2d3c37322bea66b82085486f/ext/redcarpet/markdown.c#L1017):

  .. highlight:: c

  ::

        /* looking for the matching closing bracket */
        for (level = 1; i < size; i++) {
            if (data[i] == '\n')
                text_has_nl = 1;

            else if (data[i - 1] == '\\')
                continue;

            else if (data[i] == '[')
                level++;

            else if (data[i] == ']') {
                level--;
                if (level <= 0)
                    break;
            }
        }

        if (i >= size)
            goto cleanup;


  The cleanup label looks like this:

  .. highlight:: c

  ::

            /* cleanup */
            cleanup:
                rndr->work_bufs[BUFFER_SPAN].size = (int)org_work_size;
                return ret ? i : 0;


  .. highlight:: python

  An example: ``[test \](test \)`` becomes ``[test ](test )`` instead of
  ``<a href="test \">test \</a>``

  Infact, you can see that if the current character is ``\\`` then the the 
  current iteration is skipped. If for any chance the next character is ``]`` 
  then the inline link closing parenthesis detection is ignored. ``i`` becomes
  equal to ``size`` eventually and so we jump to the ``cleanup`` label.
  That lable contains a return statement so that string is not treated as 
  inline link anymore. A similar code is implemented also for
  detecting ``(`` and ``)``. See:

  - https://github.com/vmg/redcarpet/blob/e3a1d0b00a77fa4e2d3c37322bea66b82085486f/ext/redcarpet/markdown.c#L1088
  - https://github.com/vmg/redcarpet/blob/e3a1d0b00a77fa4e2d3c37322bea66b82085486f/ext/redcarpet/markdown.c#L1099

  To solve this we use the same workaround used for ``github``.

Anchor link types and behaviours
--------------------------------

- ``github``: a translated version of the Ruby algorithm is used in md_toc. 
  The original one is repored here: 
  
  - https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb

  I could not find the code directly responsable for the anchor link generation.
  See also:

  - https://github.github.com/gfm/
  - https://githubengineering.com/a-formal-spec-for-github-markdown/
  - https://github.com/github/cmark/issues/65#issuecomment-343433978

  This is the license used in md_toc:

  ::

        Copyright (c) 2012 GitHub Inc. and Jerry Cheung
        Copyright (c) 2018, Franco Masotti <franco.masotti@student.unife.it>

        MIT License

        Permission is hereby granted, free of charge, to any person obtaining
        a copy of this software and associated documentation files (the
        "Software"), to deal in the Software without restriction, including
        without limitation the rights to use, copy, modify, merge, publish,
        distribute, sublicense, and/or sell copies of the Software, and to
        permit persons to whom the Software is furnished to do so, subject to
        the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
        NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
        LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
        OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
        WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


- ``redcarpet``: Treats consecutive dash characters by tranforming them into a 
  single dash character. A translated version of the C algorithm 
  is used in md_toc. The original version is here:

  - https://github.com/vmg/redcarpet/blob/26c80f05e774b31cd01255b0fa62e883ac185bf3/ext/redcarpet/html.c#L274

  This is the license used in md_toc:

  ::

        Copyright (c) 2009, Natacha Porté
        Copyright (c) 2015, Vicent Marti
        Copyright (c) 2018, Franco Masotti <franco.masotti@student.unife.it>

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:
        
        The above copyright notice and this permission notice shall be included in
        all copies or substantial portions of the Software.
        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,  ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER  DEALINGS IN
        THE SOFTWARE.


  See also:

  - https://github.com/vmg/redcarpet/issues/618#issuecomment-306476184
  - https://github.com/vmg/redcarpet/issues/307#issuecomment-261793668

- ``gitlab``: GitLab uses the Redcarpet parser with some modifications, such 
  as duplicate anchor link detection. A generic pseudocode is
  available here:

  - https://gitlab.com/help/user/markdown.md#header-ids-and-links


Notes about non implemented markdown parsers in md_toc
------------------------------------------------------

If you have a look at 
https://www.w3.org/community/markdown/wiki/MarkdownImplementations
you will see that there are a ton of different markdown parsers out there 
(moreover, that list has not been updated in a while).

Markdown parsers have different behaviours regarding anchor links. Some of them 
implement them while others don't; some act on the duplicate entry problem 
while others don't; some strip consecutive dash characters while others don't; 
and so on... For example:

- Gogs, Marked and Notabug: Gogs uses marked as the markdown 
  parser while *NotABug.org is powered by a liberated version of gogs*. 
  Situation seems unclear. Here are some links:

  - https://gogs.io/docs
  - https://github.com/chjj/marked
  - https://github.com/chjj/marked/issues/981
  - https://github.com/chjj/marked/search?q=anchor&type=Issues&utf8=%E2%9C%93
  - https://notabug.org/hp/gogs/

  For this reason no implementation is available for the moment.

- Kramdown: It is unclear if this feature is available. See:

  - https://github.com/gettalong/kramdown/search?q=anchor&type=Issues&utf8=%E2%9C%93

