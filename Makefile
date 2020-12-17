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

export PACKAGE_NAME=md_toc

default: doc

doc:
	pipenv run $(MAKE) -C docs html

install:
	pip3 install . --user

uninstall:
	pip3 uninstall $(PACKAGE_NAME)

install-dev:
	pipenv install --dev
	pipenv run pre-commit install

uninstall-dev:
	pipenv --rm

demo:
	asciinema/md_toc_asciinema_$$(git describe --tags $$(git rev-list --tags --max-count=1) | tr '.' '_')_demo.sh

test:
	python -m unittest $(PACKAGE_NAME).tests.tests --failfast --locals --verbose

dist:
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel
	pipenv run twine check dist/*

upload:
	pipenv run twine upload dist/*

clean:
	rm -rf build dist *.egg-info tests/benchmark-results *.md
	pipenv run $(MAKE) -C docs clean

.PHONY: default doc install uninstall install-dev uninstall-dev test clean demo benchmark
