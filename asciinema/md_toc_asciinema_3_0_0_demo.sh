#!/bin/bash

#
# md_toc_asciinema_3_0_0_demo.sh
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

# Discover md_toc of this repository not the one installed on the system.
export PYTHONPATH='..'

printf "Running a demo to show some of md_toc's capabilities...\n"
printf "\n"
sleep 2

printf "$ md_toc -h\n"
md_toc -h
printf "\n"
sleep 5

cat <<-EOF > foo.md
# Hi

[](TOC)

hey

## How are you?           !!!

## fine, thanks

### Bye

## Bye bye
EOF

printf "Inspecting the file...\n"
printf "$ cat foo.md\n"
cat foo.md
printf "\n"
sleep 5

printf "Run with default options...\n"
printf "$ md_toc foo.md github\n"
md_toc foo.md github
printf "\n"
sleep 5

printf "Ordered list...\n"
printf "$ md_toc foo.md gitlab -o\n"
md_toc foo.md gitlab -o
printf "\n"
sleep 5

printf "No links...\n"
printf "$ md_toc -l foo.md github\n"
md_toc -l foo.md github
printf "\n"
sleep 5

printf "No links and no indentation...\n"
printf "$ md_toc -l -i foo.md github\n"
md_toc -l -i foo.md github
printf "\n"
sleep 5

printf "Editing the file in-place...\n"
printf "$ md_toc -p foo.md redcarpet\n"
md_toc -p foo.md redcarpet
printf "$ cat foo.md\n"
cat foo.md

rm foo.md
