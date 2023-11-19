Pre-commit hook
---------------

This repo provides the following :download:`plugin <../.pre-commit-hooks.yaml>` to be used with the `Pre-commit framework <https://pre-commit.com/>`_

.. literalinclude:: ../.pre-commit-hooks.yaml
   :language: yaml
   :caption: The .pre-commit-hooks.yaml file
   :name: .pre-commit-hooks.yaml

Add a ``.pre-commit-config.yaml`` file in the root of your GIT repo.
Have a look at the ``/.pre-commit-hooks.yaml`` file of this repository for a
full example.

These are the default plugin settings

.. code-block:: yaml
   :caption: A simple example of a .pre-commit-config.yaml file
   :name: .pre-commit-config.yaml simple

    repos:
    -   repo: https://codeberg.org/frnmst/md-toc
        # Release updates (ATOM) https://codeberg.org/frnmst/md-toc/tags.atom
        rev: master # set a GIT tag
        hooks:
        -   id: md-toc

You can override the defaults via the ``args`` parameter, such as

.. code-block:: yaml
   :caption: Example of arguments passed as a pre-commit
   :name: .pre-commit-config.yaml args

    repos:
    -   repo: https://codeberg.org/frnmst/md-toc
        # Release updates (ATOM) https://codeberg.org/frnmst/md-toc/tags.atom
        rev: master # set a GIT tag
        hooks:
        -   id: md-toc
            args: [-p, --skip-lines, '1', redcarpet]  # CLI options

Finally, run ``pre-commit install`` to enable the hook.
