#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
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
r"""A simple benchmark file to be used to check for hidden errors as well."""

import csv
import random
import secrets
import string
import subprocess
import tempfile
import time
import traceback

import md_toc

# ~100M characters
CHAR_SIZE = 1024 * 1024 * 100
ITERATIONS = 100


def _generate_random_characters(size: int) -> str:
    pattern = string.ascii_letters + string.digits + '#\n '
    return ''.join([secrets.choice(pattern) for i in range(0, size)])


if __name__ == '__main__':
    ok: bool = True
    i: int = 0
    avg: list
    average: dict = dict()
    total: dict = dict()

    parsers = ['github', 'cmark', 'redcarpet', 'gitlab']
    parsers.sort()

    for p in parsers:
        print('parser: ' + p + ', ' + str(ITERATIONS) + ' iterations with ' + str(CHAR_SIZE) + ' characters each')
        i = 0
        avg = list()
        while ok and i < ITERATIONS:
            print(i)
            with tempfile.NamedTemporaryFile() as fp:
                print('generating random file...')
                fp.write(_generate_random_characters(CHAR_SIZE).encode('UTF-8'))
                print('building TOC...')
                try:
                    start = time.time()
                    md_toc.build_toc(filename=fp.name, parser='cmark', no_links=True, no_list_coherence=True)
                    end = time.time()
                    avg.append(end - start)
                    print('total_time: ' + str(avg[-1]))
                except Exception:
                    ok = False
                    traceback.print_exc()
            i += 1
        total[p] = sum(avg)
        average[p] = total[p] / len(avg)
        print('total = ' + str(total[p]) + '\n')
        print('avg = ' + str(average[p]) + '\n')

    # Write CSV file.
    # Fields
    #   0   md_toc git hash version
    #   1   parser name
    #   2   number of characters
    #   3   number of iterations
    #   4   total execution time in seconds
    #   5   average execution time in seconds
    md_toc_version = subprocess.check_output(['/usr/bin/git', 'rev-parse', 'HEAD']).decode('UTF-8').strip()
    with open('benchmark.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for p in parsers:
            spamwriter.writerow([md_toc_version, p, CHAR_SIZE, ITERATIONS, total[p], average[p]])
