"""
:module: mower.utils.data_storage
:synopsis: Storing and loading data
:author: Julian Sobott
:author: 

Map
-----

::

    mower
    |
    |___data
    |   |   config
    |   |
    |   |____saves
    |   |    |
    |   |    |____[name]_[date]
    |   |    |    |
    |   |    |    |____global_map
    |   |    |    |
    |   |    |    |----mower
    |   |    |    |    |
    |   |    |    |    |____local_map

public functions
-----------------

.. autofunction:: XXX

public classes
-----------------

.. autoclass:: XXX
    :members:


private functions
------------------

.. autofunction:: XXX

private classes
-----------------

.. autoclass:: XXX
    :members:

"""
import shutil
import os
import datetime
import numpy as np
import json

from mower import simulation, core

PROJECT_PATH = os.path.abspath(os.path.join(__file__, "../../../.."))
CODE_PATH = os.path.join(PROJECT_PATH, "src/mower/")
DATA_PATH = os.path.join(PROJECT_PATH, "data/")
SAVES_PATH = os.path.join(DATA_PATH, "saves")


def _create_folder(abs_path: str, empty: bool = False):
    if os.path.exists(abs_path) and empty:
        shutil.rmtree(abs_path, ignore_errors=True)
    os.makedirs(abs_path, exist_ok=True)


def init_folder_structure(empty: bool = False) -> None:
    _create_folder(SAVES_PATH, empty)


def save_data(map_obj: 'core.Map', mower_obj: 'core.Mower', name: str = "SAVE_"):
    init_folder_structure()
    save_path = os.path.join(SAVES_PATH, f"{name}{datetime.datetime.now().strftime('%y_%m_%d_%H_%M_%S')}")
    _create_folder(save_path, empty=True)

    meta_data = {"name": name,
                 "comments": "",
                 "time": str(datetime.datetime.now()),
                 "save_version": 1,
                 "global_map": {
                     "shape": map_obj.root_quad.shape,
                     "offset": map_obj.root_quad.offset,
                 },
                 "mower": {}
                 }
    if isinstance(map_obj, simulation.Map):
        map_obj: simulation.Map
        t = map_obj.transformation
        meta_data["window"] = {
            "zoom": map_obj.zoom,
            "transformation": [t.m11(), t.m12(), t.m13(), t.m21(), t.m22(), t.m23(), t.m31(), t.m32(), t.m33()],
            "max_bounds": map_obj.max_bounds
        }
    _save_meta_data(meta_data, save_path)

    map_folder_path = os.path.join(save_path, "global_map")
    _save_map(map_obj, map_folder_path)
    print(f"Successfully saved data in: {save_path}")


def _save_map(map_obj: 'core.Map', abs_folder_path: str):
    _create_folder(abs_folder_path, empty=True)
    for row_idx, row in enumerate(map_obj.root_quad.data):
        for col_idx, child_quad in enumerate(row):
            quad_path = os.path.join(abs_folder_path, f"{row_idx}_{col_idx}_quad")
            np.save(quad_path, child_quad.data)


def _save_meta_data(meta_data: dict, abs_folder_path: str):
    file_path = os.path.join(abs_folder_path, "meta_data.json")
    with open(file_path, "w") as f:
        json.dump(meta_data, f, indent=4)


def load_data(map_obj: 'core.Map', mower_obj: 'core.Mower', full_name: str) -> bool:
    """
    Data will be loaded into existing objects.

    :param map_obj:
    :param mower_obj:
    :param full_name:
    :return:
    """
    save_path = os.path.join(SAVES_PATH, full_name)
    if not os.path.exists(save_path):
        return False
    meta_data = _load_meta_data(save_path)
    _load_map(map_obj, meta_data, save_path)


def _load_meta_data(abs_folder_path: str) -> dict:
    file_path = os.path.join(abs_folder_path, "meta_data.json")
    with open(file_path, "r") as f:
        return json.load(f)


def _load_map(map_obj: 'core.Map', meta_data: dict, save_path: str) -> None:
    map_shape = meta_data["global_map"]["shape"]
    map_obj.root_quad.data = np.full(map_shape, None, dtype=core.map_utils.Quad)
    map_obj.root_quad.offset = meta_data["global_map"]["offset"]
    map_obj.root_quad.shape = map_shape
    map_obj.root_quad.is_leaf = False
    for row in range(map_shape[0]):
        for col in range(map_shape[1]):
            quad_path = os.path.join(save_path, "global_map", f"{row}_{col}_quad.npy")
            map_obj.root_quad.data[row][col] = core.map_utils.Quad.from_file(quad_path, map_obj.root_quad)
    if isinstance(map_obj, simulation.Map):
        from PyQt5 import QtGui
        map_obj: simulation.Map
        map_obj.zoom = meta_data["window"]["zoom"]
        map_obj.transformation = QtGui.QTransform(*meta_data["window"]["transformation"])
        map_obj.max_bounds = meta_data["window"]["max_bounds"]
