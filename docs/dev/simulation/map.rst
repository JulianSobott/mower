Map
========

The map is the main part of the main_window. The map renders all information saved in an array. It is grid based but
the cell size (render_size and real_size) can be adjusted.

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

