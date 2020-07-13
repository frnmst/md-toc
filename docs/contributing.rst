Contributing
============

Talk
----

Suggestions, improvements and discussion:

- https://gitter.im/md-toc/community

Git branches
------------

What follows is a table of the git branches used in this repository.

.. important:: Open pull requests on the ``dev`` target branch.
               Use ``bugfix-${fix_name}`` or ``newfeature-${new_feature_name}`` as names.

=====================================   ====================================================   ==============================
Branch                                  Description                                            Update schedule
=====================================   ====================================================   ==============================
``master``                              the main branch                                        every new release
``dev``                                 recent changes are merged here before a new release    at will
``gh-pages``                            contains the built documentation only                  every new release
``bugfix-${fix_name}``                  a generic bug fix
``newfeature-${new_feature_name}``      a generic new feature
=====================================   ====================================================   ==============================

Dependencies
------------

First of all install `pipenv <https://pipenv.readthedocs.io/en/latest/>`_ and then
install the software requirements from the Pipfile in the repository's root:


::


    $ make install-dev



Once you make changes you can install md_toc to have access to its executable file.
Install `pip <https://pypi.org/project/pip/>`_ and then:


::


    $ make install


.. note:: don't forget to add ``~/.local/bin`` to ``PATH``.

Unit tests
----------

If you have changed parts of the source code you MUST take care of adding  
the corresponding unit tests. Once you have done that run the following command 
in a terminal:


::


    $ make test


You can also add this command before every git commit as by running:


::


    $ make githook


Benchmarks
----------

Time-related benchmarks are useful to understand how different code versions perform.
A benchmark script which calls the unit tests is present in the tests directory.
You can call it with:


::


    $ make benchmark


Python PEP compliancy
---------------------

To be able to lint and test for PEP compliancy you need to run:


::


    $ make pep


Documentation
-------------

You can edit and rebuild all this documentation with:


::


    $ make doc


TODO and FIXME
--------------

Go in the repository's root and then:


::

    $ grep -e TODO -e FIXME -n */*.py


Contribution Steps
------------------

1. clone the repository
2. install the requirements
3. write code
4. write unit tests
5. run tests
6. run PEP linter and check
7. update relevant documentation, if necessary
8. pull request

.. note:: Have a look at `this post <https://frnmst.gitlab.io/notes/my-python-release-workflow.html>`_ as well.
