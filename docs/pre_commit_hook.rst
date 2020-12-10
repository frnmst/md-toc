Pre-commit hook
---------------

This repo provides the following plugin for use with the `Pre-commit framework <https://pre-commit.com/>`_:

.. literalinclude:: ../.pre-commit-hooks.yaml
   :caption: The .pre-commit-hooks.yaml file
   :name: .pre-commit-hooks.yaml
   :language: yaml

Add a ``.pre-commit-config.yaml`` file in the root of your git repo.
These are the default plugin settings:


.. code-block:: yaml
   :caption: A simple example of a .pre-commit-config.yaml file
   :name: .pre-commit-config.yaml simple

    repos:
    -   repo: https://github.com/frnmst/md-toc
        rev: master  # or a specific git tag from md-toc
        hooks:
        -   id: md-toc



You can override the defaults via the ``args`` parameter, such as:


.. code-block:: yaml
   :caption: Example of arguments passed as a pre-commit
   :name: .pre-commit-config.yaml args

    repos:
    -   repo: https://github.com/frnmst/md-toc
        rev: master  # or a specific git tag from md-toc
        hooks:
        -   id: md-toc
            args: [-p, --skip-lines, '1', redcarpet]  # CLI options


This is what I use in some repositories:

.. code-block:: yaml

    # See https://pre-commit.com for more information
    # See https://pre-commit.com/hooks.html for more hooks
    repos:
    -   repo: https://github.com/pre-commit/pre-commit-hooks
        rev: v2.4.0
        hooks:
        -   id: trailing-whitespace
        -   id: end-of-file-fixer
        -   id: check-yaml
        -   id: check-added-large-files

    -  repo: https://github.com/frnmst/md-toc
       rev: 'master'  # or a specific git tag from md-toc
       hooks:
       -    id: md-toc
            args: [-p, 'github', '-l6']  # CLI options


Finally run ``$ pre-commit install`` to enable the hook.
