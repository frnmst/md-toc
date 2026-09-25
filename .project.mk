# python-makefile
# MIT License
# Copyright (C) 2024-2026 Franco Masotti (see /README.md)
# https://software.franco.net.eu.org/frnmst/python-makefile

# Change these two. Required.
PROJECT_NAME := md-toc
PYTHON_MODULE_NAME := md_toc

# Required.
MAKEFILE_SOURCE := https://repos.franco.net.eu.org/frnmst/python-makefile/raw/branch/master/Makefile.linux.example
DOCKER_BUILD_PYTHON_DIST_SOURCE := https://repos.franco.net.eu.org/frnmst/python-makefile/raw/branch/master/Dockerfile.python3.13_hatchling.build.example

bootstrap:
	curl -o Makefile $(MAKEFILE_SOURCE)
	curl -o Dockerfile.python3.13_hatchling.build $(DOCKER_BUILD_PYTHON_DIST_SOURCE)
