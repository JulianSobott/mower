==========
Dev guide
==========

This file is the entry point, when you start developing at this project. Read it careful and use it as
reference.

.. toctree::

    getting_started
    git
    todos
    simulation/index

Software
--------

- python
- simulation: python with PyQT5

Project structure
------------------

::

    mower
    |   README.md
    |
    |___docs
    |   |
    |   |___build
    |   |
    |   |___dev
    |   |
    |   |___code
    |
    |___src
    |   |
    |   |___mower
    |       |   start_simulation.py
    |       |
    |       |___core
    |       |
    |       |___real
    |       |
    |       |___simulation
    |       |
    |       |___utils
    |       |
    |       |___tests

Style guide
-----------

This part defines naming conventions and other style conventions.

- *Package*: snake_case
- *Python file*: snake_case
- *Class*: CamelCase
- *Function*: snake_case
- *Variables*: snake_case
- *rst file* snake_case
- *tests*
    - *test file*: test_py_file_name
    - *test case*: Test...
    - *test method*: test\_... (method_name and small description e.g. test_root_failing)

Workflow
---------

This may be a useful workflow when you want to add a new feature

1. Create documentation

    - What is this feature
    - features
    - details?
    - ...

2. Define code (not implement)

    - What classes and methods are needed

3. Create tests

    - for every method

4. Implement code
5. Test

.. todo::

    Better describe `1. Create documentation`. Add parts, where to include documentation, where to add changes, ...





