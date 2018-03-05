Markdown spec
=============

Anchor link types and behaviours
--------------------------------

What follows is a list of parameters and rules used by md_toc to decide 
how to render anchor links. Note that only ``github``, ``redcarpet`` and 
``gitlab`` are currently implemented.

- ``github``: a translated version of the Ruby algorithm is used in md_toc. 
  The original one is repored here: 
  
  - https://github.com/jch/html-pipeline/blob/master/lib/html/pipeline/toc_filter.rb

  GitHub uses a forked version of cmark:

  - https://github.com/github/cmark

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
              

What are headers and what are not
---------------------------------

Only ATX-style headings are supported in md_toc.

- ``github``: the code used in md_toc is a reverse engineering of the 
  behavour described in the following:

  - https://github.github.com/gfm/#atx-heading

  The escape character ``\`` will be left as-is since they are parsed by 
  Github's markdown parser already:

  - https://github.github.com/gfm/#backslash-escapes

  Every other rule is applied.

- ``redcarpet``: asssume that ``gitlab`` uses the redcarpet algorithm.

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

