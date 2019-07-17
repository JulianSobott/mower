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

- Image recognition
    - Collect training and test images
    - Real time recognition
    - General recognition
        - Define what to recognize  and how to handle it
        - Create an algorithm with proper output
            - Define the outputs and inputs

- Simulation surface
    - Mower can drive
        - Extends the core drive functionality
    - Controls
        - Restart
    - Add layout to control window
        - clear map
        - fill area
        - line thickness

    - if mower reaches edge increase/add array
    - Change units to fit real values. sizes, velocity, ...
    - Constant fps
