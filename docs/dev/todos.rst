TODOs
=========

Milestones
---------------

- Image Recognition
- Simulation surface
- Core

Top to bottom tasks
---------------------

- Core
    - Setup mainloop
        - One in core or separate in sim and real?
    - Define interface between simulation, core and real
    - Map
        - load/save mower
            - position
            - map
    - Generalize sensor data

- Image recognition
    - Collect training and test images
    - Real time recognition
    - General recognition
        - Define what to recognize  and how to handle it
        - Create an algorithm with proper output
            - Define the outputs and inputs

- Simulation
    - Mower can drive
        - Extends the core drive functionality

    - Add layout to control window
    - Add controls to Control window
        - clear map
        - fill area
        - line thickness
        - loading path (input field, more radio buttons with all saves)

    - if mower reaches edge increase/add array
    - Change units to fit real values. sizes, velocity, ...
    - Config file

