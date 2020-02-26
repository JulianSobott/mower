Driving
=======

In this documents are the calculations, that are needed to determine the position of the mower. The goal is to be
precise as possible and to be as close as possible to the reality. To achieve this the lowest level function is the
rotation of the wheels. Based on this the new position can be calculated. Some parameters from reality are not taken
into account (for now) such at slippage.

Parameters
----------

Following parameters affect the driving behaviour. They are categorized into constants that are set once and
variables, that can change at any time.

Constants
*********

- Model of the mower

Variables
*********

- left/right motor speed
- left/right motor direction
- time since last update
