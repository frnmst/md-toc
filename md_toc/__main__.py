# Copyright (C) 2017-2020 Franco Masotti (see /README.md)
# SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""Call the CLI parser."""

import sys
import traceback

from .cli import CliInterface


def main(args=None):
    """Call the CLI interface and wait for the result."""
    retcode = 0
    try:
        ci = CliInterface()
        args = ci.parser.parse_args()
        result = args.func(args)
        if result is not None and not isinstance(result, bool):
            print(result)
        retcode = 0

        # TOC differs.
        if result:
            retcode = 128

    except Exception:
        retcode = 1
        traceback.print_exc()
    sys.exit(retcode)


if __name__ == '__main__':
    main()
