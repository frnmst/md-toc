#!/bin/bash

#
# md_toc_asciinema_5_0_0_demo.sh
#
# Copyright (C) 2019 frnmst (Franco Masotti) <franco.masotti@tutanota.com>
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

# Discover md_toc of this repository not the one installed on the system.
export PYTHONPATH='..'
TIMEOUT=1

printf "Running a demo to show some of md_toc's capabilities...\n"
printf "\n"
sleep ${TIMEOUT}

printf "$ md_toc -h\n"
md_toc -h
printf "\n"
sleep ${TIMEOUT}

cat <<-EOF > foo.md
# Hi

[](TOC)

hey

## How are you?           !!!

## fine, thanks

### Bye

## Bye bye

\`\`\`python
# This is a code
# fence with comments that might represent ATX-style headings
# if not properly parsed
\`\`\`

bye

# boo
EOF

cat <<-EOF > foo_noncoherent.md
# Hi
### boo
EOF

printf "Inspecting the file...\n"
printf "$ cat foo.md\n"
cat foo.md
printf "\n"
sleep ${TIMEOUT}

printf "Run with default options...\n"
printf "$ md_toc foo.md github\n"
md_toc foo.md github
printf "\n"
sleep ${TIMEOUT}

printf "Ordered list...\n"
printf "$ md_toc foo.md gitlab -o\n"
md_toc foo.md gitlab -o
printf "\n"
sleep ${TIMEOUT}

printf "No links...\n"
printf "$ md_toc -l foo.md github\n"
md_toc -l foo.md github
printf "\n"
sleep ${TIMEOUT}

printf "No links and no indentation...\n"
printf "$ md_toc -l -i foo.md github\n"
md_toc -l -i foo.md github
printf "\n"
sleep ${TIMEOUT}

printf "Inspecting the non-coherent file...\n"
printf "$ cat foo_noncoherent.md\n"
cat foo_noncoherent.md
printf "\n"
sleep ${TIMEOUT}

printf "Trying to parse a non coherent markdown file will raise an exception...\n"
printf "$ md_toc foo_noncoherent.md github\n"
md_toc foo_noncoherent.md github
printf "\n"
sleep ${TIMEOUT}

printf "Try to parse a non coherent markdown file without checking for coherence...\n"
printf "$ md_toc -c foo_noncoherent.md github\n"
md_toc -c foo_noncoherent.md github
printf "\n"
sleep ${TIMEOUT}

printf "Use stdin, no links and no indentation...\n"
printf "$ cat foo.md | md_toc -l -i cmark -u '*'\n"
cat foo.md | md_toc -l -i cmark -u '*'
printf "\n"
sleep ${TIMEOUT}

printf "Editing the file in-place. As you can see, code fence \
detection still needs to be implemented for redcarpet..\n"
printf "$ md_toc -p foo.md redcarpet\n"
md_toc -p foo.md redcarpet
printf "$ cat foo.md\n"
cat foo.md

rm foo.md foo_noncoherent.md
