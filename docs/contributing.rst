Contributing
============

Git branches
------------

What follows is a table of the git branches used in md-toc's repository.
Please, do NOT open pull requests on the ``master``, ``dev`` or ``gh-pages`` branches.
Use ``bugfix-${fix_name}`` or ``newfeature-${new_feature_name}`` instead.

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

Install the software requirements from the ``requirements.txt`` file in the 
repository's root:


::


    $ pip install -r requirements.txt


Unit tests
----------

If you have changed parts of the source code you MUST take care of adding  
the corresponding unit tests. Once you have done that run the following command 
in a terminal:


::


    $ python setup.py test


or simply:


::

    $ make test


You can also add this command before every git commit as by running:


::

    $ make githook


Python PEP compliancy
---------------------

To be able to lint and test for PEP compliancy you need to run:


::


    $ make pep


TODO and FIXME
--------------

Go in the repository's root and then:


::

    grep -e TODO -e FIXME -n */*.py


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
