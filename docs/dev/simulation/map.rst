Map
========

The map is the main part of the main_window. The saves the information where are and what is at a position.


Core
----------------------

- possible to be infinity
- not necessary a rectangle
- The map can be very precise at some parts and very rough at others (to save memory) ? Test it
- (cell_size can be set)

- position is a quad at a location with an average value ?
    - the quad size can be set

- get underground at position
- set underground at position
- set underground at line

Render objects
----------------

A map can color each cell individually. Each cell represents a render object. Following cell attributes are available:

- grass
    - maybe height
- obstacle

Editing the map
-----------------

It is always possible to edit the map.

- draw grass
- draw obstacle
- zoom
- move

TODO: make possible to draw map on multiple windows with different options


API
-----------

.. automodule:: mower.simulation.Map

