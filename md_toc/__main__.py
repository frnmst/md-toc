import requests
import json
import sys
from .api_exceptions import (AudioFileError, AudioFileFormatError)
from .cli_exceptions import ConfigurationParsingError
from .cli import CliInterface


def main(args=None):
    """ Call the CLI parser and handle all possible exception returned from the
        Kr class.
    """

    try:
        kr = CliInterface()
        args = kr.parser.parse_args()
        result = args.func(args)
        if result is not None:
            print(result)
        retcode = 0
    except ConfigurationParsingError:
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write("Check your configuration file\n")
        retcode = 1
    sys.exit(retcode)


if __name__ == '__main__':

    main()
