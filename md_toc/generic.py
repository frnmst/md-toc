#
# generic.py
#
# Copyright (C) 2017-2022 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
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
"""Generic functions."""


# _ctoi and _isascii taken from cpython source Lib/curses/ascii.py
# See:
# https://github.com/python/cpython/blob/283de2b9c18e38c9a573526d6c398ade7dd6f8e9/Lib/curses/ascii.py#L48
# https://github.com/python/cpython/blob/283de2b9c18e38c9a573526d6c398ade7dd6f8e9/Lib/curses/ascii.py#L56
#
# These 2 functions are released under the
# PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2
# See https://directory.fsf.org/wiki/License:Python-2.0.1
def _ctoi(c: str):
    if not len(c) == 1:
        raise ValueError

    retval = c
    if isinstance(c, str):
        retval = ord(c)

    return retval


def _isascii(c):
    return 0 <= _ctoi(c) <= 127


def _noop(var):
    # Black hole for unused variables
    # to avoid triggering flake8.
    pass


def _replace_substring(source: str, replacement: str, start: int, end: int) -> str:
    r"""Given a string called source, replace it with a string called replacement between the start ~ end interval."""
    replaced: list = list()
    was_replaced: bool = False
    i: int = 0

    while i < len(source):
        if i < start or i > end:
            replaced.append(source[i])
        elif not was_replaced:
            replaced.append(replacement)
            was_replaced = True
        i += 1

    replaced = ''.join(replaced)
    return replaced


# A weaker version of C's strncmp: this one does not count the characters
# it just notify if there are differences.
def _strncmp(s1: str, s2: str, length: int) -> int:
    i: int = 0
    retval: int = 0
    process: bool = True

    s1_prime: str = s1[:length]
    s2_prime: str = s2[:length]
    s1_prime_length: int = len(s1_prime)
    s2_prime_length: int = len(s2_prime)
    min_length: int = min(s1_prime_length, s2_prime_length)

    if s1_prime_length < s2_prime_length:
        retval = -1
        process = False
    elif s1_prime_length > s2_prime_length:
        retval = 1
        process = False

    while process and i < min_length:
        int_s1: int = ord(s1_prime[i])
        int_s2: int = ord(s2_prime[i])

        if int_s1 < int_s2:
            retval = -1
            process = False
        elif int_s1 > int_s2:
            retval = 1
            process = False

        i += 1

    return retval


if __name__ == '__main__':
    pass
