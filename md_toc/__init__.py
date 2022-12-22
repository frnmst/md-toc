# -*- coding: utf-8 -*-
#
# __init__.py
#
# Copyright (C) 2017-2021 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
#
# This file is part of md-toc.
#
# md-toc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# md-toc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with md-toc.  If not, see <http://www.gnu.org/licenses/>.
#
"""Python discovery file."""

from .api import (
    build_anchor_link,
    build_multiple_tocs,
    build_toc,
    build_toc_line,
    build_toc_line_without_indentation,
    compute_toc_line_indentation_spaces,
    filter_indices_from_line,
    get_atx_heading,
    get_md_header,
    increase_index_ordered_list,
    init_indentation_log,
    init_indentation_status_list,
    is_closing_code_fence,
    is_opening_code_fence,
    is_valid_code_fence_indent,
    remove_emphasis,
    remove_html_tags,
    replace_and_split_newlines,
    toc_renders_as_coherent_list,
    write_string_on_file_between_markers,
    write_strings_on_files_between_markers,
)
from .cli import CliInterface
from .exceptions import (
    CannotTreatUnicodeString,
    GithubEmptyLinkLabel,
    GithubOverflowCharsLinkLabel,
    GithubOverflowOrderedListMarker,
    StdinIsNotAFileToBeWritten,
    StringCannotContainNewlines,
    TocDoesNotRenderAsCoherentList,
)
