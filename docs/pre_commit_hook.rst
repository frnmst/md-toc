Pre-commit hook
---------------

This repo provides the following :download:`plugin <../.pre-commit-hooks.yaml>` to be used with the `Pre-commit framework <https://pre-commit.com/>`_:

.. literalinclude:: ../.pre-commit-hooks.yaml
   :language: yaml
   :caption: The .pre-commit-hooks.yaml file
   :name: .pre-commit-hooks.yaml

Add a ``.pre-commit-config.yaml`` file in the root of your git repo.
These are the default plugin settings

.. code-block:: yaml
   :caption: A simple example of a .pre-commit-config.yaml file
   :name: .pre-commit-config.yaml simple

    repos:
    -   repo: https://codeberg.org/frnmst/md-toc
        # Remember to keep md-toc up-to-date!
        rev: master  # set a specific git tag
        hooks:
        -   id: md-toc

You can override the defaults via the ``args`` parameter, such as

.. code-block:: yaml
   :caption: Example of arguments passed as a pre-commit
   :name: .pre-commit-config.yaml args

    repos:
    -   repo: https://codeberg.org/frnmst/md-toc
        # Remember to keep md-toc up-to-date!
        rev: master  # set a specific git tag
        hooks:
        -   id: md-toc
            args: [-p, --skip-lines, '1', redcarpet]  # CLI options

This is what I use in some repositories

.. code-block:: yaml

   # See https://pre-commit.com for more information
   # See https://pre-commit.com/hooks.html for more hooks
   repos:
   -   repo: https://github.com/pre-commit/pre-commit-hooks
       rev: 'v4.4.0'
       hooks:
       -   id: trailing-whitespace
       -   id: end-of-file-fixer
       -   id: check-yaml
       -   id: destroyed-symlinks
       -   id: detect-private-key
       -   id: check-ast
       -   id: check-case-conflict
       -   id: debug-statements
       -   id: fix-encoding-pragma
       -   id: forbid-submodules
       -   id: check-symlinks
       -   id: check-shebang-scripts-are-executable
       -   id: check-case-conflict
       -   id: check-added-large-files
           args: ['--maxkb=16384']
       -   id: destroyed-symlinks

   -  repo: https://codeberg.org/frnmst/md-toc
      # Remember to keep md-toc up-to-date!
      rev: '8.2.0'  # set a specific git tag
      hooks:
      -    id: md-toc
           args: [-p, 'cmark', '-l6']  # CLI options

   -   repo: https://github.com/jorisroovers/gitlint
       rev: 'v0.18.0'
       hooks:
       -   id: gitlint

Finally, run ``pre-commit install`` to enable the hook.
