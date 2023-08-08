#
# Makefile
#
# Copyright (C) 2017-2022 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
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

# See
# https://docs.python.org/3/library/venv.html#how-venvs-work
export VENV_CMD=. .venv/bin/activate

default: install-dev

doc:
	$(VENV_CMD) \
		&& $(MAKE) -C docs html \
		&& deactivate

install:
	# pip 23 introduced the '--break-system-packages' option.
	python3 -c 'import pip; import sys; sys.exit(0) if int(pip.__version__.split(".")[0]) >= 23 else sys.exit(1)' \
		&& pip3 install --break-system-packages . --user \
		|| pip3 install . --user

uninstall:
	# pip 23 introduced the '--break-system-packages' option.
	python3 -c 'import pip; import sys; sys.exit(0) if int(pip.__version__.split(".")[0]) >= 23 else sys.exit(1)' \
		&& pip3 uninstall --break-system-packages --verbose --yes $(PACKAGE_NAME) \
		|| pip3 uninstall --verbose --yes $(PACKAGE_NAME)

install-dev:
	python3 -m venv .venv
	$(VENV_CMD) \
		&& pip install --requirement requirements-freeze.txt \
		&& deactivate
	$(VENV_CMD) \
		&& pre-commit install \
		&& deactivate
	$(VENV_CMD) \
		&& pre-commit install --hook-type commit-msg \
		&& deactivate

regenerate-freeze: uninstall-dev
	python3 -m venv .venv
	$(VENV_CMD) \
		&& pip install --requirement requirements.txt --requirement requirements-dev.txt \
		&& pip freeze --local > requirements-freeze.txt \
		&& deactivate

uninstall-dev:
	rm -rf .venv

update: install-dev
	$(VENV_CMD) \
		&& pre-commit autoupdate \
			--repo https://github.com/pre-commit/pre-commit-hooks \
			--repo https://github.com/PyCQA/bandit \
			--repo https://github.com/pycqa/isort \
			--repo https://codeberg.org/frnmst/licheck \
			--repo https://codeberg.org/frnmst/md-toc \
			--repo https://github.com/mgedmin/check-manifest \
			--repo https://github.com/jorisroovers/gitlint \
		&& deactivate
		# --repo https://github.com/pre-commit/mirrors-mypy \

test:
	$(VENV_CMD) \
		&& python -m unittest $(PACKAGE_NAME).tests.tests --failfast --locals --verbose \
		&& deactivate

pre-commit:
	$(VENV_CMD) \
		&& pre-commit run --all \
		&& deactivate

demo:
	$(VENV_CMD) \
		&& asciinema/md_toc_asciinema_$$(git describe --tags $$(git rev-list --tags --max-count=1) | tr '.' '_')_demo.sh \
		&& deactivate

dist:
	# Create a reproducible archive at least on the wheel.
	# See
	# https://bugs.python.org/issue31526
	# https://bugs.python.org/issue38727
	# https://github.com/pypa/setuptools/issues/1468
	# https://github.com/pypa/setuptools/issues/2133
	# https://reproducible-builds.org/docs/source-date-epoch/
	$(VENV_CMD) \
		&& SOURCE_DATE_EPOCH=$$(git -c log.showSignature='false' log -1 --pretty=%ct) \
		python -m build \
		&& deactivate
	$(VENV_CMD) \
		&& twine check --strict dist/* \
		&& deactivate

upload:
	$(VENV_CMD) \
		&& twine upload dist/* \
		&& deactivate

clean:
	rm -rf build dist *.egg-info tests/benchmark-results
	# Remove all markdown files except the readmes.
	find -regex ".*\.[mM][dD]" ! -name 'README.md' ! -name 'CONTRIBUTING.md' -type f -exec rm -f {} +
	$(VENV_CMD) \
		&& $(MAKE) -C docs clean \
		&& deactivate

# This serves both as benchmark and as fuzzer.
benchmark:
	$(VENV_CMD) \
		&& python3 -m md_toc.tests.benchmark \
		&& deactivate

.PHONY: default doc install uninstall install-dev uninstall-dev update test clean demo benchmark pre-commit
