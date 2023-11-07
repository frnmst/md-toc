#!/bin/bash

#
# python -m md_toc_asciinema_7_1_0_demo.sh
#
# Copyright (C) 2021 Franco Masotti (see /README.md)
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

# Discover python -m md_toc of this repository not the one installed on the system.
export PYTHONPATH='..'
TIMEOUT=1
alias python='pipenv run python'

###
###

printf "Running a demo to show some of python -m md_toc's capabilities...\n"
printf "\n"
sleep ${TIMEOUT}

printf "$ python -m md_toc -h\n"
python -m md_toc -h
printf "\n"
sleep ${TIMEOUT}

cat <<-EOF > foo.md
# Hi

<!--TOC-->

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

cat <<-EOF > foo_skiplines.md
# I want this line to be a comment
#### And this as well
## And this
###### ByeBye

# Hi
## How
### Are
## You
# Today ?
EOF

printf "Inspecting the file...\n"
printf "$ cat foo.md\n"
cat foo.md
printf "\n"
sleep ${TIMEOUT}

printf "Run with default options...\n"
printf "$ python -m md_toc github foo.md\n"
python -m md_toc github foo.md
printf "\n"
sleep ${TIMEOUT}

printf "Ordered list...\n"
printf "$ python -m md_toc gitlab -o '.' foo.md\n"
python -m md_toc gitlab -o '.' foo.md
printf "\n"
sleep ${TIMEOUT}

printf "Constant ordered list...\n"
printf "$ python -m md_toc github -c -o '.' foo.md\n"
python -m md_toc github -c -o '.' foo.md
printf "\n"
sleep ${TIMEOUT}

printf "No links...\n"
printf "$ python -m md_toc -l github foo.md\n"
python -m md_toc -l github foo.md
printf "\n"
sleep ${TIMEOUT}

printf "No links and no indentation...\n"
printf "$ python -m md_toc -l -i github foo.md\n"
python -m md_toc -l -i github foo.md
printf "\n"
sleep ${TIMEOUT}

printf "Inspecting the non-coherent file...\n"
printf "$ cat foo_noncoherent.md\n"
cat foo_noncoherent.md
printf "\n"
sleep ${TIMEOUT}

printf "Trying to parse a non coherent markdown file will raise an exception...\n"
printf "$ python -m md_toc github foo_noncoherent.md\n"
python -m md_toc github foo_noncoherent.md
printf "\n"
sleep ${TIMEOUT}

printf "Try to parse a non coherent markdown file without checking for coherence...\n"
printf "$ python -m md_toc -c github foo_noncoherent.md\n"
python -m md_toc -c github foo_noncoherent.md
printf "\n"
sleep ${TIMEOUT}

printf "Use stdin, no links and no indentation...\n"
printf "$ cat foo.md | python -m md_toc -l -i - cmark -u '*'\n"
cat foo.md | python -m md_toc -l -i cmark -u '*'
printf "\n"
sleep ${TIMEOUT}

printf "Inspecting a file where the first 5 lines need to be skipped...\n"
printf "$ cat foo_skiplines.md\n"
cat foo_skiplines.md
printf "\n"
sleep ${TIMEOUT}

printf "Using the skip lines option...\n"
printf "$ python -m md_toc -s 5 github foo_skiplines.md\n"
python -m md_toc -s 5 github foo_skiplines.md
printf "\n"
sleep ${TIMEOUT}

printf "Editing the file in-place. As you can see, code fence \
detection still needs to be implemented for redcarpet...\n"
printf "$ python -m md_toc -p redcarpet foo.md\n"
python -m md_toc -p redcarpet foo.md
printf "$ cat foo.md\n"
cat foo.md

rm foo.md foo_noncoherent.md foo_skiplines.md
