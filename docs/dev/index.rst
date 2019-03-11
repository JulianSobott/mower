==========
Dev guide
==========

This file is the entry point, when you start developing at this project. Read it careful and use it as
reference.

We start with some general project details.

General
==========

Abstract
-------------

The goal of this project is to build a intelligent self-driven mower which drives an optimal way with the help of Ai.

Problem
-------------

There are already self-driven mowers available, but they have a few disadvantages.

1. They are very expensive
2. They need wires at all edges -> Expensive (money and work)
3. They drive a random route -> slow

Solution
-------------

Build a mower that has sensors. These sensors can evaluate if there is an edge. These sensors may be cameras,
distance_sensor, color_sensor, bumper, ... . (Solves problem 2.)

The mower somehow has a sense for its actual position and his surroundings. This way a non-random route can be
calculated and driven. (Solves problem 3.)

The first problem is hard to estimate, whether it can be solved. But because most parts are self build it may cheaper.
It is a goal to keep the mower as cheap as possible (but don't lose quality or functionality).

Target group
-------------

The project is for now, for hobbyists, that want to build a own mower. Every person with a garden could use
a finished mower.

Core features
--------------

- self driven
- no wires
- intelligent driving algorithm
- graphical simulation

Possible features
------------------

- App for access

Details
===========

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
    |   |   start_simulation.py
    |   |
    |   |___core
    |   |
    |   |___real
    |   |
    |   |___simulation
    |   |
    |   |___utils
    |   |
    |   |___tests

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

Workflow:
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





