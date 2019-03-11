======================
Working with git
======================

This project uses gut as version control software. The repository is located at
`Gitlab <https://gitlab.com/JulianSobott/mower/>`_.

Important git terms
=====================

There are better resources for more detailed descriptions.
e.g. `git Grundlagen <https://git-scm.com/book/de/v1/Los-geht%E2%80%99s-Git-Grundlagen>`_ However this will give you a
rough understanding of the different terms.

repository
    All files are located here. It keeps track of all versions and branches.

branch
    A branch offers the opportunity, to work on different tasks in parallel. Every branch can have
    different files. The "main" branch is the ``master`` branch.

commit
    To add a new version of files, you have to commit them. Only then the version control keeps track of them.
    Commits always have a short message, that describes what was changed and may have a longer detailed description.
    Commits are only added to the local `repository`.

local vs remote
    All changes that you make are only made to the local repository. This is because you **cloned** the repository.
    To push the changes to the remote repository you need to ``push`` them. Only then every one can see them, and
    update their project.

push
    A ``push`` pushes all commits of a branch to the remote repository.

pull
    A ``pull`` pulls every changes from the remote, that were made to the branch. It is like a update.

merge
    Because changes can be made in parallel it is necessary, to bring all changes together. A merge tries to automatically
    merge all changes from one branch into the other. If it can't be made automatically a merge conflict appears.
    Merge conflicts must me solved manually.

checkout
    Changes to another branch. Only files from this branch are visible, but the others are not gone.

Standard git workflow
======================

To get the project clone it:


.. code-block:: console

    git clone https://gitlab.com/JulianSobott/mower.git

Then checkout the branch you want to work on. Usually ``dev``

.. code-block:: console

    git checkout dev

Or choose in your IDE a local branch and checkout, or if you have no local path already, choose a remote
branch and choose ``Checkout As...``, where the name should be the same as the remote.

**Every time before** you make any changes ``pull`` possible changes. This will prevent later merge conflicts.

.. code-block:: console

    git pull

Then you can start working. Every time when you have made a relevant change, that you want to keep track of you make a
``commit``. In the console you first need to add all files, to the version control.

.. code-block:: console

    git add *
    git commit -m "commit message"

Or in PyCharm you can hit ``STR+k`` To open the commit window. Here you must edit the commit message.
After two blank lines you can add details. You can also define what changes you want to commit, by de selecting those,
you don't want to commit.

When you are finished with your work or you want to share your code ``push`` it. Don't forget this at the end of your
work otherwise the other members will not see the changes.

.. code-block:: console

    git push

In PYCharm hit ``STR+CTRL+K`` or ``VCS->Git->Push``

.. todo::

    Maybe add merge, rebase, amend, revert, checkout_previous