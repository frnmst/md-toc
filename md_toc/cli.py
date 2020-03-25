#
# cli.py
#
# Copyright (C) 2017-2020 frnmst (Franco Masotti) <franco.masotti@live.com>
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
from pkg_resources import (get_distribution, DistributionNotFound)
from .api import (write_strings_on_files_between_markers, build_multiple_tocs)
from .constants import common_defaults
from .constants import parser as md_parser

PROGRAM_DESCRIPTION = 'Markdown Table Of Contents: Automatically generate a compliant table\nof contents for a markdown file to improve document readability.'
VERSION_NAME = 'md_toc'
try:
    VERSION_NUMBER = str(get_distribution('md_toc').version)
except DistributionNotFound:
    VERSION_NUMBER = 'vDevel'
VERSION_COPYRIGHT = 'Copyright (C) 2017-2020 Franco Masotti, frnmst'
VERSION_LICENSE = 'License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.'
RETURN_VALUES = 'Return values: 0 ok, 1 error, 2 invalid command'
ADVICE = 'Please read the documentation to understand how each parser works'
PROGRAM_EPILOG = ADVICE + '\n\n' + RETURN_VALUES + '\n\n' + VERSION_COPYRIGHT + '\n' + VERSION_LICENSE


class CliToApi():
    """An interface between the CLI and API functions."""

    def write_toc(self, args):
        """Write the table of contents."""
        ordered = False
        if args.ordered_list_marker is not None:
            list_marker = args.ordered_list_marker
            ordered = True
        elif args.unordered_list_marker is not None:
            list_marker = args.unordered_list_marker
        toc_struct = build_multiple_tocs(
            filenames=args.filename,
            ordered=ordered,
            no_links=args.no_links,
            no_indentation=args.no_indentation,
            no_list_coherence=args.no_list_coherence,
            keep_header_levels=args.header_levels,
            parser=args.parser,
            list_marker=list_marker,
            skip_lines=args.skip_lines)
        if args.in_place:
            write_strings_on_files_between_markers(
                filenames=args.filename,
                strings=toc_struct,
                marker=args.toc_marker)
        else:
            for toc in toc_struct:
                print(toc, end='')


class CliInterface():
    """The interface exposed to the final user."""

    def __init__(self):
        """Set the parser variable that will be used instead of using create_parser."""
        self.parser = self.create_parser()

    def add_filename_argument(self, parser):
        """Add the filename argument to the pecified parser.

        The filename argument is common to all markdown parsers.
        See commit b65cf32.
        """
        parser.add_argument(
            'filename',
            metavar='FILE_NAME',
            nargs='*',
            help='the I/O file name')

    def create_parser(self):
        """Create the CLI parser."""
        parser = argparse.ArgumentParser(
            description=PROGRAM_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(PROGRAM_EPILOG))

        # markdown parser is first positional argument.
        # File names are arguments to the subparser.
        subparsers = parser.add_subparsers(
            dest='parser',
            title='markdown parser',
            help='<markdown parser> --help')
        subparsers.required = True

        # github + cmark + gitlab + commonmarker.
        github = subparsers.add_parser(
            'github',
            aliases=['cmark', 'gitlab', 'commonmarker'],
            description='Use Commonmark rules to generate an output. If no \
                         option is selected, the default output will be an \
                         unordered list with the respective default values \
                         as listed below')
        self.add_filename_argument(github)

        megroup = github.add_mutually_exclusive_group()
        megroup.add_argument(
            '-u',
            '--unordered-list-marker',
            choices=md_parser['github']['list']['unordered']['bullet markers'],
            nargs='?',
            const=md_parser['github']['list']['unordered']['default marker'],
            default=md_parser['github']['list']['unordered']['default marker'],
            help='set the marker and enables unordered list. Defaults to ' +
            md_parser['github']['list']['unordered']['default marker'])
        megroup.add_argument(
            '-o',
            '--ordered-list-marker',
            choices=md_parser['github']['list']['ordered']['closing markers'],
            nargs='?',
            const=md_parser['github']['list']['ordered']
            ['default closing marker'],
            help='set the marker and enables ordered lists. Defaults to ' +
            md_parser['github']['list']['ordered']['default closing marker'])
        github.add_argument(
            '-l',
            '--header-levels',
            type=int,
            choices=range(1, md_parser['github']['header']['max levels'] + 1),
            nargs='?',
            const=md_parser['github']['header']['default keep levels'],
            help='set the maximum level of headers to be considered as part \
                  of the TOC. Defaults to ' + str(
                md_parser['github']['header']['default keep levels']))
        github.set_defaults(
            header_levels=md_parser['github']['header']['default keep levels'])

        # Redcarpet.
        redcarpet = subparsers.add_parser(
            'redcarpet',
            description='Use Redcarpet rules to generate an output. If no \
                         option is selected, the default output will be an \
                         unordered list with the respective default values \
                         as listed below. Gitlab rules are the same as \
                         Redcarpet except that conflicts are avoided with \
                         duplicate headers.')
        self.add_filename_argument(redcarpet)

        megroup = redcarpet.add_mutually_exclusive_group()
        megroup.add_argument(
            '-u',
            '--unordered-list-marker',
            choices=md_parser['redcarpet']['list']['unordered']
            ['bullet markers'],
            nargs='?',
            const=md_parser['redcarpet']['list']['unordered']
            ['default marker'],
            default=md_parser['redcarpet']['list']['unordered']
            ['default marker'],
            help='set the marker and enables unordered list. Defaults to ' +
            md_parser['redcarpet']['list']['unordered']['default marker'])
        megroup.add_argument(
            '-o',
            '--ordered-list-marker',
            choices=md_parser['redcarpet']['list']['ordered']
            ['closing markers'],
            nargs='?',
            const=md_parser['redcarpet']['list']['ordered']
            ['default closing marker'],
            help='set the marker and enables ordered lists. Defaults to ' +
            md_parser['redcarpet']['list']['ordered']['default closing marker']
        )
        redcarpet.add_argument(
            '-l',
            '--header-levels',
            type=int,
            choices=range(1,
                          md_parser['redcarpet']['header']['max levels'] + 1),
            nargs='?',
            const=md_parser['redcarpet']['header']['default keep levels'],
            help='set the maximum level of headers to be considered as part \
                  of the TOC. Defaults to ' + str(
                md_parser['redcarpet']['header']['default keep levels']))
        redcarpet.set_defaults(header_levels=md_parser['redcarpet']['header']
                               ['default keep levels'])

        no_list_coherence_or_no_indentation = parser.add_mutually_exclusive_group(
        )
        no_list_coherence_or_no_indentation.add_argument(
            '-c',
            '--no-list-coherence',
            action='store_true',
            help='avoids checking for TOC list coherence')
        no_list_coherence_or_no_indentation.add_argument(
            '-i',
            '--no-indentation',
            action='store_true',
            help='avoids adding indentations to the TOC')

        parser.add_argument(
            '-l',
            '--no-links',
            action='store_true',
            help='avoids adding links to the TOC')
        parser.add_argument(
            '-m',
            '--toc-marker',
            metavar='TOC_MARKER',
            default=common_defaults['toc marker'],
            help='set the string to be used as the marker for positioning the \
                  table of contents. Defaults to ' +
            common_defaults['toc marker'])
        parser.add_argument(
            '-p',
            '--in-place',
            action='store_true',
            help='overwrite the input file')
        parser.add_argument(
            '-s',
            '--skip-lines',
            metavar='SKIP_LINES',
            type=int,
            default=0,
            help='skip parsing of the first selected number of lines. \
                  Defaults to 0, i.e. do not skip any lines')
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=VERSION_NAME + ' ' + VERSION_NUMBER)

        parser.set_defaults(func=CliToApi().write_toc)

        return parser
