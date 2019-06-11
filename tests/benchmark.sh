#!/usr/bin/bash
#
# benchmark.sh
#
# Copyright (C) 2019 frnmst (Franco Masotti) <franco.masotti@live.com>
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

set -euo pipefail

OUTPUT_DIRECTORY="benchmark-results"

repeat=${1}

[ -z "${repeat}" ] && printf "%s\n" "help: benchmark.sh repeat" && exit 1

rm -rf "${OUTPUT_DIRECTORY}"
mkdir -p "${OUTPUT_DIRECTORY}"

i=0
while [ ${i} -lt ${repeat} ]; do
    nosetests tests.py --with-timer --timer-json-file "${OUTPUT_DIRECTORY}"/benchmark-"${i}".json
    i=$((${i}+1))
done
