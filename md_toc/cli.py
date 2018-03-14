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
import copy
import pkg_resources
from .api import (write_string_on_file_between_markers, build_toc)
from .constants import common_defaults
from .constants import parser as md_parser

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
        # FIXME: Can this logic be moved into the create_parser function?
        ordered = False
        if args.parser == 'github' or args.parser == 'cmark':
            if args.ordered_list_marker is not None:
                list_marker = args.ordered_list_marker
                ordered = True
            elif args.unordered_list_marker is not None:
                list_marker = args.unordered_list_marker
            else:
                list_marker = md_parser['github']['list']['unordered']

        toc = build_toc(
            filename=args.filename,
            ordered=ordered,
            no_links=args.no_links,
            keep_header_levels=int(args.header_levels),
            parser=args.parser,
            list_marker=list_marker)
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

        subparsers = parser.add_subparsers(
            dest='parser', title='markdown parser')
        subparsers.required = False

        # Common optional parameters.
        in_place = [
            '-i', '--in-place', 'store_true', 'overwrite the input file'
        ]
        no_links = [
            '-n', '--no-links', 'store_true',
            'avoids adding links to the corresponding content'
        ]
        toc_marker = [
            '-t', '--toc-marker', 'TOC_MARKER',
            'set the string to be used as the marker for positioning the \
                      table of contents. Defaults to ' +
            common_defaults['toc_marker']
        ]

        # Github + cmark.
        github = subparsers.add_parser('github', aliases=['cmark'])
        github.add_argument(
            in_place[0], in_place[1], action=in_place[2], help=in_place[3])
        github.add_argument(
            no_links[0], no_links[1], action=no_links[2], help=no_links[3])
        megroup = github.add_mutually_exclusive_group()
        megroup.add_argument(
            '-u',
            '--unordered-list-marker',
            choices=md_parser['github']['list']['unordered']['bullet_markers'],
            nargs='?',
            const=md_parser['github']['list']['unordered']['default_marker'],
            help='set the marker and enables unordered list. Defaults to ' +
            md_parser['github']['list']['unordered']['default_marker'])
        megroup.add_argument(
            '-o',
            '--ordered-list-marker',
            choices=md_parser['github']['list']['ordered']['closing_markers'],
            nargs='?',
            const=md_parser['github']['list']['ordered'][
                'default_closing_marker'],
            help='set the marker and enables ordered lists. Defaults to ' +
            md_parser['github']['list']['ordered']['default_closing_marker'])
        github.add_argument(
            '-l',
            '--header-levels',
            choices=[
                str(i)
                for i in range(1,
                               md_parser['github']['header']['max_levels'] + 1)
            ],
            nargs='?',
            const=str(md_parser['github']['header']['default_keep_levels']),
            help='set the maximum level of headers to be considered as part \
                  of the TOC. Defaults to ' +
            str(md_parser['github']['header']['default_keep_levels']))
        github.set_defaults(header_levels='3')
        github.add_argument(
            toc_marker[0],
            toc_marker[1],
            metavar=toc_marker[2],
            help=toc_marker[3])
        github.set_defaults(toc_marker=common_defaults['toc_marker'])

        parser.add_argument(
            'filename', metavar='FILE_NAME', help='the I/O file name')

        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=VERSION_NAME + ' ' + VERSION_NUMBER)

        parser.set_defaults(func=CliToApi().write_toc)

        return parser
