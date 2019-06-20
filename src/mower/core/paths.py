"""
:module: mower.core.paths
:synopsis: paths
:author: Julian Sobott
:author: 

public module members
----------------------

.. autodata:: PROJECT_PATH
.. autodata:: CODE_PATH
"""
import os

PROJECT_PATH = os.path.abspath(os.path.join(os.path.realpath(__file__), "../../../.."))
CODE_PATH = os.path.join(PROJECT_PATH, "src/mower/")
