"""
@author: Julian
@brief:
@description:
"""

import logging

import logging


logger = logging.getLogger("Real")
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(levelname)-8s %(message)s \t\t(%(filename)s %(lineno)d)')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
