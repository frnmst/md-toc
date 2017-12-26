# C+L
"""Call the CLI parser."""

import sys
from .cli import CliInterface


def main(args=None):
    """Call the CLI interface and wait for the result."""
    retcode = 0
    try:
        ci = CliInterface()
        args = ci.parser.parse_args()
        result = args.func(args)
        if result is not None:
            print(result)
        retcode = 0
    except Exception as e:
        retcode = 1
        print(e)
    sys.exit(retcode)


if __name__ == '__main__':
    main()
