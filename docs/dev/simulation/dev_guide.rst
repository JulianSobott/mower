TODO next
===========

- The data of the local map is not rendered.
- Mower local copy global map by driving
- Add layout to control window
- Add parameters for drawing on map to control window
- Change units to fit real values. sizes, velocity, ...
- Constant fps


Relations
-----------

Global Map -> Mower : Transformations of map must be applied to mower
Mower -> Global Map : Sensors must read current data of Global Map
Mower -> Local Map : In Core. Mower must have access to its self generated map
Local Map -> Mower : Transformations of map must be applied to mower


Maps
---------

**Map:** Core. Map that has a data array: 2d numpy array. The data array contains the cell type.

**DrawableMap:** Simulation. Map that extends Map. Additional transformations, color tables and draw methods, ....


Objects:

Core mower: local_map: Map
Simulation mower:




