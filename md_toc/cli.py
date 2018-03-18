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
        if args.ordered_list_marker is not None:
            list_marker = args.ordered_list_marker
            ordered = True
        elif args.unordered_list_marker is not None:
            list_marker = args.unordered_list_marker
        else:
            if args.parser == 'github' or args.parser == 'cmark':
                list_marker = md_parser['github']['list']['unordered'][
                    'default_marker']
            if args.parser == 'redcarpet' or args.parser == 'gitlab':
                list_marker = md_parser['redcarpet']['list']['unordered'][
                    'default_marker']

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

        # Github + cmark.
        github = subparsers.add_parser(
            'github',
            aliases=['cmark'],
            description='Use Commonmark rules to generate an output. If no \
                         option is selected, the default output will be an \
                         unordered list with the respective default values \
                         as listed below')
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
        github.set_defaults(
            header_levels=md_parser['github']['header']['default_keep_levels'])

        # Redcarpet.
        redcarpet = subparsers.add_parser(
            'redcarpet',
            aliases=['gitlab'],
            description='Use Redcarpet rules to generate an output. If no \
                         option is selected, the default output will be an \
                         unordered list with the respective default values \
                         as listed below. Gitlab rules are the same as \
                         Redcarpet except that conflicts are avoided with \
                         duplicate headers.')

        megroup = redcarpet.add_mutually_exclusive_group()
        megroup.add_argument(
            '-u',
            '--unordered-list-marker',
            choices=md_parser['redcarpet']['list']['unordered'][
                'bullet_markers'],
            nargs='?',
            const=md_parser['redcarpet']['list']['unordered'][
                'default_marker'],
            help='set the marker and enables unordered list. Defaults to ' +
            md_parser['redcarpet']['list']['unordered']['default_marker'])
        megroup.add_argument(
            '-o',
            '--ordered-list-marker',
            choices=md_parser['redcarpet']['list']['ordered'][
                'closing_markers'],
            nargs='?',
            const=md_parser['redcarpet']['list']['ordered'][
                'default_closing_marker'],
            help='set the marker and enables ordered lists. Defaults to ' +
            md_parser['redcarpet']['list']['ordered']['default_closing_marker']
        )
        redcarpet.add_argument(
            '-l',
            '--header-levels',
            choices=[
                str(i)
                for i in range(
                    1, md_parser['redcarpet']['header']['max_levels'] + 1)
            ],
            nargs='?',
            const=str(md_parser['redcarpet']['header']['default_keep_levels']),
            help='set the maximum level of headers to be considered as part \
                  of the TOC. Defaults to ' +
            str(md_parser['redcarpet']['header']['default_keep_levels']))
        redcarpet.set_defaults(header_levels=md_parser['redcarpet']['header'][
            'default_keep_levels'])

        parser.add_argument(
            'filename', metavar='FILE_NAME', help='the I/O file name')
        parser.add_argument(
            '-i',
            '--in-place',
            action='store_true',
            help='overwrite the input file')
        parser.add_argument(
            '-n',
            '--no-links',
            action='store_true',
            help='avoids adding links to the corresponding content')
        parser.add_argument(
            '-t',
            '--toc-marker',
            metavar='TOC_MARKER',
            help='set the string to be used as the marker for positioning the \
                  table of contents. Defaults to ' +
            common_defaults['toc_marker'])
        parser.set_defaults(toc_marker=common_defaults['toc_marker'])

        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=VERSION_NAME + ' ' + VERSION_NUMBER)

        parser.set_defaults(func=CliToApi().write_toc)

        return parser
