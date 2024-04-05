PROJECT_NAME := md-toc
PYTHON_MODULE_NAME := md_toc

MAKEFILE_SOURCE := https://software.franco.net.eu.org/frnmst/python-makefile/raw/branch/master/Makefile.example
DOCKER_BUILD_DIST_SOURCE := https://software.franco.net.eu.org/frnmst/python-makefile/raw/branch/master/.dockerfile_build_python_dist.example
bootstrap:
	curl -o Makefile $(MAKEFILE_SOURCE)
	curl -o .dockerfile_build_python_dist $(DOCKER_BUILD_DIST_SOURCE)
