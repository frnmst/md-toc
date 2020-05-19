Pre-commit hook
---------------

This repo provides the following plugin for use with the `Pre-commit framework <https://pre-commit.com/>`_:

.. literalinclude:: ../.pre-commit-hooks.yaml
   :caption: The .pre-commit-hooks.yaml file
   :name: .pre-commit-hooks.yaml
   :language: yaml

Add a ``.pre-commit-config.yaml`` file in your git repo
to use the default plugin settings:


.. code-block:: yaml
   :caption: A simple example of a .pre-commit-config.yaml file
   :name: .pre-commit-config.yaml simple

    repos:
    - repo: https://github.com/frnmst/md-toc
      rev: master  # or a specific git tag from md-toc
      hooks:
      - id: md-toc



You can override the default settings via the ``args`` parameter, such as:


.. code-block:: yaml
   :caption: Example of arguments passed as a pre-commit
   :name: .pre-commit-config.yaml args

    repos:
    - repo: https://github.com/frnmst/md-toc
      rev: master  # or a specific git tag from md-toc
      hooks:
      - id: md-toc
        args: [-p, --skip-lines, '1', redcarpet]  # CLI options
