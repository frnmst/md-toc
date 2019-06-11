#!/usr/bin/env make

#
# Makefile
#
# Copyright (C) 2017-2018 frnmst (Franco Masotti) <franco.masotti@live.com>
#                                            <franco.masotti@student.unife.it>
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
	yapf --style '{based_on_style: pep8; indent_width: 4}' -i md_toc/*.py tests/*.py
	flake8 --ignore=F401,E501,W503,W504,W605,E125 md_toc/*.py tests/*.py

doc:
	$(MAKE) -C docs html

install:
	pip install .

test:
	python setup.py test

uninstall:
	pip uninstall md_toc

dist:
	python setup.py sdist
	python setup.py bdist_wheel

upload:
	twine upload dist/*

clean:
	rm -rf build dist *.egg-info tests/benchmark-results

.PHONY: default pep doc install test uninstall dist upload clean
