# -*- coding: utf-8 -*-
#
# cli.py
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
"""Command line interface file."""

import argparse
import textwrap

from pkg_resources import DistributionNotFound, get_distribution

from .api import build_multiple_tocs, write_strings_on_files_between_markers
from .constants import common_defaults
from .constants import parser as md_parser

PROGRAM_DESCRIPTION = 'Markdown Table Of Contents: Automatically generate a compliant table\nof contents for a markdown file to improve document readability.'
VERSION_NAME = 'md_toc'
try:
    VERSION_NUMBER = str(get_distribution('md_toc').version)
except DistributionNotFound:
    VERSION_NUMBER = 'vDevel'
VERSION_COPYRIGHT = 'Copyright (C) 2017-2022 Franco Masotti, frnmst'
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
        newline_string = args.newline_string
        if newline_string == r'\n':
            newline_string = '\n'
        elif newline_string == r'\r':
            newline_string = '\r'
        if newline_string == r'\r\n':
            newline_string = '\r\n'

        toc_struct = build_multiple_tocs(
            filenames=args.filename,
            ordered=ordered,
            no_links=args.no_links,
            no_indentation=args.no_indentation,
            no_list_coherence=args.no_list_coherence,
            keep_header_levels=args.header_levels,
            parser=args.parser,
            list_marker=list_marker,
            skip_lines=args.skip_lines,
            constant_ordered_list=args.constant_ordered_list,
            newline_string=newline_string,
        )
        if args.in_place:
            write_strings_on_files_between_markers(
                filenames=args.filename,
                strings=toc_struct,
                marker=args.toc_marker,
                newline_string=newline_string,
            )
        else:
            for toc in toc_struct:
                print(toc, end='')


class CliInterface():
    """The interface exposed to the final user."""

    def __init__(self):
        """Set the parser variable that will be used instead of using create_parser."""
        self.parser = self.create_parser()

    def _add_filename_argument(self, parser):
        # The filename argument is common to all markdown parsers.
        # See commit b65cf32.
        parser.add_argument(
            'filename',
            metavar='FILE_NAME',
            nargs='*',
            help='the I/O file name',
        )

    def _add_cmark_like_megroup_arguments(self, megroup, parser_name: str):
        megroup.add_argument(
            '-u',
            '--unordered-list-marker',
            choices=md_parser[parser_name]['list']['unordered']
            ['bullet markers'],
            nargs='?',
            const=md_parser[parser_name]['list']['unordered']
            ['default marker'],
            default=md_parser[parser_name]['list']['unordered']
            ['default marker'],
            help='set the marker and enables unordered list. Defaults to ' +
            md_parser[parser_name]['list']['unordered']['default marker'],
        )
        megroup.add_argument(
            '-o',
            '--ordered-list-marker',
            choices=md_parser[parser_name]['list']['ordered']
            ['closing markers'],
            nargs='?',
            const=md_parser[parser_name]['list']['ordered']
            ['default closing marker'],
            help=('set the marker and enable ordered lists. Defaults to ' +
                  md_parser[parser_name]['list']['ordered']
                  ['default closing marker']),
        )

    def _add_cmark_like_arguments(self, parser, parser_name: str):
        parser.add_argument(
            '-c',
            '--constant-ordered-list',
            action='store_true',
            help='intead of progressive numbers use a single integer as \
                  list marker. This options enables ordered lists',
        )
        parser.add_argument(
            '-l',
            '--header-levels',
            type=int,
            choices=range(1,
                          md_parser[parser_name]['header']['max levels'] + 1),
            nargs='?',
            const=md_parser[parser_name]['header']['default keep levels'],
            help='set the maximum level of headers to be considered as part \
                  of the TOC. Defaults to ' +
            str(md_parser[parser_name]['header']['default keep levels'], ),
        )

    def create_parser(self):
        """Create the CLI parser."""
        parser = argparse.ArgumentParser(
            description=PROGRAM_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(PROGRAM_EPILOG),
        )

        # markdown parser is first positional argument.
        # File names are arguments to the subparser.
        subparsers = parser.add_subparsers(
            dest='parser',
            title='markdown parser',
            help='<markdown parser> --help',
        )
        subparsers.required = True

        #########################
        # github + commonmarker #
        #########################
        github = subparsers.add_parser(
            'github',
            aliases=['commonmarker'],
            description='Use GitHub Flavored Markdown rules to generate \
                         an output. If no \
                         option is selected, the default output will be an \
                         unordered list with the respective default values \
                         as listed below',
        )
        self._add_filename_argument(github)
        megroup = github.add_mutually_exclusive_group()
        self._add_cmark_like_megroup_arguments(megroup, 'github')
        self._add_cmark_like_arguments(github, 'github')
        github.set_defaults(header_levels=md_parser['github']['header']
                            ['default keep levels'], )

        ##########
        # gitlab #
        ##########
        gitlab = subparsers.add_parser(
            'gitlab',
            description='Use GitLab Flavored Markdown rules to generate an \
                         output. If no \
                         option is selected, the default output will be an \
                         unordered list with the respective default values \
                         as listed below',
        )
        self._add_filename_argument(gitlab)
        megroup = gitlab.add_mutually_exclusive_group()
        self._add_cmark_like_megroup_arguments(megroup, 'gitlab')
        self._add_cmark_like_arguments(gitlab, 'gitlab')
        gitlab.set_defaults(header_levels=md_parser['gitlab']['header']
                            ['default keep levels'], )

        ####################
        # cmark + Goldmark #
        ####################
        cmark = subparsers.add_parser(
            'cmark',
            aliases=['goldmark'],
            description='Use CommonMark rules to generate an output. If no \
                         option is selected, the default output will be an \
                         unordered list with the respective default values \
                         as listed below',
        )
        self._add_filename_argument(cmark)
        megroup = cmark.add_mutually_exclusive_group()
        self._add_cmark_like_megroup_arguments(megroup, 'cmark')
        self._add_cmark_like_arguments(cmark, 'cmark')
        cmark.set_defaults(header_levels=md_parser['cmark']['header']
                           ['default keep levels'], )

        #############
        # Redcarpet #
        #############
        redcarpet = subparsers.add_parser(
            'redcarpet',
            description='Use Redcarpet rules to generate an output. If no \
                         option is selected, the default output will be an \
                         unordered list with the respective default values \
                         as listed below. Gitlab rules are the same as \
                         Redcarpet except that conflicts are avoided with \
                         duplicate headers.',
        )
        self._add_filename_argument(redcarpet)
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
            md_parser['redcarpet']['list']['unordered']['default marker'],
        )
        megroup.add_argument(
            '-o',
            '--ordered-list-marker',
            choices=md_parser['redcarpet']['list']['ordered']
            ['closing markers'],
            nargs='?',
            const=md_parser['redcarpet']['list']['ordered']
            ['default closing marker'],
            help='set the marker and enables ordered lists. Defaults to ' +
            md_parser['redcarpet']['list']['ordered']
            ['default closing marker'],
        )
        redcarpet.add_argument(
            '-c',
            '--constant-ordered-list',
            action='store_true',
            help='intead of progressive numbers use a single integer as list \
                  marker. This options enables ordered lists',
        )
        redcarpet.add_argument(
            '-l',
            '--header-levels',
            type=int,
            choices=range(
                1,
                md_parser['redcarpet']['header']['max levels'] + 1,
            ),
            nargs='?',
            const=md_parser['redcarpet']['header']['default keep levels'],
            help='set the maximum level of headers to be considered as part \
                  of the TOC. Defaults to ' +
            str(md_parser['redcarpet']['header']['default keep levels'], ),
        )
        redcarpet.set_defaults(header_levels=md_parser['redcarpet']['header']
                               ['default keep levels'], )

        ##########
        # Common #
        ##########
        no_list_coherence_or_no_indentation = parser.add_mutually_exclusive_group(
        )
        no_list_coherence_or_no_indentation.add_argument(
            '-c',
            '--no-list-coherence',
            action='store_true',
            help='avoids checking for TOC list coherence',
        )
        no_list_coherence_or_no_indentation.add_argument(
            '-i',
            '--no-indentation',
            action='store_true',
            help='avoids adding indentations to the TOC',
        )

        parser.add_argument(
            '-l',
            '--no-links',
            action='store_true',
            help='avoids adding links to the TOC',
        )
        parser.add_argument(
            '-m',
            '--toc-marker',
            metavar='TOC_MARKER',
            default=common_defaults['toc marker'],
            help=(
                'set the string to be used as the marker for positioning the \
                table of contents. Put this value between single quotes. \
                Defaults to \'' + common_defaults['toc marker']) + '\'',
        )
        parser.add_argument(
            '-n',
            '--newline-string',
            choices=[r'\n', r'\r', r'\r\n'],
            metavar='NEWLINE_STRING',
            type=str,
            default=common_defaults['newline string'],
            help=('the string used to separate the lines of the TOC. \
                  Use single quotes to delimit the string. \
                  If you output in place all the newlines of the \
                  input file will be replaced with this value. \
                  Defaults to ' + repr(common_defaults['newline string'])),
        )
        parser.add_argument(
            '-p',
            '--in-place',
            action='store_true',
            help='overwrite the input file',
        )
        parser.add_argument(
            '-s',
            '--skip-lines',
            metavar='SKIP_LINES',
            type=int,
            default=0,
            help='skip parsing of the first selected number of lines. \
                  Defaults to 0, i.e. do not skip any lines',
        )
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=VERSION_NAME + ' ' + VERSION_NUMBER,
        )

        parser.set_defaults(func=CliToApi().write_toc)

        return parser
