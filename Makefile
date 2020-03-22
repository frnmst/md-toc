#!/usr/bin/env make

#
# Makefile
#
# Copyright (C) 2017-2020 frnmst (Franco Masotti) <franco.masotti@live.com>
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

default: pep doc test

githook:
	git config core.hooksPath .githooks

pep:
	pipenv run yapf --style '{based_on_style: pep8; indent_width: 4}' -i md_toc/*.py tests/*.py
	pipenv run flake8 --ignore=F401,E501,W503,W504,W605,E125,E129 md_toc/*.py tests/*.py

doc:
	pipenv run $(MAKE) -C docs html

install:
	pip3 install . --user

uninstall:
	pip3 install md_toc

install-dev:
	pipenv install

uninstall-dev:
	pipenv --rm

demo:
	asciinema/md_toc_asciinema_2_0_0_demo.sh

test:
	pipenv run python setup.py test

benchmark:
	pushd tests && ./benchmark.sh 10 && popd

dist:
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel

upload:
	pipenv run twine upload dist/*

clean:
	rm -rf build dist *.egg-info tests/benchmark-results
	pipenv run $(MAKE) -C docs clean

.PHONY: default pep doc install install-dev uninstall uninstall-dev test benchmark dist upload clean demo
