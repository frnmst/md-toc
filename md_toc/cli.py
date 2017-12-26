# LICENSE and COPYRIGHT
"""Command line interface file."""

import argparse
import pkg_resources
from .api import (write_toc_on_md_file, build_toc)

class CliToApi():
    def write_toc_on_md_file(self,args):
        result = write_toc_on_md_file(args.filename,toc=build_toc(args.filename,args.ordered),in_place=args.in_place)
        if result is not None:
            print(result,end='')

class CliInterface():
    def __init__(self):
        self.parser = self.create_parser()

    def create_parser(self):
        parser = argparse.ArgumentParser(
            description='Markdown Table Of Contents',
            epilog="Return values: 0 OK, 1 \
                                         Error, 2 Invalid command")
        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True
        #
        # TOC marker option MISSING TODO TODO TODO
        #
        write_toc_prs = subparsers.add_parser(
            'wtoc', help='write the table of contents')
        write_toc_prs.add_argument(
            'filename', metavar='FILE_NAME', help='the file name')
        write_toc_prs.add_argument(
            '-i', '--in-place', help='in place', action='store_true')
        write_toc_prs.add_argument(
            '-o', '--ordered', help='ordered', action='store_true')
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=pkg_resources.get_distribution('md_toc').version)
        write_toc_prs.set_defaults(
            func=CliToApi().write_toc_on_md_file
        )

        return parser
