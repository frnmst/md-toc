Installation
============

Run the following command in either a root or normal terminal (depending on 
your Python setup) from the root directory of the project's cloned repository,

First of all install `pipenv <https://pipenv.readthedocs.io/en/latest/>`_ and then:

::


    $ make install


You can also install md_toc via pip (i.e: without having to download the source 
code):

::

    $ pip3 install md_toc --user


All the necessary dependencies should be installed automatically along with the 
program.

Distribution packages
---------------------

- A ``PKGBUILD`` for Arch Linux like distributions is available under
  the ``./packages/aur`` directory as well as on the AUR website.


Dependencies
------------

- Python >= 3.5
- fpyutils_

.. _fpyutils: https://github.com/frnmst/fpyutils
