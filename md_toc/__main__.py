import sys
from .cli import CliInterface
"""Call the CLI parser."""


def main(args=None):
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
    """
    except ConfigurationParsingError:
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write("Check your configuration file\n")
        retcode = 1
    """
    sys.exit(retcode)


if __name__ == '__main__':
    main()
