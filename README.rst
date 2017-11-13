.. image:: https://badge.fury.io/py/git-ls-anytree.svg
    :target: https://badge.fury.io/py/git-ls-anytree

.. image:: https://travis-ci.org/wizardsoftheweb/git-ls-anytree.svg?branch=master
    :target: https://travis-ci.org/wizardsoftheweb/git-ls-anytree

.. image:: https://coveralls.io/repos/github/wizardsoftheweb/git-ls-anytree/badge.svg?branch=master
    :target: https://coveralls.io/github/wizardsoftheweb/git-ls-anytree?branch=master


``git-ls-anytree``
==================

``git-ls-anytree`` provides ``tree``-like output from ``git`` tree(ish)s.

Until ``v1``, the API might change slightly as I add more options and streamline what I've got.

.. contents::

Overview
--------

``git-ls-tree`` (`man <https://git-scm.com/docs/git-ls-tree>`__) is a great little tool to view the contents of a tree(ish). It functions in a manner similar to ``ls``, where each line contains all the information you'd need and the lines don't really connect. ``tree`` (`man <https://linux.die.net/man/1/tree>`__) is a fantastic CLI addition that adds visual context to directory information. ``anytree`` (`package <https://pypi.python.org/pypi/anytree/>`__) is a great Python tool that implements the visual cues from ``tree`` on abstract trees.

``git-ls-anytree`` is my attempt to link all of those neat things together. I built this primarily for usage in Python code itself, but adding CLI support was really fun.

Installation
------------

::

    $ pip install --user git-ls-anytree
    # or whatever; the number of ways to install things is fairly large

Tests
~~~~~

You can find the tests in `the source repo <https://github.com/wizardsoftheweb/git-ls-anytree/tree/master/tests>`__

Quick Examples
--------------

``git ls-tree`` (baseline)
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git ls-tree -rtl --abbrev HEAD
    100644 blob b2b0820     184     .editorconfig
    100644 blob 9744e3b    1291     .gitignore
    100644 blob af55cdb     230     .travis.yml
    100644 blob 93bb548     724     LICENSE.rst
    100644 blob 5d22467     132     MANIFEST.in
    100644 blob 1670bfb    1830     README.rst
    040000 tree 4d2dd1d       -     git_ls_anytree
    100644 blob 0c62199       6     git_ls_anytree/VERSION
    100644 blob ee53f20     243     git_ls_anytree/__init__.py
    100644 blob 626d501      33     git_ls_anytree/__main__.py
    100644 blob 5cc512a     259     git_ls_anytree/__version__.py
    100644 blob c23d837    2844     git_ls_anytree/cli_file.py
    100644 blob a90da6c     356     git_ls_anytree/convert_path_to_list.py
    100644 blob f6485bf    4235     git_ls_anytree/git_ls_tree.py
    100644 blob a73aeb4    4584     git_ls_anytree/git_ls_tree_node.py
    100644 blob b14931a     648     git_ls_anytree/local_exceptions.py
    100644 blob 55f8a08     427     setup.cfg
    100644 blob 823c34b     321     setup.py
    040000 tree c8d53d3       -     tests
    100644 blob a941a90     953     tests/test_cli.py
    100644 blob eb2a9dd     609     tests/test_convert_path_to_list.py
    100644 blob dc7c7a9   13337     tests/test_git_ls_tree.py
    100644 blob b96675d    5709     tests/test_git_ls_tree_node.py
    100644 blob 9a60bad     182     tests/test_main.py
    100644 blob c5389bc     152     tox.ini

``git ls-anytree`` (default)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git ls-anytree HEAD --abbrev
    mode    type    object   size   HEAD
    100644  blob    b2b0820   184   ├── .editorconfig
    100644  blob    9744e3b  1291   ├── .gitignore
    100644  blob    af55cdb   230   ├── .travis.yml
    100644  blob    93bb548   724   ├── LICENSE.rst
    100644  blob    5d22467   132   ├── MANIFEST.in
    100644  blob    1670bfb  1830   ├── README.rst
    040000  tree    4d2dd1d     -   ├── git_ls_anytree
    100644  blob    0c62199     6   │   ├── VERSION
    100644  blob    ee53f20   243   │   ├── __init__.py
    100644  blob    626d501    33   │   ├── __main__.py
    100644  blob    5cc512a   259   │   ├── __version__.py
    100644  blob    c23d837  2844   │   ├── cli_file.py
    100644  blob    a90da6c   356   │   ├── convert_path_to_list.py
    100644  blob    f6485bf  4235   │   ├── git_ls_tree.py
    100644  blob    a73aeb4  4584   │   ├── git_ls_tree_node.py
    100644  blob    b14931a   648   │   └── local_exceptions.py
    100644  blob    55f8a08   427   ├── setup.cfg
    100644  blob    823c34b   321   ├── setup.py
    040000  tree    c8d53d3     -   ├── tests
    100644  blob    a941a90   953   │   ├── test_cli.py
    100644  blob    eb2a9dd   609   │   ├── test_convert_path_to_list.py
    100644  blob    dc7c7a9 13337   │   ├── test_git_ls_tree.py
    100644  blob    b96675d  5709   │   ├── test_git_ls_tree_node.py
    100644  blob    9a60bad   182   │   └── test_main.py
    100644  blob    c5389bc   152   └── tox.ini

``git ls-anytree`` (tree only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git ls-anytree --name-only
    HEAD
    ├── .editorconfig
    ├── .gitignore
    ├── .travis.yml
    ├── LICENSE.rst
    ├── MANIFEST.in
    ├── README.rst
    ├── git_ls_anytree
    │   ├── VERSION
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── __version__.py
    │   ├── cli_file.py
    │   ├── convert_path_to_list.py
    │   ├── git_ls_tree.py
    │   ├── git_ls_tree_node.py
    │   └── local_exceptions.py
    ├── setup.cfg
    ├── setup.py
    ├── tests
    │   ├── test_cli.py
    │   ├── test_convert_path_to_list.py
    │   ├── test_git_ls_tree.py
    │   ├── test_git_ls_tree_node.py
    │   └── test_main.py
    └── tox.ini

Usage
-----

CLI
~~~

Installation via ``pip`` should add an executable to your ``PATH`` (you might need to add ``$HOME/.local/bin`` to your ``PATH`` first if you used ``--user``).

::

    $ which git-ls-anytree
    /home/user/.local/bin/git-ls-anytree

This should register it with ``git``, which you can check with ``git help -a``

::

    $ git help -a | grep 'ls-anytree' > /dev/null || echo 'whoops'

This means you can either call it via ``git-ls-anytree`` or ``git ls-anytree``.

Currently, to access the help, you'll have to use one of these options:

::

    $ git ls-anytree -h
    $ git-ls-anytree --help

The package doesn't install a ``man`` page, so ``git`` can't find any help when you run ``git ls-anytree --help``.

Options
<<<<<<<

::

    usage: git-ls-anytree [-h] [-v] [-w WORKING_DIRECTORY] [--name-only]
                          [--abbrev | --abbrev-n ABBREV] [-d] [-F]
                          [tree-ish] [patterns [patterns ...]]

    Python tool to pretty-print git-ls-tree

    positional arguments:
      tree-ish              Reference to tree-ish. Defaults to HEAD
      patterns              Subtrees within the main tree-ish

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -w WORKING_DIRECTORY, --working-directory WORKING_DIRECTORY
                            The directory to use for the git commands. Defaults to cwd (path/to/cwd)

    Inherited git-ls-tree arguments:
      --name-only, --name-status
                            Only print the tree structure per git-ls-tree
                            --name-(only|status)
      --abbrev              Equivalent to git-ls-tree --abbrev. Uses the default
                            git short hash of seven characters.
      --abbrev-n ABBREV     Sets the git object abbreviation per git-ls-tree
                            --abbrev=n
      -d, --trees-only      Only print trees per git-ls-tree -d

    Inherited tree arguments:
      -F, --classify        Appends ( *@/) to filename per ls -F

    Due to known issues with nargs='?' consuming positionals under the right
    circumstances, --abbrev[=n] was split into --abbrev, for the default, and
    --abbrev-n INT, to specify a level.


``import``
~~~~~~~~~~

Check out the last lines of ``cli_file.py`` (`source <https://github.com/wizardsoftheweb/git-ls-anytree/tree/master/git_ls_anytree/cli_file.py#L95>`__) for a simple usage example:

::

    ...
    args = parser.parse_args(passed_args)

    full_tree = GitLsTree(
        tree_ish=args.tree_ish,
        patterns=args.patterns,
        trees_only=args.trees_only,
        working_dir=args.working_directory,
        abbrev=args.abbrev if hasattr(args, 'abbrev') else None
    )
    full_tree.pretty_print(
        name_only=args.name_only,
        classify=args.classify
    )

More here later.

Roadmap
-------

These are all things I'd like to have finished before tagging ``v1``.

* Build and install ``man`` page
* Compile docs
* Test docs
* Clean up ``tests``
* Code Climate, Hound, something of that nature
* Refactor the ``pylint`` refactor issues
