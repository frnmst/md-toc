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
import ctypes
import platform
import random
import secrets
import string
import subprocess
import tempfile
import time
import traceback

import md_toc

# ~50M characters
CHAR_SIZE = 1024 * 1024 * 50
ITERATIONS = 1000

# At what nTH character to put a header.
# MIN_HEADER_STEP must be >= 10.
MIN_HEADER_STEP = 10
MAX_HEADER_STEP = 50


def _generate_random_characters(size: int,
                                min_header_step: int = 10,
                                max_header_step: int = 1000) -> str:

    secret_gen: random.SystemRandom = secrets.SystemRandom()
    alphanumerics: str = ''.join([string.ascii_letters, string.digits])

    # Do not use '#' as content to avoid triggering an empty link label exception.
    printable_except_hash: str = string.printable.replace('#', '')

    file_content: str = ''.join(
        [secrets.choice(printable_except_hash) for i in range(0, size)])
    string_buf = ctypes.create_string_buffer(bytes(file_content, 'UTF-8'),
                                             size=size + 1)

    if min_header_step < 10 or max_header_step < min_header_step:
        # 10 - 1 = header (maximum 6) + '\n' + space + alphanum char
        raise ValueError

    print('adding headers to file...')

    i = 0
    j: int = 1
    for i in range(0, size,
                   secret_gen.randrange(min_header_step, max_header_step)):
        # Reset header level.
        if j % 6 == 1:
            j = 1

        if i + j + 3 < size:
            # Replace next character so we are sure never to raise the empty
            # link label exception.
            string_buf[i:i + j + 3] = bytes(
                ''.join(['\n', '#' * j, ' ',
                         secrets.choice(alphanumerics)]), 'UTF-8')

        j += 1

    return string_buf.value.decode('UTF-8')


if __name__ == '__main__':
    ok: bool = True
    i: int = 0
    j: int = 0
    total_iterations: int
    percent_progress: int
    current_parser_counter: int = 0
    avg: list
    average: dict = dict()
    total: dict = dict()

    parsers = ['github', 'cmark', 'redcarpet', 'gitlab']
    parsers.sort()

    total_iterations = len(parsers) * ITERATIONS
    for current_parser_counter, p in enumerate(parsers):
        print('parser: ' + p + ', ' + str(ITERATIONS) + ' iterations with ' +
              str(CHAR_SIZE) + ' characters each')
        print('min step: ' + str(MIN_HEADER_STEP) + ' , max step: ' +
              str(MAX_HEADER_STEP))
        i = 0
        avg = list()
        while ok and i < ITERATIONS:
            print('parser ' + str(p) + ' (' + str(current_parser_counter + 1) +
                  ' of ' + str(len(parsers)) + '), iteration: ' + str(i + 1) +
                  ' of ' + str(ITERATIONS))
            percent_progress = (j / total_iterations) * 100
            print('total progress percent = ' + str(percent_progress))
            with tempfile.NamedTemporaryFile() as fp:
                print('generating random file...')
                fp.write(
                    _generate_random_characters(
                        CHAR_SIZE,
                        min_header_step=MIN_HEADER_STEP,
                        max_header_step=MAX_HEADER_STEP).encode('UTF-8'))
                print('building TOC...')
                try:
                    start = time.time()
                    md_toc.build_toc(filename=fp.name, parser=p)
                    end = time.time()
                    avg.append(end - start)
                    print('total_time: ' + str(avg[-1]))
                except Exception:
                    ok = False
                    traceback.print_exc()
            i += 1
            j += 1
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
    #   4   min_header_step
    #   5   max_header_step
    #   6   total execution time in seconds
    #   7   average execution time in seconds
    #   8->n system information
    # File header:
    # md_toc_git_hash,markdown_parser,total_characters,iterations,min_header_step,max_header_step,total,avg,platform_python_version,platform_architecture,platform_machine,platform_python_implementation,platform_python_compiler,platform_libc_ver
    md_toc_version = subprocess.check_output(
        ['/usr/bin/git', 'rev-parse', 'HEAD']).decode('UTF-8').strip()
    with open('benchmark.csv', 'a') as csvfile:
        spamwriter = csv.writer(csvfile,
                                delimiter=',',
                                quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
        for p in parsers:
            spamwriter.writerow([
                md_toc_version, p, CHAR_SIZE, ITERATIONS, MIN_HEADER_STEP,
                MIN_HEADER_STEP, total[p], average[p],
                platform.python_version(), ' '.join(platform.architecture()),
                platform.machine(),
                platform.python_implementation(),
                platform.python_compiler(), ' '.join(platform.libc_ver())
            ])
