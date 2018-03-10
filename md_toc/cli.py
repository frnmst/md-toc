#
# cli.py
#
# Copyright (C) 2017-2018 frnmst (Franco Masotti) <franco.masotti@live.com>
#                                            <franco.masotti@student.unife.it>
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
"""Command line interface file."""

import argparse
import textwrap
import pkg_resources
from .api import (write_string_on_file_between_markers, build_toc)

DEFAULT_TOC_MARKER = '[](TOC)'
DEFAULT_MD_PARSER = 'github'
PROGRAM_DESCRIPTION = 'Markdown Table Of Contents: Automatically generate a compliant table\nof contents for a markdown file to improve document readability.'
VERSION_NAME = 'md_toc'
VERSION_NUMBER = str(pkg_resources.get_distribution('md_toc').version)
VERSION_COPYRIGHT = 'Copyright (C) 2018 Franco Masotti, frnmst'
VERSION_LICENSE = 'License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.'
PROGRAM_EPILOG = 'Return values: 0 OK, 1 Error, 2 Invalid command' + '\n\n' + VERSION_COPYRIGHT + '\n' + VERSION_LICENSE


class CliToApi():
    """An interface between the CLI and API functions."""

    def write_toc(self, args):
        """Write the table of contents."""
        if args.toc_marker is None:
            args.toc_marker = DEFAULT_TOC_MARKER
        if args.parser is None:
            args.parser = DEFAULT_MD_PARSER
        toc = build_toc(
            filename=args.filename,
            ordered=args.ordered,
            no_links=args.no_links,
            keep_header_levels=int(args.header_levels),
            parser=args.parser)
        if args.in_place:
            write_string_on_file_between_markers(
                filename=args.filename, string=toc, marker=args.toc_marker)
        else:
            print(toc, end='')


class CliInterface():
    """The interface exposed to the final user."""

    def __init__(self):
        """Set the parser variable that will be used instead of using create_parser."""
        self.parser = self.create_parser()

    def create_parser(self):
        """Create the CLI parser."""
        parser = argparse.ArgumentParser(
            description=PROGRAM_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(PROGRAM_EPILOG))
        parser.add_argument(
            'filename', metavar='FILE_NAME', help='the I/O file name')
        parser.add_argument(
            '-i',
            '--in-place',
            help='overwrite the input file',
            action='store_true')
        parser.add_argument(
            '-n',
            '--no-links',
            help='avoids adding links to corresponding content',
            action='store_true')
        parser.add_argument(
            '-o',
            '--ordered',
            help='write as an ordered list',
            action='store_true')
        parser.add_argument(
            '-p',
            '--parser',
            choices=['github', 'cmark', 'redcarpet', 'gitlab'],
            default=DEFAULT_MD_PARSER,
            help='decide what markdown parser will be used to generate the \
                  links. Defaults to ' + DEFAULT_MD_PARSER)
        parser.add_argument(
            '-t',
            '--toc-marker',
            metavar='TOC_MARKER',
            help='set the string to be used as the marker for positioning the \
                  table of contents. Defaults to ' + DEFAULT_TOC_MARKER)
        parser.add_argument(
            '-l',
            '--header-levels',
            default=3,
            help='set the maximum level of headers to be considered as part \
                  of the TOC')
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=VERSION_NAME + ' ' + VERSION_NUMBER)

        parser.set_defaults(func=CliToApi().write_toc)

        return parser
