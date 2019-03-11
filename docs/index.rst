Welcome to mower's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   dev/index


Abstract
-------------

The goal of this project is to build an intelligent self-driven mower which drives an optimal way with the help of Ai.

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

