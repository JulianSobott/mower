"""
:module: mower.simulation.paths
:synopsis: paths
:author: Julian Sobott
:author:

public module members
----------------------

.. autodata:: PROJECT_PATH
.. autodata:: CODE_PATH
"""
from mower.core.paths import *

ASSETS_PATH = os.path.join(CODE_PATH, "simulation/assets/")


def get_asset_path(asset_name: str) -> str:
    return os.path.join(ASSETS_PATH, asset_name)
