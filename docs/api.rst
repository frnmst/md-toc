Developer Interface
===================

.. module:: md_toc

Main Interface
--------------

Examples for the most relevant api functions can be viewed in the test
file. md_toc's API uses `type hints`_ instead of assertions to check input and
output types.

.. _type hints: https://docs.python.org/3/library/typing.html

.. autofunction:: get_atx_heading
.. autofunction:: get_md_header
.. autofunction:: build_toc_line
.. autofunction:: increase_index_ordered_list
.. autofunction:: build_anchor_link
.. autofunction:: build_toc
.. autofunction:: build_multiple_tocs
.. autofunction:: write_string_on_file_between_markers
.. autofunction:: write_strings_on_files_between_markers
.. autofunction:: init_indentation_log
.. autofunction:: compute_toc_line_indentation_spaces
.. autofunction:: build_toc_line_without_indentation
.. autofunction:: is_valid_code_fence_indent
.. autofunction:: is_opening_code_fence
.. autofunction:: is_closing_code_fence
.. autofunction:: init_indentation_status_list
.. autofunction:: toc_renders_as_coherent_list
.. autofunction:: remove_html_tags
.. autofunction:: remove_emphasis
.. autofunction:: replace_and_split_newlines


Exceptions
----------

.. autoexception:: GithubOverflowCharsLinkLabel
.. autoexception:: GithubEmptyLinkLabel
.. autoexception:: GithubOverflowOrderedListMarker
.. autoexception:: StdinIsNotAFileToBeWritten
.. autoexception:: TocDoesNotRenderAsCoherentList
.. autoexception:: StringCannotContainNewlines
