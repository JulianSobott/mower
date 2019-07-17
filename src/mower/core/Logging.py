"""
@author: Julian
@brief:
@description:
"""

import logging

import logging


logger = logging.getLogger("Core")
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(levelname)-8s %(message)s \t\t(core.%(filename)s %(lineno)d)  \t%(relativeCreated).9s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
