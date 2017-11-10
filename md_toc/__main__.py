import requests
import json
import sys
from .api_exceptions import (AudioFileError,
                             AudioFileFormatError)
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
    except requests.exceptions.RequestException as e:
        sys.stderr.write("Requests error\n")
        sys.stderr.write(str(e) + "\n")
        retcode = 1
        # Inspired by https://stackoverflow.com/a/20725965
    except json.decoder.JSONDecodeError as e:
        # end of inspired by.
        sys.stderr.write("JSON decoder error (probably not a Kalliope 
server)\n")
        sys.stderr.write(str(e) + "\n")
        retcode = 1
    except AudioFileError as e:
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write("File " + args.audio_file + " not found\n")
        retcode = 1
    except AudioFileFormatError as e:
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write("Only WAV or MP3 files are compatible\n")
        retcode = 1
    sys.exit(retcode)


if __name__ == '__main__':

    main()

