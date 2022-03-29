Link label
==========

If the user decides to generate the table of contents with the anchor links,
then link label rules will be applied.

``cmark``, ``github``, ``gitlab``
---------------------------------

- https://spec.commonmark.org/0.30/#link-label

If a line ends in 1 or more '\' characters, this disrupts the anchor
title. For example ``- [xdmdmsdm\](#xdmdmsdm)`` becomes
``<ul><li>[xdmdmsdm](#xdmdmsdm)</li></ul>`` instead of
``<ul><li><a href="xdmdmsdm">xdmdmsdm\</a></li></ul>``.
The workaround used in md-toc is to add a space character at the end of the
string, so it becomes: ``<ul><li><a href="xdmdmsdm">xdmdmsdm\ </a></li></ul>``

If the link label contains only whitespace characters a ``GithubEmptyLinkLabel``
exception is raised.

If the number of characters inside the link label is over 999 a
``GithubOverflowCharsLinkLabel`` is raised.

If the headers contains ``[`` or ``]``, these characters
are treated with the following rules.

- https://spec.commonmark.org/0.30/#link-text
- https://spec.commonmark.org/0.30/#link-destination

According to a function in the source code, balanced square brackets do not
work, however they do when interpeted by the web interface. It is however
possible that they are supported within the ``handle_close_bracket``
function.

- https://github.com/github/cmark/blob/6b101e33ba1637e294076c46c69cd6a262c7539f/src/inlines.c#L881
- https://github.com/github/cmark/blob/6b101e33ba1637e294076c46c69cd6a262c7539f/src/inlines.c#L994

Here is the original C function with some more comments added:

.. code-block:: c
   :linenos:

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

``redcarpet``
-------------

- https://github.com/vmg/redcarpet/blob/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae/ext/redcarpet/markdown.c#L998

Let's inspect this loop:

- https://github.com/vmg/redcarpet/blob/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae/ext/redcarpet/markdown.c#L1017

.. code-block:: c
   :linenos:

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

.. code-block:: c
   :linenos:

   /* cleanup */
   cleanup:
       rndr->work_bufs[BUFFER_SPAN].size = (int)org_work_size;
       return ret ? i : 0;

An example: ``[test \](test \)`` becomes ``[test ](test )`` instead of
``<a href="test \">test \</a>``

Infact, you can see that if the current character is ``\\`` then the the
current iteration is skipped. If for any chance the next character is ``]``
then the inline link closing parenthesis detection is ignored. ``i`` becomes
equal to ``size`` eventually and so we jump to the ``cleanup`` label.
That lable contains a return statement so that string is not treated as
inline link anymore. A similar code is implemented also for
detecting ``(`` and ``)``. See:

- https://github.com/vmg/redcarpet/blob/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae/ext/redcarpet/markdown.c#L1088
- https://github.com/vmg/redcarpet/blob/6270d6b4ab6b46ee6bb57a6c0e4b2377c01780ae/ext/redcarpet/markdown.c#L1099

To solve this we use the same workaround used for ``cmark``, ``github``, ``gitlab``.
