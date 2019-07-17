"""
@author: Julian
@brief:
@description:
"""

import logging

import logging


logger = logging.getLogger("Simulation")
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(levelname)-8s %(message)s \t\t(simulation.%(filename)s %(lineno)d) \t%(relativeCreated).5s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
