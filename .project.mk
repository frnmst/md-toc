PROJECT_NAME := md-toc
PYTHON_MODULE_NAME := md_toc

MAKEFILE_SOURCE := https://software.franco.net.eu.org/frnmst/python-makefile/raw/branch/master/Makefile.example
bootstrap:
	curl -o Makefile $(MAKEFILE_SOURCE)
