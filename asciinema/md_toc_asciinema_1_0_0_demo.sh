#!/bin/bash

#
# md_toc_asciinema_1_0_0_demo.sh
#
# Copyright (C) 2017-2018 Franco Masotti (see /README.md)
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

printf "$ cat foo.md\n"
cat foo.md
printf "\n"
sleep 5

printf "$ md_toc -p github foo.md\n"
md_toc -p github foo.md
printf "\n"
sleep 5

printf "$ md_toc -o -p gitlab foo.md\n"
md_toc -o -p gitlab foo.md
printf "\n"
sleep 5

printf "$ md_toc -n foo.md\n"
md_toc -n foo.md
printf "\n"
sleep 5

printf "$ Editing the file in-place...\n"
printf "$ md_toc -i -p redcarpet foo.md\n"
md_toc -i -p redcarpet foo.md
printf "$ cat foo.md\n"
cat foo.md

rm foo.md
