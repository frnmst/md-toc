#
# cli.py
#
# Copyright (C) 2017 frnmst (Franco Masotti) <franco.masotti@live.com>
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
import pkg_resources
from .api import (write_string_on_file_between_markers, build_toc)


class CliToApi():
    """An interface between the CLI and API functions."""

    def write_toc(self, args):
        """Write the table of contents."""
        if args.toc_marker is None:
            args.toc_marker = '[](TOC)'
        if args.parser is None:
            args.parser = 'standard'
        toc = build_toc(
            filename=args.filename,
            ordered=args.ordered,
            no_links=args.no_links,
            max_header_levels=int(args.header_levels),
            anchor_type=args.parser)
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
            description='Markdown Table Of Contents',
            epilog="Return values: 0 OK, 1 Error, 2 Invalid command")
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
            choices=['standard', 'github', 'redcarpet', 'gitlab'],
            default='standard',
            help='decide what markdown parser will be used to generate the \
                  links. Defaults to standard')
        parser.add_argument(
            '-t',
            '--toc-marker',
            metavar='TOC_MARKER',
            help='set the string to be used as the marker for positioning the \
                  table of contents')
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
            version=pkg_resources.get_distribution('md_toc').version)

        parser.set_defaults(func=CliToApi().write_toc)

        return parser
