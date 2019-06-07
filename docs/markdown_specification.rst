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

  - "CommonMark parsing and rendering library and program in C".

- ``commonmarker``:

  - a "Ruby wrapper for libcmark (CommonMark parser)". 

  - As described on their website: "It also includes extensions to 
    the CommonMark spec as documented in the GitHub Flavored Markdown spec,
    such as support for tables, strikethroughs, and autolinking.". For this 
    reason we assume that ``commonmarker`` is an alias of ``github``.

- ``github``: 

  - uses a forked version of ``cmark`` with some added extensions
    which should not concern md_toc. For this reason we assume that ``cmark`` 
    and ``github`` represent the same parser in md_toc.

- ``gitlab``: 
  
  - uses ``commonmarker``. Older versions of md_toc, prior to 
    version ``3.0.0``, use ``gitlab`` as an alias of ``redcarpet`` while 
    newer versions use ``github`` instead, because in the past GitLab used 
    Redcarpet as markdown parser.

  - The extensions used in GitLab Flavored Markdown (not to be confused 
    with GitHub Flavored Markdown) should not concern md_toc. For this 
    reason we assume that ``gitlab`` is an alias of ``github``.

- ``redcarpet``:

  - "The safe Markdown parser, reloaded."

Parser Summary
``````````````

   ===================   ============   ==================================================================================  =============================================
   Parser                Alias of       Supported parser version                                                            Source
   ===================   ============   ==================================================================================  =============================================
   ``cmark``             ``github``                                                                                         https://github.com/commonmark/cmark
   ``commonmarker``      ``github``                                                                                         https://github.com/gjtorikian/commonmarker
   ``github``                           ``Version 0.28-gfm (2017-08-01)``                                                   https://github.com/github/cmark
   ``gitlab``            ``github``                                                                                         https://docs.gitlab.com/ee/user/markdown.html
   ``redcarpet``                        ``https://github.com/vmg/redcarpet/tree/94f6e27bdf2395efa555a7c772a3d8b70fb84346``  https://github.com/vmg/redcarpet
   ===================   ============   ==================================================================================  =============================================

Rules
-----

Headers
```````

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

- ``redcarpet``: this is the license used in md_toc:


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
```````````````

Problems
^^^^^^^^

We are interested in sublists indentation rules for all types of lists, and 
integer overflows in case of ordered lists.

For ordered lists, we are not concerned about using ``0`` or negative numbers 
as list markers so these cases will not be considered. Infact ordred lists 
generated by md_toc will always start from ``1``.

Talking about indentation rules, I need to mention that the user is responsible 
for generating a correct markdown list according to the parser's rules. Let's 
see this example:


  ::

     # foo
     ## bar
     ### baz


no problem here because this is rendered by md_toc, using ``github`` as parser, 
with:


  ::

     - [foo](#foo)
       - [bar](#bar)
         - [baz](#baz)


Now, let's take the previous example and reverse the order of the lines:


  ::

     ### baz
     ## bar
     # foo


and this is what md_toc renders using ``github``:


  ::


    - [baz](#baz)
    - [foo](#foo)
    - [bar](#bar)


while the user might expect this:


  ::


        - [baz](#baz)
      - [foo](#foo)
    - [bar](#bar)

Indentation
^^^^^^^^^^^

- ``github``: list indentation for sublists with this parser is based on the 
  previous state, as stated in the GitHub Flavored Markdown document, at 
  section 5.2:

    "The most important thing to notice is that the position of the text after the 
    list marker determines how much indentation is needed in subsequent blocks in 
    the list item. If the list marker takes up two spaces, and there are three 
    spaces between the list marker and the next non-whitespace character, then 
    blocks must be indented five spaces in order to fall under the list item."

  - https://github.github.com/gfm/#list-items

  This is also true with the specular case: if our new list element needs less 
  indentation than the one processed currently, we have to use the same number
  of indentation spaces used somewhere earlier in the list.

- ``redcarpet``:

  - https://github.com/vmg/redcarpet/blob/94f6e27bdf2395efa555a7c772a3d8b70fb84346/ext/redcarpet/markdown.c#L1553
  - https://github.com/vmg/redcarpet/blob/94f6e27bdf2395efa555a7c772a3d8b70fb84346/ext/redcarpet/markdown.c#L1528

  The following C function returns the first non-whitespace character
  after the list marker. The value of ``0`` is returned if the input
  line is not a list element. List item rules are explained in the 
  single line comments.

  .. highlight:: c

  ::


      /* prefix_uli • returns unordered list item prefix */
      static size_t
      prefix_uli(uint8_t *data, size_t size)
      {
          size_t i = 0;

          // There can be up to 3 whitespaces before the list marker.
          if (i < size && data[i] == ' ') i++;
          if (i < size && data[i] == ' ') i++;
          if (i < size && data[i] == ' ') i++;

          // The next non-whitespace character must be a list marker and
          // the character after the list marker must be a whitespace.
          if (i + 1 >= size ||
             (data[i] != '*' && data[i] != '+' && data[i] != '-') ||
              data[i + 1] != ' ')
              return 0;

          // Check that the next line is not a header
          // that uses the `-` or `=` characters as markers.
          if (is_next_headerline(data + i, size - i))
              return 0;

          // Return the first non whitespace character after the list marker.
          return i + 2;
      }


  As far as I can tell from the previous and other functions, on a new list 
  block the 4 spaces indentation rule applies:

  - https://github.com/vmg/redcarpet/blob/94f6e27bdf2395efa555a7c772a3d8b70fb84346/ext/redcarpet/markdown.c#L1822
  - https://github.com/vmg/redcarpet/blob/94f6e27bdf2395efa555a7c772a3d8b70fb84346/ext/redcarpet/markdown.c#L1873

  This means that anything that has more than 3 whitespaces is considered as 
  sublist. The only exception seems to be for the first sublist in a list 
  block, in which that case even a single whitespace counts as a sublist. 
  The 4 spaces indentation rule appllies nontheless, so to keep things simple 
  md_toc will always use 4 whitespaces for sublists. Apparently, ordered and 
  unordered lists share the same proprieties.

  Let's see this example:


  ::


      - I
       - am
           - foo

      stop

      - I 
          - am
              - foo


  This is how redcarpet renders it once you run ``$ redcarpet``:


   ::


      <ul>
      <li>I

      <ul>
      <li>am

      <ul>
      <li>foo</li>
      </ul></li>
      </ul></li>
      </ul>

      <p>stop</p>

      <ul>
      <li>I

      <ul>
      <li>am

      <ul>
      <li>foo</li>
      </ul></li>
      </ul></li>
      </ul>


  What follows is an extract of a C function in redcarpet that parses list 
  items. I have added all the single line comments.


  .. highlight:: c


  ::


        /* parse_listitem • parsing of a single list item */
        /*  assuming initial prefix is already removed */
        static size_t
        parse_listitem(struct buf *ob, struct sd_markdown *rndr, uint8_t *data, 
        size_t size, int *flags)
        {
            struct buf *work = 0, *inter = 0;
            size_t beg = 0, end, pre, sublist = 0, orgpre = 0, i;
            int in_empty = 0, has_inside_empty = 0, in_fence = 0;

            // This is the base case, usually of indentation 0 but it can be
            // from 0 to 3 spaces. If it was 4 spaces it would be a code 
            // block.
            /* keeping track of the first indentation prefix */
            while (orgpre < 3 && orgpre < size && data[orgpre] == ' ')
                orgpre++;

            // Get the first index of string after the list marker. Try both 
            // ordered and unordered lists
            beg = prefix_uli(data, size);
            if (!beg)
                beg = prefix_oli(data, size);

            if (!beg)
                return 0;

            /* skipping to the beginning of the following line */
            end = beg;
            while (end < size && data[end - 1] != '\n')
                end++;

            // Iterate line by line using the '\n' character as delimiter.
            /* process the following lines */
            while (beg < size) {
                size_t has_next_uli = 0, has_next_oli = 0;

                // Go to the next line.
                end++;

                // Find the end of the line.
                while (end < size && data[end - 1] != '\n')
                    end++;

                // Skip the next line if it is empty.
                /* process an empty line */
                if (is_empty(data + beg, end - beg)) {
                    in_empty = 1;
                    beg = end;
                    continue;
                }

                // Count up to 4 characters of indentation.
                // If we have 4 characters then it might be a sublist.
                // Note that this is an offset and does not point to an
                // index in the actual line string.
                /* calculating the indentation */
                i = 0;
                while (i < 4 && beg + i < end && data[beg + i] == ' ')
                    i++;

                pre = i;

                /* Only check for new list items if we are **not** inside
                 * a fenced code block */
                 if (!in_fence) {
                   has_next_uli = prefix_uli(data + beg + i, end - beg - i);
                   has_next_oli = prefix_oli(data + beg + i, end - beg - i);
                }

                /* checking for ul/ol switch */
                if (in_empty && (
                    ((*flags & MKD_LIST_ORDERED) && has_next_uli) ||
                    (!(*flags & MKD_LIST_ORDERED) && has_next_oli))){
                    *flags |= MKD_LI_END;
                    break; /* the following item must have same list type */
                }

                // Determine if we are dealing with:
                // - an empty line
                // - a new list item
                // - a sublist
                /* checking for a new item */
                if ((has_next_uli && !is_hrule(data + beg + i, end - beg - i)) || has_next_oli) {
                    if (in_empty)
                        has_inside_empty = 1;

                    // The next list item's indentation (pre) must be the same as 
                    // the previous one (orgpre), otherwise it might be a 
                    // sublist.
                    if (pre == orgpre) /* the following item must have */
                        break;             /* the same indentation */
    
                    // If the indentation does not match the previous one then
                    // assume that it is a sublist. Check later whether it is
                    // or not.
                    if (!sublist)
                        sublist = work->size;
                }
                /* joining only indented stuff after empty lines */
                else if (in_empty && i < 4 && data[beg] != '\t') {
                    *flags |= MKD_LI_END;
                    break;
                }
                else if (in_empty) {
                    // Add a line delimiter to the next line if it is missing.
                    bufputc(work, '\n');
                    has_inside_empty = 1;
                }

                in_empty = 0;
                beg = end;
            }

            if (*flags & MKD_LI_BLOCK) {
                /* intermediate render of block li */
                if (sublist && sublist < work->size) {
                    parse_block(inter, rndr, work->data, sublist);
                    parse_block(inter, rndr, work->data + sublist, work->size - sublist);
            }
            else
                parse_block(inter, rndr, work->data, work->size);
        }


  According to the code, ``parse_listitem`` is called indirectly by 
  ``parse_block`` (via ``parse_list``), but ``parse_block`` is called directly 
  by ``parse_listitem`` so the code analysis 
  is not trivial. For this reason I might be mistaken about the 4 spaces 
  indentation rule.

  - https://github.com/vmg/redcarpet/blob/94f6e27bdf2395efa555a7c772a3d8b70fb84346/ext/redcarpet/markdown.c#L2418
  - https://github.com/vmg/redcarpet/blob/94f6e27bdf2395efa555a7c772a3d8b70fb84346/ext/redcarpet/markdown.c#L1958

  Here is an extract of the ``parse_block`` function with the calls to 
  ``parse_list``:

  .. highlight:: c

  ::


      /* parse_block • parsing of one block, returning next uint8_t to parse */
      static void
      parse_block(struct buf *ob, struct sd_markdown *rndr, uint8_t *data, size_t 
      size)
      {
          while (beg < size) {

              else if (prefix_uli(txt_data, end))
                beg += parse_list(ob, rndr, txt_data, end, 0);

              else if (prefix_oli(txt_data, end))
                beg += parse_list(ob, rndr, txt_data, end, MKD_LIST_ORDERED);
          }
      } 


Overflows
^^^^^^^^^

- ``github``: ordered list markers cannot exceed ``99999999`` according to 
  the following. If that is the case then a  ``GithubOverflowOrderedListMarker``
  exception is raised:

  - https://github.github.com/gfm/#ordered-list-marker
  - https://spec.commonmark.org/0.28/#ordered-list-marker

- ``redcarpet``: apparently there are no cases of ordered list marker 
  overflows:

  - https://github.com/vmg/redcarpet/blob/8db31cb83e7d81b19970466645e899b5ac3bc15d/ext/redcarpet/markdown.c#L1529  

Link label
``````````

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


- ``redcarpet``:

  - https://github.com/vmg/redcarpet/blob/e3a1d0b00a77fa4e2d3c37322bea66b82085486f/ext/redcarpet/markdown.c#L998

  Let's inspect this loop:

  - https://github.com/vmg/redcarpet/blob/e3a1d0b00a77fa4e2d3c37322bea66b82085486f/ext/redcarpet/markdown.c#L1017):

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
````````````````````````````````

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


- ``redcarpet``: treats consecutive dash characters by tranforming them 
  into a single dash character. A translated version of the C algorithm 
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


Code fence
``````````

Code fences are sections of a markdown document where some parsers treat the 
text within them as verbatim. Usually the purpose of these sections is to 
display source code. Some programming languages use the character ``#`` as a 
way to comment a line in the code. For this reason md_toc needs to ignore code 
fences in order not to treat the ``#`` character as an ATX-style heading and thus
get parsed as an element of the TOC.

- ``github``: the rules followed are the ones reported on the 
  documentation:

  - https://github.github.com/gfm/#code-fence

- ``redcarpet``: needs to be implemented:

  - https://github.com/vmg/redcarpet/blob/26c80f05e774b31cd01255b0fa62e883ac185bf3/ext/redcarpet/markdown.c#L1389

TOC marker
``````````

A TOC marker is a string that marks that the start and the end of the table
of contents in a markdown file.

By default it was decided to use ``[](TOC)`` as the default TOC marker because
it would result invisible in some markdown parsers. In other cases, however, such
as the one used by Gitea, that particular TOC marker was still visible. HTML 
comments seem to be a better solution.

- ``github``:

  - https://spec.commonmark.org/0.28/#html-comment

- ``redcarpet``:

  I cannot find the corresponding code, but I found this:

  - https://github.com/vmg/redcarpet/blob/master/test/MarkdownTest_1.0.3/Tests/Inline%20HTML%20comments.html

Other markdown parsers
----------------------

If you have a look at 
https://www.w3.org/community/markdown/wiki/MarkdownImplementations
you will see that there are a ton of different markdown parsers out there.
Moreover, that list has not been updated in a while.

Markdown parsers have different behaviours regarding anchor links. Some of them 
implement them while others don't; some act on the duplicate entry problem 
while others don't; some strip consecutive dash characters while others don't.
And it's not just about anchor links, as you have read before. For example:

- Gogs, Marked, Notabug, Gitea: Gogs uses marked as the markdown 
  parser while *NotABug.org is powered by a liberated version of gogs*.
  Gitea, a fork of Gogs, probably uses a custom parser. See link below.
  Situation is unclear. Here are some links:

  - https://gogs.io/docs
  - https://github.com/chjj/marked
  - https://github.com/chjj/marked/issues/981
  - https://github.com/chjj/marked/search?q=anchor&type=Issues&utf8=%E2%9C%93
  - https://notabug.org/hp/gogs/
  - https://github.com/go-gitea/gitea
  - https://github.com/go-gitea/gitea/blob/2a03e96bceadfcc5e18bd61e755980ee72dcdb15/modules/markup/markdown/markdown.go

  For this reason no implementation is available for the moment.

- Kramdown: It is unclear if this feature is available. See:

  - https://github.com/gettalong/kramdown/search?q=anchor&type=Issues&utf8=%E2%9C%93

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
