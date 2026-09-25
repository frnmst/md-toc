# Copyright (C) 2017-2022 Franco Masotti (see /README.md)
# SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)
#
# SPDX-License-Identifier: GPL-3.0-or-later
r"""A cmark implementation file."""

# License F applies to this file except for non derivative code:
# in that case the license header at the top of the file applies.
# See docs/copyright_license.rst


def _cmark_HOUDINI_ESCAPED_SIZE(x: int) -> float:
    return (x * 12) / 10


def _cmark_HOUDINI_UNESCAPED_SIZE(x: int) -> int:
    return x
