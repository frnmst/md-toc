#
# Makefile
#
# Copyright (C) 2017-2024 Franco Masotti (see /README.md)
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
		&& $(MAKE) -C docs latexpdf \
		&& deactivate

install:
	# pip 23 introduced the '--break-system-packages' option.
	python3 -c 'import pip; import sys; sys.exit(0) if int(pip.__version__.split(".")[0]) >= 23 else sys.exit(1)' \
		&& pip3 install --break-system-packages --disable-pip-version-check  . --user \
		|| pip3 install --disable-pip-version-check  . --user

uninstall:
	# pip 23 introduced the '--break-system-packages' option.
	python3 -c 'import pip; import sys; sys.exit(0) if int(pip.__version__.split(".")[0]) >= 23 else sys.exit(1)' \
		&& pip3 uninstall --break-system-packages --disable-pip-version-check --verbose --yes $(PACKAGE_NAME) \
		|| pip3 uninstall --disable-pip-version-check --verbose --yes $(PACKAGE_NAME)

install-dev:
	python3 -m venv .venv
	$(VENV_CMD) \
		&& { python3 -c 'import pip; import sys; sys.exit(0) if int(pip.__version__.split(".")[0]) >= 23 else sys.exit(1)' \
		&& pip install --disable-pip-version-check --require-virtualenv --requirement requirements-freeze.txt --require-hashes  \
		|| pip install --require-virtualenv --requirement requirements-freeze.txt --require-hashes ; } \
		&& deactivate
	$(VENV_CMD) \
		&& pre-commit install \
		&& deactivate
	$(VENV_CMD) \
		&& pre-commit install --hook-type commit-msg \
		&& deactivate

# Add hashes to the freeze file be re-downloading the packages locally and
# generating their hashes locally.
# Assume that each package has one corresponding file only.
regenerate-freeze: regenerate-freeze-no-hashes
	python3 -m venv .venv
	$(VENV_CMD) \
		&& mkdir .pip-hashes \
		&& cd .pip-hashes \
		&& pip download --require-virtualenv --disable-pip-version-check --requirement ../requirements-freeze.txt \
		&& find . \
		-type f \
		-regex "\(.*\.whl\|.*\.tar\.gz\)" \
		-not -name "setuptools*" \
		-exec pip hash --algorithm sha512 --no-color {} \; \
		| sed -n 'n;p' > tmp.hashes \
		&& paste -d '|' ../requirements-freeze.txt tmp.hashes | sed 's/|/ \\\n    /g' > req.freeze \
		&& cd .. \
		&& mv .pip-hashes/req.freeze requirements-freeze.txt \
		&& rm -rf .pip-hashes \
		&& deactivate

regenerate-freeze-no-hashes: uninstall-dev
	python3 -m venv .venv
	$(VENV_CMD) \
		&& pip install --require-virtualenv --disable-pip-version-check --requirement requirements.txt --requirement requirements-dev.txt \
		&& pip freeze --require-virtualenv --disable-pip-version-check --local > requirements-freeze.txt \
		&& deactivate

uninstall-dev:
	rm -rf .venv .pip-hashes

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
		&& tox run-parallel \
		&& deactivate

fuzzer:
	$(VENV_CMD) \
		&& tox run -e fuzzer \
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
		&& twine upload --repository md-toc dist/* \
		&& deactivate

clean:
	rm -rf build dist *.egg-info tests/benchmark-results
	# Remove all markdown files except the readmes.
	find -regex "\(.*/crash-[a-f0-9]+\|.*\.[mM][dD]\)$$" \
		! -name 'README.md' \
		! -name 'CONTRIBUTING.md' \
		! -name 'SECURITY.md' \
		! -path './.venv/*' \
		! -path './.git/*' -type f -exec rm -f {} +
	$(VENV_CMD) \
		&& $(MAKE) -C docs clean \
		&& deactivate

# This serves both as benchmark and as fuzzer.
benchmark:
	$(VENV_CMD) \
		&& python3 -m md_toc.tests.benchmark \
		&& deactivate

.PHONY: default doc install uninstall install-dev uninstall-dev update test clean demo benchmark pre-commit regenerate-freeze regenerate-freeze-no-hashes
