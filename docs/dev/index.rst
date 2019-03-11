==========
Dev guide
==========

This file is the entry point, when you start developing at this project. Read it careful and use it as
reference.

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
=========

Here a useful workflow is described when a new feature should be implemented

- Create documentation
    - What is this feature
    - features
    - details?
    - ...
- Define code (not implement)
    - What classes and methods are needed
- Create tests
    - for every method
- Implement code
- Test

.. todo:

    Better describe documentation. Add parts, where to include documentation, where to add changes, ...





