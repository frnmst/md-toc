# SPDX-FileCopyrightText: 2017-2026 Franco Masotti (See /README.md)
#
# SPDX-License-Identifier: GPL-3.0-or-later

import importlib.metadata
import logging
import os
import pathlib
import subprocess
import tempfile


def main():
    pkg_name: str = 'md-toc'
    version: str = importlib.metadata.version(pkg_name)
    logging.info(version)

    header: str = "#!/bin/bash\nread -r -d '' payload << 'EOF'"
    footer: str = 'which curl pipx sort tr jq echo && echo "${payload}" | gpg --verify - && { echo "${payload}" | gpg --decrypt - | sh; } || exit 1'

    checksum_files: list[str] = list(pathlib.Path('dist/').glob('*SUM.txt'))
    if len(checksum_files) == 4:
        # Just get the hashes, ignore the file names.
        local_hashes: str = ''.join(
            sorted([c.read_text().split(' ')[0] for c in checksum_files]))

        payload_to_sign: str = f"""\
local_hashes="{local_hashes}" && remote_hashes=$(curl https://pypi.org/pypi/md-toc/json | jq '.urls[] | .digests | to_entries[] | select(.key != "blake2b_256") | .value' | tr -d '"' | sort | tr -d "\\n") && [ ${{local_hashes}} = ${{remote_hashes}} ] && export PIP_ONLY_BINARY=:all: && pipx install {pkg_name}=={version}"""

        payload_and_signature: str = ''
        with tempfile.NamedTemporaryFile() as fp:
            pathlib.Path(fp.name).write_text(payload_to_sign)
            result: str = subprocess.run(
                f'gpg --output - --clearsign {fp.name}',
                shell=True,
                check=True,
                capture_output=True)
            payload_and_signature = result.stdout.decode('UTF-8').strip()

        if payload_and_signature:
            final_output: str = os.linesep.join(
                [header, payload_and_signature, 'EOF', footer])
            pathlib.Path('safe_install.sh').write_text(final_output)
        else:
            logging.error('unable to generate script')
    else:
        logging.error('local checksum file(s) missing')


if __name__ == '__main__':
    main()
