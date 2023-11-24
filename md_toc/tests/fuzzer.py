#
# fuzzer.py
#
# Copyright (C) 2023 Franco Masotti (see /README.md)
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
r"""A basic fuzzer for the build_toc function."""
import atheris

with atheris.instrument_imports():
    import string
    import sys
    import tempfile

    from .. import api, exceptions


def TestBuildToc(data):
    r"""Test the md_toc.api.build_toc function."""
    with tempfile.NamedTemporaryFile() as fp:

        bytez: bytes = b''.join([
            b'# ',
            bytes(string.ascii_letters, 'UTF-8'), data,
            bytes(string.ascii_letters, 'UTF-8')
        ])
        fp.write(bytez)

        # Move pointer to the start of the file.
        fp.seek(0)

        try:
            for parser in ['cmark', 'github', 'gitlab', 'redcarpet']:
                api.build_toc(filename=fp.name,
                              parser=parser,
                              keep_header_levels=6)
        except (exceptions.GithubEmptyLinkLabel,
                exceptions.TocDoesNotRenderAsCoherentList,
                exceptions.GithubOverflowCharsLinkLabel) as e:
            # The input string cannot be guaranteed to have a non-empty label
            # (GithubEmptyLinkLabel)
            # or a newline with '#' sequences can be inserted
            # (TocDoesNotRenderAsCoherentList)
            # or header a line too long
            # (GithubOverflowCharsLinkLabel)
            print(e)


atheris.Setup(sys.argv, TestBuildToc)
atheris.Fuzz()
