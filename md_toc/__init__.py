#
# __init__.py
#
# Copyright (C) 2017-2019 frnmst (Franco Masotti) <franco.masotti@live.com>
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
    get_md_header, get_atx_heading, build_toc_line,
    increase_index_ordered_list, build_anchor_link, build_list_marker_log,
    compute_toc_line_indentation_spaces, build_toc_line_without_indentation,
    build_toc, build_multiple_tocs, write_string_on_file_between_markers,
    write_strings_on_files_between_markers, is_valid_code_fence_indent,
    is_opening_code_fence, is_closing_code_fence)
from .cli import (CliInterface)
from .exceptions import (GithubOverflowCharsLinkLabel, GithubEmptyLinkLabel,
                         GithubOverflowOrderedListMarker,
                         StdinIsNotAFileToBeWritten)
